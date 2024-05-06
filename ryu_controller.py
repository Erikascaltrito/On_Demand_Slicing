from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
import multiprocessing
import subprocess
import threading
import time

class TrafficSlicing(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficSlicing, self).__init__(*args, **kwargs)

        #destination mapping [router --> MAC Destination --> Eth Port Output]
        self.mac_to_port = {
            1: {"00:00:00:00:00:01": 3, "00:00:00:00:00:02": 4, "00:00:00:00:00:03": 5, "00:00:00:00:00:04": 6},
            2: {"00:00:00:00:00:05": 3, "00:00:00:00:00:06": 4},
            3: {"00:00:00:00:00:07": 3, "00:00:00:00:00:08": 4},
            4: {"00:00:00:00:00:09": 3, "00:00:00:00:00:0a": 4}
        }

        #source mapping        
        self.port_to_port = {
            1: {3:1, 4:1, 5:1, 6:1},
            2: {3:2, 4:2},
            3: {3:3, 4:3},
            4: {3:4, 4:4},
        }

        #avvio le funzioni contemporaneamente
        t1 = multiprocessing.Process(target=self.activate_hacker_mode)
        t2 = threading.Thread(target=self.inserimento)
        t1.start()
        t2.start()

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        #install the table-miss flow entry
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)
        ]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        #construct flow_mod message and send it
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match, instructions=inst
        )
        datapath.send_msg(mod)

    def _send_package(self, msg, datapath, in_port, actions):
        data = None
        ofproto = datapath.ofproto
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        in_port = msg.match["in_port"]

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        
        dst = eth.dst
        src = eth.src
        
        dpid = datapath.id
        
        if dpid in self.mac_to_port:
                if dst in self.mac_to_port[dpid]:
                    out_port = self.mac_to_port[dpid][dst]
                    actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                    match = datapath.ofproto_parser.OFPMatch(eth_dst=dst)
                    self.add_flow(datapath, 1, match, actions)
                    self._send_package(msg, datapath, in_port, actions)

    def activate_hacker_mode(self):
        while True:
                time.sleep(90)
                subprocess.call("Slicing/./hacker_mod.sh")
                print('*********** Be careful! Network down ***********')                

    def inserimento(self):
            deactive_slices = [False for _ in range(4)]
            while True:
                time.sleep(1)
                print("*** Insert: (ACTIVE/DEACTIVE SLICE 1-4) note: IT services always ACTIVE")
                var = input()
                splitString = var.split(" ")
                status = splitString[0]
                control=0
		
                if (status !='ACTIVE' and status !='active' and status !='Active' and status !='DEACTIVE' and status !='deactive' and status !='Deactive' and status !='deactiveall' and status !='DEACTIVEALL' and status !='Deactiveall' and status !='DeactiveALL' and status !='conf' and status !='Conf' and status !='conference' and status !='Conference' and status !='CONFERENCE'):
                        print('*** Error! Insert ACTIVE/DEACTIVE or DEACTIVEALL/CONFERENCE')
                        continue
			
                if len(splitString)>1:
                        slice_number = int(splitString[1])
                        control=1
                        if slice_number < 1 or slice_number > 4:
                                print('*** Number of slices must be between 1 and 4')
                                continue

		
                if (status == 'DEACTIVE' or status =='deactive' or status =='Deactive'):
                        if control==1:
                                if slice_number == 1:
                                        print('*** Turn-off Slice 1: North Offices')
                                        deactive_slices[0]=True;
                                        subprocess.call("Slicing/./slice1.sh")
                                if slice_number == 2:
                                        print('*** Turn-off Slice 2: Conference Room')
                                        deactive_slices[1]=True;
                                        subprocess.call("Slicing/./slice2.sh")
                                if slice_number == 3:
                                        print('*** Turn-off Slice 3: East Offices')
                                        deactive_slices[2]=True;
                                        subprocess.call("Slicing/./slice3.sh")
                                if slice_number == 4:
                                        print('*** Turn-off Slice 4: West Offices')
                                        deactive_slices[3]=True;
                                        subprocess.call("Slicing/./slice4.sh")
                        else:
                                print('*** De-activating all Slices')
                                for i in range(len(deactive_slices)):
                                        str_slice = "Slicing/./slice"
                                        if (not deactive_slices[i]):
                                                str_slice += str(i+1) + ".sh"
                                                deactive_slices[i] = True
                                                subprocess.call([str_slice])

                elif (status == 'ACTIVE' or status =='active' or status =='Active'):
                        subprocess.call("Slicing/./total_activity.sh")
                        if control==0:
                                print('*** Activate Slices')
                                deactive_slices = [False for _ in range(4)]
                        else:
                                print('*** Activate Slice ',slice_number)
                                deactive_slices[slice_number-1]=False
                                for i in range(len(deactive_slices)):
                                        str_slice="Slicing/./slice"
                                        if deactive_slices[i]:
                                                str_slice += str(i+1) + ".sh"
                                                subprocess.call([str_slice, str(1)])
                elif (status == 'DEACTIVEALL' or status =='deactiveall' or status =='Deactiveall' or status =='DeactiveALL'):
                        subprocess.call("Slicing/./hacker_mod.sh")
                        print('*** De-activing all! Hacker mode ON')
                elif (status == 'conference' or status =='Conference' or status =='Conf' or status =='conf' or status == 'CONFERENCE'):
                        subprocess.call("Slicing/./conf_mod.sh")
                        print('*** Conference mode ON') 
    
     
                        
                