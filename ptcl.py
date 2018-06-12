import argparse
import sys
import os

from tabulate import tabulate

from router import Router
import configure


def show_dhcpinfo(rapi):
    '''
    Shows DHCP information.
    '''
    table_data = [[k] + v for k, v in rapi.dhcp().items()]
    print(tabulate(table_data, tablefmt='fancy_grid', headers=["#", "HOSTNAME", "MAC", "LOCAL-IP", "EXPIRES"], showindex="always"))


def show_active_dev(rapi):
    '''
    Shows active devices (Mac Addresses) and their hostnames.
    '''

    table_data = [[i] for i in rapi.station()]
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

    if args.configure:
        configure.process_config()

    config_dict = configure.fetch_config().dict()
    get_auth = lambda parameter: config_dict['Auth'][parameter] 
    papi = Router(gateway=get_auth('gateway'), username=get_auth('username'), password=get_auth('password'))


    if args.restart:
        # print "Calling restart Function"
        papi.reboot()

    elif args.show_dhcp:
        # print "Calling DHCP_info Function"
        show_dhcpinfo(papi)

    elif args.show_active == '.':
        show_active_dev(papi)

    else:
        print("Invalid Argument")


if __name__ == '__main__':
    main()
