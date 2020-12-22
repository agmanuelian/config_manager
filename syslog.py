#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python example script showing proper use of the Cisco Sample Code header.
Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

#Script to automate Logging configuration on IOS XE devices.
import requests
import json
from datetime import datetime
import csv
import urllib3
urllib3.disable_warnings()

def syslog(username, password, ip_addr, restconf_port, headers, confgen_params, confgen_response):

    restconf_base_url = f"https://{ip_addr}:{restconf_port}/restconf/data"
    logging_dir = "Cisco-IOS-XE-native:native/logging"

    #Chequeo si existe la VRF de management (siempre tiene el mismo nombre) - "VRF02", y dependiendo de eso voy por un camino o el otro.
    vrf_dir = "/Cisco-IOS-XE-native:native/ip/vrf"
    vrf_list = []
    try:
        vrf_list_dict = requests.get(url=f"{restconf_base_url}/{vrf_dir}", headers= headers, auth=(username, password), verify= False).json()["Cisco-IOS-XE-native:vrf"]
        for vrf in vrf_list_dict:
            vrf_list.append(vrf["name"])
    except:
        print("-> No VRFs configured!")

    vrf_name = "VRF-1"

    #START BULDING CONFIGURATION DICTIONARY
    if "logging_discriminator" in confgen_response["syslog_parameters"].keys():
        logging_conf = {
        "Cisco-IOS-XE-native:logging": {
            "discriminator": [
                {
                    "name": "DSCR",
                    "facility": {
                        #"drops": confgen_response["logging_discriminator"]
                        "drops": "DISCRIM_NAME"
                    }
                }
            ],
            "buffered": {
                "discriminator": [
                    {
                        "name": "DSCR",
                        "size-value": 1048576
                    }
                ]
            }
        }
        }
    else:
        logging_conf = {
        "Cisco-IOS-XE-native:logging": {
            "buffered": {
                "size": {
                    "size-value": confgen_response["syslog_buffered"] #Es size, o severity??
                }
            }   
        }
        }
    
    if vrf_name in vrf_list:
        #Agregar server-list - Existe VRF
        logging_conf["Cisco-IOS-XE-native:logging"]["host"]= {
            "ipv4-host-vrf-list": [
                {
                    "ipv4-host": confgen_response["syslog_parameters"]["syslog_server"],
                    "vrf": vrf_name
                }
                ]
            }

        logging_conf["Cisco-IOS-XE-native:logging"]["source-interface"] = [
                {
                    "interface-name": confgen_params["mgmt_interface"],
                    "vrf": vrf_name
                }
            ]
        logging_conf["Cisco-IOS-XE-native:logging"]["trap"] = {
                "severity": "notifications"
            }

    else:
        logging_conf["Cisco-IOS-XE-native:logging"]["host"]= {
            "ipv4-host-list": [
            {
                "ipv4-host": confgen_response["syslog_parameters"]["syslog_server"]
            }
            ]
        }
        logging_conf["Cisco-IOS-XE-native:logging"]["source-interface"] = [
            {
            "interface-name": confgen_params["mgmt_interface"]
            }
        ]

        logging_conf["Cisco-IOS-XE-native:logging"]["trap"] = {
                "severity": "notifications"
            }
        

    #Antes enviar la configuración, se escribe un archivo de log con la configuración actual.

    log_file = open ("/Users/amanueli/Documents/DevNet/Scripts/DevNet/SNMP_NTP_SYSLOG/log_file_logging.txt", "a")
    log_file.write("\n##################################\n\n")
    log_file.write(f"Current configuration for device {ip_addr}  -   Update: {datetime.now()}\n")

    current_logging_config = requests.get(url=f"{restconf_base_url}/{logging_dir}", headers= headers, auth=(username, password), verify= False).content.decode("utf-8") 
    log_file.write(current_logging_config)
    print(current_logging_config)
    log_file.close()
    print("-> LOG FILE GENERATED")
    # Se aplica nueva configuración
    send_config = requests.put(url=f"{restconf_base_url}/{logging_dir}", headers= headers, auth=(username, password), data = json.dumps(logging_conf), verify= False).status_code

    if send_config == 204:
        print("-> SUCCESS! Logging configured")
        #Agregar prompt para conservar nueva config, o hacer rollback.
    else:
        print("-> Yikes! Something went wrong...")


        # #TESTEO
        