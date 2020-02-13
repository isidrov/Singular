from zeep import Client
from zeep.exceptions import TransportError
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Transport
import os



dir_project = os.path.dirname(os.path.abspath(__file__))
cucm_ip = '10.85.141.20'
usr = 'ccmawdmin'
psw = 'sdfsd'
wsdl = os.path.join(dir_project, 'schema/11.5/AXLAPI.wsdl')
cucm_url = 'https://' + cucm_ip + ':8443/axl/'
session = Session()
session.verify = False
session.auth = HTTPBasicAuth(usr, psw)
transport = Transport(session=session, timeout=30)
history = HistoryPlugin()
client = Client(wsdl, transport=transport, plugins = [history])
service = client.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
                                          "https://{0}:8443/axl/".format(cucm_ip))
query = "select name, description from device where name like 'SEP%'"
try:
    sql_result = service.executeSQLQuery(sql=query)
    print(sql_result)
except TransportError as e:
    print(e)
except Fault as e:
    print('FAULT EXCEPTION')
    print(e) # Unknown fault occured

    print(str(type(e.detail)))

    print(history.last_received)

    #print(e.message)

except Exception as e:
    print(e)
    print(history.last_sent)
    print(history.last_received)