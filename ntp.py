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

#Script to automate NTP configuration on IOS XE devices.
import requests
import json
from datetime import datetime
import csv
import urllib3
urllib3.disable_warnings()

def ntp(username, password,ip_addr, restconf_port, headers, confgen_params, confgen_response):

    restconf_base_url = f"https://{ip_addr}:{restconf_port}/restconf/data"
    ntp_dir = "Cisco-IOS-XE-native:native/ntp"

    # Static values. They should be received via API call to CONFGEN application.

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

    if vrf_name in vrf_list:
        #Agregar server-list - Existe VRF
        ntp_config = {
        "Cisco-IOS-XE-native:ntp": {
            "Cisco-IOS-XE-ntp:authenticate": [
                None
            ],
            "Cisco-IOS-XE-ntp:authentication-key": [
                {
                    "number": 24,
                    "md5": confgen_response["ntp_parameters"]["ntp_key_hashed"],
                    "encryption-type": 7
                }
            ],
            "Cisco-IOS-XE-ntp:server": {
                "vrf": [
                    {
                        "name": vrf_name,
                        "server-list": [
                            {
                                "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_1"],
                                "key": 24
                            },
                            {
                                "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_2"],
                                "key": 24
                            },
                            {
                                "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_3"],
                                "key": 24
                            },
                            {
                                "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_4"],
                                "key": 24
                            }
                        ]
                    }
                ]
            },
            "Cisco-IOS-XE-ntp:source": {
                confgen_params["mgmt_interface"].split(" ")[0]: confgen_params["mgmt_interface"].split(" ")[1]
            },
            "Cisco-IOS-XE-ntp:trusted-key": [
                {
                    "number": 24
                }
            ]
        }
        }
    else:
        #Agregar server-list - No existe VRF
        ntp_config = {
        "Cisco-IOS-XE-native:ntp": {
            "Cisco-IOS-XE-ntp:authenticate": [
                None
            ],
            "Cisco-IOS-XE-ntp:authentication-key": [
                {
                    "number": 24,
                    "md5": confgen_response["ntp_parameters"]["ntp_key_hashed"],
                    "encryption-type": 7
                }
            ],
            "Cisco-IOS-XE-ntp:server": {
                "server-list": [
                    {
                        "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_1"]
                    },
                    {
                        "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_2"]
                    },
                    {
                        "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_3"]
                    },
                    {
                        "ip-address": confgen_response["ntp_parameters"]["ntp_servers"]["ntp_sv_4"]
                    }
                ]
            },
            "Cisco-IOS-XE-ntp:source": {
                confgen_params["mgmt_interface"].split(" ")[0]: confgen_params["mgmt_interface"].split(" ")[1]
            },
            "Cisco-IOS-XE-ntp:trusted-key": [
                {
                    "number": 24
                }
            ]
        }
    }

    #Imprimo en terminal cómo quedó el ntp_config después de evaluar si existía la VRF
    # print(json.dumps(ntp_config, indent=2))

    #Antes enviar la configuración, se escribe un archivo de log con la configuración actual.

    log_file = open ("/Users/amanueli/Documents/DevNet/Scripts/DevNet/SNMP_NTP_SYSLOG/log_ntp.txt", "a")
    log_file.write("\n##################################\n\n")
    log_file.write(f"Current configuration for device {ip_addr}  -   Update: {datetime.now()}\n")

    current_ntp_config = requests.get(url=f"{restconf_base_url}/{ntp_dir}", headers= headers, auth=(username, password), verify= False).content.decode("utf-8") 
    log_file.write(current_ntp_config)
    print(current_ntp_config)
    log_file.close()
    print("-> LOG FILE GENERATED")
    # Se aplica nueva configuración
    send_config = requests.put(url=f"{restconf_base_url}/{ntp_dir}", headers= headers, auth=(username, password), data = json.dumps(ntp_config), verify= False).status_code

    if send_config == 204:
        print("-> SUCCESS! NTP Configured")
    else:
        print("-> Yikes! Something went wrong...")


            #TESTEO
            