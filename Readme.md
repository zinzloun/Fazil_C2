# FAZIL C2
### YAC2: yet another C&C framework, created only for fun & learning

## Notes
Based on the [0xRick](https://0xrick.github.io/misc/c2/)'s job.

<b>Essentially, the C2 allows you to execute remote commands on agents and eventually get the output.</b>

### Disclaimer
The only pourpose of this project is to learn how a C2 framework works. 0xRick applied the KISS principle, and I continued using this approach. Eventually, for me, it has been the occasion to learn how Flask works.

It shouldn't be necessary to say that: <i>"This software was created for educational purposes only and that I'm not responsible for any misuse in any way"</i>. Note that the server use self-signed certificates, that as you know, it suitable only in a test enviroment, morover the agents complitely skip the certificate validation, that again, is a very bad implementation. Having said that, don't
expose the server on Internet.

## Changes respect the original project
- Update required libraries according to Python version 3.12
- Removed AES encryption
- The server now run HTTPS
- Only x64 exe payloads are supported
- Commands send to the agent are displayed on the app console
- Supports Linux agents (v 2.0)
- Added registry persistence (v 2.1) for windows agent


## Architecture

1. The server is a Flask Python (3.12) application, running on Linux x64 (Debian 12 in my case).
2. Payloads:
   - C# console application (.Net 4.8), compiled with mono-mcs on Linux x64 (Debian 12 in my case)
   - Rust zip project source code, that you can compile on a windows machine
   - Rust executable for Linux x64

## Requirements

- Install figlet
- You must have installed <b>mono-complete package</b>
- You must have installed <b>rustc and cargo</b> to compile the Linux agent 
- You must have a SSL/TLS certificate. You have to set <b>ssl_context</b> to point to the certificate and the related key path, in the following file: <b>Simple_C2/core/listener.py</b>, around line 88
```
self.app.run(port=self.port, host=self.ipaddress, ssl_context=('/path/to/your/cert.crt', '/path/to/your/cert.key'))
```

## How to use

Create a virtual enviroment and activate it:

      python3 -m venv fazilc2 && source fazilc2/bin/activate

Install the required libraries:

```
pip3 install -r requirements.txt
```

Start the server:

    sudo ./c2.py

Then if you know how a C2 tool works you are good to go. Use help command to get started:

```
(c2)::> help

[*] Avaliable commands: 


+-----------+-----------------------+--------+
| Command   | Description           | Args   |
+===========+=======================+========+
| help      | Show help.            |        |
+-----------+-----------------------+--------+
| home      | Return home.          |        |
+-----------+-----------------------+--------+
| clear     | Clear the screen.     |        |
+-----------+-----------------------+--------+
| exit      | Exit.                 |        |
+-----------+-----------------------+--------+
| listeners | Manage listeners.     |        |
+-----------+-----------------------+--------+
| agents    | Manage active agents. |        |
+-----------+-----------------------+--------+
| payloads  | Generate payloads.    |        |
+-----------+-----------------------+--------+

```

## Known issues
- If you rename the Rust agent you will not get the returned command's output back, that implies you won't be able to interact with the victim anymore

    



