## Galileo - Web Application Audit Framework
![python](https://img.shields.io/badge/python-2.7-green.svg) ![version](https://img.shields.io/badge/version-0.1.0-brightgreen.svg) ![licence](https://img.shields.io/badge/license-GPLv3-lightgrey.svg) 

Galileo is an open source penetration testing tool for web application, which helps developers and penetration testers identify and exploit vulnerabilities in their web applications.

Screenshots
----
![screen](https://raw.githubusercontent.com/m4ll0k/Galileo/master/screen.png)


Installation
----
```
$ git clone https://github.com/m4ll0k/Galileo.git galileo
$ cd galileo
```
__Install requirements__
```
$ pip install -r requirements.txt
```
__or__ 
```
$ apt-get install python-pysocks
```
__For windows__
```
$ python -m pip install pysocks
```
__Run__
```
$ python galileo.py
```

Usage
----

Set global options:

```
galileo #> set
  Set A Context-Specific Variable To A Value
  ------------------------------------------
  - Usage: set <option> <value>
  - Usage: set COOKIE phpsess=hacker_test


  Name        Current Value                            Required  Description
  ----------  -------------                            --------  -----------
  PAUTH                                                no        Proxy auth credentials (user:pass)
  PROXY                                                no        Set proxy (host:port)
  REDIRECT    True                                     no        Set redirect
  THREADS     5                                        no        Number of threads
  TIMEOUT     5                                        no        Set timeout
  USER-AGENT  Mozilla/5.0 (X11; Ubuntu; Linux x86_64)  yes       Set user-agent
  VERBOSITY   1                                        yes       Verbosity level (0 = minimal,1 = verbose)
```

Search module:
```
galileo #> search disclosure
[+] Searching for 'disclosure'...

  Disclosure
  ----------
    disclosure/code
    disclosure/creditcard
    disclosure/email
    disclosure/privateip

```
Show modules:
```
galileo #> show modules

  Bruteforce
  ----------
    bruteforce/auth_brute
    bruteforce/backup_brute
    bruteforce/file_dir_brute

  Disclosure
  ----------
    disclosure/code
    disclosure/creditcard
    disclosure/email
    disclosure/privateip

  Exploits
  --------
    exploits/shellshock

  Fingerprint
  -----------
    fingerprint/cms
    fingerprint/framework
    fingerprint/server

  Injection
  ---------
    injection/os_command_injection
    injection/sql_injection

  Scanner
  -------
    scanner/asp_trace

  Tools
  -----
    tools/socket
```
Use module:
```
galileo #> use bruteforce/backup_brute
galileo bruteforce(backup_brute) #> 
```
Set module options

```
galileo bruteforce(backup_brute) #> show options

  Name      Current Value  Required  Description
  --------  -------------  --------  -----------
  EXTS                     no        Set backup extensions
  HOST                     yes       The target address
  METHOD    GET            no        HTTP method
  PORT      80             no        The target port
  URL_PATH  /              no        The target URL path
  WORDLIST                 yes       Common directory wordlist

galileo bruteforce(backup_brute) #> set HOST www.xxxxxxx.com
HOST => www.xxxxxxx.com
galileo bruteforce(backup_brute) #> set WORDLIST /home/m4ll0k/Desktop/all.txt
WORDLIST => /home/m4ll0k/Desktop/all.txt
```
Run:
```
galileo bruteforce(backup_brute) #> run
```
![run](https://raw.githubusercontent.com/m4ll0k/Galileo/master/screen2.png)

