import asyncio
import aiohttp
import logging
from axapi import Axapi
import xmltodict
import json
import sys

logger = logging.getLogger(__name__)


class Webex:

    def __init__(self, token, concurrent = 20):

        self.token = token
        self.url = 'https://api.ciscospark.com/v1/'
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + self.token}
        self.concurrent = concurrent
        self.data = []
        self.arguments = []

    def runIt(self,command, argument1 = ''): #TODO consider removing argument1

        try:

            response = asyncio.run(self.run_webex_command( command = command, argument1 = argument1))  #TODO consider removing argument1

        except Exception as err:

            logging.error('Error in async loop in Webex, consider lowering concurrent sessions')
            logging.error(err)


        return response


    async def run_webex_command(self,command, argument1 = ''): #TODO consider removing argument1

        connector = aiohttp.connector.TCPConnector(limit = self.concurrent)

        tasks = []

        error_list = []

        rType= self.obtain_request_type(command) # get / post / delete

        async with aiohttp.ClientSession(headers = self.headers, connector = connector) as session:

            if rType == 'get':

                url = self.url + self.obtain_url(command, argument1)

                task = asyncio.create_task(
                    self.get_url(command = command,  url=url, session=session, argument1 = argument1))  # to schedule the execution of a coroutine object

                tasks.append(task)


            elif rType == 'post':

                try:

                    url = self.url + self.obtain_url(command)

                    if command == 'add webexPlaces4migration()':

                        if isinstance(argument1, Axapi):

                            for ip_key, endpoint_dict in argument1.endpoints.items():

                                if endpoint_dict['canMigrate']:

                                    data = {'displayName':endpoint_dict['name'] , 'type':'room_device'}

                                    task = asyncio.create_task( self.post( url= url, data = data, session=session,
                                                                           command = command, argument1 = argument1))

                                    tasks.append(task)

                                else:
                                    error_list.append({ip_key:endpoint_dict['migrationError']})

                    elif command == 'get webexActivationCode4migration()':

                        if isinstance(argument1, Axapi):

                            for ip_key, endpoint_dict in argument1.endpoints.items():

                                if (endpoint_dict['canMigrate'] == True) and 'placeId' in endpoint_dict:

                                    data = {'placeId': endpoint_dict['placeId']}

                                    task = asyncio.create_task(self.post(url=url, data=data, session=session,
                                                                         command=command, argument1=argument1))

                                    tasks.append(task)


                except Exception as err:
                    logging.error(err)



            elif rType == 'delete':

                for id in self.data:

                    url = self.url + self.obtain_url(command, id)
                    task = asyncio.create_task(self.delete_url(command=command, url=url, session=session, argument1 = argument1))
                    tasks.append(task)

            else:

                return f'Implementation Error. Could not determine request type for {command}'


            responses = await asyncio.gather(*tasks) # Returns a LIST of dicts being each item an endpoint # Run all the tasks in parallel

            return responses

    def obtain_request_type(self, command):

        map_dict = {
            'run migrate2cloud()': 'post',
            'list webexDevices()' : 'get',
            'show webex places()' : 'get',
            'get webexPlaces()': 'get',
            'get webexActivationCode4migration()' : 'post',
            'add webexPlaces()' : 'post',
            'add webexPlaces4migration()': 'post',
            'delete webex places()': 'delete',
            'show webex devices status()': 'get'

        }

        if command in map_dict: # means the key exist
            return map_dict[command]

        else:
            logging.error(f'Implementation Error, no request type for {command}')
            return None

    def obtain_url(self, command, argument1 = ''):

        if argument1: #TODO consider removing

            map_dict = {
                'show webex places()' : f'places?displayName={argument1}',
                'get webexPlace()': 'places',
                'add webexPlaces()': 'places',
                'add webexPlaces4migration()': 'places',
                'delete webex places()': f'places/{argument1}'
            }

        else:

            map_dict = {
                'show webex devices()': 'devices',
                'list webexDevices()' : 'devices',
                'show webex places()' : 'places',
                'get webexPlace()': 'places',
                'add webexPlaces()': 'places',
                'add webexPlaces4migration()': 'places',
                'delete webexPlaces()': 'places',
                'get webexActivationCode4migration()': 'devices/activationCode'
                'show webex devices status()'
            }


        return map_dict[command]


    async def get_url(self,command, url ,session,argument1=''):

        try:

            resp = await session.request(method="GET", url = url, ssl = False)

            resp.raise_for_status()

            logger.info(f"GET response {resp.status} for {command} in {url}")

            text = await resp.text()

            data = json.loads(text)

            root_cmd = command.replace('()',f'({argument1})')

            response = {root_cmd: {
                'status': resp.status,
                'response': data}
            }

            return response

        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError,) as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = getattr(e, "strerror", None)

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'GET response {error} for {command} in {url}')

            #response = {'url': url, 'result': f'Error {error}'}

            root_cmd = command.replace('()', f'({argument1})')

            response = {root_cmd: {
                'status': 'Error',
                'response': error}
            }

            return response

        except Exception as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = f'Error {getattr(e, "strerror", None)}'

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'Got response {error} for {command} in {url}')

            response = {url:{
                'status': 'ERROR',
                'response': error}}

            return response


    async def post(self, url,data, session,command,argument1=''):

        try:

            resp = await session.request(method="POST",json = data, url=url, ssl = False)

            resp.raise_for_status()

            logger.info(f"POST response {resp.status} for {url}")

            text = await resp.text()

            json_response = json.loads(text)

            if command == 'get webexActivationCode4migration()':
                json_response['placeId'] = data['placeId']

            root_cmd = command.replace('()', f'({argument1})')

            response = {root_cmd: {
                'status': resp.status,
                'response': json_response}
            }

            return response


        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError,) as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = f'Error {getattr(e, "strerror", None)}'

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'Got response {error} for {url}')

            response = {url : {
                'status': 'ERROR',
                'response': error}}

            return response

    async def delete_url(self,command, url ,session,argument1):

        try:

            resp = await session.request(method="DELETE", url = url, ssl = False)

            resp.raise_for_status()

            logger.info(f"Got response {resp.status} for {command} in {url}")

            root_cmd = command.replace('()', f'({argument1})')

            response = {root_cmd: {
                'status': resp.status,
                'response': 'OK'}
            }

            return response

            return response

        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError,) as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = getattr(e, "strerror", None)

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'Got response {error} for {command} in {url}')

            response = {'url': url, 'result': f'Error {error}'}

            return response

        except Exception as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = f'Error {getattr(e, "strerror", None)}'

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'Got response {error} for {command} in {url}')

            response = {url:{
                'status': 'ERROR',
                'response': error}}

            return response

    def canMigrate2Cloud(self,endpoint_dict): #TODO add verification if system name is empty or if a place already exists with that name!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        version = float(endpoint_dict['versionNumber'])

        if endpoint_dict['sw'] == 'CE':  # migrate2cloud is only supportted on CE sw

            if version >= 9.8:  # only CE9.8 or higher supports migrate2cloud

                # if mode is Webex, we should not attempt to migrate as it is already in hub
                if endpoint_dict['mode'] != 'Webex':

                    endpoint_dict['canMigrate'] = True
                    endpoint_dict['migrationError'] = None

                    return True

                else:

                    logging.error(f'endpoint {endpoint_dict["name"]} ({endpoint_dict["ip"]})'
                                  f' cannot be migrated because is already in Webex provisioning mode')

                    endpoint_dict['canMigrate'] = False
                    endpoint_dict['migrationError'] = 'already in Webex provisioning mode'
                    return False


            else:

                logging.error(
                    f'endpoint {endpoint_dict["name"]} ({endpoint_dict["ip"]})'
                    f' cannot be migrated because is not on CE 9.8 version or higher')

                endpoint_dict['canMigrate'] = False
                endpoint_dict['migrationError'] = 'not on CE 9.8 version or higher'
                return False

        else:
            logging.error(f'endpoint {endpoint_dict["name"]} ({endpoint_dict["ip"]}) '
                          f'cannot be migrated because is not on CE software')
            endpoint_dict['canMigrate'] = False
            endpoint_dict['migrationError'] = 'not on CE software'
            return False

        return False