```                                                                                                                                                                                                                                            
                    ##                                                                                                                                                                                                                      
#####            #   #     ####  ##                                                                                                                                                                                                         
 #  #                #    #   # #  #                                                                                                                                                                                                        
 #    ###  #### ##   #   #         #                                                                                                                                                                                                        
 ###  #  # # #   #   #   #        #                                                                                                                                                                                                         
 #     ###  #    #   #   #       #                                                                                                                                                                                                          
 #    #  # #  #  #   #    #   # #                                                                                                                                                                                                           
###   #### #### ### ###    ###  ####      
```

## Notes about this repo
~~This project exists as a forked repo from the original project~~, developed by [0xRick](https://0xrick.github.io/misc/c2/), to whom goes all my devotion for being able to explain, in simple and understandable code, how a C2 framework works. 
~~At the moment there is a pending pull request to merge the changes.~~ 

Since the pull request was not merged, I assume that the repo is not mantained anymore, so here I am!
<b>Essentially, the C2 allows you to execute remote commands (cmd and powershell) on the agents and eventually get the output.</b>

### Disclaimer
The only pourpose of this project is to learn how a C2 framework works. 0xRick applied the KIS principle, and I continued using this methodology. For me, it has been the occasion to learn how Flask works too, since I didn't know this micro-framework at all.

It shouldn't be necessary to say that: <i>"This software was created for educational purposes only and that I'm not responsible for any misuse in any way"</i>. 
Note that the server use self-signed certificates, that as you know, it suitable only in a test enviroment, morover the agent complitely skip the certificate validation, that again, is a very bad implementation. Having said that, don't
expose the server on Internet.

## Changes respect the original project
- Update required libraries according to Python version 3.12
- Removed the encryption logic based on AES key
- The server now run HTTPS
- Only one x64 exe (console app) payload is available
- Commands send to the agent are displayed on the app console


## Architecture

1. The server is a Flask Python (3.12) app running on Linux x64, in my case, on Kali 2024.3
2. The implant is a C# app (.Net 4.8) compiled with mono-mcs on Linux x64, in my case, on Kali 2024.3


## Requirements

- You must have installed mono-complete package
- You must have a SSL/TLS certificate. You have to set the certificate and the related key in the following file: <b>Simple_C2/core/listener.py</b>, around line 88

```
self.app.run(port=self.port, host=self.ipaddress, ssl_context=('/path/to/your/cert.crt', '/path/to/your/cert.key'))
```

## How to use

Install the required libraries:

```
pip3 install -r requirements.txt
```

Then start the server:

```
python3 c2.py
```
## TODO
1. Refactoring & clean the server code
2. ~~Make the server endpoints randomly generated~~
3. ~~Implements client messages on the console~~

    


