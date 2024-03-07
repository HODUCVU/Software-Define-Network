# SDN Contoller Lecture
* [Link](https://learning.knetsolutions.in/docs/ryu/)
# Lecture
* Get MAC Address in subnet by ping IP Address:
	* To h1 get MAC Address of h2
	```
	mininet>h1 ping h2
	// see ARP (Address Resolution Protocol) of h1
	mininet>h1 arp -a
	```

	![](images/h1ARP.png)
	* Delete MAC Address of host 2 in ARP entry of host 1
	'''
	h1 arp -d 10.0.0.2
	'''
* Create network with many topos
	* Linear Topology
	```
	sudo mn --topo linear,4 --mac --controller remote,ip=127.0.0.1 -i 10.0.0.0/24 --switch ovsk
	```
	![](images/linear-topo.png)
	* Tree Topology
	```
	sudo mn --topo tree,depth=2,fanout=3 --mac --controller remote,ip=127.0.0.1 -i 10.0.0.0/24 --switch ovsk
	```
	![](images/tree-topo.png)
	* Single Topology
	```
	sudo mn --topo single,4 --mac --controller remote,ip=127.0.0.1 -i 10.0.0.0/24 --switch ovsk
	```
* Testing TCP and UDP bandwidth performance
	* Simple test
	```
	mininet>iperf src-node dst-node
	```
	Example:\
	> mininet> iperf h1 h2\
	Result: ['30.3 Gbits/sec', '30.2 Gbits/sec']
	* Test detail: test connect between h1 and h4
	```
	mininet>xterm h1
	mininet>xterm h4
	```
		* In h1
		```
		iperf -u -s
		```
		> -u: UDP\
		> -s: server
		* In h4
		```
		iperf -u -c 10.0.0.1 -b 10m -i 10 -t 30
		iperf -u -c 10.0.0.1 -b 10m -i 10 -P 10 -t 30
		```
		> -c: client\
		> -i: reporting interval\
		> -t: test duration in seconds (test in 30s)\
		> -b 10m: bandwith 10Mbps\
		> -P: parallel connections (the number connect from h4 to h1)
* Run ryu
	* Run virtual environment ryu
	```
	source ryu-venv/bin/activate
	```
	* Run a simple ryu app to get infor packet
	```
	// Get infor from header packet when entries table don't have matching flows
	ryu-manager ryu.app.simple_switch_13
	```
* Check connect between controller and network:
	```
	mininet> sh ovs-vsctl show
	```
	> check connect stage\
	> check connect ip of controller\
