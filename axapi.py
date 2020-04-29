import asyncio
import aiohttp
import async_timeout
from aiohttp import FormData
import logging
import xmltodict
import json
import sys
import re
import os
from time import time
#import aiofiles
from helper_functions import calc_sha512

logger = logging.getLogger(__name__)

class Axapi:

    def __init__(self, username, password, concurrent = 20):

        self.username = username
        self.password = password
        self.versionInfo = False # we use this flag to know whether we have sw info from the endpoints
        self.endpoints ={} # we use this dict to store relevant information around the endpints, like sw version.
        self.sw_init = False # Change to True when 'sw' in endpoints is populated
        self.concurrent = concurrent
        self.data_column_size = 0
        self.exp_data = []


    def runIt(self,command, argument = '', argument2 = ''): # Entry point and EVENT LOOP


        try:

            response = asyncio.run(self.run_tp_command( command = command, argument = argument, argument2 = argument2))  # Event Loop

        except Exception as err:
            logging.error('Error in async loop')
            logging.error(err)

        '''
        treat mainly how the output will be presented after the command results are returned
            show commands will show in flattened way
            init sw will only initialize axapi.endpoints with different attributes
        '''

        treated_response = self.treat_commands(command, response,argument)

        return treated_response


    async def run_tp_command(self,command, argument = '', argument2 = ''):

        if command == 'init sw()':
            logging.info('Discovering sw versions')
            if self.sw_init: # if endpoints are initialized already, skip de command
                logging.info('sw already discovered on previous commands')
                return None

        auth = aiohttp.BasicAuth(self.username, self.password)

        connector = aiohttp.connector.TCPConnector(limit = self.concurrent)

        tasks = []

        error_list = []

        rType= self.obtain_request_type(command) # get_url / post_xml / post_url / expressway / post_mime

        async with aiohttp.ClientSession(auth=auth, connector = connector) as session:

            if rType == 'get_url':

                url = self.obtain_url(command)

                for ep in self.endpoints:

                    task = asyncio.create_task(

                        self.get_url(command = command, ip = ep, url=url, session=session, filter = argument))  # to schedule the execution of a coroutine object

                    tasks.append(task)

            elif rType == 'get_file':  # download files

                sw_support = self.supported_sw(command)

                for ip, ep in self.endpoints.items():

                    url = self.obtain_url(command,sw=ep['sw'])

                    if ep['sw'] in sw_support:

                        task = asyncio.create_task(

                            self.get_file(command = command, ip = ip, url=url, session=session, path = argument))  # to schedule the execution of a coroutine object

                        tasks.append(task)

                    else:
                        logging.error(f'{command }is not supported on {ep["sw"]} and will not be run against {ep} ')

            elif rType == 'expressway':

                url = self.obtain_url(command)

                for ep in self.exp_data:

                    for ip,dict_data in ep.items():

                        jsonData = json.dumps(dict_data)

                        task = asyncio.create_task(
                            self.post_json(command=command, ip=ip, url=url, data=jsonData,
                                          session=session))
                        tasks.append(task)


            elif rType == 'post_mime': # upload files with Multipart

                url = self.obtain_url(command)

                for ep in self.endpoints:

                    # where arguments[0] is the file path

                    mime_arguments =  self.obtain_file(command, argument, ep)

                    task = asyncio.create_task(

                        self.post_mime(command = command, ip = ep, url=url, session=session, arguments = mime_arguments))

                    tasks.append(task)


            elif rType == 'post_url':

                url = self.obtain_url(command)

                #command = self.clean_command(command, argument)

                for ep in self.endpoints:

                    task = asyncio.create_task(
                        #TODO the idea is that argument[0] is always the data needed, need to port to other methods
                        self.post_url(command = command, ip = ep, url=url, session=session))  # to schedule the execution of a coroutine object

                    tasks.append(task)

            elif rType == 'post_xml':

                url = '/putxml'

                '''
                use needs_sw_type if XML body is different depending of the type of sw (TC, CE, roomOS)
                also when the command is supported in CE and not TC or viceversa
                If CE/TC XML matches, no need to populate anything un this method, by default returns False
                '''

                needs_sw = self.needs_sw_type(command)

                customXML = self.customXML(command) # use customXML if XML body is unique per endpoint

                if needs_sw:

                    # the below exceptions can be fixed by passing list arguments as later examples (show users)

                    if command.startswith('upload branding') or command.startswith('upload panel'): #argument = file_name, argument2 = encoded_image

                        data = argument2 # encoded image

                    elif command.startswith('upload macro'):

                        data = [argument,argument2]

                    else:

                        data = argument

                    if not customXML:

                        tcData = self.obtain_data(command = command, argument =data, sw = 'TC')

                        ceData = self.obtain_data(command=command, argument = data, sw = 'CE')

                        roomData = self.obtain_data(command=command, argument = data, sw = 'RoomOS')

                    try:

                        for k,v in self.endpoints.items():

                            if customXML:

                                data = [argument,k] # k = ip. We needit to pass the XML specific information about the endpoint

                                tcData = self.obtain_data(command=command, argument=data, sw='TC')

                                ceData = self.obtain_data(command=command, argument=data, sw='CE')

                                roomData = self.obtain_data(command=command, argument=data, sw='RoomOS')


                            if (v['sw'] == 'CE') and (ceData is not None):

                                if command == 'run migrateEndpoints2cloud()':

                                    if v['canMigrate']:

                                        data = v['activationCode']
                                        ceData = self.obtain_data(command=command, argument=data, sw='CE')
                                        task = asyncio.create_task(
                                            self.post_xml(command=command, ip=v['ip'], url=url, data=ceData,
                                                          session=session, argument=argument))
                                        tasks.append(task)
                                    else:
                                        pass
                                else:

                                    task = asyncio.create_task(
                                        self.post_xml(command=command, ip = v['ip'], url=url, data=ceData,
                                                      session=session, argument = argument))

                                    tasks.append(task)

                            elif (v['sw'] == 'RoomOS') and (roomData is not None):

                                task = asyncio.create_task(
                                    self.post_xml(command=command, ip=v['ip'], url=url, data=roomData,
                                                  session=session, argument = argument))

                                tasks.append(task)

                            elif (v['sw'] == 'TC') and (tcData is not None):

                                task = asyncio.create_task(
                                    self.post_xml(command=command, ip= v['ip'], url=url, data=tcData,
                                                  session=session, argument = argument))

                                tasks.append(task)

                            else:

                                if command == 'run migrateEndpoints2cloud()':

                                    pass

                                else:

                                    logging.warning(f"Command {command} is not supported on {v['sw']} with IP {v['ip']}")

                                    if 'error' in v:

                                        err = v['error']

                                    else:

                                        err = 'unknown error'

                                    error_list.append({v['ip']:{command: {'status':'ERROR', 'response':err}}})

                    except Exception as e:

                        logging.error(e)

                elif customXML:

                    for k, v in self.endpoints.items():



                            xml_body = self.obtain_data(command=command, argument=v['data'])

                            task = asyncio.create_task(
                                self.post_xml(command=command, ip=v['ip'], url=url, data=xml_body,
                                              session=session, argument=argument))

                            tasks.append(task)

                else:
                    if command == 'add contact()':
                        data = [argument,argument2]
                        rData = self.obtain_data(command=command, argument=data)

                    else:
                        rData = self.obtain_data(command=command, argument = argument)


                    for ep in self.endpoints:
                        task = asyncio.create_task(
                            self.post_xml(command = command, ip = ep, url=url,data = rData,
                                          session=session, argument = argument))
                        tasks.append(task)


            else:

                return f'Implementation Error. Could not determine request type for {command}'


            '''
            gather() is meant to neatly put a collection of coroutines (futures) into a single future.
            As a result, it returns a single future object, and, if you await asyncio.gather()
            and specify multiple tasks or coroutines, you’re waiting for all of them to be completed

            The result of gather() will be a list of the results across the inputs:

            '''


            responses = await asyncio.gather(*tasks) # Returns a LIST of dicts being each item an endpoint # Run all the tasks in parallel

            for d in error_list:

                responses.append(d)

            return responses




    async def get_url(self,command, ip, url, session, filter):

        try:

            url = f"https://{ip}{url}"

            resp = await session.request(method="GET", url=url, ssl = False)

            resp.raise_for_status()

            logger.info(f"Got response {resp.status} for {command} in {ip}")

            xml_response = await resp.text()

            dict_response = xmltodict.parse(xml_response)

            #dict_response_debugging = json.dumps(dict_response, indent = 4)

            if filter == 'internal':

                return {'ip': ip, 'result': dict_response}

            flat_response = self.digger(dict_response) # TODO Only for specific commands ??

            sanitized = self.sanitize_digger(flat_response)

            if filter:

                filtered = self.filter_response(response = sanitized, filter = filter)

            else:

                filtered = sanitized
            # Add the arguments back to the root command
            command_w_filter = command.replace('()',f'({filter})')

            response = { ip : { command_w_filter : {
                'status' : resp.status,
                'response' : filtered }}}

            return response

        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError,) as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = getattr(e, "strerror", None)

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'Got response {error} for {command} in {ip}')

            response = {'ip': ip, 'result': f'ERROR'}

            return response

        except Exception as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = f'Error {getattr(e, "strerror", None)}'

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'Got response {error} for {command} in {ip}')

            response = {ip: {command: {
                'status': 'ERROR',
                'response': error}}}

            return response


    async def post_xml(self, command, ip, url, data, session, argument):

        try:

            url = f"https://{ip}{url}"

            resp = await session.request(method="POST", data=data, url=url, ssl=False)

            resp.raise_for_status()

            logger.info(f"Got response {resp.status} for {command} in {ip}")

            xml_response = await resp.text()

            dict_response = xmltodict.parse(xml_response)

            # flat_response = self.digger(dict_response) Does not look to be needed

            # dict_response_debug = json.dumps(dict_response)

            if command == 'show favorites()':

                dict_response = self.clean_favorites(dict_response)

            original_command = command.replace('()', f'({argument})')

            response = {ip: {original_command: {
                'status': resp.status,
                'response': dict_response}}}

            if command == 'show panels()': #TODO dict converstion needs to be moved on treated commands

                response = {ip: {original_command: {
                    'status': resp.status,
                    'response': xml_response}}}

                return response

            return response

        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError,) as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = f'Error {getattr(e, "strerror", None)}'

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'Got response {error} for {command} in {ip}')

            response = {ip: {command: {
                'status': 'ERROR',
                'response': error}}}

            return response


    async def post_url(self, command, ip, url,session):

        try:

            url = f"https://{ip}{url}"

            resp = await session.request(method="POST", url=url, ssl=False)

            resp.raise_for_status()

            logger.info(f"Got response {resp.status} for {command} in {ip}")

            response = await resp.text()

            #dict_response = xmltodict.parse(xml_response) #looks like for post URL responses are already on json format (srting type

            response = {ip: {command: {
                'status': resp.status,
                'response': response}}}

            return response

        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError,) as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = f'Error {getattr(e, "strerror", None)}'

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'Got response {error} for {command} in {ip}')

            response = {ip: {command: {
                'status': 'ERROR',
                'response': error}}}

            return response

        except Exception as err:

            logging.error(err)

    async def post_json(self, command, ip, url, data, session):

        try:

            url = f"https://{ip}{url}"

            resp = await session.request(method="POST", data=data, url=url, ssl=False)

            resp.raise_for_status()

            logger.info(f"Got response {resp.status} for {command} in {ip}")

            response = await resp.text()

            response = {ip: {command: {
                'status': resp.status,
                'response': response}}}

            return response

        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError,) as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = f'Error {getattr(e, "strerror", None)}'

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'Got response {error} for {command} in {ip}')

            response = {ip: {command: {
                'status': 'ERROR',
                'response': error}}}

            return response

        except Exception as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = f'Error {getattr(e, "strerror", None)}'

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'Got response {error} for {command} in {ip}')

            response = {ip: {command: {
                'status': 'ERROR',
                'response': error}}}

            return response

    async def get_file(self, command, ip, url,session,path):

        try:

            total_size = 0
            start = time()
            url = f"https://{ip}{url}"
            filename = os.path.basename(f'{ip}.zip')
            chunk_size = 5 * 2 ** 20
            backup_path = os.path.join(path, filename)
            f = open(backup_path, 'wb')

            async with session.request(method="GET",url = url, timeout=None, ssl = False) as response:

                data_to_read = True

                logger.info(f"Got response {response.status} for {command} in {ip}")

                while data_to_read:

                    data = bytearray()
                    red = 0

                    while red < chunk_size:

                        chunk = await response.content.read(chunk_size - red)

                        if not chunk:
                            data_to_read = False
                            break

                        data.extend(chunk)
                        red += len(chunk)

                    f.write(data)
                f.close()

                response = {ip: {command: {
                    'status': response.status,
                    'response': response.reason}}}

                return response



        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError,) as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = f'Error {getattr(e, "strerror", None)}'

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'Got response {error} for {command} in {ip}')

            response = {ip: {command: {
                'status': 'ERROR',
                'response': error}}}

            return response

        except Exception as err:

            logging.error(err)


    async def post_mime(self, command, ip, url,session,arguments):

        try:

            url = f"https://{ip}{url}"

            data = FormData()

            with open(arguments[0], 'rb') as f:

                data.add_field('file', f, filename=arguments[0], content_type=arguments[1])

                resp = await session.request(method="POST", url=url, data = data, ssl=False)

                resp.raise_for_status()

            logger.info(f"Got response {resp.status} for {command} in {ip}")

            response = await resp.text()

            #dict_response = xmltodict.parse(xml_response) #looks like for post URL responses are already on json format (srting type

            response = {ip: {command: {
                'status': resp.status,
                'response': response}}}

            return response

        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError,) as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = f'Error {getattr(e, "strerror", None)}'

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'Got response {error} for {command} in {ip}')

            response = {ip: {command: {
                'status': 'ERROR',
                'response': error}}}

            return response

        except Exception as err:

            logging.error(err)

    def obtain_request_type(self, command):

        map_dict = {
            'show status()': 'get_url',
            'show config()': 'get_url',
            'show commands()': 'get_url',
            'init sw()': 'get_url',
            'show favorites()': 'post_xml',
            'show users()': 'post_xml',
            'show panels()': 'post_xml',
            'add contact()': 'post_xml',
            'add user()': 'post_xml',
            'add userRole()': 'post_xml',
            'add exp searchRules()': 'expressway',
            'set config()': 'post_xml',
            'set password()': 'post_xml',
            'set systemName()': 'post_xml',
            'factoryReset()': 'post_xml',
            'upload brandingAwake()' : 'post_xml',
            'upload brandingHalfwake()': 'post_xml',
            'upload brandingBackground()': 'post_xml',
            'upload macro()': 'post_xml',
            'upload panel()': 'post_xml',
            'upload wallpaper()': 'post_mime',
            'delete macro()': 'post_xml',
            'enable macro()': 'post_xml',
            'disable macro()': 'post_xml',
            'delete callHistory()': 'post_xml',
            'delete itl()': 'post_xml',
            'delete user()': 'post_xml',
            'delete userRole()':'post_xml',
            'run migrateEndpoints2cloud()':'post_xml',
            'run tp backup()': 'get_file',
            'run tp restore()': 'post_mime',
            'enable macroEditor()':'post_xml',
            'disable macroEditor()': 'post_xml',
            'restart()': 'post_url',
            'restart macroRuntime()':'post_xml',
            'init nextPanelOrder()': 'post_xml',
            'call dial()': 'post_xml',
            'call sendDTMF()': 'post_xml',
            'call disconnect()': 'post_xml'
        }

        if command in map_dict: # means the key exist
            return map_dict[command]

        else:
            logging.error(f'Implementation Error, no request type for {command}')
            return None


    def obtain_url(self, command, sw = ''):

        map_dict = {
            'show status()': '/status.xml',
            'show commands()': '/command.xml',
            'init sw()': '/getxml?location=Configuration/', #populate endpoint info in axapi object
            'show config()': '/getxml?location=/Configuration/&internal=true',
            'restart()' : '/api/restart',
            'upload wallpaper()': '/api/wallpapers',
            'run tp restore()' : '/api/backup'
        }

        if command == 'run tp backup()':
            if sw == 'CE' or sw == 'roomOS':
                return '/api/backup'
            else:
                return '/web/backup/download'

        elif command == 'add exp searchRules()':
            return '/api/provisioning/common/searchrule'

        return map_dict[command]

    def obtain_file(self, command, argument, ep):

        # Arguments[0] being the file path, arguments[1] being the content-type
        arguments = []

        if command == 'upload wallpaper()':

            arguments.append(argument[0])
            arguments.append('image/png')

            return arguments

        elif command == 'run tp restore()':

            backup_file_name = f'{ep}.zip'

            # argument[0] = 'C:\\Users\\ifernand\\Projects\\nautilus\\output\\telepresence\\backup'

            filePath = os.path.join(argument, backup_file_name)

            arguments.append(filePath)
            arguments.append('zip')

        return arguments


    def needs_sw_type(self, command):

        needs_sw = ['show favorites()', 'delete itl()', 'upload brandingAwake()','upload brandingHalfwake()',
                    'upload brandingBackground()','upload macro()','set password()', 'run migrateEndpoints2cloud()',
                    'enable macroEditor()', 'disable macroEditor()','delete macro()', 'enable macro()',
                    'disable macro()','upload panel()','restart macroRuntime()', 'add user()', 'delete user()',
                    'show users()','add userRole()', 'delete userRole()','init nextPanelOrder()', 'show panels()',
                    'run tp restore()']

        for c in needs_sw:
            if command == c:

                return True

        return False

    def supported_sw(self, command):

        if command == 'run tp backup()':

            return ['TC','CE','roomOS']

        else:

            return None



    def customXML(self, command):

        custom_xml = ['set systemName()','run tp restore()','call dial()', 'call sendDTMF()']

        for c in custom_xml:
            if command == c:
                return True

        return False

    def obtain_data(self, command, argument = '', sw = ''):

        if command == 'set config()' and argument:

            try:

                config = json.loads('{' + argument + '}')

            except Exception as err:

                logging.error(err)

                return 'ERROR'

            for k, v in config.items():

                list_with_items = k.split('.')

                dict_result = self.list2dict(list_with_items, v)

            xml_result = xmltodict.unparse(dict_result,full_document=False)

            return xml_result

        elif command == 'show favorites()':

            xml_string = '<Command><Phonebook><Search><PhonebookType>Local</PhonebookType></Search></Phonebook></Command>'

            return xml_string

        elif command == 'add contact()':

            xml_string = f'<Command><Phonebook><Contact><Add><Name>{argument[0]}</Name><Number>{argument[1]}</Number></Add></Contact></Phonebook></Command>'

            return xml_string

        elif command == 'set systemName()':

            xml_string = '''
                        <Configuration>
            	            <SystemUnit>
            	            	<Name>''' + argument[0] + '''</Name>
            	            </SystemUnit>
                        </Configuration>
                        '''

            return xml_string

        elif command == 'call dial()':

            xml_string = '''
                        <Command>
            	            <Dial>
            	            	<Number>''' + argument[0] + '''</Number>
            	            </Dial>
                        </Command>
                        '''

            return xml_string

        elif command == 'call sendDTMF()':

            xml_string = '''
                         <Command>
             	            <Call>
             	            	<DTMFSend>
             	            	    <DTMFString>''' + argument[0] + '''</DTMFString>
             	            	</DTMFSend>
             	            </Call>
                         </Command>
                         '''

            return xml_string

        elif command == 'call disconnect()':

            xml_string = '''
                         <Command>
             	            <Call>
             	            	<Disconnect>
             	            	</Disconnect>
             	            </Call>
                         </Command>
                         '''
            return xml_string


        elif command == 'set password()':

            if sw == 'CE' or sw == 'RoomOS':

                xml_string = '''
                            <Command>
                	            <UserManagement>
                	            	<User>
                	            		<Passphrase>
                	            			<Change>
                	            				<NewPassphrase>''' + argument + '''</NewPassphrase>
                	            				<OldPassphrase>''' + self.password + '''</OldPassphrase>
                	            			</Change>
                	            		</Passphrase>
                	            	</User>
                	            </UserManagement>
                            </Command>

                            '''

            elif sw == 'TC':

                xml_string = '''
                            <Command>
                	            <SystemUnit>
                	            	<AdminPassword>
                	            		<Set>
                	            			<Password>''' + argument + '''</Password>
                	            		</Set>
                	            	</AdminPassword>
                	            </SystemUnit>
                            </Command> 
                            '''

        elif command == 'add user()':

            if sw == 'CE' or sw == 'RoomOS':

                xml_string = '''
                            <Command>
                	            <UserManagement>
                	            	<User>
                	            		<Add>,
                	            		
                	            			<Active>True</Active>
                	            			<Passphrase>''' + argument[1] + '''</Passphrase>
                	            			<Role>''' + argument[2] + '''</Role>
                	            			<Username>''' + argument[0] + '''</Username>
                	            			<YourPassphrase>''' + self.password + '''</YourPassphrase>
                	            		</Add>
                	            	</User>
                	            </UserManagement>
                            </Command>
                            '''
            else:
                return None

        elif command == 'delete user()':

            if sw == 'CE' or sw == 'RoomOS':

                xml_string = '''
                            <Command>
                	            <UserManagement>
                	            	<User>
                	            		<Delete>
                	            			<Username>''' + argument[0] + '''</Username>
                	            			<YourPassphrase>''' + self.password + '''</YourPassphrase>
                	            		</Delete>
                	            	</User>
                	            </UserManagement>
                            </Command>
                            '''
            else:
                return None

        elif command == 'show users()':

            if sw == 'CE' or sw == 'RoomOS':

                xml_string = '''
                            <Command>
                	            <UserManagement>
                	            	<User>
                	            		<List>
                	            		</List>
                	            	</User>
                	            </UserManagement>
                            </Command>
                            '''
            else:
                return None

        elif command == 'add userRole()':

            if sw == 'CE' or sw == 'RoomOS':

                xml_string = '''
                            <Command>
                	            <UserManagement>
                	            	<User>
                	            		<Modify>
                	            		    <AddRole>''' + argument[1] + '''</AddRole>
                	            		    <Username>''' + argument[0] + '''</Username>
                	            		    <YourPassphrase>''' + self.password + '''</YourPassphrase>
                	            		</Modify>
                	            	</User>
                	            </UserManagement>
                            </Command>
                            '''
            else:
                return None

        elif command == 'delete userRole()':

            if sw == 'CE' or sw == 'RoomOS':

                xml_string = '''
                            <Command>
                	            <UserManagement>
                	            	<User>
                	            		<Modify>
                	            		    <RemoveRole>''' + argument[1] + '''</RemoveRole>
                	            		    <Username>''' + argument[0] + '''</Username>
                	            		    <YourPassphrase>''' + self.password + '''</YourPassphrase>
                	            		</Modify>
                	            	</User>
                	            </UserManagement>
                            </Command>
                            '''
            else:
                return None

        elif command.startswith('upload branding'):

            if sw != 'TC':
                if command == 'upload brandingAwake()':
                    type = 'Branding'
                elif command == 'upload brandingHalfwake()':
                    type = 'HalfwakeBranding'
                elif command == 'upload brandingBackground()':
                    type = 'HalfwakeBackground'
                elif command == 'upload background()':
                    type = 'Background'

                else:
                    type = ''

                xml_string = '''
                            <Command>
                                <UserInterface>
                                	<Branding>
                                		<Upload>
                                			<Type>''' + type + '''</Type>
                                			<body>''' + argument + '''</body>
                                		</Upload>
                                	</Branding>
                                </UserInterface>
                            </Command>
                            '''

            else:

                return None


        elif command == 'upload macro()':

            if sw != 'TC':

                xml_string = '''
                            	<Command>
                            		<Macros>
                            			<Macro>
                            				<Save>
                            					<Name>''' + argument[0] + '''</Name>
                            					<Overwrite>True</Overwrite>
                            					<body>''' + argument[1] + '''</body>
                            				</Save>
                            			</Macro>
                            		</Macros>
                            	</Command>
    
                            '''
            else:
                return None

        elif command == 'upload panel()':
            """
            if sw != 'TC':

                xml_string = '''
                                    <Command>
                		                <UserInterface>
                		                	<Extensions>
                		                		<Save>
                                                    <PanelId>''' + argument[0] + '''</PanelId>
                		                			<body>''' + argument[1] + '''</body>
                                                </Save>
                		            	    </Extensions>
                		                </UserInterface>
                	                </Command>
                                                '''
            else:
                return None
            """

            if sw != 'TC':

                xml_string = '''
                    <Command>
		                <UserInterface>
		                	<Extensions>
		                		<Set>
                                    <ConfigId>1</ConfigId>
		                			<body>''' + argument + '''</body>
                                </Set>
		            	    </Extensions>
		                </UserInterface>
	                </Command>
                                    '''
            else:
                return None


        elif command == 'show panels()':

            if sw != 'TC':
                xml_string = '''
                        <Command>
                            <UserInterface>
                            	<Extensions>
                            		<List></List>
                        	    </Extensions>
                            </UserInterface>
                        </Command>
                                        '''
            else:
                return None

        elif command == 'enable macro()':

            if sw != 'TC':

                xml_string = '''

                <Command>
                    <Macros>
                        <Macro>
                            <Activate>
                                <Name>''' + argument + '''</Name>
                            </Activate>	
                        </Macro>
                    </Macros>
                </Command>
    
            '''
            else:
                return None

        elif command == 'disable macro()':

            if sw != 'TC':

                xml_string = '''

                <Command>
                    <Macros>
                        <Macro>
                            <Deactivate>
                                <Name>''' + argument + '''</Name>
                            </Deactivate>	
                        </Macro>
                    </Macros>
                </Command>
    

            '''
            else:
                return None

        elif command == 'restart macroRuntime()':

            if sw != 'TC':

                xml_string = '''

                <Command>
                    <Macros>
                        <Runtime>
                            <Restart>
                            </Restart>	
                        </Runtime>
                    </Macros>
                </Command>

            '''
            else:
                return None


        elif command == 'enable macroEditor()':

            if sw != 'TC':

                xml_string = '''
	                            <Configuration>
	                            	<Macros>
	                            		<Mode>On</Mode>
	                            	</Macros>
	                            </Configuration>
                            '''
            else:
                return None

        elif command == 'disable macroEditor()':

            if sw != 'TC':
                xml_string = '''
                                    <Configuration>
                                        <Macros>
                                            <Mode>Off</Mode>
                                        </Macros>
                                    </Configuration>
                                '''
            else:
                return None

        elif command == 'factoryReset()':

            xml_string = '''
            
                <Command>
                    <SystemUnit>
                        <FactoryReset>
                            <Confirm>yes</Confirm>
                            <Keep item='1'>Network</Keep>
                            <Keep item='2'>LocalSetup</Keep>
                            <Keep item='3'>SerialPort</Keep>
                            <Keep item='4'>Certificates</Keep>
                            <Keep item='5'>HTTP</Keep>
                        </FactoryReset>
                    </SystemUnit>
                </Command>
            
            '''

        elif command == 'run migrateEndpoints2cloud()':

            if sw == 'CE':

                xml_string = f'<Command><Webex><Registration><Start><ActivationCode>{argument}</ActivationCode>' \
                            f'<SecurityAction>NoAction</SecurityAction></Start></Registration></Webex></Command>'
            else:

                return None


        elif command == 'delete callHistory()':

            xml_string = '<Command><CallHistory><DeleteAll></DeleteAll></CallHistory></Command>'

        elif command == 'delete macro()':

            if sw != 'TC':

                xml_string = '''
    
                    <Command>
                        <Macros>
                            <Macro>
                                <Remove>
                                    <Name>''' + argument + '''</Name>
                                </Remove>	
                            </Macro>
                        </Macros>
                    </Command>
    
                '''

            else:
                return None

        elif command == 'delete itl()':

            if sw == 'TC':

                xml_string = '<Command><Provisioning><CUCM><CTL><Delete command="True"/></CTL></CUCM></Provisioning></Command>'

            elif sw == 'CE':

                xml_string = '''<XmlDoc internal="true"><Command><Security><Certificates><CUCM><CTL>
                <Delete command="True"></Delete></CTL></CUCM></Certificates></Security></Command></XmlDoc>'''

            elif sw == 'RoomOS':

                return None

            else:
                logging.error('SW type not identified while removing ITL file')
                return None

        elif command == 'run tp restore()':

            if sw == 'CE' or sw == 'RoomOS':

                # argument[1] = ip

                backup_file_name = f'{argument[1]}.zip'

                # argument[0] = 'C:\\Users\\ifernand\\Projects\\nautilus\\output\\telepresence\\backup'

                filePath = os.path.join(argument[0], backup_file_name)

                sha512 = calc_sha512(filePath)

                backup_url = f'http://localhost:8000/output/telepresence/backup/{backup_file_name}'

                xml_string = '''
                            <Command>
                	            <Provisioning>
                	            	<Service>
                	            		<Fetch>
                	            		    <Checksum>''' + sha512 + '''</Checksum>
                	            		    <URL>''' + backup_url + '''</URL>
                	            		</Fetch>
                	            	</Service>
                	            </Provisioning>
                            </Command>
                            '''
            else:
                return None

        else:

            err = f'Unable to provide XML data due to a version issue for {command}'
            logging.error(err)
            return err


        return xml_string

    def new_digger(self,d, keyList=[]):

        # Goes through a nested dict, concatenates the key sequence until it finds de value
        # stores the key sequence and the value in a new flat dict
        # returns the new dict

        status = {}

        for key, value in d.items():
            for ke, va in value.items(): # looping dictionary
                for k, v in va['response'].items():
                    keyList.append(k) # We save each key which will be shown as a flat result
                    if isinstance(v, dict): # we check if the value is a dict
                        st = self.new_digger(v, keyList) #if v is a dict, we want to get into it recursevely and keep storing its jey lists
                        status.update(st)
                        if len(keyList) > 0:
                            keyList.pop()
                    elif isinstance(v, list):
                        n = 1
                        for i in v:
                            keyList.append(str(n)) # we append the item number in the key list to make sure we capture all items in a list,
                            st = self.digger(i, keyList)
                            status.update(st)
                            n += 1
                            keyList.pop()
                        if len(keyList) > 0:
                            keyList.pop()
                    else:
                        stringy = ''
                        for k in keyList:
                            if len(stringy) == 0:
                                stringy = k
                            else:
                                stringy = stringy + '.' + k
                        status[stringy] = v
                        keyList.pop()
        return status

    def digger(self,d, keyList=[]):

        # Goes through a nested dict, concatenates the key sequence until it finds de value
        # stores the key sequence and the value in a new flat dict
        # returns the new dict

        status = {}

        try:

            for k, v in d.items(): # looping dictionary

                keyList.append(k) # We save each key which will be shown as a flat result

                if isinstance(v, dict): # we check if the value is a dict

                    st = self.digger(v, keyList) #if v is a dict, we want to get into it recursevely and keep storing its jey lists

                    status.update(st)

                    if len(keyList) > 0:

                        keyList.pop()

                elif isinstance(v, list):

                    n = 1

                    for i in v:

                        keyList.append(str(n)) # we append the item number in the key list to make sure we capture all items in a list,

                        st = self.digger(i, keyList)

                        status.update(st)

                        n += 1

                        keyList.pop()

                    if len(keyList) > 0:

                        keyList.pop()

                else:

                    stringy = ''

                    for k in keyList:

                        if len(stringy) == 0:

                            stringy = k

                        else:

                            stringy = stringy + '.' + k

                    status[stringy] = v

                    keyList.pop()
        except Exception as e:
            logging.error(e)

        return status

    def sanitize_digger(self, dicty):

        try:

            sanitized_config = {}

            for k, v in dicty.items(): # 'k' is the concatenated config string, 'v' the actual value

                if '@valueSpaceRef' in k:
                    pass

                elif '@maxOccurrence' in k:
                    pass

                elif '@hidden' in k:
                    pass

                elif '@item' in k:
                    pass

                elif '.#text' in k:

                    new_k = k.replace('.#text','')

                    sanitized_config[new_k] = v

                else:
                    sanitized_config[k] = v

            return sanitized_config

        except Exception as e:

            logging.error('Error sanitizing digger')
            logging.error(str(e))

            return dicty


    def filter_response(self, response, filter):

        temp_config = {}

        try:

            for key, value in response.items(): # key is configuration item
                if filter in key:
                    temp_config[key] = value

            return temp_config

        except Exception as e:

            logging.error('Error on axapi.filter_response ')

            logging.error(str(e))

            return response


    def flatten_dict(self, d): # Nicer but not used yet, TODO migrate from my own grown if it makes sense

        def expand(key, value):

            if isinstance(value, dict):

                return [(key + '.' + k, v) for k, v in self.flatten_dict(value).items()]
            else:
                return [(key, value)]

        items = [item for k, v in d.items() for item in expand(k, v)]

        return dict(items)


    def list2dict(self, listy, value):

        tree_dict = {}

        first_iteration = True # to load the final value

        for key in reversed(listy):

            if first_iteration:

                tree_dict = {key: value}
                first_iteration = False

            else:

                if key.isdigit():

                    attribute = {"@item": key}
                    tree_dict.update(attribute)

                else:

                    tree_dict = {key: tree_dict}

        return tree_dict


    def clean_favorites(self, response):

        is_TC = False

        final_response = {}

        try:

            num_entries = response["Command"]["PhonebookSearchResult"]["ResultInfo"]["TotalRows"]

        except KeyError as k:

            is_TC = True

            try:

                num_entries = response["Command"]["PhonebookSearchResult"]["ResultSet"]["ResultInfo"]["TotalRows"]["#text"]

            except KeyError as e:

                logging.error('Unable to pull number of entries in favorites, it will not reformat the result')

                return response


        if  num_entries ==  '0':

            final_response = 'This endpoint does not have favorites'

        else:

            cleaned_response = self.sanitize_dict_response(response)

            cleaned_response_debug = json.dumps(cleaned_response, indent=4) # for debugging only, please comment when when finished

            if is_TC == False: # CE and roomOS endpoints

                try:

                    if 'Contact' in cleaned_response['Command']['PhonebookSearchResult']:
                        contact_response = cleaned_response['Command']['PhonebookSearchResult']['Contact']

                        final_response['Contact'] = contact_response

                    if 'Folder' in cleaned_response['Command']['PhonebookSearchResult']:

                        folder_response = cleaned_response['Command']['PhonebookSearchResult']['Folder']
                        final_response['Folder'] = folder_response

                except KeyError as k:

                    logging.error(' while sanitizing favorites for a CE/roomOS endpoint')
                    logging.error(k)

            else: # TC software

                try:

                    if 'Contact' in cleaned_response['Command']['PhonebookSearchResult']["ResultSet"]:

                        contact_response = cleaned_response['Command']['PhonebookSearchResult']["ResultSet"]['Contact']

                        final_response['Contact'] = contact_response

                    if 'Folder' in cleaned_response['Command']['PhonebookSearchResult']["ResultSet"]:

                        folder_response = cleaned_response['Command']['PhonebookSearchResult']["ResultSet"]['Folder']
                        final_response['Folder'] = folder_response

                except KeyError as k:

                    logging.error(' while sanitizing favorites for a TC endpoint')
                    logging.error(k)

        return final_response



    def sanitize_dict_response(self, d):

        # We recursevely get into each dict and remove unnecesary tags

        sanitized_response = {}

        for k, v in d.items():

            if k == "ResultInfo":

                pass

            elif k == 'Title':
                pass

            elif isinstance(v,
                            dict):  # If the value is another dict, we recursively call the same function to get into it

                temp_result = self.sanitize_dict_response(v)

                if '#text' in temp_result:  # removing #text key and putting the value one level up

                    sanitized_response[k] = temp_result['#text']

                else:
                    sanitized_response[k] = temp_result  # store the cleaned response in the new dict


            elif isinstance(v, list):  # If the value is a list, we iterate the items, which are always a dict

                temp_list = []  # this will be the new list with dicts cleaned

                for di in v:
                    temp = self.sanitize_dict_response(di)

                    temp_list.append(temp)  # appending each item to the new list

                sanitized_response[k] = temp_list  # add the new list to the cleaned dict

            elif '@valueSpaceRef' in k:  # removing this tags and the ones below
                pass

            elif '@maxOccurrence' in k:
                pass

            elif '@hidden' in k:
                pass

            elif '@item' in k:
                pass

            elif '@queryId' in k:
                pass

            elif '@offSet' in k:
                pass

            elif '@pageSize' in k:
                pass

            elif '@totalResultSet' in k:
                pass

            elif '@localId' in k:
                pass

            else:
                sanitized_response[k] = v

        return sanitized_response


    async def init_sw(self,ip, url, session):

        try:

            url = f"https://{ip}{url}"

            resp = await session.request(method="GET", url=url, ssl = False)

            resp.raise_for_status()

            logger.info(f"Got response {resp.status} for endpoint: {ip}")

            xml_response = await resp.text()

            dict_response = xmltodict.parse(xml_response)

            #dict_response_debugging = json.dumps(dict_response, indent = 4)

            return {'ip': ip, 'sw': dict_response}


        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError,) as e:

            status = getattr(e, "status", None)
            message = getattr(e, "message", None)
            strerror = getattr(e, "strerror", None)

            if strerror:
                error = strerror
            else:
                error = f'{status} : {message}'

            logger.error(f'{error} for endpoint: {ip}')

            response = {'ip': ip, 'sw': None, 'error': error}

            return response

    def nameInWebexPlace(self,name, webexPlaces):

        try:

            if isinstance(webexPlaces, list):

                for place in webexPlaces:

                    if place['displayName'] == name:

                        return True

            else:
                logging.error('NameInWebexPlace did not receive a list')

            return False

        except Exception as err:

            logging.error(err)


    def canMigrate2cloud(self, webexPlaces):

        for k, endpoint_dict in self.endpoints.items():

            try:

                if endpoint_dict['sw'] == 'unknown':

                    endpoint_dict['canMigrate'] = False
                    endpoint_dict['migrationError'] = 'Unable to access the endpoint'

                else:

                    name = endpoint_dict['name']
                    version = float(endpoint_dict['versionNumber'])
                    ip = endpoint_dict['ip']
                    existingPlace = self.nameInWebexPlace(endpoint_dict['name'], webexPlaces)
                    endpoint_dict['migrationError'] = ''
                    endpoint_dict['canMigrate'] = True

                    if not name:

                        endpoint_dict['canMigrate'] = False
                        endpoint_dict['migrationError'] = 'No System Name found'

                    if existingPlace:
                        endpoint_dict['canMigrate'] = False
                        endpoint_dict['migrationError'] += f"Webex Place already exist with name {endpoint_dict['name']} "

                    if endpoint_dict['sw'] != 'CE':
                        endpoint_dict['canMigrate'] = False
                        endpoint_dict['migrationError'] += 'Only CE software can be migrated'

                    if endpoint_dict['canMigrate'] and endpoint_dict['sw'] == 'CE':  # migrate2cloud is only supportted on CE sw

                        if version >= 9.8:  # only CE9.8 or higher supports migrate2cloud

                            endpoint_dict['canMigrate'] = True

                        else:

                            endpoint_dict['canMigrate'] = False
                            endpoint_dict['migrationError'] += f"version {endpoint_dict['version']} is lower than minimum CE 9.8"


            except Exception as err:

                logging.error(err)

    def initialize_sw_on_endpoints(self, responses):


        for resp in responses:

            try:

                ip =resp['ip']

                if resp['result'] == 'ERROR':

                    version = 'Unknown'

                elif resp['result'] is not None:
                    version = resp['result']['Configuration']['@version']

                else:
                    version = 'Unknown'

                if version.startswith('TC'):
                    sw = 'TC'
                    reg = re.search("TC(.)\.(.)\.(.*)\..*", version)
                    versionNumber = f'{reg.group(1)}.{reg.group(2)}{reg.group(3)}'


                elif version.startswith('ce'):
                    sw = 'CE'
                    reg = re.search("ce(.)\.(.).*", version)
                    versionNumber = f'{reg.group(1)}.{reg.group(2)}'

                else:
                      sw = 'unknown'

                if sw == 'unknown':
                    self.endpoints[ip]['sw'] = sw

                else:

                    self.endpoints[ip]['sw'] = sw
                    self.endpoints[ip]['version'] = version
                    self.endpoints[ip]['versionNumber'] = versionNumber
                    self.endpoints[ip]['mode'] = resp['result']['Configuration']['Provisioning']['Mode']['#text']

                    if '#text' in resp['result']['Configuration']['SystemUnit']['Name']:
                        self.endpoints[ip]['name'] = resp['result']['Configuration']['SystemUnit']['Name']['#text']
                    else:
                        self.endpoints[ip]['name'] = ''

                    #self.endpoints[ip]['mode'] = resp['result']['Configuration']['Provisioning']['Mode']['#text']




            except KeyError as ke:

                logging.error(f'While initializing sw on endpoint {resp}')
                logging.error(ke)

        return None


    def clean_command(self, command, arguments): # used to pass the root command + filter to POST, GET method for proper response output

        # The idea is that arguments[1] is always the unencoded filter for proper response handling

        if command == 'upload wallpaper()':

            return f'upload wallpaper({arguments[1]})'

    def treat_commands(self, command, response,argument):

        '''
        treat mainly how the output will be presented
            show commands will show in flattened way
            init sw will only initialize axapi.endpoints with different attributes
        '''

        logging.info('treating command')

        if command == 'init sw()':

            if self.sw_init == False:

                self.initialize_sw_on_endpoints(response)
                self.sw_init = True
                return None

        elif command == 'show users()': # for show users we present it in a flattened way with digger.

            sanitized_results = []

            for ep in response:

                temp_result = {}

                for ip, value in ep.items():
                    for command, va in value.items():  # looping dictionary
                        flat_response = self.digger(va['response']['Command']['UserListResult'])  #
                        sanitized = self.sanitize_digger(flat_response)
                        if argument:
                         sanitized = self.filter_response(response=sanitized, filter=argument[0])

                        try:
                            temp_result[ip] = {}
                            temp_result[ip][command] = sanitized

                        except Exception as err:
                            logging.error(err)

                sanitized_results.append(temp_result)

            '''response = {ip: {command_w_filter: {
                'status': resp.status,
                'response': filtered}}}'''

            return sanitized_results

        elif command == 'init nextPanelOrder()':

            self.initialize_nextPanelOrder(response)
            return None



        else:
            return response