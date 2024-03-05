import csv
import time
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import packet, ethernet, ipv4, ether_types
from ryu.ofproto import ofproto_v1_3

class SimpleController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleController, self).__init__(*args, **kwargs)
        self.packet_log = 'packet_log.csv'

        # Create or reset the CSV file
        with open(self.packet_log, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Timestamp', 'Source MAC', 'Destination MAC', 'Source IP', 'Destination IP', 'Protocol'])

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Install the table-miss flow entry
        match = parser.OFPMatch(in_port=1)  # Modifica con i tuoi criteri di corrispondenza
        actions = [parser.OFPActionOutput(2)]  # Modifica con le tue azioni
        self.add_flow(datapath, 1, match, actions)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocols(ethernet.ethernet)[0]
        ip_pkt = pkt.get_protocol(ipv4.ipv4)

        if eth_pkt.ethertype == ether_types.ETH_TYPE_IP and ip_pkt:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            src_mac = eth_pkt.src
            dst_mac = eth_pkt.dst
            src_ip = ip_pkt.src
            dst_ip = ip_pkt.dst
            protocol = ip_pkt.proto

            # Log packet information to CSV
            with open(self.packet_log, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([timestamp, src_mac, dst_mac, src_ip, dst_ip, protocol])

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

if __name__ == '__main__':
    from ryu.lib import hub
    from ryu.controller import controller

    app_manager.require_app('ryu.app.ofctl_rest')

    # Avvia il controller Ryu
    ryu_app = app_manager.AppManager.get_instance().instantiate(controller.RyuController)
    hub.joinall([hub.spawn(ryu_app.main, args)])