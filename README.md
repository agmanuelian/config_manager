# config_manager


## Description 
Script to automate configuration of NTP, SNMP and Logging on IOS XE devices

This Python script will iterate over a list of IOS XE devices specified on the devices.csv file, and will push a standard NTP, SNMP or Logging configuration depending on the selected option.
This will be done using the RESTCONF protocol.

## About the LAB to run the demo.

The _devices.csv_ file contains the CSR1000v Always-on DevNet sandbox as part of this demo. 
Sandbox URL: https://devnetsandbox.cisco.com/RM/Diagram/Index/27d9747a-db48-4565-8d44-df318fce37ad?diagramType=Topology

CSR1000V Host: ios-xe-mgmt.cisco.com

SSH Port: 8181

NETCONF Port: 10000

RESTCONF Ports: 9443 (HTTPS)


Credentials of this public available Sandbox to specify when prompted for it:

**Username:** developer

**Password:** C1sco12345

## Usage

1. Clone this repo in your local machine typing on your terminal "git clone https://github.com/agmanuelian/config_manager.git"
2. Install the required dependencies specified on the _requirements.txt_ file > "pip install requirements.txt"
3. Edit the _devices.csv_ file with the parameters (IP address and RESTCONF port) of the list of devices that you want to configure.
4. Replace the _confgen_response_ JSON object with your infrastructure parameters (NTP server, SNMP and Logging parameters)
5. Run the _main_file.py_ script.
6. You will be prompted to enter your TACACS credentials to access the list of devices.
7. You will be prompted to enter the desired option (whether to configure NTP, Logging or SNMP)
8. Based on your selection, the script will configure your selection on the list of devices.

## Release Notes
### Version 1.0

The configuration parameters are specified statically on the script. In order to configure the list of network devices, these NTP, SNMP and Logging parameters should be statically typed on the JSON structure embedded on the script. On future releases, it will be get using an API call to a specific application that generates config files.
