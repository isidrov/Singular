
import paramiko
from paramiko_expect import SSHClientInteraction
import logging
import traceback
from time import sleep


logger = logging.getLogger(__name__)

class CliExpect:

    def __init__(self):

        self.prompt = r'.*admin.'
        self.pagination_1 = 'Press <enter> for 1 line, <space> for one page, or <q> to quit'
        self.pagination_2 = r'options: q=quit, n=next, p=prev, b=begin, e=end.*'


        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())



    def connect(self,ipaddress = '',username = '', password = ''):

        self.username = username
        self.password = password
        self.ipaddress = ipaddress

        try:
            # self.ssh.connect(self.ipaddress, username=self.username, password=self.password, banner_timeout = 20)

            self.ssh.connect(self.ipaddress, username=self.username, password=self.password,timeout = 30, banner_timeout = 20)

            self.interact = SSHClientInteraction(self.ssh, timeout=200,display=True)

            # program will wait till session is established and CUCM returns admin prompt

            index = self.interact.expect(self.prompt)

            result = self.interact.current_output

            if index ==  0:
                logging.info('intitial admin: promp matched')
                self.interact.send('set cli pagination off')
                index = self.interact.expect(self.prompt)
                result += self.interact.current_output
            else:
                logging.info('Error - Intitial prompt has not been matched')


            return result


        except  KeyboardInterrupt as kbi:
            logging.error('Ctrl + C pressed')
            logging.error(kbi)
            logging.error(traceback.print_exc())
            return None

        except (paramiko.AuthenticationException) as exc:
            logging.error('ClieExpect .connect() Authentication Exception')
            logging.error(exc)
            logging.error(traceback.print_exc())
            return None

        except (paramiko.ssh_exception.SSHException) as exc:
            logging.error('ClieExpect .connect() SSHException')
            logging.error(exc)
            logging.error(traceback.print_exc())
            return None

        except Exception as err:
            logging.error('Matched general exception')
            logging.error(err)
            return None


    def execute(self,command,pages = 10):

        #logging.info('current output clean before sending command: ' + self.interact.current_output_clean)

        #logging.info('current output before sending command: ' + self.interact.current_output)

        #logging.info('last match before sending command: ' + self.interact.last_match)

        #results = self.interact.current_output

        #TODO Pagination works, need to add 'file view...' capabilities

        #results += 'admin:' + command + '\n\n'

        # program runs a command
        logging.info('Sending command (cli expect) : ' + command)
        self.interact.send(command)


        # program waits for show status command to finish (this happen when CUCM returns admin or pagination prompt)
        self.interact.expect([self.prompt, self.pagination_1,self.pagination_2])

        ### We store output after expect ###

        results = self.interact.current_output

        # We handle pagination

        if self.interact.last_match == self.pagination_2:

            logging.info('paginating flavour 2...')

            if ('end of the file reached' in self.interact.current_output):
                logging.info('end of the file reached, sending q')
                self.interact.send('q')
                self.interact.expect([self.prompt])
                results += self.interact.current_output
            else:
                n = 0

                while (n < pages):

                    n += 1

                    if self.interact.last_match == self.prompt: #TODO this option might never happen, consider removing it
                        logging.info('Matched admin: prompt while paginating, exiting pagination')
                        logging.info('end of the file reached, sending q')
                        self.interact.send('q')
                        n = pages

                    elif 'end of the file reached' in self.interact.current_output:
                        logging.info('end of the file reached, sending q')
                        self.interact.send('q')
                        n = pages

                    elif self.interact.last_match == self.pagination_2:
                        logging.info('Matched pagination prompt, continuing paginating, current pages: ' + str(n))

                        if n == pages:
                            logging.info('number of defined pages reached, exiting pagination by sending q')
                            self.interact.send('q')

                        else:

                            logging.info('sending n')
                            self.interact.send('n')
                            self.interact.expect([self.prompt,self.pagination_2])
                            results += self.interact.current_output

                    else:
                        logging.error('Error when paginating... exiting pagination, sending q')
                        self.interact.send('q')
                        n = pages

                self.interact.expect([self.prompt])
                results += self.interact.current_output


        elif self.interact.last_match == self.pagination_1:

            logging.info('paginating flavour 1...')
            n = 0

            while (n < pages):

                n += 1
                self.interact.send(' ')
                self.interact.expect([self.prompt, self.pagination_1])
                results += self.interact.current_output

                if self.interact.last_match == self.prompt:
                    logging.info('Matched admin: prompt while paginating, exiting pagination')
                    n = pages
                elif self.interact.last_match == self.pagination_1:
                    logging.info('Matched pagination prompt, continuing paginating, current pages: ' + str(n))
                else:
                    logging.error('Error when paginating...')
                    break
            logging.info('sending q')
            self.interact.send('q')
            self.interact.expect([self.prompt])
            results += self.interact.current_output

        else:
            pass


        #TODO make a disconnect function

        #self.ssh.close()

        return results

    '''
        checks for unauthorized vulenrability 
        
        https://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-20171115-vos
    '''

    def unauth_vulenrability_check(self,ipaddress = ''):

        logging.info('Testing vulnerability cisco-sa-20171115-vos')

        self.username = 'root'
        self.password = 'cisco'
        self.ipaddress = ipaddress

        try:
            self.ssh.connect(self.ipaddress, username=self.username, password=self.password)
            self.interact = SSHClientInteraction(self.ssh, timeout=200, display=True)
            self.ssh.close()
            return self.ipaddress + ' is VULNERABLE to cisco-sa-20171115-vos'

        except paramiko.AuthenticationException as exce:
            logging.info(exce)
            logging.info(self.ipaddress + ' is NOT vulnerable to cisco-sa-20171115-vos')
            return self.ipaddress + ' is NOT vulnerable to cisco-sa-20171115-vos'

        except:
            logging.info(self.ipaddress + ' is NOT vulnerable to cisco-sa-20171115-vos')
            logging.warning('Exception not catched under cisco-sa-20171115-vos check')
            return self.ipaddress + ' is NOT vulnerable to cisco-sa-20171115-vos'
