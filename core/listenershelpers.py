from common import *
from agentshelpers import getAgentsForListener, removeAgent, taskAgentToQuit
from listener import Listener

from collections import OrderedDict
from shutil import rmtree
from tabulate import tabulate

import os
import netifaces

import random
import string

listeners = OrderedDict()
letters = string.ascii_lowercase
           

def checkListenersEmpty(s):

    if len(listeners) == 0:

        if s == 1:
            error("There are no active listeners.")
            return True
        else:
            return True

    else:
        return False


def isValidListener(name, s):

    vListeners = ulisteners()

    if name in vListeners:
        return True
    else:
        if s == 1:
            error("Invalid listener.")
            return False
        else:
            return False


def viewListeners():

    if checkListenersEmpty(1) == False:

        success("Active HTTPS listeners:")
        
        print(YELLOW)
        
        header = ["Name", "IP", "Port", "Running"]
	# Prepara i dati per la tabella
	
        rows = [(listeners[i].name, listeners[i].ipaddress, listeners[i].port, listeners[i].isRunning) for i in listeners]
       
        print(tabulate(rows, headers=header, tablefmt="grid"))

        
        print(cRESET)

        


def ulisteners():

    l = []

    for listener in listeners:
        l.append(listeners[listener].name)

    return l


def startListener(args):
    
	
    if len(args) == 1:
        name = args[0]
        if name in listeners:
             try:
                 listeners[name].start()
                 success("Started listener {}.".format(name))
             except:
                 error("Cannot start the listener.")
        else:
             error("Listener {} does not exist.".format(name))
    else:
        if len(args) != 3:
            error("Invalid arguments.")
        else:
            name = args[0]

            try:
                port = int(args[1])
            except:
                error("Invalid port.")
                return 0
            
            iface = args[2]

            try:
                netifaces.ifaddresses(iface)
                ipaddress = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
            except:
                error("Invalid interface.")
                return 0

            if isValidListener(name, 0):
                error("Listener {} already exists.".format(name))
            else:
                # new listener: generate random uri 
                uri_reg = '/0' + ''.join(random.choice(letters) for i in range(8))
                uri_tasks = '/1' + ''.join(random.choice(letters) for i in range(8))
                uri_results = '/2' + ''.join(random.choice(letters) for i in range(8))
                uri_download = '/3' + ''.join(random.choice(letters) for i in range(8))
           	
                listeners[name] = Listener(name, port, ipaddress, uri_reg, uri_tasks, uri_results, uri_download)
                progress("Starting listener {} on {}:{}.".format(name, ipaddress, str(port)))

                try:
                    listeners[name].start()
                    success("Listener started.")
                except:
                    error("Failed. Check your options.")
                    del listeners[name]

def stopListener(args):

    if len(args) != 1:
        error("Invalid arguments.")
    else:
        
        name = args[0]
        
        if isValidListener(name, 1):
            
            if listeners[name].isRunning == True:
                progress("Stopping listener {}".format(name))
                listeners[name].stop()
                success("Stopped.")
            else:
                error("Listener {} is already stopped.".format(name))
        else:
            pass

def removeListener(args):
    
    if len(args) != 1:
        error("Invalid arguments.")
    else:
        
        name = args[0]
        
        if isValidListener(name,1):
            
            listenerAgents = getAgentsForListener(name)

            for agent in listenerAgents:
                removeAgent([agent])

            rmtree(listeners[name].Path)
            
            if listeners[name].isRunning == True:
                stopListener([name])
                del listeners[name]
            else:
                del listeners[name]

        else:
            pass

def saveListeners():

    if len(listeners) == 0:
        clearDatabase(listenersDB)
    else:
        data = OrderedDict()
        clearDatabase(listenersDB)
        
        for listener in listeners:
        
            name       = listeners[listener].name
            port       = str(listeners[listener].port)
            ipaddress  = listeners[listener].ipaddress
            flag = "0"
        
            if listeners[listener].isRunning == True:    
                flag       = "1"
                listeners[listener].stop()
                
            data[name] = name + " " + port + " " + ipaddress + " " + flag + " " + listeners[listener].uri_reg + " " + listeners[listener].uri_tasks + " " + listeners[listener].uri_results + " " + listeners[listener].uri_download
    
        writeToDatabase(listenersDB, data)

def loadListeners():
    
    if os.path.exists(listenersDB):
        
        data = readFromDatabase(listenersDB)
        temp = data[0]

        for listener in temp:
            
            listener = temp[listener].split()

            name      = listener[0]
            port      = int(listener[1])
            ipaddress = listener[2]
            flag      = listener[3]
            uri_reg   = listener[4]
            uri_tasks = listener[5]
            uri_results = listener[6]
            uri_download = listener[7]

            listeners[name] = Listener(name, port, ipaddress, uri_reg, uri_tasks, uri_results, uri_download)

            if flag == "1":
                listeners[name].start()

    else:
        pass
