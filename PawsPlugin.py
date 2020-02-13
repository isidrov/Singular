from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth
#from requests.packages import urllib3
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urllib3.connection import NewConnectionError
from urllib3 import HTTPSConnectionPool
import logging.config
import logging
import os
import sys

logger = logging.getLogger(__name__)

class PawsPlugin:

    last_exception = None

    '''

    Constructor - Create new instance

    https://developer.cisco.com/site/paws/documents/developer-guide/

    https://developer.cisco.com/site/paws/develop-and-test/api-reference/

    '''


    def __init__(self, username, password, server_ip, tls_verify=False):

        if getattr(sys, 'frozen', False):
            # we are running in a bundle
            self.installPath = sys._MEIPASS


        else:
            # we are running in a normal Python environment
            self.installPath = os.path.dirname(os.path.abspath(__file__))

        self.server_ip = server_ip
        self.session = Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.verify = tls_verify
        self.cache = SqliteCache(path=os.path.join(self.installPath, 'sqlite_{0}.db)'.format(self.server_ip)), timeout=60)






    def create_service(self, api):

        if api == "HardwareInformationService":

            wsdl = os.path.join(self.installPath, 'schema/paws/paws_hardware_info_updated.wsdl')

            binding = "{http://services.api.platform.vos.cisco.com}HardwareInformationServiceSoap11Binding"

            endpoint = "https://{0}:8443/platform-services/services/HardwareInformationService." \
                       "HardwareInformationServiceHttpsSoap11Endpoint/".format(self.server_ip)

        elif api == "ClusterNodesService":

            wsdl = "https://{0}:8443/platform-services/services/ClusterNodesService?wsdl".format(self.server_ip)

            binding = "{http://services.api.platform.vos.cisco.com}ClusterNodesServiceSoap11Binding"

            endpoint = "https://{0}:8443/platform-services/services/ClusterNodesService." \
                       "ClusterNodesServiceHttpsSoap11Endpoint/".format(self.server_ip)

        else:
            pass




        try:

            client = Client(wsdl=wsdl, transport=Transport(cache=self.cache, session=self.session))

            service = client.create_service(binding,endpoint)

            return service

        except Exception as exc:

            logging.error(exc)

            return None






    def get_hardware_information(self, service):

        hw_info = service.getHardwareInformation()

        return hw_info

    def get_cluster_status(self, service):

        cl_status = service.getClusterStatus()['clusterNodeStatus']

        return cl_status



