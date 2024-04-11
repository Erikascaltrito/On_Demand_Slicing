# On Demand SDN Slices in ComNetsEmu Project

This README provides an overview of the "On Demand SDN Slices in ComNetsEmu" project developed for the Networking 2 course at the University of Trento.

## Introduction

The objective is to implement a network slicing approach allowing dynamic activation and deactivation of network slices via CLI/GUI commands, the SDN controller used is a RYU. On-demand functionality means users can activate and deactivate different slices as needed. Slice descriptions should include identifiers for flows, topology, and percentage of link capacity for each slice.

## Project Description

We created a basic layout of an entire floor in the DICAM building in Trento. It includes 8 rooms: 2 offices on the north side, 2 on the east side, 2 on the west side, a conference room, and an IT services office. Those rooms are basically our slices, all with different services.
- Slice 1: h5, h6
- Slice 2: h3, h4
- Slice 3: h9, h10
- Slice 4: h7, h8
- Slice 5: h1, h2 ➝ this slice is always active, with the exception of the hacker mode.
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/Mappa_Mesiano_completa.jpeg" width="100%" height="100%"><br>

### How it works 

Initially, all hosts can communicate with each others, all slices are active.
<p align="center">
    <img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/All_Active.jpeg"  width="80%" height="80%">
</p>

**Test bandwidth** of slices with ```iperf```
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/136bbd54b384e65e683ab4b19a875922e713f6b7/Slicing_scenarios/Normal_Bnd.png" width="60%" height="60%"><br>

In the Ryu controller, we have the capability to deactivate specific slices as needed, enabling us to allocate more bandwidth to other slices, such as during conference mode.
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/136bbd54b384e65e683ab4b19a875922e713f6b7/Slicing_scenarios/Deactive1.png" width="60%" height="60%"><br>
<center><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/Slice1_off.jpeg" alt="centered image" width="80%" height="80%"><center>

**Test bandwidth** of slices with ```iperf```
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/136bbd54b384e65e683ab4b19a875922e713f6b7/Slicing_scenarios/High_Bnd.png" width="60%" height="60%"><br>

**Test reachability** by running ```mininet> pingall```
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/7afd41dff1bf53df073bf008db7b0f2dd4c6cd6d/Slicing_scenarios/Pingall.png" width="60%" height="60%"><br>

We can notice that h5 and h6 are unable to communicate.
This process can be repeated for every slice.

The **Hacker mode** simulates a security breach scenario where all network slices, including essential IT services, are deliberately deactivated. It serves as a simulation tool to assess system resilience and response mechanisms under adverse conditions.
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/f0febde733e35a0a1e93dd06932f6191a1f50c48/Slicing_scenarios/Hack_mod.png" width="60%" height="60%"><br> 
<center><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/Hack_mod.jpeg" alt="centered image" width="80%" height="80%"><center> 


## Repository structure

1. **topology_slice.py**: This Python file defines the specific layout of our network. It includes 4 switches, 10 hosts and all the connection between them.

2. **ryu_controller.py**: Python file containing our SDN controller. It takes commands from users to control the activation or deactivation of network slices with our setup.

3. **gui.py**: This Python script creates a user-friendly interface for our project. It displays our network structure visually and allows users to manage slices using buttons.

4. **Slicing/total_activity.sh**: This shell script establishes the initial network setup where all hosts can communicate freely with each other.

5. **Slicing/slice#.sh**: These shell scripts represent different network slice configurations. Each script defines specific settings and restrictions for individual slices.

6. **Slicing/hacker_mod.sh**: This shell script simulates a security breach scenario by turning off all network slices, including IT services.

7. **Slicing_scenarios**: This directory contains images used in the project to illustrate various network slicing scenarios.

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
