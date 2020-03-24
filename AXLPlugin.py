#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import zeep.helpers
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from zeep.exceptions import TransportError
from zeep.cache import SqliteCache
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests.exceptions import HTTPError, Timeout
from requests.exceptions import ConnectionError, RetryError, ConnectTimeout
from urllib3.exceptions import ConnectTimeoutError
import json
from xml.dom.minidom import parseString
from tabulate import tabulate
import time
from zeep.plugins import HistoryPlugin
from helper_functions import sql_decoder
import sys
import re
import logging
import math
import xmltodict
from lxml import etree
import lxml.etree as ET

logger = logging.getLogger(__name__)

frozen = ''



if getattr(sys, 'frozen', False):
    # we are running in a bundle
    dir_project = sys._MEIPASS
    dir_executable = os.path.dirname(sys.argv[0])
    print('we are running in a bundle')

else:
    # we are running in a normal Python environment
    dir_project = os.path.dirname(os.path.abspath(__file__))
    dir_executable = dir_project
    print('we are running in a normal Python environment')


from zeep import Plugin


import logging.config

# to enable

'''
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})
'''

class UcmAXLConnection:

    last_exception = None
    history = HistoryPlugin()

    def __init__(self, ip='', usr='', psw='', version = '12.5', timeout=30):

        self.failure = False
        self.cucm_ip = ip
        self.usr = usr
        self.psw = psw
        self.schemaPath = os.path.join(dir_project, 'schema')
        self.cucm_url = 'https://' + self.cucm_ip + ':8443/axl/'
        self.long_version = ''
        self.version = version
        #self.long_version = self.getCucmVersion() # TODO consider not having this at constructor, for SQL we don't care about the version
        #self.version = self.getShortVersion(self.long_version)

        self.wsdl = os.path.join(os.path.join(self.schemaPath, self.version), 'AXLAPI.wsdl')

        self.cache = SqliteCache(path=os.path.join(dir_project, 'sqlite_{0}.db)'.format(self.cucm_ip)), timeout=60)
        self.session = Session()
        self.session.verify = False
        self.session.auth = HTTPBasicAuth(self.usr, self.psw)
        transport = Transport(session=self.session, timeout=timeout, operation_timeout=timeout, cache=self.cache)

        #self.history = HistoryPlugin()

        self.client = Client(self.wsdl, transport=transport)
        self.service = self.client.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
                                                  "https://{0}:8443/axl/".format(self.cucm_ip))


    def get_service(self):

        return self.service

    # TODO nodeUsage returned on wrong sequence, Jira opened, as workaround will use SQL query instead
    # TODO https://jira-eng-sjc12.cisco.com/jira/browse/AXL-1952

    '''
    def list_process_nodes(self, name = '%', description = '%'):

        search_criteria = {'name':name, 'description': description}



        #returned_tags = {'name': '', 'processNodeRole': '','nodeUsage':''}

        returned_tags = {'name': '','description':'','nodeUsage':'','lbmHubGroup': '', 'processNodeRole': ''}

        result = self.service.listProcessNode(searchCriteria=search_criteria, returnedTags=returned_tags)

        return result
    '''

    def update_dp_in_phone(self, deviceName, DevicePool):

        try:

            result = self.service.updatePhone(name=deviceName, devicePoolName=DevicePool)

            return { deviceName : result["return"]}

        except Exception as fault:
            self.last_exception = fault
            return {'result': str(fault)}

        return None

    def add_phone(self, phone_info_list):

        result = []

        for phone_info in phone_info_list:
            try:

                vendor_config_temp = phone_info['vendorConfig']
                if vendor_config_temp:
                    vendor_config = ET.fromstring(vendor_config_temp)
                else:
                    vendor_config = ET.fromstring('<ciscoSupportField></ciscoSupportField>')

                phone_data = {
                    'name': phone_info['name'],
                    'description': phone_info['description'],
                    'product': phone_info['product'],
                    'class': 'Phone',
                    'protocol': 'SIP',
                    'protocolSide': 'User',
                    'callingSearchSpaceName': phone_info['callingSearchSpaceName'],
                    'devicePoolName': phone_info['devicePoolName'],
                    'commonPhoneConfigName': 'Standard Common Phone Profile',
                    'locationName': phone_info['locationName'],
                    'securityProfileName': phone_info['securityProfileName'],
                    'sipProfileName': phone_info['sipProfileName'],
                    'ownerUserName': phone_info['ownerUserName'],
                    'vendorConfig': vendor_config,
                    'lines': {
                        'line': {
                            'index': '1',
                            'dirn': {
                                'pattern': phone_info['pattern'],
                                'routePartitionName': phone_info['routePartitionName']
                            },
                            'associatedEndusers': {
                                'enduser': {
                                    'userId': phone_info['ownerUserName']
                                }
                            }
                        }
                    }
                }

                temp = self.service.addPhone(phone=phone_data)
                temp2 =f"{phone_info['name']},{temp['return']}"
                result.append(temp2)

            except Exception as ex:

                logging.error(ex)
                return str(ex)

        return result


    """
    def add_phone(self, data):

        try:

            deviceName = data['deviceName']
            devicedescription = data['devicedescription']
            modelname = data['modelname']
            phoneclass = data['phoneclass']
            protocol = data['protocol']
            css = data['css']
            devicePool = data['devicePool']
            location = data['location']
            dn = data['dn']
            securityProfileName = data['securityProfileName']
            sipProfile = data['sipProfile']





            result = self.service.addPhone(name=deviceName, devicePoolName=DevicePool)

            return { deviceName : result["return"]}

        except Exception as fault:
            self.last_exception = fault
            return {'result': str(fault)}

        return None

        """

    def load_add_phone(self):
        data = []
        headers = []

    def list_process_nodes(self):

        query = '''
        select processnode.name as processnode,typenodeusage.name as nodeusage,typeprocessnoderole.name as processnoderole 
        from processnode
        join typenodeusage on processnode.tknodeusage = typenodeusage.enum
        join typeprocessnoderole on processnode.tkprocessnoderole = typeprocessnoderole.enum
        '''

        result = self.run_sql_query(query)

        return result

    def get_service_and_enterprise_params(self):

        query = '''
        select processconfig.paramvalue,processconfig.paramname, 
        typeparam.name as paramtype, processnode.name as nodename,
        typeservice.name as service,typereset.name resettype

        from processconfig

        join typeparam on typeparam.enum = processconfig.tkparam
        join processnode on processnode.pkid = processconfig.fkprocessnode
        join typeservice on typeservice.enum = processconfig.tkservice
        join typereset on typereset.enum = processconfig.tkreset
        '''

        result = self.run_sql_query(query)

        return result

    def get_ucm_version(self):

        sql_query_text = "SELECT DISTINCT Version AS cmversion FROM ComponentVersion WHERE SoftwareComponent = " \
                         "'cm-ver' OR SoftwareComponent = 'Cisco CallManager' ORDER BY Version DESC"

        version = self.run_sql_query(sql_query_text)

        logging.info('Version:' + str(version) + ' version type:' + str(type(version)))

        if version != None:
            return version['rows'][0]['cmversion']
        else:
            return '10.5.000'

    def sql_decode(self, sql_result):

        result = dict()

        num_rows = 0
        result_rows = []

        if sql_result is not None:
            if sql_result['return'] is not None:
                for row in sql_result['return']['row']:
                    result_rows.append({})
                    for column in row:
                        result_rows[num_rows][column.tag] = column.text
                    num_rows += 1

        result['num_rows'] = num_rows

        if num_rows > 0:
            result['rows'] = result_rows

        return result

    def run_sql_query(self, query):

        sql_full_result = {'num_rows': 0, 'rows': []}


        try:

            sql_result = self.service.executeSQLQuery(sql=query)

            test = self.client.transport
            test2 = self.client.transport.logger


            ''' To printout sent received XML envelopes

            try:
                for hist in [self.history.last_sent, self.history.last_received]:
                    print(etree.tostring(hist["envelope"], encoding="unicode", pretty_print=True))
            except (IndexError, TypeError):
                # catch cases where it fails before being put on the wire
                pass
            '''
            decoded_result = self.sql_decode(sql_result)
            return decoded_result


        except ConnectTimeoutError as timeout:

            logging.error('ERROR in run_sql_query function: ConnectTimeoutError')
            logging.error(timeout)
            logging.error(sql_result)
            self.last_exception = timeout
            self.failure = True
            return None

        except ConnectTimeout as tout:

            logging.error('ERROR in run_sql_query function: ConnectTimeout')
            logging.error(tout)
            self.last_exception = tout
            self.failure = True
            return None

        except TransportError as te:

            status_code = te.status_code

            if status_code == '401':
                logging.error('401')
            else:
                logging.info(status_code)


        except Fault as fault:

            logging.error(fault.message)

            '''
            try:

                for r in fault:
                    logging.info(r)
                    pass

                for k,v in fault.items():

                    logging.info(k)
                    logging.info(v)


                
                
                #dict_error = xmltodict.parse(strFault)

                http_response = fault['detail']['html']['body']['div'][1]['div']['#text']

                if '401' in http_response:

                    return '401'
                else:
                    return http_response
                '''


            '''
            results returned are > 8mb, we need to break out the output

            https://www.cisco.com/c/en/us/td/docs/voice_ip_comm/cucm/devguide/9_1_1/xmldev-911/axl.html

            '''


            logging.warning('Zeep fault caught! error 198')

            if not 'Query request too large' in fault.message:

                sql_full_result['rows'] = fault.message
                return sql_full_result

            else:

                logging.info('result to be returned > 8mb, we need to break out the output')

                rows_dict = self.process_axl_response(fault.message)

                logging.info(json.dumps(rows_dict, indent=2))


                if rows_dict is not None:

                    total_rows = int(rows_dict['total_rows'])

                    suggested_rows = int(rows_dict['suggested_rows'])

                    round_up = math.ceil(total_rows / suggested_rows)

                    better_suggestion = int(total_rows / round_up)

                    logging.info('BETTER_SUGGESTION:' + str((better_suggestion)))

                    skip = 0
                    first = better_suggestion

                    while skip < total_rows:

                        try:

                            logging.info('skip: ' + str(skip))
                            logging.info('first: ' + str(first))

                            batch_addition = 'Select SKIP ' + str(skip) + ' First ' + str(first)

                            select_insensitive = re.compile("select", re.IGNORECASE)

                            query_replaced = select_insensitive.sub(batch_addition, query)

                            logging.info('Original Query: ')
                            logging.info(query)

                            logging.info('Query replaced: ')
                            logging.info(query_replaced)

                            sql_partial_result = self.service.executeSQLQuery(sql=query_replaced)

                            decoded_partial_result = self.sql_decode(sql_partial_result)

                            sql_full_result['num_rows'] += decoded_partial_result['num_rows']
                            sql_full_result['rows'] += decoded_partial_result['rows']

                            skip += suggested_rows
                            first += skip

                            if first > total_rows:
                                first = total_rows


                        except Exception as gen:

                            logging.error('Exception executeSQL broken down before looping')
                            logging.error(gen)
                            self.last_exception = gen
                            self.failure = True
                            return None

                else:

                    logging.error('Rows_dict returned from process axl resopnse = None')


        except Exception as gen:

            logging.error('executing run_sql_query function: Exception')
            logging.error(gen)

            # self.process_axl_response(gen)
            self.last_exception = gen
            self.failure = True

            return None

        return sql_full_result

    def getCucmVersion(self):

        sql_decod = sql_decoder()
        session = Session()
        session.verify = False
        session.auth = HTTPBasicAuth(self.usr, self.psw)
        transport = Transport(session=session, timeout=10, cache=SqliteCache())
        sql_query_text = "SELECT DISTINCT Version AS cmversion FROM ComponentVersion WHERE SoftwareComponent = " \
                         "'cm-ver' OR SoftwareComponent = 'Cisco CallManager' ORDER BY Version DESC"
        temp_wsdl = os.path.join(os.path.join(self.schemaPath, '10.5'), 'AXLAPI.wsdl')

        try:
            client = Client(temp_wsdl, transport=transport)
            service = client.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding", self.cucm_url)

            try:

                SQL_resp = service.executeSQLQuery(sql_query_text)

                return self.sql_decode(SQL_resp)['rows'][0]['cmversion']


            except Fault as error:
                detail = 'Error: ' + error.message
                logging.error('Error in getCucmVersion - Helper functions:\n ' + detail)
                return detail

        except (HTTPError, Timeout, RetryError, ConnectionError) as error:
            logging.error(error.args)
            return 'Error connecting to ' + self.cucm_ip


    def getShortVersion(self, longVersion):

        if (longVersion[0] == '8') | (longVersion[0] == '9'):
            return longVersion[0:3]
        elif longVersion[0] == '1':
            return longVersion[0:4]
        else:
            return 'UCM version not supported'

    # TODO Remove the below if not needed (replaced with run_sql_query


    def cleanZeepResponse(self, zeepRespone):

        sql_decod = sql_decoder()

        try:
            cleaned_zeep_response = zeepRespone['return']['row']
        except:
            return 'None'

        decoded_list = []

        # decode list of elements, it returns a list of lists of dicts

        for element in cleaned_zeep_response:
            decoded_list.append(sql_decod.serialize_expand(element))

        # convert list of lists of dicts to a list of dicts

        list_of_dicts = sql_decod.unnest_list(decoded_list)

        return list_of_dicts
        # Prettify the SQL response

        # return tabulate(list_of_dicts, headers="keys")


    def process_axl_response(self, response):

        reg_parsing = re.search("Total rows matched: (.*) rows. Suggestive Row Fetch: less than (.*) rows", response)

        try:
            total_rows = reg_parsing.group(1)
            suggested_rows = reg_parsing.group(2)

            return {'total_rows': total_rows,
                    'suggested_rows': suggested_rows}
        except Exception as excep:

            logging.error('Exception under process_axl_response \n ' + excep)

            return None

    def exportConfig(self, axlQueries, configOutputPath):

        # It does export configuration given json file path with queries and output folder path

        nodePath = os.path.join(configOutputPath, self.cucm_ip)

        with open(axlQueries, 'r+') as queriesF:

            logging.info('Opening axlQueries JSON file ')

            jsonQueriesF = json.load(queriesF)
            logging.debug(json.dumps(jsonQueriesF, indent=2))
            queryList = jsonQueriesF['SQL']

            # If ConfigOutput folder does not exist, create it

            if not os.path.exists(configOutputPath):
                os.makedirs(configOutputPath)
                logging.info('Creating folder ' + configOutputPath)

            # If IP address folder under ConfigOutput does not exist, create it

            if not os.path.exists(nodePath):
                os.makedirs(nodePath)
                logging.info('Creating folder' + nodePath)

            # Iterating queries from JSON

            for item in queryList:

                logging.info('Reading query ' + item['name'])

                D = {item['name']: ''}

                sql_response = self.executeSQL(item['query'])

                # we add the query name key to later clasify the output file

                D = {item['name']: sql_response}

                #  convert list of dicts to json

                json_response = json.dumps(D, indent=2)

                with open(os.path.join(nodePath, item['name']) + '_' + time.strftime('%Y%m%d-%H%M') + '.json', 'w') \
                        as jsonfile:
                    logging.info('Writting results to ' + os.path.join(nodePath, item['name']))
                    jsonfile.write(json_response)

                if sql_response[0:5] == 'Error':
                    logging.error(sql_response)

                elif sql_response == 'None':
                    logging.error(sql_response)

                else:
                    logging.debug(tabulate(sql_response, headers="keys"))

        return 'completed'

    def count_devices_per_model(self):

        query = '''
            SELECT count(device.name),typemodel.name
            FROM device
            JOIN typemodel on device.tkmodel= typemodel.enum
            GROUP BY typemodel.name
            '''

        try:
            sql_result = self.run_sql_query(query)
        except Exception as fault:
            sql_result = None
            self.last_exception = fault

        return sql_result

    def count_devices_per_class(self):

        query = '''
            SELECT count(device.name),typeclass.name
            FROM device
            JOIN typeclass on device.tkclass= typeclass.enum
            GROUP BY typeclass.name
            '''

        try:
            sql_result = self.run_sql_query(query)
        except Exception as fault:
            sql_result = None
            self.last_exception = fault

        return sql_result

    def count_dns_per_usage(self):

        query = '''
            select count(dnorpattern),typepatternusage.name
            from numplan
            join typepatternusage on numplan.tkpatternusage = typepatternusage.enum
            group by typepatternusage.name
            '''

        try:
            sql_result = self.run_sql_query(query)
        except Exception as fault:
            sql_result = None
            self.last_exception = fault

        return sql_result

    def count_std_ccm_endusers(self):

        query = '''
		select count(enduser.userid)
		from enduser
		join enduserdirgroupmap on enduserdirgroupmap.fkenduser = enduser.pkid
		join dirgroup on enduserdirgroupmap.fkdirgroup = dirgroup.pkid
		where dirgroup.name = 'Standard CCM End Users'
        '''
        try:
            sql_result = self.run_sql_query(query)
        except Exception as fault:
            sql_result = None
            self.last_exception = fault

        return sql_result

    def count_mobility_endusers(self):

        query = '''
    		select count(enduser.userid)
    		from enduser
    		join enduserdirgroupmap on enduserdirgroupmap.fkenduser = enduser.pkid
    		join dirgroup on enduserdirgroupmap.fkdirgroup = dirgroup.pkid
    		where enduser.enablemobility = 't'
            '''
        try:
            sql_result = self.run_sql_query(query)
        except Exception as fault:
            sql_result = None
            self.last_exception = fault

        return sql_result

    def get_ip_and_analog_phones_per_dp(self):

        query = '''
SELECT sum(analog_phones) as analog_phones,
       sum(ip_phones) as ip_phones,
       devicepool
FROM
  (SELECT 0 AS analog_phones,
                  count(d.name) AS IP_Phones,
                  dp.name AS DevicePool
   FROM Device AS d
   INNER JOIN DevicePool AS dp ON d.fkDevicePool=dp.pkid
   INNER JOIN typemodel AS tm ON tm.enum=d.tkmodel
   WHERE (tm.name != 'Analog Phone'
          AND tm.name != 'Conference Bridge'
          AND tm.name != 'CTI Route Point'
          AND tm.name != 'CTI Port'
          AND tm.name != 'MGCP Station'
          AND tm.name != 'Route List'
          AND tm.name != 'H.323 Gateway'
          AND tm.name != 'Music On Hold'
          AND tm.name != 'Media Termination Point'
          AND tm.name != 'Tone Announcement Player'
          AND tm.name != 'Cisco IOS Conference Bridge (HDV2)'
          AND tm.name != 'Cisco IOS Software Media Termination Point (HDV2)'
          AND tm.name != 'Cisco IOS Media Termination Point (HDV2)'
          AND tm.name != 'SIP Trunk'
          AND dp.name LIKE '%PH%')
   GROUP BY dp.name
   UNION ALL SELECT count(d.name) AS Analog_Phones,
                    0 AS ip_phones,
                            dp.name AS DevicePool
   FROM Device AS d
   INNER JOIN DevicePool AS dp ON d.fkDevicePool=dp.pkid
   INNER JOIN typemodel AS tm ON tm.enum=d.tkmodel
   WHERE (tm.name = 'Analog Phone'
          AND dp.name LIKE '%PH%')
   GROUP BY dp.name) a
GROUP BY devicepool
ORDER BY devicepool
        '''

        try:
            sql_result = self.run_sql_query(query)
        except Exception as fault:
            sql_result = None
            self.last_exception = fault

        return sql_result

    def count_configured_sip_phones(self):

        query = '''
        select count(device.name)
FROM device
LEFT JOIN typemodel on device.tkmodel= typemodel.enum
LEFT JOIN typedeviceprotocol on device.tkdeviceprotocol = typedeviceprotocol.enum
LEFT JOIN typeclass on typemodel.tkclass = typeclass.enum 
LEFT JOIN typeproduct on device.tkproduct = typeproduct.enum
where typeclass.name = "Phone" and typedeviceprotocol.name = "SIP"
        '''

        try:
            sql_result = self.run_sql_query(query)
        except Exception as fault:
            sql_result = None
            self.last_exception = fault

        return sql_result

    def count_configured_sccp_phones(self):

        query = '''
            select count(device.name)
    FROM device
LEFT JOIN typemodel as typemodel on device.tkmodel= typemodel.enum
LEFT JOIN typedeviceprotocol on device.tkdeviceprotocol = typedeviceprotocol.enum
LEFT JOIN typeclass on device.tkclass = typeclass.enum 
LEFT JOIN typeproduct on device.tkproduct = typeproduct.enum
    where typeclass.name = "Phone" and typedeviceprotocol.name = "SCCP"
            '''

        try:
            sql_result = self.run_sql_query(query)
        except Exception as fault:
            sql_result = None
            self.last_exception = fault

        return sql_result

    def count_configured_cti_ports(self):

        query = '''
                select count(device.name)
        FROM device
    LEFT JOIN typemodel as typemodel on device.tkmodel= typemodel.enum
    LEFT JOIN typedeviceprotocol on device.tkdeviceprotocol = typedeviceprotocol.enum
    LEFT JOIN typeclass on device.tkclass = typeclass.enum 
    LEFT JOIN typeproduct on device.tkproduct = typeproduct.enum
        where typemodel.name = "CTI Port"
                '''

        try:
            sql_result = self.run_sql_query(query)
        except Exception as fault:
            sql_result = None
            self.last_exception = fault

        return sql_result

    def massage_data(self,phone_info):

        massaged_data = []

        phone_dict = {}

        headers = phone_info[0]

        phone_info.pop(0)

        counter = 0

        for phone in phone_info:

            for header in headers:
                #phone_dict[header] = phone[counter]
                counter = counter + 1


