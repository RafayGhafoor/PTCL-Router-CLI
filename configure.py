from pathlib import Path, PurePath

import configobj


class Configure:
    '''
    A class for handling config object providing an intuitive
    interface to work with the config object and enhances config
    file flexibility for the addition and removal of attributes
    in a systematic manner.
    '''

    def __init__(config, config_path):
        self.config = config


    def create_sect(self, section_name):
        '''Creates a section in the config file.'''
        self.config[section_name] = {}


    def rm_sect_elem(self, element):
        pass

    
    def sect_exists(self, section_name):
        return self.config.get(section_name)


    def elem_exists(self, section_name, element):
        '''Checks for the existence of an element in the config.'''
        return self.config.get(section_name).get(element):
    
    
    def get_sect(self, section_name):
        '''Gets the (key, value) pair of the section.'''
        if not self.sect_exists(section_name): 
            raise Exception("{} not found.".format(section_name))
        
        return self.config.get(section_name)


    def get_sect_elem(self, section_name, element):
        if not self.sect_exists(section_name) or not self.elem_exists(section_name, element):
            raise Exception("{}: {} not found".format(section_name, element))
        
        return config[section_name][element]


    def add_elem(self, section, element, value):
        '''Add an element with its corresponding value in the given section.'''
        if not self.sect_exists:
            raise Exception("{} not found")
        self.config[section][element] = value

    
    def rm_elem(self, section, element, value):
        pass


    def update_config(self):
        with open(config_path, 'r+') as configfile:
            self.config.write(configfile)
        

def generate_config(fn):
    config = configobj.ConfigObj()    
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

    with open(fn, 'wb') as configfile:
        config.write(configfile)
    
    print('\nConfiguration file Generated.')


def process_config():
    CONFIG_PATH = PurePath(Path.home(), '.config', 'ptcl')
    CONFIG_FILE_PATH = PurePath(CONFIG_PATH, 'config.ini')

    '''Creates directory structure for configuration file if not exists.'''
    p = Path(CONFIG_PATH)
    
    if not p.exists(): 
        p.mkdir(parents=True, exist_ok=True)
        generate_config( str(CONFIG_FILE_PATH) )