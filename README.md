# config_manager


## Description 
Script to automate configuration of NTP, SNMP and Logging on IOS XE devices

This Python script will iterate over a list of IOS XE devices specified on the devices.csv file, and will push a standard NTP, SNMP or Logging configuration depending on the selected option.
This will be done using the RESTCONF protocol.

## Release Notes
### Version 1.0

The configuration parameters are specified statically on the script. In order to configure the list of network devices, these NTP, SNMP and Logging parameters should be statically typed on the JSON structure embedded on the script. On future releases, it will be get using an API call to a specific application that generates config files.

## About the LAB to run the demo.

The _devices.csv_ file contains the CSR1000v Always-on DevNet sandbox as part of this demo. 

Credentials of this public available Sandbox to specify when prompted for it:

*Username:* developer

*Password:* C1sco12345
