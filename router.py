'''
A PTCL router class which allows basic functionality for PTCL router.

Usage Example:
# papi is used as an instance for the Router class in all examples.
>>> from router import Router
>>> papi = Router(gateway='192.168.1.1')      # Launches session for interacting with router
>>>
>>> papi.reboot() # Reboots router

>>> papi.stationinfo() # Returns a list of active devices
['macxxx', 'macxxx2', 'macxx3']

>>> papi.dhcpinfo() # Returns a dictionary object for dhcpinfo

{'HOSTNAME': ['Mac', 'LocalIp', 'Expires']}

{'my-computer': ['macxx', '192.168.10.1', '23 Hours, 59 Minutes']}
'''
import re

import requests
import bs4

import utils

class Router():
    '''
    A PTCL router class.

    To create connection to the router interface, call the class using these
    arguments:
            gateway, username, password
    All the arguments are strings.
    '''
    mac_pattern = re.compile(u'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')

    week_days = {
        "Mon": 1,
        "Tue": 2,
        "Wed": 4,
        "Thu": 8,
        "Fri": 16,
        "Sat": 32,
        "Sun": 64,
        "Everyday": 127
        }


    def __init__(self, gateway="192.168.1.1", username="admin", password="ptcl"):
        if utils.validate_gateway(gateway):
            self.gateway = "http://" + gateway + '/'
        else:
            raise ValueError("Invalid Gateway format specified, Valid format is",
                             "192.168.1.1")

        self.username = username
        self.password = password
        self.dev_info = {}      # Devices info
        self.active_dev = []    # Active Devices on Wi-Fi
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.sessionKey = None


    def scrape_page(self, url, params='', soup='n'):
        '''
        Scrape given link and create a beautiful soup object.
        - url:  Url to scrape.
        - soup: "n" to not create soup object and only return request response.
        '''
        try:
            request_url = self.session.get(url, params=params)

            if request_url.status_code == 401:
                sys.exit("Username or Password is incorrect.")

            elif request_url.status_code == 200:
                if soup == 'y':
                    html_soup = bs4.BeautifulSoup(request_url.content, 'lxml')
                    return html_soup
                return request_url

        except requests.exceptions.ConnectionError:
            raise Exception("Internet Connection Down.\nExiting...")


    def get_session_key(self):
        '''
        Gets session key from the html page for interacting with forms which
        require session key for authentication.
        '''
        r = self.scrape_page(url=self.gateway + 'wlmacflt.cmd')

        if not self.sessionKey:
            self.sessionKey = re.search('\d{5,13}', r.content.decode()).group()

        return self.sessionKey


    def dhcp(self):
        '''
        Gets information from dhcp page.
        Format:
            HOSTNAME | MAC | LOCAL IP | EXPIRES IN

        Example:
        >>>  my-pc | xx:xx..| 192.168..| 19 Hours ...

        Return:
            self.dev_info (Dictionary object)
        '''
        soup = self.scrape_page(url=(self.gateway + "dhcpinfo.html"), soup='y')
        td = soup.findAll('td')

        for i in td:

            if self.mac_pattern.search(i.text):
                '''
                The HTML page contains hostnames and mac addresses right next
                to each other in the form of table. We search in the tables list
                (td) until a mac address is found, then appends it to the
                mac_address list. The hostname is located before it so by using
                index less than the current index of mac address, we obtain the
                hostname and append it to the dev_hostname list.
                '''
                # Before mac_addresses, there is hostname
                # After mac_addresses, there are local ip and expire time for
                # the devices connected
                hostname = td[td.index(i) - 1].text
                self.dev_info[hostname] = [i.text, td[td.index(i) + 1].text, td[td.index(i) + 2].text]

        return self.dev_info


    def station(self):
        '''
        Gets information about the connected devices.
        '''
        soup = self.scrape_page(url=self.gateway + "wlstationlist.cmd", soup='y')

        for i in soup.findAll('td'):
            searchstr = i.text.replace('&nbsp','').strip()

            if self.mac_pattern.search(searchstr):
                self.active_dev.append(searchstr.lower())

        return self.active_dev


    #TODO if already username defined, raise Error
    def time_limit(self, username="User_1", mac="", days="Everyday", start="1", end="24"):
        '''
        Restricts user from using internet for limited time.
        Creates a user profile containing mac, days, start_time, end_time.
        - username: Create a profile for time limit of the provided username.
        - mac:      Device mac address on which time limit is applied.
        - days:     Day/days on which the time limit is applied.
        # Time is 24-hour format.
        - start:    Start time of device connection limit.
        - end:      End time of device connection limit.

        Example:
        Creates a profile named as User-1 and sets time limit for mac [x] at
        Monday beginning from 3 am to 6 pm.
        >>> papi.time_limit(username="User-1", mac="xx:xx...", days="Mon", start=3, end=6)

        Sets time limit from Monday to Friday.
        >>> papi.time_limit(username="User-1", mac="xx:xx...", days="Mon-Fri", start=3, end=6)
        '''

        # The day field in the request takes the power of 2 for the corresponding day in week.
        # Monday is    2^0
        # Tuesday is   2^1
        # Wednesday is 2^2
        
        gen_params = lambda days: {
        'username': username, 'days': days, 'start_time': start,
        'end_time': end, 'sessionKey': self.get_session_key()
        }

        start, end = utils.convert_time(start_time=start, end_time=end)
        days = days.split('-')

        if days and len(days) < 3:
            if len(days) == 1:
                	self.session.get(self.gateway + 'todmngr.tod?action=add&mac={}'.format(mac), params=gen_params(days=week_days[days[0]]))

            elif len(days) == 2 and days[0] in week_days and days[1] in week_days:
                if days[0] == days[1]:
                    self.session.get(self.gateway + 'todmngr.tod?action=add&mac={}'.format(mac), params=gen_params(days=week_days["Everyday"]))

                elif days[0] != days[1]:
                    self.session.get(self.gateway + 'todmngr.tod?action=add&mac={}'.format(mac), params=gen_params(days=str(week_days[days[1]])))
            else:
                print("Specified day is not in week_days.")

        return 'Successful'
		
    
    def web_filter(self, url):
        '''
        Block website temporarily/permanently (i.e Temporarily, when time is specified).
        '''
        return 'Successful'


    def block(self, mac):
        '''
        Block device using Mac Address.
        - mac: Device mac address to block.

        Example:
        >>> router.block('xx:xx:xx:xx:xx:xx')
        '''
        return self.session.get(self.gateway + "wlmacflt.cmd?action=add&rmLst={}&sessionKey={}".format(devmac, self.get_session_key())) 
        

    def unblock(self, mac):
        '''
        Unblock device using Mac Address.
        - mac: Device mac address to unblock.

        Example:
        >>> router.unblock('xx:xx:xx:xx:xx:xx')
        '''
        return self.session.get(self.gateway + "wlmacflt.cmd?action=remove&rmLst={}&sessionKey={}".format(udevmac, self.get_session_key()))


    def reboot(self):
        '''
        Reboots Router.
        '''
        return self.session.get(self.gateway + "rebootinfo.cgi?sessionKey={}".format(self.get_session_key()))


    def __repr__(self):
        return self.gateway