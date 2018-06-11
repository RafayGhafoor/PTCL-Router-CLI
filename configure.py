from pathlib import Path, PurePath
import sys

import configobj


CONFIG_PATH = PurePath(Path.home(), '.config', 'ptcl') # Configuration folder path
CONFIG_FP = str(PurePath(CONFIG_PATH, 'config.ini')) # Configuration file path
get_config = lambda path: configobj.ConfigObj(path) # Get configuration object


def generate_config(config=get_config(CONFIG_FP)):
    DEFAULT = {'gateway': '192.168.1.1', 'username': 'admin', 'password': 'admin'}

    gateway = input("Leave empty for default configuration.\nPlease enter router gateway\t(Default 192.168.1.1)\t: ")
    username = input("Please enter router username\t(Default admin)\t: ")
    password = input("Please enter router password\t(Default admin)\t: ")

    if gateway:
        DEFAULT['gateway'] = gateway

    if username:
        DEFAULT['username'] = username

    if password:
        DEFAULT['password'] = password
    
    config['Auth'] = DEFAULT
    config['Alias'] = {}
    config.write()
    sys.exit('Configuration file Generated.')


def process_config():
    '''Creates directory structure for configuration file if not exists.'''
    config_obj = configobj.ConfigObj('config.ini')
    p = Path(CONFIG_PATH)
    
    if not p.exists(): 
        p.mkdir(parents=True, exist_ok=True)
        generate_config()
    else:
        raise Exception("Path already exists")


def add_alias(alias, mac, config=get_config(CONFIG_FP)):
    '''Add an alias with its mac address to the configuration file.'''
    config.reload()
    config['Alias'][alias] = mac
    config.write()


def add_multiple_alias(aliases, macs, config=get_config(CONFIG_FP), separator=','):
    '''Map aliases to macs and write them to the configuration file.
    
    @args:
    
    aliases: List of strings containing the nicknames/alias of the users
    macs: List of strings containing the mac-addresses of the users
    separator: Delimiter for the alias-mac pair - defaults to comma (,)

    Example:

    add_multiple_alias(aliases='user1, user2, user3', macs='mac1, mac2, mac3')
    '''
    config.reload()
    aliases, macs = map(lambda x: x.strip(), aliases.split(separator) ), map(lambda x: x.strip(), macs.split(separator))
    for alias, mac in zip(aliases, macs):
        config['Alias'][alias] = mac
        
    config.write()