class UcmRisPortToolkit:
    last_exception = None

    '''
    Constructor - Create new instance 
    '''

    def __init__(self, ip='', usr='', psw='', tls_verify=False):
        wsdl = 'https://{0}:8443/realtimeservice2/services/RISService70?wsdl'.format(ip)

        self.session = Session()
        self.session.auth = HTTPBasicAuth(usr, psw)
        self.session.verify = tls_verify

        self.cache = SqliteCache(path='sqlite_risport.db', timeout=60)

        self.client = Client(wsdl=wsdl, transport=Transport(cache=self.cache, session=self.session))

        self.service = self.client.create_service("{http://schemas.cisco.com/ast/soap}RisBinding",
                                                  "https://{0}:8443/realtimeservice2/services/RISService70".format(ip))

        # enable_logging()

    def get_service(self):

        return self.service

'''

typeclass

  enum  name                                 moniker
------  -----------------------------------  -----------------------------------------
     1  Phone                                CLASS_PHONE
     2  Gateway                              CLASS_GATEWAY
     4  Conference Bridge                    CLASS_CONF_BRIDGE
     5  Media Termination Point              CLASS_MTP
     7  Route List                           CLASS_ROUTE_LIST
     8  Voice Mail                           CLASS_VOICE_MAIL
    10  CTI Route Point                      CLASS_CTI_ROUTE_POINT
    12  Music On Hold                        CLASS_MUSIC_ON_HOLD
    13  Simulation                           CLASS_SIMULATION
    14  Pilot                                CLASS_PILOT
    15  GateKeeper                           CLASS_GATEKEEPER
    16  Add-on modules                       CLASS_ADDON_MODULES
    17  Hidden Phone                         CLASS_HIDDEN_PHONE
    18  Trunk                                CLASS_TRUNK
    19  Tone Announcement Player             CLASS_ANN
    20  Remote Destination Profile           CLASS_REMOTE_DESTINATION_PROFILE
   248  EMCC Base Phone Template             CLASS_EMCC_TEMPLATE
   249  EMCC Base Phone                      CLASS_EMCC
   250  Remote Destination Profile Template  CLASS_REMOTE_DESTINATION_PROFILE_TEMPLATE
   251  Gateway Template                     CLASS_GATEWAY_TEMPLATE
   252  UDP Template                         CLASS_UDP_TEMPLATE
   253  Phone Template                       CLASS_PHONE_TEMPLATE
   254  Device Profile                       CLASS_DEVICE_PROFILE
   255  Invalid                              CLASS_INVALID
   301  Interactive Voice Response           CLASS_IVR

'''

