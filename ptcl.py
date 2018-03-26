import argparse
import sys
import os

import configobj
from tabulate import tabulate

from router import Router

papi = Router()

def show_dhcpinfo():
    '''
    Shows DHCP information.
    '''
    table_data = [[k] + v for k, v in papi.dhcpinfo().items()]
    print(tabulate(table_data, tablefmt='fancy_grid', headers=["#", "HOSTNAME", "MAC", "LOCAL-IP", "EXPIRES"], showindex="always"))


def show_active_dev():
    '''
    Shows active devices (Mac Addresses) and their hostnames.
    '''

    table_data = [[i] for i in papi.stationinfo()]
    print(tabulate(table_data, tablefmt='fancy_grid', headers=["#", "MAC-ADDRESSES"], showindex="always"))


def main():
    parser = argparse.ArgumentParser(description="Control PTCL router from command-line.")
    parser.add_argument('-b', '--block', help="Block device.", nargs='?')
    parser.add_argument('-sb', '--blocked_dev', help='Display blocked devices.', action='store_true')
    parser.add_argument('-ub', '--unblock', help="Unblock device.", nargs='?')
    parser.add_argument('-a', '--active-devices', help="Gets number of devices connected to the router.", action='store_true')
    parser.add_argument('-r', '--restart', help="Restart Router.", action='store_true')
    parser.add_argument('-sd', '--show-dhcp', help='Show DHCP Info.', action='store_true')
    parser.add_argument('-s', '--show-active', help='Show Active Devices.', default='.')
    parser.add_argument('--configure', help='Configure router settings.', action='store_true')
    parser.add_argument('-sa', '--set-alias', help='Set custom alias for a device hostname.', action='store_true')
    parser.add_argument('-c', '--cli', help='Silent mode.', nargs='?', default='False')
    args = parser.parse_args()


    if args.active_devices:
        # print "Calling Station info Function"
        papi.stationinfo()

    elif args.restart:
        # print "Calling restart Function"
        papi.reboot()

    elif args.show_dhcp:
        # print "Calling DHCP_info Function"
        show_dhcpinfo()

    elif args.show_active == '.':
        show_active_dev()

    else:
        print("Invalid Argument")

main()
