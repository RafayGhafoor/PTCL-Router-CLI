# PTCL-Router-CLI

A CLI that provides a flexible and intuitive interface for controlling your (ptcl) router by consuming [papi](https://github.com/RafayGhafoor/PTCL-Router-API/)

# Usage:

```
Usage: ptcl.py [-h] [-b [BLOCK]] [-sb] [-u [UNBLOCK]] [-a] [-r] [-sd]
               [-s SHOW_ACTIVE] [-c] [-q [QUIET]]

Control PTCL router from command-line.

Options:

  -h, --help            show this help message and exit
  
  -b [BLOCK], --block [BLOCK]
                        Block device.
  
  -sb, --blocked_dev    Display blocked devices.
  
  -u [UNBLOCK], --unblock [UNBLOCK]
                        Unblock device.
  
  -a, --active-devices  Gets number of devices connected to the router.
  
  -r, --restart         Restart Router.
  
  -sd, --show-dhcp      Show DHCP Info.
  
  -s SHOW_ACTIVE, --show-active SHOW_ACTIVE
                        Show Active Devices.
  
  --configure       Configure router settings.
  
  -c [CLI], --cli [CLI]
                        CLI mode (used in conjunction with -u or -b).
```

# Examples:

```
>>> python ptcl.py --configure        # Configure router gateway, username and password

>>> python ptcl.py                    # Shows currently active devices.

>>> python ptcl.py -sa                # Set custom aliases for mac addresses.

>>> python ptcl.py -b USER            # Block user from custom defined alias.

>>> python ptcl.py -ub USER           # Unblock user from custom defined alias.

>>> python ptcl.py -b -c              # Block devices from the active devices display.

>>> python ptcl.py -sb                # Show blocked users.

>>> python ptcl.py -sd                # Show DHCP info.

>>> python ptcl.py -r                 # Reboots router.
```

# Current-Features:

- Obtain station information, showing their hostnames alongside for better readability (devices currently connected to the router).
- Obtain DHCP information.
- Block and unblock devices using their mac addresses.
- Block and unblock devices using their predefined aliases.
- Reboot router.
- Over-ride hostnames associated to the mac address with custom hostnames.
- Display blocked devices.
- Added two modes for blocking users ( CLI-MODE and SILENT-MODE (Default) ).

# TODO:

- [ ] Port-Forwarding from command line.
- [X] Display number of active devices.
- [X] Optimize Regular Expressions.
- [ ] Obtaining Pin-Code of the router and changing it.
- [ ] Displaying current password of the SSID.
- [X] Setting up custom hostname for specific device (mac address).
- [ ] Changing router username and password from the command-line.
- [ ] Changing Router SSID-Name.
- [X] Add CLI MODE for unblocking devices.
- [ ] Option to change frequency 2.4 Ghz or 5 Ghz.
- [X] Testing on other routers from the same vendor.
- [ ] Option to change router transmission power.
- [X] Improving display for blocked devices.
- [ ] Time restriction for user (by specifying or choosing from station info) device mac address or hostname.
- [ ] Adding URL to block unnecessary use for a website, also time limit for a site usage.
- [X] Reboot router from script.
- [ ] Getting devices connection info in a nice CSV file.
- [X] CLI MODE and SILENT MODE for blocking devices.





