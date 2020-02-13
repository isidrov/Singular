from http.server import HTTPServer, BaseHTTPRequestHandler
from PyQt5.QtCore import QRunnable,QObject,pyqtSignal, pyqtSlot, QThreadPool,Qt

import http.server
import socketserver
import traceback
import sys

"""
def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
"""

"""
def run():
    PORT = 8000

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

run()
"""

class PerhapsMyHttpServer(QRunnable):

    def __init__(self,*args, **kwargs):

        super(PerhapsMyHttpServer, self).__init__()
        # Store constructor arguments (re-used for processing)

        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them

        print("Thread start")

        try:
            PORT = 8000

            Handler = http.server.SimpleHTTPRequestHandler

            with socketserver.TCPServer(("10.82.176.52", PORT), Handler) as httpd:
                print("serving at port", PORT)
                httpd.serve_forever()
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit('good')  # Return the result of the processing
            print("Thread complete")
        finally:
            self.signals.finished.emit()  # Done

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, node,user, password, commands,*args, **kwargs):

        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.node = node
        self.user = user
        self.password = password
        self.commands = commands
        self.signals = WorkerSignals()
        self.interrupted = False

        # Add the callback to our kwargs
        #kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them

        try:
            result = self.fn(self.node, self.user, self.password, self.commands, *self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done



class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    '''

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    stopit = pyqtSignal()

#Flask