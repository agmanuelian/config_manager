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

#Script to automate Logging configuration on IOS XE devices.
import requests
import json
from datetime import datetime
import csv
import urllib3
urllib3.disable_warnings()

def snmp(username, password, ip_addr, restconf_port, headers, confgen_params, confgen_response):
    restconf_base_url = f"https://{ip_addr}:{restconf_port}/restconf/data"
    snmp_server_dir = "Cisco-IOS-XE-native:native/snmp-server"

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
    if confgen_response["snmp_parameters"]["environment_code"]== "retail":
        snmp_conf = {
            "Cisco-IOS-XE-native:snmp-server": {
                "Cisco-IOS-XE-snmp:community": [
                    {
                        "name": "1.1.1.2",
                        "RO": [
                            None
                        ],
                        "access-list-name": 2
                    }
                ],
                "Cisco-IOS-XE-snmp:enable": {
                    "enable-choice": {
                        "traps": {
                            "alarms": {
                                "alarm-type": "informational"
                            }
                        }
                    }
                },
                "Cisco-IOS-XE-snmp:host": [
                    {
                        "ip-address": "1.1.1.1",
                        "community-or-user": "COM_string"
                    }
                ]
            }
        }
    else:
        if vrf_name in vrf_list:
            #  VRF exists
            snmp_conf = {
            "Cisco-IOS-XE-native:snmp-server": {
                "Cisco-IOS-XE-snmp:community": [
                    {
                        "name": "COM_NAME",
                        "RO": [
                            None
                        ],
                        "access-list-name": "ALLOW-SNMP"
                    }
                ],
                "Cisco-IOS-XE-snmp:enable": {
                    "enable-choice": {
                        "traps": {
                            "snmp": {
                                "linkdown": [
                                    None
                                ],
                                "linkup": [
                                    None
                                ]
                            }
                        }
                    }
                },
                "Cisco-IOS-XE-snmp:host": [
                    {
                        "ip-address": confgen_response["snmp_parameters"]["snmp_sv_prod"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_trap_group"],
                        "vrf": vrf_name
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["snmp_sv_failover"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_trap_group"],
                        "vrf": vrf_name
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["Opennms_DC_dest1"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_trap_group"],
                        "vrf": vrf_name
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["Opennms_DC_dest2"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_trap_group"],
                        "vrf": vrf_name
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["Opennms_DC_dest3"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_trap_group"],
                        "vrf": vrf_name
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["Opennms_DC_dest4"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_trap_group"],
                        "vrf": vrf_name
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["snmp_sv_macmove"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_community_macmove"],
                        "vrf": vrf_name,
                        "version": "2c",
                        "trap-enable": {
                            "bfd": [ 
                                None
                            ]
                        }
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["region.radius_sv_primary"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_community_macmove"],
                        "vrf": vrf_name,
                        "version": "2c",
                        "trap-enable": {
                            "bfd": [ 
                                None
                            ]
                        }
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["region.radius_sv_secondary"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_community_macmove"],
                        "vrf": vrf_name,
                        "version": "2c",
                        "trap-enable": {
                            "bfd": [ 
                                None
                            ]
                        }
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["region.radius_sv_tertiary"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_community_macmove"],
                        "vrf": vrf_name,
                        "version": "2c",
                        "trap-enable": {
                            "bfd": [ 
                                None
                            ]
                        }
                    }
                ],
                "Cisco-IOS-XE-snmp:source-interface": {
                    "informs": {
                        "Loopback": 117
                    }
                },
                "Cisco-IOS-XE-snmp:trap-source": {
                    "Loopback": 117
                }
            }
        }
        else:
            #  VRF doesn't exist
            snmp_conf = {
            "Cisco-IOS-XE-native:snmp-server": {
                "Cisco-IOS-XE-snmp:community": [
                    {
                        "name": "COM_NAME",
                        "RO": [
                            None
                        ],
                        "access-list-name": "ALLOW-SNMP"
                    }
                ],
                "Cisco-IOS-XE-snmp:enable": {
                    "enable-choice": {
                        "traps": {
                            "snmp": {
                                "linkdown": [
                                    None
                                ],
                                "linkup": [
                                    None
                                ]
                            }
                        }
                    }
                },
                "Cisco-IOS-XE-snmp:host": [
                    {
                        "ip-address": confgen_response["snmp_parameters"]["snmp_sv_prod"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_trap_group"]
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["snmp_sv_failover"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_trap_group"]
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["Opennms_DC_dest1"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_trap_group"]
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["Opennms_DC_dest2"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_trap_group"]
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["Opennms_DC_dest3"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_trap_group"]
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["Opennms_DC_dest4"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_trap_group"]
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["snmp_sv_macmove"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_community_macmove"],
                        "version": "2c",
                        "trap-enable": {
                            "bfd": [ 
                                None
                            ]
                        }
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["region.radius_sv_primary"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_community_macmove"],
                        "version": "2c",
                        "trap-enable": {
                            "bfd": [ 
                                None
                            ]
                        }
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["region.radius_sv_secondary"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_community_macmove"],
                        "version": "2c",
                        "trap-enable": {
                            "bfd": [ 
                                None
                            ]
                        }
                    },
                    {
                        "ip-address": confgen_response["snmp_parameters"]["region.radius_sv_tertiary"],
                        "community-or-user": confgen_response["snmp_parameters"]["snmp_community_macmove"],
                        "version": "2c",
                        "trap-enable": {
                            "bfd": [ 
                                None
                            ]
                        }
                    }
                ],
                "Cisco-IOS-XE-snmp:source-interface": {
                    "informs": {
                        "GigabitEthernet": 3
                    }
                },
                "Cisco-IOS-XE-snmp:trap-source": {
                    "GigabitEthernet": 3
                }
            }
        }

        

    #Imprimo en terminal cómo quedó el logging_conf después de evaluar si existía la VRF
    #print(json.dumps(logging_conf, indent=2))

    #Antes enviar la configuración, se escribe un archivo de log con la configuración actual.

    log_file = open ("/Users/amanueli/Documents/DevNet/Scripts/DevNet/SNMP_NTP_SYSLOG/log_file_snmp.txt", "a")
    log_file.write("\n##################################\n\n")
    log_file.write(f"Current configuration for device {ip_addr}  -   Update: {datetime.now()}\n")

    current_snmp_config = requests.get(url=f"{restconf_base_url}/{snmp_server_dir}", headers= headers, auth=(username, password), verify= False).content.decode("utf-8") 
    log_file.write(current_snmp_config)
    #print(current_snmp_config)
    log_file.close()
    print("-> LOG FILE GENERATED")
    # Se aplica nueva configuración
    send_config = requests.put(url=f"{restconf_base_url}/{snmp_server_dir}", headers= headers, auth=(username, password), data = json.dumps(snmp_conf), verify= False).status_code

    if send_config == 204:
        print("-> SUCCESS! SNMP Configured")
        #Agregar prompt para conservar nueva config, o hacer rollback.
    else:
        print("-> Yikes! Something went wrong...")


    # #TESTEO