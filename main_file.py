#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

#Script to automate Logging, SNMP and NTP configuration on IOS XE devices.
import json
import csv
from getpass import getpass
from prettytable import PrettyTable
from ntp import ntp
from snmp import snmp
from syslog import syslog

# Enter credentials via Prompt
username = input("Username: ")
password = getpass("Password: ")

#Showing menu

menu = PrettyTable(['OPTION', 'CONFIG'])
menu.add_row(["1", "NTP"])
menu.add_row(["2", "SNMP"])
menu.add_row(["3", "LOGGING"])
print(menu)
choice = int(input("Please select an option: "))

#Replace the following directory with personal directory where the script is located.
with open('/Users/amanueli/Documents/DevNet/Scripts/DevNet/SNMP_NTP_SYSLOG/devices.csv', mode='r') as csv_file:
    #Reading CSV file 
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        #Setting up variables
        ip_addr = row["ipaddr"]
        restconf_port= row["port"]

        headers ={
            "Content-Type": "application/yang-data+json",
            "Accept": "application/yang-data+json"
        }
        confgen_params = {
            "hostname": "{{hostname}}",
            "os_type": "{{os_type}}",
            "os_version": "{{os_version}}",
            "model": "{{model}}",
            "vendor": "{{vendor}}",
            "config_block": ["BRANCH_RESTCONF"],
            "mgmt_interface": "GigabitEthernet 3"
        }

        #Static values defined, but they could be received by another app by sending the "confgen_params" and based on each device parameters.
        confgen_response = {
             "syslog_parameters": {
                "syslog_server": "1.1.1.1",
                "syslog_buffered": 5000,
                "logging_discriminator": "DISCRIM_NAME"
             },
             "ntp_parameters":
            {
                "ntp_key_hashed": "123456",
                "ntp_servers":
                {
                    "ntp_sv_1": "1.1.1.1",
                    "ntp_sv_2": "2.2.2.2",
                    "ntp_sv_3": "3.3.3.3",
                    "ntp_sv_4": "4.4.4.4"
                }
            },
            "snmp_parameters":{ 
                "environment_code": "demo",  
                "radius_snmp_community": "COM-NAME-RADIUS",
                "snmp_community_name": "COM-NAME",
                "snmp_sv_prod": "1.1.1.1",
                "snmp_trap_group": "TRAP-GROUP",
                "snmp_sv_failover": "2.2.2.2",
                "Opennms_DC_dest1": "3.3.3.3",
                "Opennms_DC_dest2": "4.4.4.4",
                "Opennms_DC_dest3": "5.5.5.5",
                "Opennms_DC_dest4": "6.6.6.6",
                "snmp_sv_macmove": "1.2.3.4",
                "snmp_community_macmove": "MACMOVE-NAME",
                "region.radius_sv_primary": "1.2.2.2",
                "region.radius_sv_secondary": "1.3.3.3",
                "region.radius_sv_tertiary": "1.4.4.4"
            }
        }

        if choice == 1:
            #Implement NTP configuration
            ntp(username, password, ip_addr, restconf_port, headers, confgen_params, confgen_response)
        elif choice == 2:
            #Implement SNMP configuration
            snmp(username, password, ip_addr, restconf_port, headers, confgen_params, confgen_response)
        else:
           #Implement Logging configuration
           syslog(username, password, ip_addr, restconf_port, headers, confgen_params, confgen_response)
