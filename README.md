# Exercise 1
## Group members:
* Ho Duc Vu - 106200284 
*  Nguyen Minh Phuong - 106200 
*  Huynh Vu Dinh Phuong - 106200

# Topic
* Start a topology with 1 switch and 4 hosts
* Manage the flow entries in ttthe created network manually using 'ovs-ofctl' command
	* Check current status of the switch
	* Check flow entries in the switch and modify them (add/remove)
	* Implementing some bassic forwarding entries with 'ovs-ofctl' command: Host 1 can send packet to any host, host 2 can sen packets to host 4, drop all packets from host 3
		* Use port number information
		* Use MAC address information
		* UsE IPpp address information
# Solution

## Start a topology with 1 switch and 4 hosts
### Code
'sudo mn --topo single,4 --controller=none --mac'
> --topo single,4: Use to create a switch and 4 host
> --controller=none: No controller
> --mac: Assign MAC address from 00:00:00:00:00:01 to 00:00:00:00:00:04 for host 1 to host 4
### Result

