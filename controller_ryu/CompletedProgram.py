from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto import ofproto_v1_3_parser
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import ipv4

class Controller(app_manager.RyuApp):
	OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

	def __init__(self, *args, **kwargs):
		super(Controller,self).__init__(*args, **kwargs)
		self.mac_to_port = {}

	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
	def switch_features_hanlder(self, ev):
		datapath = ev.msg.datapath
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser

		# Install table-miss flow entry (add-flow entries table)
		match = parser.OFPMatch()
		actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]

		self.add_flow(datapath, 0, match, actions)

		# Request port statistics
		request = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
		datapath.send_msg(request)

	def add_flow(self, datapath, priority, match, actions, buffer_id = None):
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser

		inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

		if buffer_id:
			modify = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
						priority=priority, match=match, instructions=inst)
		else:
			modify = parser.OFPFlowMod(datapath=datapath,priority=priority,
						match=match, instructions=inst)
		datapath.send_msg(modify)


	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def _packet_in_handler(self, ev):
		if ev.msg.msg_len < ev.msg.total_len:
			self.logger.debug("packet truncated: only %s oF %s bytes", ev.msg.msg_len, ev.msg.total_len)

		msg = ev.msg
		datapath = msg.datapath
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		in_port = msg.match['in_port']

		pkt = packet.Packet(msg.data)
		eth = pkt.get_protocols(ethernet.ethernet)[0]

		if eth.ethertype == ether_types.ETH_TYPE_LLDP:
			return # ignore lldp packet

		dst = eth.dst
		src = eth.src

		dpid = datapath.id
		self.mac_to_port.setdefault(dpid, {})

		self.logger.info("packet in id %s src %s dst %s port %s", dpid, src, dst, in_port)

		# Learn mac address to avoid FLOOD
		self.mac_to_port[dpid][src] = in_port
		if dst in self.mac_to_port[dpid]:
			out_port = self.mac_to_port[dpid][dst]
		else:
			out_port = ofproto.OFPP_FLOOD

		actions = [parser.OFPActionOutput(out_port)]

		# Add a flow to avoid packet_in next time
		if out_port != ofproto.OFPP_FLOOD:
			#check IIp and create a match for it
			if eth.ethertype == ether_types.ETH_TYPE_IP:
				ip = pkt.get_protocol(ipv4.ipv4)
				srcIP = ip.src
				dstIP = ip.dst
				match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP,
							ipv4_src=srcIP,ipv4_dst=dstIP)

				if msg.buffer_id != ofproto.OFP_NO_BUFFER:
					self.add_flow(datapath, 1, match, actions, msg.buffer_id)
					return
				else:
					self.add_flow(datapath, 1, match, actions)

		data = None
		if msg.buffer_id == ofproto.OFP_NO_BUFFER:
			data = msg.data
		out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
					in_port=in_port, actions=actions,data=data)

		datapath.send_msg(out)
		#self.port_stats_reply_handler(ev)
	# Get reply statitics from switch
	@set_ev_cls(ofp_event.EventOFPPortStatsReply, [MAIN_DISPATCHER,CONFIG_DISPATCHER])
	def port_stats_reply_handler(self, ev):
		stats = []
		for stat in ev.msg.body:
			stats.append({
				'port': stat.port_no,
				'rx_packets': stat.rx_packets,
				'tx_packets': stat.tx_packets,
				'rx_byte': stat.rx_bytes,
				'tx_byte': stat.tx_bytes,
				'rx_error': stat.rx_errors,
				'tx_error': stat.tx_errors,
				'rx_drop': stat.rx_dropped,
				'tx_drop': stat.tx_dropped,
				'rx_frame_err': stat.rx_frame_err,
				'rx_over_err': stat.rx_over_err,
				'rx_crc_err': stat.rx_crc_err,
				'collisions': stat.collisions
			})
		print(stats)