'''
typemodel

  enum    tkclass  name                                        tkrisclass
------  ---------  ----------------------------------------  ------------
     1          1  Cisco 30 SP+                                         1
     2          1  Cisco 12 SP+                                         1
     3          1  Cisco 12 SP                                          1
     4          1  Cisco 12 S                                           1
     5          1  Cisco 30 VIP                                         1
     6          1  Cisco 7910                                           1
     7          1  Cisco 7960                                           1
     8          1  Cisco 7940                                           1
     9          1  Cisco 7935                                           1
    10          1  Cisco VGC Phone                                      2
    11          1  Cisco VGC Virtual Phone                              2
    12          1  Cisco ATA 186                                        2
    20          1  SCCP Phone                                           1
    61          1  H.323 Phone                                          3
    72          1  CTI Port                                             4
   115          1  Cisco 7941                                           1
   119          1  Cisco 7971                                           1
   302          1  Cisco 7985                                           1
   307          1  Cisco 7911                                           1
   308          1  Cisco 7961G-GE                                       1
   309          1  Cisco 7941G-GE                                       1
   335          1  Motorola CN622                                       1
   336          1  Third-party SIP Device (Basic)                       1
   348          1  Cisco 7931                                           1
   358          1  Cisco Unified Personal Communicator                  1
   365          1  Cisco 7921                                           1
   369          1  Cisco 7906                                           1
   374          1  Third-party SIP Device (Advanced)                    1
   375          1  Cisco TelePresence                                   1
   376          1  Nokia S60                                            1
   404          1  Cisco 7962                                           1
   412          1  Cisco 3951                                           1
   431          1  Cisco 7937                                           1
   434          1  Cisco 7942                                           1
   435          1  Cisco 7945                                           1
   436          1  Cisco 7965                                           1
   437          1  Cisco 7975                                           1
   446          1  Cisco 3911                                           1
   468          1  Cisco Unified Mobile Communicator                    1
   478          1  Cisco TelePresence 1000                              1
   479          1  Cisco TelePresence 3000                              1
   480          1  Cisco TelePresence 3200                              1
   481          1  Cisco TelePresence 500-37                            1
   484          1  Cisco 7925                                           1
   493          1  Cisco 9971                                           1
   495          1  Cisco 6921                                           1
   496          1  Cisco 6941                                           1
   497          1  Cisco 6961                                           1
   503          1  Cisco Unified Client Services Framework              1
   505          1  Cisco TelePresence 1300-65                           1
   520          1  Cisco TelePresence 1100                              1
   521          1  Transnova S3                                         1
   522          1  BlackBerry MVS VoWifi                                1
   537          1  Cisco 9951                                           1
   540          1  Cisco 8961                                           1
   547          1  Cisco 6901                                           1
   548          1  Cisco 6911                                           1
   550          1  Cisco ATA 187                                        2
   557          1  Cisco TelePresence 200                               1
   558          1  Cisco TelePresence 400                               1
   562          1  Cisco Dual Mode for iPhone                           1
   564          1  Cisco 6945                                           1
   575          1  Cisco Dual Mode for Android                          1
   577          1  Cisco 7926                                           1
   580          1  Cisco E20                                            1
   582          1  Generic Single Screen Room System                    1
   583          1  Generic Multiple Screen Room System                  1
   584          1  Cisco TelePresence EX90                              1
   585          1  Cisco 8945                                           1
   586          1  Cisco 8941                                           1
   588          1  Generic Desktop Video Endpoint                       1
   590          1  Cisco TelePresence 500-32                            1
   591          1  Cisco TelePresence 1300-47                           1
   592          1  Cisco 3905                                           1
   593          1  Cisco Cius                                           1
   596          1  Cisco TelePresence TX1310-65                         1
   598          1  Ascom IP-DECT Device                                 1
   604          1  Cisco TelePresence EX60                              1
   606          1  Cisco TelePresence Codec C90                         1
   607          1  Cisco TelePresence Codec C60                         1
   608          1  Cisco TelePresence Codec C40                         1
   609          1  Cisco TelePresence Quick Set C20                     1
   610          1  Cisco TelePresence Profile 42 (C20)                  1
   611          1  Cisco TelePresence Profile 42 (C60)                  1
   612          1  Cisco TelePresence Profile 52 (C40)                  1
   613          1  Cisco TelePresence Profile 52 (C60)                  1
   614          1  Cisco TelePresence Profile 52 Dual (C60)             1
   615          1  Cisco TelePresence Profile 65 (C60)                  1
   616          1  Cisco TelePresence Profile 65 Dual (C90)             1
   617          1  Cisco TelePresence MX200                             1
   619          1  Cisco TelePresence TX9000                            1
   620          1  Cisco TelePresence TX9200                            1
   621          1  Cisco 7821                                           1
   622          1  Cisco 7841                                           1
   623          1  Cisco 7861                                           1
   626          1  Cisco TelePresence SX20                              1
   627          1  Cisco TelePresence MX300                             1
   628          1  IMS-integrated Mobile (Basic)                        1
   631          1  Third-party AS-SIP Endpoint                          1
   632          1  Cisco Cius SP                                        1
   633          1  Cisco TelePresence Profile 42 (C40)                  1
   634          1  Cisco VXC 6215                                       1
   635          1  CTI Remote Device                                    1
   642          1  Carrier-integrated Mobile                            1
   645          1  Universal Device Template                            0
   647          1  Cisco DX650                                          1
   648          1  Cisco Unified Communications for RTX                 1
   652          1  Cisco Jabber for Tablet                              1
   659          1  Cisco 8831                                           1
   681          1  Cisco ATA 190                                        2
   682          1  Cisco TelePresence SX10                              1
   683          1  Cisco 8841                                           1
   684          1  Cisco 8851                                           1
   685          1  Cisco 8861                                           1
   688          1  Cisco TelePresence SX80                              1
   689          1  Cisco TelePresence MX200 G2                          1
   690          1  Cisco TelePresence MX300 G2                          1
 20000          1  Cisco 7905                                           1
 30002          1  Cisco 7920                                           1
 30006          1  Cisco 7970                                           1
 30007          1  Cisco 7912                                           1
 30008          1  Cisco 7902                                           1
 30016          1  Cisco IP Communicator                                1
 30018          1  Cisco 7961                                           1
 30019          1  Cisco 7936                                           1
 30027          1  Analog Phone                                         2
 30028          1  ISDN BRI Phone                                       2
 30035          1  IP-STE                                               1
 36042          1  Cisco DX80                                           1
 36043          1  Cisco DX70                                           1
 36207          1  Cisco TelePresence MX700                             1
 36208          1  Cisco TelePresence MX800                             1
 36210          1  Cisco TelePresence IX5000                            1
 36213          1  Cisco 7811                                           1
 36216          1  Cisco 8821                                           1
 36217          1  Cisco 8811                                           1
 36224          1  Cisco 8845                                           1
 36225          1  Cisco 8865                                           1
 36227          1  Cisco TelePresence MX800 Dual                        1
 36232          1  Cisco 8851NR                                         1
 36235          1  Cisco Spark Remote Device                            1
 36239          1  Cisco TelePresence DX80                              1
 36241          1  Cisco TelePresence DX70                              1
 36247          1  Cisco 7832                                           1
 36248          1  Cisco 8865NR                                         1
 36251          1  Cisco Spark Room Kit                                 1
 36254          1  Cisco Spark Room 55                                  1
 36255          1  Cisco Spark Room Kit Plus                            1
 36258          1  Cisco 8832                                           1
 36260          1  Cisco 8832NR                                         1

'''

