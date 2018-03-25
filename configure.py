import configobj
import os

config = ""

def write_config():
  # Creating a config file
  try:
      os.chdir(os.path.expanduser(os.path.join('~', '')))
      os.makedirs('.config' + os.sep + "ptcl")
      os.chdir('.config' + os.sep + "ptcl")

  except OSError:
      # If already exists
      pass

  config = configobj.ConfigObj()
  DEFAULT = {'mask': '192.168.1.1', 'username': 'admin', 'password': 'admin'}
  mask = input("Leave empty for default configuration.\nPlease enter router gateway\t(Default 192.168.1.1)\t: ")

  if mask:
      DEFAULT['mask'] = mask
  username = input("Please enter router username\t(Default admin)\t: ")

  if username:
      DEFAULT['username'] = username
  password = input("Please enter router password\t(Default admin)\t: ")

  if password:
      DEFAULT['password'] = password
  config['Router-Auth'] = DEFAULT
  config['Aliases'] = {}

  with open('config.ini', 'w') as configfile:
      config.write(configfile)
  print('\nConfiguration file Generated.')


def set_alias():
    # Defining custom aliases
    config = configobj.ConfigObj('config.ini')

    while True:
        hostname = input("Set Alias for hosname: ")
        if hostname == 'q':
            break
        macaddress= input("Enter it\'s macaddress: ")

        if macaddress == 'q':
            break

        else:
            if hostname not in config["Aliases"]:
                config["Aliases"][hostname] = macaddress
                with open('config.ini', 'r+') as configfile:
                    config.write(configfile)
    else:
        print("Already Present.")


def get_alias():
    # Return Aliases
    config = configobj.ConfigObj('config.ini')
    return config["Aliases"]


def config_check():
    path = os.path.expanduser(os.path.join('~', '.config' + os.sep + 'ptcl'))

    if os.path.exists(path):
        os.chdir(path)
        global config
        config = configobj.ConfigObj('config.ini')
        return True
    else:
        write_config()
        return False
