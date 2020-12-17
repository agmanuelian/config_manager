# config_manager
Script to automate configuration of NTP, SNMP and Logging on IOS XE devices

Run the file main_file.py to execute this script.

This script will iterate over a list of IOS XE devices specified on the devices.csv file, and will push a standard NTP, SNMP or Logging configuration depending on the selected option.
This will be done using the protocol RESTCONF.

v1.0
The configuration parameters are specified statically on the script. On future releases, it will be get using an API call to a specific application that generates config files.

The devices.csv file contains the CSR1000v Always-on DevNet sandbox as part of this demo.