'''
  enum    tkclass  typemodel.name                count
------  ---------  -----------------------    ------------
     1          1  Cisco 30 SP+                    115                     1
     2          1  Cisco 12 SP+                    858                    1
     3          1  Cisco 12 SP                     15                    1
     4          1  Cisco 12 S                                           1
     5          1  Cisco 30 VIP                                         1
     6          1  Cisco 7910                                           1
     7          1  Cisco 7960                                           1
     8          1  Cisco 7940                                           1
     9          1  Cisco 7935                                           1
    10          1  Cisco VGC Phone                                      2
    11          1  Cisco VGC Virtual Phone                              2

'''

'''
typepatternusage

  enum  name
------  --------------------------------------
     0  CallPark
     1  Conference
     2  Device
     3  Translation
     4  Call Pick Up Group
     5  Route
     6  Message Waiting
     7  Hunt Pilot
     8  Voice Mail Port
     9  Domain Routing
    10  IPAddress Routing
    11  Device template
    12  Directed Call Park
    13  Device Intercom
    14  Translation Intercom
    15  Translation Calling Party Number
    16  Mobility Handoff
    17  Mobility Enterprise Feature Access
    18  Mobility IVR
    19  Device Intercom Template
    20  Called Party Number Transformation
    21  Call Control Discovery Learned Pattern
    22  Uri Routing
    23  ILS Learned Enterprise Number
    24  ILS Learned E164 Number
    25  ILS Learned Enterprise Numeric Pattern
    26  ILS Learned E164 Numeric Pattern
    27  Alternate Number
    28  ILS Learned URI
    29  ILS Learned PSTN Failover Rule
    30  ILS Imported E164 Number


'''