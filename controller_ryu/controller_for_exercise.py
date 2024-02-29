from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class Controller(app_manager.RyuApp):
	OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

	def __init__(self, *args, **kwargs):
		super(Controller, self).__init__(*args, **kwargs)

	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
	def switch_features_handler(self,ev):
		datapath = ev.msg.datapath
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser

		#Install flow entries to capture all messages
		match = parser.OFPMatch()
		actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
		self.add_flow(datapath,0,match,actions)

		#Send on OFPPortStatsRequst to get current network statistics
		self.request_port_stats(datapath)

	def add_flow(self,datapath,priority,match,actions):
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser

		inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
		modify = parser.OFPFlowMod(datapath=datapath,priority=priority,match=match,instructions=inst)

		datapath.send_msg(modify)

	def request_port_stats(self, datapath):
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser

		request = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
		datapath.send_msg(request)

	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def packet_in_handler(self, ev):
		msg = ev.msg
		dp = msg.datapath
		ofp = dp.ofproto
		ofp_parser = dp.ofproto_parser

		actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
		data = None
		if msg.buffer_id == ofp.OFP_NO_BUFFER:
			data = msg.data

		if hasattr(msg, 'in_port'):
			in_port = msg.in_port
		else:
			in_port = None

		#out = ofp_parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id, in_port=in_port, actions=actions, data=data)
		if in_port is not None:  # Check if in_port is not None before using it
			out = ofp_parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id, in_port=in_port, actions=actions, data=data)
		else:
			out = ofp_parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id, actions=actions, data=data)

		dp.send_msg(out)


	@set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
	def port_stats_reply_handler(self, ev):
		pass
