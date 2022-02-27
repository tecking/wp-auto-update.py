# wp-auto-update.py

## What's this?

wp-auto-update.py is a Python script to update WordPress websites. Once you setup a configuration file (YAML format), it cruises multiple websites and updates WordPress automatically.

The script is ported from a Ruby script [wp-auto-update.rb](https://github.com/tecking/wp-auto-update.rb)

## Features

The script updates WordPress websites the following processes.

1. Exports database
2. Updates WordPress core files
3. Updates all plugins (only distributed on [plugins directory](https://wordpress.org/plugins/))
4. Updates all themes (only distributed on [themes directory](https://wordpress.org/themes/))
5. Updates WP-CLI
6. Checks the website is whether in active or inactive
7. Sends execution results by email

## Requires

### Local host

* Connection with SSH is allowed
* Python3
  * [Paramiko](https://github.com/paramiko/paramiko) (apply with ``pip install paramiko``)
  * [PyYAML](https://github.com/yaml/pyyaml/) (apply with ``pip install pyyaml``)

### Remote host

* Connection with SSH is allowed (also possible SSH public key authentication)
* WP-CLI

## Installation and usage

1. ``git clone`` or download zip file from repository and expand
2. Rename config-sample.yml to config.yml (is the configuration file)
3. Setup wp-auto-update.py and config.yml 
4. Run ``python wp-auto-update.py``

## Settings

### wp-auto-update.py

Set the constants related to sending email.

* MAIL_SMTP  
  SMTP host name (or IP address)
* MAIL_PORT  
  Port number
* MAIL_USER  
  Username
* MAIL_PASS  
  Password
* MAIL_SUBJ  
  Subject (also possible ISO 8601 date format)
* MAIL_TO  
  Receipient address
* MAIL_FROM  
  Sender address

### config.yml

Set the variables related to hosting server for WordPress.

* name  
Identify name (*)
* url  
Site URL (*)
* host  
Hostname (FQDN, also possible IP address) (*)
* user  
Username (*)
* pass  
Password (you can omit under SSH public key authentication)
* port  
SSH port (*)
* key  
Full path to the private key file (it requires under SSH public key authentication)
* phrase  
Passphrase (it requires under SSH public key authentication)
* dir  
Path to the directory WordPress is installed (*)
* options
  * search
    Search strings for commands
  * replace
    Replacement strings for commands

## Option

Run with configuration file name, you can choose any configuration file. If it is empty, the script reads "config.yml" in the same directory.

### Example

``python wp-auto-update.py config.foobar.yml``

## Notice

* Please use At Your Own Risk
* The script was developed in Python 3.8 under the WSL2 (Ubuntu 20.04 LTS)
* Tested remote host
  * [SAKURA Rental Server](https://www.sakura.ne.jp/) (jp)
  * [LOLIPOP! Rentel Server](https://lolipop.jp/) (jp)
  * [XSERVER](https://www.xserver.ne.jp/) (jp)

## Changelog

* 1.1.0 (2022-02-27)
  * Update the method for commands execution
* 1.0.0 (2022-02-23)
  * Opening to the public

## License

[MIT License](https://opensource.org/licenses/mit-license.php)
