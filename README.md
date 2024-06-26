# On Demand SDN Slices in ComNetsEmu Project

This README provides an overview of the "On Demand SDN Slices in ComNetsEmu" project developed for the Networking 2 course at the University of Trento.

## Introduction

The objective is to implement a network slicing approach allowing dynamic activation and deactivation of network slices via CLI/GUI commands, the SDN controller used is a RYU. On-demand functionality means users can activate and deactivate different slices as needed. Slice descriptions should include identifiers for flows, topology, and percentage of link capacity for each slice.

## Project Description

We created a basic layout of an entire floor in the DICAM building in Trento. It includes 8 rooms: 2 offices on the north side, 2 on the east side, 2 on the west side, a conference room, and an IT services office. These offices are our slices, all with different services.

- **Slice 1 (h5, h6)**: Offices on the north side that offer specific services to the university, like administrative support or academic advice.

- **Slice 2 (h3, h4)**: It's the conference room, where important meetings, conferences, workshops, and training sessions happen. These hosts are capable of receiving UDP flows because for calls, security is not essential rather than speed.

- **Slice 3 (h9, h10)**: Offices on the east side offering specialized services, like research resources or advanced technical support.

- **Slice 4 (h7, h8)**: Offices on the west side providing services like student support.

- **Slice 5 (h1, h2)**: It's the IT services department responsible for managing and supporting all the university's computer and technology resources, such as networks, systems, applications, and digital services. This slice is always active except during hacker mode.

<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/Mappa_Mesiano_completa.jpeg" width="100%" height="100%"><br>

### How it works 

Initially, all hosts can communicate with each others, all slices are active.
<p align="center">
    <img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/All_Active.jpeg"  width="80%" height="80%">
</p>

In the Ryu controller, we have the capability to deactivate specific slices as needed.
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/b963ea2684213976dd572b791fb534ee387c08df/Slicing_scenarios/Deactive1.png" width="60%" height="60%"><br>
<p align="center">
     <img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/Slice1_off.jpeg" width="80%" height="80%">
</p>

**Test bandwidth** of hosts with ```iperf```
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/31dcdb221e4f888987f08f85152868f58ed462ca/Slicing_scenarios/bw.png" width="60%" height="60%"><br>
Notice that when a slice is deactivated its bandwidth decreases.

**Test reachability** by running ```mininet> pingall```
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/31dcdb221e4f888987f08f85152868f58ed462ca/Slicing_scenarios/Pingall.png" width="40%" height="40%"><br>
It can be observed that h5 and h6 are unable to communicate with other hosts.
This process can be repeated for each slice.

**Send UDP packets in slice 2**:
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/31dcdb221e4f888987f08f85152868f58ed462ca/Slicing_scenarios/UDP_ok.png" width="60%" height="60%"><br> 
**Send UDP packets in others slices**:
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/31dcdb221e4f888987f08f85152868f58ed462ca/Slicing_scenarios/UDP_fail.png" width="60%" height="60%"><br> 
It's evident here that UDP flows are only permissible in slice 2, whereas they are blocked in the remaining slices.

The **Conference mode** simulates a scenario wherein there is an important meeting, so slice 2 requires more bandwidth compared to the other slices.
<p align="center">
    <img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/cb1e5cf29c2eda64a173322a955582a3383f0238/Slicing_scenarios/Slice1_3_4_off.jpeg"  width="80%" height="80%">
</p>

**Test bandwidth** of h3 and h4 with ```iperf``` before and after activating the Conference mode
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/cb1e5cf29c2eda64a173322a955582a3383f0238/Slicing_scenarios/bw_conf.png" width="60%" height="60%"><br> 

The **Hacker mode** simulates a security breach scenario where all network slices, including essential IT services, are deliberately deactivated. It serves as a simulation tool to assess system robustness and response mechanisms under adverse conditions. This scenario automatically activates in a random time.
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/b963ea2684213976dd572b791fb534ee387c08df/Slicing_scenarios/Hack_mod.png" width="60%" height="60%"><br> 

<p align="center">
     <img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/Hack_mod.jpeg" width="80%" height="80%">
</p>

The **GUI** displays our network structure visually and allows users to manage slices using buttons to activate and deactivate the slices.
<p align="center">
     <img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/cb1e5cf29c2eda64a173322a955582a3383f0238/Slicing_scenarios/Gui.png" width="80%" height="80%">
</p>


## Repository structure

1. **topology_slice.py**: This Python file defines the specific layout of our network. It includes 4 switches, 10 hosts and all the connection between them.

2. **ryu_controller.py**: Python file containing our SDN controller. It takes commands from users to control the activation or deactivation of network slices with our setup.

3. **gui.py**: This Python script creates a user-friendly interface for our project. It displays our network structure visually and allows users to manage slices using buttons.

4. **Slicing/total_activity.sh**: This shell script establishes the initial network setup where all hosts can communicate freely with each other.

5. **Slicing/slice#.sh**: These shell scripts represent different network slice configurations. Each script defines specific settings and restrictions for individual slices.

6. **Slicing/hacker_mod.sh**: This shell script simulates a security breach scenario by turning off all network slices, including IT services.

7. **Slicing/conf_mod.sh**: This shell script enable the conference mode, where more bandwidth is assigned to the slice 2.

8. **Slicing_scenarios**: This directory contains images used in the project to illustrate various network slicing scenarios.

## Installation

To install this project, follow these steps:

1. Clone the repository: `git clone https://github.com/Erikascaltrito/On_Demand_Slicing`
2. Navigate to the project directory: `cd On_Demand_Slicing`

## How to run CLI

1. Run the controller: `ryu-manager ryu_controller.py`
2. Open another terminal to create the mininet network: `sudo python3 topology_slicing.py`
3. On the controller window you can activate or deativate the slices using `active # of slice` or `deactive # of slice`
4. On the mininet window you can visualize the connections and the bandwidth
5. Delete the network after using it: `sudo mn -c`

## How to run GUI

1. Run the controller: `ryu-manager ryu_controller.py`
2. Open another terminal to create the mininet network: `sudo python3 topology_slicing.py`
3. In another terminal run the gui: `python3 gui.py`
4. Use the interface and visualize the connections and the bandwidth in the mininet window.
5. Delete the network after using it: `sudo mn -c`

## Contributors

- Erika Scaltrito (erika.scaltrito@studenti.unitn.it)
- Ylenia Graziadei (ylenia.graziadei@studenti.unitn.it)
- Roman Morozov (roman.morozov@studenti.unitn.it)
