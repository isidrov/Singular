
#test
from time import sleep
import os

import logging
# the one below needs to be installed
import xmltodict
import time
import json
import traceback

import http.server
import socketserver

import requests

import csv

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client


#http_client.HTTPConnection.debuglevel = 1

logger = logging.getLogger(__name__)



class XAPI:

    def __init__(self):

        self.ip = ''
        self.auth = ''
        self.headers = ''
        self.mac = ''
        self.system_name = ''
        self.sw = ''
        self.uri = ''
        self.version = ''



    def set_params(self,ip = '', username = '', password = ''):


        self.auth = (username, password)
        self.headers = {'Content-Type': 'text/xml'}

        self.ip = ip
        self.xml_url = 'https://' + self.ip + '/putxml'
        self.xmlform_url = 'https://' + self.ip + '/formputxml' #TODO not used?
        self.status_url = 'https://' + self.ip + '/status.xml'


        status = self.get_status()


        if status['code'] == 'OK':

            try:

                temp_version = status['result']['Status']['SystemUnit']['Software']['Version']

                try:

                    self.version = temp_version.get('#text')

                except Exception as exc:

                    self.version = temp_version

                if self.version.startswith('TC'):

                    self.sw = 'TC'

                elif self.version.startswith('ce'):

                    display = status['result']['Status']['SystemUnit']['Software']['DisplayName']

                    if display.startswith('RoomOS'):

                        self.sw = 'roomOS'

                    elif display.startswith('ce'):

                        self.sw = 'CE'

                    else:

                        self.sw = 'ERROR'
                        logging.error('Endpoint SW originally classified as CE cannot be confirmed')

                else:

                    self.sw = 'ERROR'
                    logging.error('Endpoint SW cannot be determmined')

                logging.info('Endpoint sw type is: ' + self.sw)
                logging.info('Endpoint sw version is: ' + self.version)

                self.mac = self.get_value(status['result']['Status']['Network']['Ethernet']['MacAddress'])

                if self.sw == 'TC':
                    self.uri = status['result']['Status']['SIP']['Profile']['Registration']['URI']['#text']

                elif self.sw == 'CE':
                    self.uri = status['result']['Status']['SIP']['Registration']['URI']

                elif self.sw == 'roomOS':
                    self.uri = status['result']['Status']['UserInterface']['ContactInfo']['ContactMethod']['Number']

                else:
                    self.uri = 'ERROR'

                if self.sw == 'TC':
                    self.system_name = status['result']['Status']['SystemUnit']['ContactInfo']['#text']

                elif self.sw == 'CE' or self.sw =='roomOS':
                    self.system_name = status['result']['Status']['UserInterface']['ContactInfo']['Name']

                else:
                    self.system_name = 'ERROR'

                return status

            except KeyError as kerror:

                logging.error('KeyError under set_params()')
                logging.error(kerror)

                return status

            except Exception as gen:

                logging.error('Generic Error under set_params()')
                logging.error(gen)

                return status


        else:

            logging.error(status['result'])

            return status

        ''' 
        Values in  TC software are given with key '#text' while CE doesn't
        get_value(dict, key sequence) does check the software and returns the correct value taking into
        account the above condition.
        '''


    def get_value(self,dict):

        if self.sw == 'CE':

            return dict

        elif self.sw == 'TC':

            return dict['#text']

        else:
            return 'ERROR'

    def post_xml(self, xml_str):

        logging.info('Posting XML')

        try:

            response = requests.request("POST", url=self.xml_url, data=xml_str, auth= self.auth,headers=self.headers, verify=False)

            logging.info('POST Response code: ' + str(response.status_code))

            return {'code':'OK','result': xmltodict.parse(response.content)}

        except Exception as exc:

            logging.error('returning error under post_xml():\n' + str(exc))

            return {'code': 'ERROR', 'result': exc}


    def postform_xml(self, xml_str): # TODO NOT USED???

        logging.info('Posting XML')

        try:

            response = requests.request("POST", url=self.xmlform_url, data=xml_str, auth= self.auth,headers=self.headers, verify=False)

            logging.info('POST Response code: ' + str(response.status_code))

            return {'code':'OK','result': xmltodict.parse(response.content)}

        except Exception as exc:

            logging.error('returning error under post_xml():\n' + str(exc))

            return {'code': 'ERROR', 'result': exc}



    def post_url(self, url):

        logging.info('Posting URL')

        try:

            response = requests.request("POST", url=url, auth= self.auth,headers=self.headers, verify=False)

            return {'code':'OK','result': response.text}


        except Exception as exc:

            logging.error('returning error under post_url():\n' + str(exc))

            return {'code': 'ERROR', 'result': exc}

    def post_file(self, url, file):

        logging.info('Posting URL with data')

        try:

            files = {'file': (file, open(file, 'rb'), 'image/png')}

            response = requests.request("POST", url=url, files=files, auth=self.auth,
                                        verify=False)

            logging.info('POST Response code: ' + str(response.status_code))
            logging.info('POST Response content: ' + str(response.content))

            return {'code': 'OK', 'result': response.text}

        except Exception as exc:

            logging.error('returning error under post_file():\n' + str(exc))

            return {'code': 'ERROR', 'result': exc}

    def get_url(self , url):

        try:

            response = requests.request("GET", url = url,auth= self.auth,headers=self.headers, verify=False)

            response.raise_for_status() # raise an exception if it is not a 200 response


        except requests.exceptions.HTTPError as exc:

            # Whoops it wasn't a 200

            return {'code': 'ERROR', 'result': str(exc)}

        except Exception as exc:

            logging.error('returning error under get_url():\n' + str(exc))

            return {'code': 'ERROR', 'result': str(exc)}

        # Must have been a 200 status code

        rContent = response.content

        return {'code': 'OK', 'result': xmltodict.parse(rContent)}

    def digger(self,d, keyList=[]):

        # Goes through a nested dict, concatenates the key sequence until it finds de value
        # stores the key sequence and the value in a new flat dict
        # returns the new dict

        status = {}

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

                    stringy = stringy + '.' + k

                status[stringy] = v

                keyList.pop()

        return status

    def sanitize_dict_response(self,d):

        #We recursevely get into each dict and remove unnecesary tags

        sanitized_response = {}


        for k, v in d.items():

            if k == "ResultInfo":

                pass

            elif k == 'Title':
                pass

            elif isinstance(v, dict): #If the value is another dict, we recursively call the same function to get into it


                temp_result = self.sanitize_dict_response(v)

                if '#text' in temp_result: # removing #text key and putting the value one level up

                    sanitized_response[k] = temp_result['#text']

                else:
                    sanitized_response[k] = temp_result # store the cleaned response in the new dict


            elif isinstance(v, list): #If the value is a list, we iterate the items, which are always a dict

                temp_list = []# this will be the new list with dicts cleaned

                for di in v:

                    temp = self.sanitize_dict_response(di)

                    temp_list.append(temp) # appending each item to the new list

                sanitized_response[k] = temp_list # add the new list to the cleaned dict

            elif '@valueSpaceRef' in k: #removing this tags and the ones below
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

    def sanitize_digger(self, dicty):

        sanitized_response = {}

        for k, v in dicty.items():

            if '@valueSpaceRef' in k:
                pass

            elif '@maxOccurrence' in k:
                pass

            elif '@hidden' in k:
                pass

            elif '@item' in k:
                pass

            elif 'xperimental' in k:
                pass

            elif '.#text' in k:
                new_k = k.replace('.#text','')
                sanitized_response[new_k] = v

            else:
                sanitized_response[k] = v


        return sanitized_response

    def call(self, destination):

        logging.info('calling ' + destination)

        xml_string = '<Command><Dial><Number>' + destination + '</Number></Dial></Command>'

        response = self.post_xml(xml_string)

        # TODO timers, we will probably need to look at async
        
        try:
            if response['code'] == 'OK':

                call_id = self.get_value(response['result']['Command']['DialResult']['CallId'])

                logging.info('Call initiated succesfully, returning callId ' + str(call_id))

            else:
                logging.error(response)

        except Exception as e:
            logging.error(e)

    #TODO figure out what to do with the method below

    def call_endpoint(self , endpoint):

        logging.info('calling ' + endpoint.uri)

        xml_string = '<Command><Dial><Number>' + endpoint.uri + '</Number></Dial></Command>'

        response =  self.post_xml(xml_string)

        try:
            if response['code'] == 'OK': #TODO for roomOS

                call_id = self.get_value(response['result']['Command']['DialResult']['CallId'])


                logging.info('Call initiated succesfully, returning callId ' + str(call_id))

                sleep(2)
                resp = endpoint.answer()

                if resp['code'] == 'OK':
                    logging.info('Call ' + call_id + 'answered correctly')
                    return call_id
                else:
                    logging.error('Call ' + call_id + 'was NOT answered correctly')
                    return None
            else:
                logging.error('Call to number ' + endpoint.uri + ' not initiated succesfully')
                return None

        except Exception as ex:

            logging.error(ex)

            return None

    def answer(self):

        logging.info('answering call')

        xml_string = '<Command><Call><Accept></Accept></Call></Command>'

        response =  self.post_xml(xml_string)

        return response

    def disconnect(self):

        logging.info('disconnecting call')

        callId_temp = self.get_status()
        json_temp = json.dumps(callId_temp)

        try:


            callId = callId_temp['result']['Status']['Call']['@item']

            xml_string = '<Command><Call><Disconnect><CallId>' + callId + '</CallId></Disconnect></Call></Command>'

            response = self.post_xml(xml_string)


            return response

        except Exception as ex:

            logging.error(ex)

            return None



    def deleteITL(self):

        logging.info('Deleting ITL file')

        if self.sw == 'TC':

            xml_string = '<Command><Provisioning><CUCM><CTL><Delete command="True"/></CTL></CUCM></Provisioning></Command>'

        elif self.sw == 'CE':

            xml_string = '''<XmlDoc internal="true"><Command><Security><Certificates><CUCM><CTL>
            <Delete command="True"></Delete></CTL></CUCM></Certificates></Security></Command></XmlDoc>'''

        elif self.sw == 'roomOS':
            logging.warning('delete_itl() is not supported on roomOS/cloud registered endpoints')
            return None

        else:
            logging.error('SW type not identified while removing ITL file')
            return None

        return self.post_xml(xml_string)


    def set_provisioning_mode(self , mode ):

        logging.info('Setting provisioning mode to ' + str(mode))

        xml_string = '<Configuration><Provisioning><Mode>' + mode + '</Mode></Provisioning></Configuration>'

        return self.post_xml(xml_string)



    def set_external_manager_protocol(self , mode):

        # HTTP or HTTPS
        if self.sw == 'roomOS':

            logging.warning('set_external_manager_protocol not supported on roomOS/cloud registered endpoints')

            return None
        else:

            logging.info('Setting external manager to ' + mode)

            xml_string = '<Configuration><Provisioning><ExternalManager><Protocol>' + mode + '</Protocol></ExternalManager></Provisioning></Configuration>'

            return self.post_xml(xml_string)

    def set_wakeup_in_motion(self , mode):


        if self.sw == 'TC':

            err = 'set wakeupOnMotionDetection is not supported on TC software'
            logging.warning(err)

            return {'code':'ERROR', 'result':err}

        else:

            logging.info('set_wakeup_in_motion() ' + mode)

            xml_string = '<Configuration><Standby><WakeupOnMotionDetection>' + mode + '</WakeupOnMotionDetection></Standby></Configuration>'

            return self.post_xml(xml_string)

    def set_password(self , old , new):

        if self.sw == 'TC':

            xml_string = '''
            
            <Command>
	            <SystemUnit>
	            	<AdminPassword>
	            		<Set>
	            			<Password>''' + new + '''</Password>
	            		</Set>
	            	</AdminPassword>
	            </SystemUnit>
            </Command> 
            '''

        else:

            xml_string = '''
            
            <Command>
	            <UserManagement>
	            	<User>
	            		<Passphrase>
	            			<Change>
	            				<NewPassphrase>''' + new + '''</NewPassphrase>
	            				<OldPassphrase>''' + old + '''</OldPassphrase>
	            			</Change>
	            		</Passphrase>
	            	</User>
	            </UserManagement>
            </Command>
            
            '''

        return self.post_xml(xml_string)

    def upload_branding(self, image = '', type = '' ):

        if self.sw != 'TC':

            logging.info('Setting background awake image')

            xml_string = '''
            <Command>
                <UserInterface>
                	<Branding>
                		<Upload>
                			<Type>''' + type + '''</Type>
                			<body>''' + image + '''</body>
                		</Upload>
                	</Branding>
                </UserInterface>
            </Command>
            '''

            return self.post_xml(xml_string)

        else:

            return {'code' : 'ERROR', 'result':'set_background_awake not supported on TC software'}

    def upload_wallpaper(self, file=''):

        if self.sw == 'TC':

            logging.info('Uploading wallpaper on TC endpoint')

            url = 'https://' + self.ip + '/api/wallpapers'


            return self.post_file(url = url, file=file)

        else:

            return {'code' : 'ERROR', 'result':'wallpaper upload is not supported on any other than TC software'}

    def set_custom_message(self,  message=''):

        if self.sw != 'TC':

            logging.info('Setting custom message')

            xml_string = '''
             <Command>
                 <UserInterface>
                 	<ContactInfo>
                 		<CustomMessage>''' + message + '''</CustomMessage>
                 	</ContactInfo>
                 </UserInterface>
             </Command>
             '''

            return self.post_xml(xml_string)

        else:

            logging.warning('set_background_awake not supported on TC software')

    def enable_macro_editor(self):

        if self.sw == 'CE' or self.sw == 'roomOS':

            logging.info('Enabling macro editor ...')

            xml_string = '''
    
	            <Configuration>
	            	<Macros>
	            		<Mode>On</Mode>
	            	</Macros>
	            </Configuration>
    
                '''

            return self.post_xml(xml_string)

        else:

            return {'code': 'ERROR', 'result': 'Command not supported on TC software'}

    def disable_macro_editor(self):

        if self.sw == 'CE' or self.sw == 'roomOS':

            logging.info('Disabling macro editor ...')

            xml_string = '''
    
	            <Configuration>
	            	<Macros>
	            		<Mode>Off</Mode>
	            	</Macros>
	            </Configuration>
    
                '''

            return self.post_xml(xml_string)

        else:

            return {'code': 'ERROR', 'result': 'Command not supported on TC software'}

    def enable_macro(self, name=''):

        if self.sw == 'CE' or self.sw == 'roomOS':

            logging.info('Activating macro: ' + name)

            xml_string = '''
    
                <Command>
                    <Macros>
                        <Macro>
                            <Activate>
                                <Name>''' + name + '''</Name>
                            </Activate>	
                        </Macro>
                    </Macros>
                </Command>
    
            '''

            return self.post_xml(xml_string)

        else:

            return {'code': 'ERROR', 'result': 'Command not supported on TC software'}

    def delete_macro(self, name=''):

        if self.sw == 'CE' or self.sw == 'roomOS':

            logging.info('Deleting macro: ' + name)

            xml_string = '''

                <Command>
                    <Macros>
                        <Macro>
                            <Remove>
                                <Name>''' + name + '''</Name>
                            </Remove>	
                        </Macro>
                    </Macros>
                </Command>

            '''

            return self.post_xml(xml_string)

        else:

            return {'code': 'ERROR', 'result': 'Command not supported on TC software'}

    def delete_call_history(self):

        xml_string = '''
        <Command>
	        <CallHistory>
	        	<DeleteAll>
	        	</DeleteAll>
	        </CallHistory>
        </Command>
        '''

        return self.post_xml(xml_string)

    def delete_favorites(self, type):

        if type == 'All': # will delete all folders and contacts from favorites

            temp_response = self.dump_local_phonebooks()

            debug_response = json.dumps(temp_response, indent=4)

            final_response = {'code':'OK', 'result':{}}

            try:

                if 'Folder' in temp_response['result']: # check if there are folders in favorites

                    if isinstance(temp_response['result']['Folder'],list) == False: # If no list (1 folder) we put in on a list to save code

                        temp_list = []
                        temp_list.append(temp_response['result']['Folder'])
                        temp_response['result']['Folder'] = temp_list

                    for folder in  temp_response['result']['Folder']: #loop folder list

                        if 'ParentFolderId' in folder: # we only need to delete root folders, not subfolders
                            pass

                        else:

                            result = self.delete_favorites_folder(folder['FolderId'])

                            debug_result = json.dumps(result, indent=4)

                            if 'FolderDeleteResult' in result['result']['Command']: # CE or roomOS software

                                delete_status = result['result']['Command']['FolderDeleteResult']['@status']

                            elif 'PhonebookFolderDeleteResult' in result['result']['Command']: # TC software

                                delete_status = result['result']['Command']['PhonebookFolderDeleteResult']['@status']

                            else:

                                delete_status = 'unknown'


                            final_response['result'][folder['Name']] = delete_status

                            if delete_status != 'OK':

                                final_response['code'] = 'ERROR'

                if 'Contact' in temp_response['result']: # check if there are contacts in favorites

                    if isinstance(temp_response['result']['Contact'],list) == False: # If no list (1 contact) we put in on a list to save code

                        temp_list = []
                        temp_list.append(temp_response['result']['Contact'])
                        temp_response['result']['Contact'] = temp_list

                    for contact in  temp_response['result']['Contact']: #loop contact list

                        if 'FolderId' in contact: # Contacts inside a folder were already deleted in the previous step (when folder was removed)
                            pass

                        else: # Contact is not inside a folder, needs to be specifically deleted

                            result = self.delete_favorites_contact(contact['ContactId'])

                            debug_result = json.dumps(result, indent=4)

                            if 'ContactDeleteResult' in result['result']['Command']:  # CE or roomOS software

                                delete_status = result['result']['Command']['ContactDeleteResult']['@status']

                            elif 'PhonebookContactDeleteResult' in result['result']['Command']:  # TC software

                                delete_status = result['result']['Command']['PhonebookContactDeleteResult'][
                                    '@status']

                            else:

                                delete_status = 'unknown'

                            final_response['result'][contact['Name']] = delete_status

                            if delete_status != 'OK':

                                final_response['code'] = 'ERROR'

                return final_response

            except KeyError as ke:

                logging.error(ke)
                logging.error(traceback.print_exc())

                final_response['code'] = 'ERROR'
                final_response['result'] = str(ke)

                return final_response


            except Exception as ex:

                logging.error(ex)
                logging.error(traceback.print_exc())

                final_response['code'] = 'ERROR'
                final_response['result'] = str(ex)

                return final_response

        else:
            return {'code':'ERROR','result':'Argument not supported'}




    def delete_favorites_folder(self, FolderId):

        logging.info('Deleting folder: ' + FolderId)

        xml_string = '''
            <Command>
	            <Phonebook>
	            	<Folder>
	            		<Delete>
	            			<FolderId>''' + FolderId + '''</FolderId>
	            		</Delete>
	            	</Folder>
	            </Phonebook>
            </Command>
    
        '''
        return self.post_xml(xml_string)


    def delete_favorites_contact(self, ContactId):

        logging.info('Deleting contact: ' + ContactId)

        xml_string = '''
            <Command>
	            <Phonebook>
	            	<Contact>
	            		<Delete>
	            			<ContactId>''' + ContactId + '''</ContactId>
	            		</Delete>
	            	</Contact>
	            </Phonebook>
            </Command>
        '''
        return self.post_xml(xml_string)


    def disable_macro(self, name=''):

        if self.sw == 'CE' or self.sw == 'roomOS':

            logging.info('Deactivating macro: ' + name)

            xml_string = '''
    
                <Command>
                    <Macros>
                        <Macro>
                            <Deactivate>
                                <Name>''' + name + '''</Name>
                            </Deactivate>	
                        </Macro>
                    </Macros>
                </Command>
    
            '''

            return self.post_xml(xml_string)

        else:

            return {'code': 'ERROR', 'result': 'Command not supported on TC software'}


    def upload_macro(self, name = '', code = ''):

        if self.sw == 'CE' or self.sw == 'roomOS':

            logging.info('Uploading macro')

            xml_string =  '''
    
            	<Command>
            		<Macros>
            			<Macro>
            				<Save>
            					<Name>''' + name + '''</Name>
            					<Overwrite>True</Overwrite>
            					<body>''' + code + '''</body>
            				</Save>
            			</Macro>
            		</Macros>
            	</Command>
    
            '''
            return self.post_xml(xml_string)

        else:

            return {'code':'ERROR', 'result':'Command not supported on TC software'}




    def activate_macro(self, value=''):

        if self.sw == 'CE' or self.sw == 'roomOS':

            logging.info('Uploading macro')

            xml_string = '''

            	<Command>
            		<Macros>
            			<Macro>
            				<Activate>
    					        <Name>''' + value + '''</Name>
    				        </Activate>	
            			</Macro>
            		</Macros>
            	</Command>

            '''

            return self.post_xml(xml_string)

        else:

            return {'code': 'ERROR', 'result': 'Command not supported on TC software'}

    def upload_inroom_config(self, code = ''):

        if self.sw == 'CE' or self.sw == 'roomOS':

            logging.info('Uploading inroom config')

            xml_string = '''
            
            <Command>
		        <UserInterface>
		        	<Extensions>
		        		<Set>
                            <ConfigId>1</ConfigId>
		        			<body>''' + code + '''</body>
                        </Set>
		    	    </Extensions>
		        </UserInterface>
	        </Command>
            
            '''

            return self.post_xml(xml_string)

        else:

            return {'code': 'ERROR', 'result': 'Command not supported on TC software'}

    def upload_CA_cert(self, name = '', cert = ''):

        logging.info('Uploading certificate')

        if self.sw != 'TC':

            xml_string =  '''
    
            	<Command>
            		<Security>
            			<Certificates>
            				<CA>
            				    <Add>
            					    <body>''' + cert + '''</body>
            					</Add>
            				</CA>
            			</Certificates>
            		</Security>
            	</Command>
    
            '''
        else:

            url = 'https://' + self.ip + '/api/auths'

            return self.post_file(url = url, file='root_ottawa_lab.cer')

        return self.post_xml(xml_string)


    def restart(self): #TODO to test and promote

        logging.info('Restarting endpoint: ' + self.ip)

        url = 'https://'+ self.ip + '/api/restart'

        return self.post_url(url)


    def set_autoAnswer(self , mode ):

        logging.info('Setting autoanswer mode to ' + str(mode))

        xml_string = '<Configuration><Conference><AutoAnswer><Mode>' + mode + '</Mode></AutoAnswer></Conference></Configuration>'

        return self.post_xml(xml_string)

     
    def set_external_manager_address(self, cucm):

        if self.sw == 'roomOS':

            logging.warning('set_external_manager_address not supported on roomOS/cloud registered endpoints')

            return None

        else:

            logging.info('Setting external manager IP address to: ' + cucm)

            xml_string = '<Configuration><Provisioning><ExternalManager><Address>' + cucm + '</Address></ExternalManager></Provisioning></Configuration>'

            return self.post_xml(xml_string)



    def set_external_manager_alternate_address(self, cucm):

        if self.sw == 'roomOS':

            logging.warning('set_external_manager_alternate_address not supported on roomOS/cloud registered endpoints')

            return None

        else:

            logging.info('Setting external alternate manager IP address to: ' + cucm)

            xml_string = '<Configuration><Provisioning><ExternalManager><AlternateAddress>' + cucm + '</AlternateAddress></ExternalManager></Provisioning></Configuration>'

            return self.post_xml(xml_string)


    def set_sip_proxy(self,number, address):

        if self.sw == 'roomOS':

            logging.warning('set_sip_proxy not supported on roomOS/cloud registered endpoints')

            return None

        elif self.sw == 'TC':

            xml_string = '<Proxy item="' + number + '"><Address>' + address + '</Address></Proxy>'

            xml_string = '<Configuration><SIP><Profile>' + xml_string + '</Profile></SIP></Configuration>'

            return self.post_xml(xml_string)

        elif self.sw == 'CE':

            xml_string = '<Proxy item="' + number + '"><Address>' + address + '</Address></Proxy>'

            xml_string = '<Configuration><SIP>' + xml_string + '</SIP></Configuration>'

            return self.post_xml(xml_string)

        else:
            return 'ERROR'

    def set_sip_uri(self,uri):

        if self.sw == 'roomOS':

            logging.warning('set sipURI not supported on roomOS/cloud registered endpoints')

            return None

        elif self.sw == 'TC':

            xml_string = '''
            <Configuration>
            		<SIP>
            			<Profile>
            				<URI>''' + uri + '''</URI>
            			</Profile>
            		</SIP>
            </Configuration>
            '''
            
            return self.post_xml(xml_string)

        elif self.sw == 'CE':

            xml_string = '''
            
            <Configuration>
            		<SIP>
            			<URI>''' + uri + '''</URI>
            		</SIP>
            </Configuration>
            '''

            return self.post_xml(xml_string)

        else:
            return 'ERROR'

    def set_book_url(self, url):

        logging.info('Setting URL for phonebook')

        xml_string = '<Configuration><Phonebook><Server><URL>' + url + '</URL></Server></Phonebook></Configuration>'

        url = 'https://'+ self.ip + '/putxml'

        return self.post_xml(xml_string)



    def get_status(self):

        logging.info('Getting status for ' + self.ip)

        url = 'https://' + self.ip + '/status.xml'

        status = self.get_url(url)

        return status

    def get_internal_configuration(self, filter = ''):

        filtered_response = {}

        url = 'https://'+ self.ip + '/getxml?location=/Configuration/&internal=true'

        nested_response = self.get_url(url)

        flat_dict_response = self.digger(nested_response['result'])

        clean_response = self.sanitize_digger(flat_dict_response)

        if filter == '':

            return clean_response

        else:

            for k, v in clean_response.items():

                if filter in k:

                    filtered_response[k] = v

            return filtered_response

    def get_cdp_info(self): # TODO TEST

        logging.info('Getting cdp info')

        url = 'https://'+ self.ip + '/getxml?location=/Status/Network/CDP'

        response = self.get_url(url)

        cdp = response['result']['Status']['Network']

        response['result'] = cdp

        return response


    def get_network(self): #TODO TEST

        logging.info('Getting mac info')

        url = 'https://'+ self.ip + '/getxml?location=/Status/Network/'

        response = self.get_url(url)

        net = response['result']['Status']

        response['result'] = net

        return response


    
    def get_phonebook(self): #TODO Test

        logging.info('Getting phonebook')

        url = 'https://'+ self.ip + '/getxml?location=/Configuration/PhoneBook/'

        response = self.get_url(url)

        net = response['result']['Configuration']

        response['result'] = net

        return response



    def get_phonebook_url(self): #TODO Test

        logging.info('Getting phonebook url')

        url = 'https://'+ self.ip + '/getxml?location=/Configuration/PhoneBook/Server/URL'

        response = self.get_url(url)

        url = response['result']['Configuration']['Phonebook']['Server']['URL']['#text']

        response['result'] = url

        return response


    def get_corporate_phonebook(self): #TODO Test

        logging.info('Searching corporate phonebook in:' + self.ip)

        xml_string = '<Command><Phonebook><Search><PhonebookType>Corporate</PhonebookType></Search></Phonebook></Command>'

        response = self.post_xml(xml_string)

        if response['code'] == 'OK':

            cpb = response['result']['Command']

            response['result'] = cpb

            return response
        else:
            'ERROR'

    def get_local_phonebook(self):

        logging.info('Searching local phonebook in: ' + self.ip)

        xml_string = '<Command><Phonebook><Search><PhonebookType>Local</PhonebookType></Search></Phonebook></Command>'

        response = self.post_xml(xml_string)

        return response


    def dump_status_with_filter(self, filter = ''):

        response = {}

        nested_response = self.get_status()

        debug_nested_response = json.dumps(nested_response, indent = 4)

        flat_dict_response = self.digger(nested_response['result'])

        debug_flat_dict_response = json.dumps(flat_dict_response, indent=4)

        #Saniize removing @value space and other lines that are not interesting

        clean_response = self.sanitize_digger(flat_dict_response)

        debug_clean_response = json.dumps(clean_response, indent=4)


        if filter: # check if command has any filter

            for k, v in clean_response.items():

                if filter in k:

                    response[k] = v
        else:
            response = clean_response

        return response


    def dump_local_phonebooks(self):

        response = self.get_local_phonebook() # raw response for endpoint favorites

        debug_response = json.dumps(response, indent = 4) #debugging purposes

        try:

            if (self.sw == 'CE') or (self.sw == 'roomOS'):

                num_entries = response["result"]["Command"]["PhonebookSearchResult"]["ResultInfo"]["TotalRows"]

            elif self.sw == 'TC':

                num_entries = \
                response["result"]["Command"]["PhonebookSearchResult"]["ResultSet"]["ResultInfo"]["TotalRows"]["#text"]

            else:

                response['code'] =  'ERROR'
                response['result'] = 'SW type not found'

                return response

            if (response["code"] == "OK" and num_entries ==  '0'):

                response['result'] = 'this endpoint does not have favorites'

                return response

            elif response['code'] != "OK":

                response['result'] = 'There was an error querying favorites of this endpoint'

                return response

            else: # OK response and at least 1 favorite

                cleaned_response = self.sanitize_dict_response(response) # recursively inspects all keys and values and removes unnecesary ones

                cleaned_response_debug = json.dumps(cleaned_response, indent = 4) #debuggin purposes

                final_response = {}
                final_response['code'] = 'OK'
                final_response['result'] = {}

                if self.sw == 'CE' or self.sw == 'roomOS':

                    if 'Contact' in cleaned_response['result']['Command']['PhonebookSearchResult']:

                        contact_response = cleaned_response['result']['Command']['PhonebookSearchResult']['Contact']
                        final_response['result']['Contact'] = contact_response

                    if 'Folder' in cleaned_response['result']['Command']['PhonebookSearchResult']:

                        folder_response = cleaned_response['result']['Command']['PhonebookSearchResult']['Folder']
                        final_response['result']['Folder'] = folder_response


                elif self.sw == 'TC':

                    if 'Contact' in cleaned_response['result']['Command']['PhonebookSearchResult']["ResultSet"]:

                        contact_response = cleaned_response['result']['Command']['PhonebookSearchResult']["ResultSet"][
                        'Contact']

                        final_response['result']['Contact'] = contact_response

                    if 'Folder' in cleaned_response['result']['Command']['PhonebookSearchResult']["ResultSet"]:

                        folder_response = cleaned_response['result']['Command']['PhonebookSearchResult']["ResultSet"]['Folder']
                        final_response['result']['Folder'] = folder_response

                else:
                    return 'ERROR'

                return final_response


        except KeyError as ke:

            logging.error(ke)
            logging.error(traceback.print_exc())

            response['code'] = 'ERROR'
            response['result'] = str(ke)

            return response


        except Exception as ex:

            logging.error(ex)
            logging.error(traceback.print_exc())

            response['code'] = 'ERROR'
            response['result'] = str(ex)

            return response

        # TODO remove the below, is NOT USED

        system_dict = {}
        contact_list_json = []

        if response['code'] == 'OK':

            logging.debug('response with no error')

            if self.sw == 'TC':

                logging.debug('Trying TC software')

                try:

                    numberOfContacts = int(response['result']['Command']['PhonebookSearchResult']['ResultSet']['ResultInfo']['TotalRows']['#text'])

                    if numberOfContacts == 1:

                        c = response['result']['Command']['PhonebookSearchResult']['ResultSet']['Contact']
                        dict_contact = {}
                        dict_contact['Name'] = c['Name']['#text']
                        dict_contact['Number'] = c['ContactMethod']['Number']['#text']
                        dict_contact['ContactId'] = c['ContactId']['#text']
                        #dict_contact['ContactMethodId'] = c['ContactMethod']['ContactMethodId']['#text']
                        contact_list_json.append(dict_contact)

                    elif numberOfContacts > 1:

                        for c in response['result']['Command']['PhonebookSearchResult']['ResultSet']['Contact']:

                            dict_contact = {}
                            dict_contact['Name'] = c['Name']['#text']
                            dict_contact['Number'] = c['ContactMethod']['Number']['#text']
                            dict_contact['ContactId'] = c['ContactId']['#text']
                            #dict_contact['ContactMethodId'] = c['ContactMethod']['ContactMethodId']['#text']
                            contact_list_json.append(dict_contact)

                    else:

                        logging.info(self.ip + ' did not have any local favourites')

                except KeyError as ke:

                    logging.error(ke)
                    logging.error(traceback.print_exc())
                    logging.error('Full response below\n' + response)

                except Exception as ex:

                    logging.error(ex)
                    logging.error(traceback.print_exc())
                    logging.error('Full response below\n' + response)



            elif self.sw == 'CE' or self.sw == 'roomOS':

                logging.debug('Trying CE software')

                try:

                    numberOfContacts = int(response['result']['Command']['PhonebookSearchResult']['ResultInfo']['TotalRows'])

                    if numberOfContacts == 1:

                        c = response['result']['Command']['PhonebookSearchResult']['Contact']

                        #contact = c['Name'] + ':' + c['ContactMethod']['Number']

                        #local_contacts.append(contact)

                        dict_contact = {}
                        dict_contact['Name'] = c['Name']
                        dict_contact['Number'] = c['ContactMethod']['Number']
                        dict_contact['ContactId'] = c['ContactId']
                        dict_contact['ContactMethodId'] = c['ContactMethod']['ContactMethodId']
                        contact_list_json.append(dict_contact)


                    elif numberOfContacts > 0:

                        logging.debug('More than 1 Local favourites records found')

                        for c in response['result']['Command']['PhonebookSearchResult']['Contact']:

                            logging.debug('Contact below:\n' + str(c))

                            #contact = c['Name'] + ':' + c['ContactMethod']['Number']

                            #local_contacts.append(contact)

                            dict_contact = {}
                            dict_contact['Name'] = c['Name']
                            dict_contact['Number'] = c['ContactMethod']['Number']
                            dict_contact['ContactId'] = c['ContactId']
                            dict_contact['ContactMethodId'] = c['ContactMethod']['ContactMethodId']
                            contact_list_json.append(dict_contact)

                    else:

                        logging.info(self.ip + ' did not have any local favourites')

                except KeyError as ke:
                    logging.error(ke)
                    logging.error(traceback.print_exc())
                    logging.error('Full response below\n' + response)

            else:

                logging.error('SW could not be detected')

            system_dict['Result'] = contact_list_json

            return system_dict

            # CSV Export

            headers = ['System Name', 'IP address' ]




            if os.path.exists('local_favorites.csv'):
                pass
            else:
                for c in range(10):
                    headers.append('Favorite ' + str(c))
                with open('local_favorites.csv', mode='a+', newline="") as file:
                    local_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    local_writer.writerow(headers)

            with open('local_favorites.csv', mode='a+', newline="") as file:
                local_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                local_writer.writerow(local_contacts)
        else:
            logging.error('Local phonebooks could not be exported ')

        logging.info('Export favorites completed')




    def dump_call_stats(self, called_endpoint, interval = 10, period = 60): #TODO test

        file_name = 'call_stats.csv'

        loops = int(round(period / interval))

        while loops > 0:

            sleep(interval)

            calling_status = self.get_status()

            called_status = called_endpoint.get_status()


        append_write = ''


        calling_ip = self.ip
        called_ip = called_endpoint.ip
        calling_dest_rtp_ip = self.get_value(
            calling_status['result']['Status']['MediaChannels']['Call']['IncomingAudioChannel']['Transport']['RTP'][
                'Remote']['IpAddress'])
        called_dest_rtp_ip = self.get_value(
            calling_status['result']['Status']['MediaChannels']['Call']['IncomingAudioChannel']['Transport']['RTP'][
                'Remote']['IpAddress'])

        if os.path.exists(file_name):
            append_write = 'a+'  # append if already exist
            with open(file_name, append_write) as my_file:
                my_file.write(calling_ip + ',' + called_ip + '\n')

        else:
            append_write = 'w+'  # create a new file if not
            with open(file_name, append_write) as my_file:
                my_file.write('CALLING SYSTEM NAME, CALLING URI, CALLING IP,CALLING DESTINATION IP,CALLED SYSTEM NAME, CALLED URI, CALLED IP,CALLED DESTINATION IP\n')
                my_file.write(calling_ip + ',' + calling_dest_rtp_ip + called_ip + ',' + self.uri + '\n')


        append_write = 'a+'

    def get_call_stats(self):

        logging.info('Getting status')

        call_url = 'https://' + self.ip + '/getxml?location=/Status/Call/'

        call_response = self.get_url(call_url)

        diag_url = 'https://' + self.ip + '/getxml?location=/Status/Diagnostics/'

        diag_response = self.get_url(diag_url)

        call_response['result']['Status'].update(diag_response['result']['Status'])

        media_url = 'https://' + self.ip + '/getxml?location=/Status/MediaChannels/'

        media_response = self.get_url(media_url)

        call_response['result']['Status'].update(diag_response['result']['Status'])

        return call_response

    def set_activeControl(self, mode):

        logging.info('Setting active control mode to ' + mode)



        xml_string = '''
        
        <Configuration>
		    <Conference>
		    	<ActiveControl>
		    		<Mode>''' + mode + '''</Mode>
		    	</ActiveControl>
		    </Conference>
        </Configuration>
        
        '''

        return self.post_xml(xml_string)

    def factory_reset(self):

        logging.info('Factory resetting ' + self.ip)

        xml_string = '<Command><SystemUnit><FactoryReset><confirm>yes</confirm></FactoryReset></SystemUnit></Command>'

        return self.post_xml(xml_string)




    def call_history(self , last = '1' ):

        logging.info('call history for  last ' + last + ' calls')

        xml_string = '''
                <Command>
                	<CallHistory>
        	        	<Get>
        		        	<DetailLevel>Full</DetailLevel>
        			        <limit>''' + last + '''</limit>
        		        </Get>
        	        </CallHistory>
                </Command>
        '''

        return self.post_xml(xml_string)


    def create_server(self , port = 8080):

        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", port), Handler) as httpd:
            print("serving at port", port)
            httpd.serve_forever()

