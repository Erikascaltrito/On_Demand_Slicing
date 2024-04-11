# On Demand SDN Slices in ComNetsEmu Project

This README provides an overview of the "On Demand SDN Slices in ComNetsEmu" project developed for the Networking 2 course at the University of Trento.

## Introduction

The objective is to implement a network slicing approach allowing dynamic activation and deactivation of network slices via CLI/GUI commands, the SDN controller used is a RYU. On-demand functionality means users can activate and deactivate different slices as needed. Slice descriptions should include identifiers for flows, topology, and percentage of link capacity for each slice.

## Project Description

We created a basic layout of an entire floor in the DICAM building. It includes 8 rooms: 2 offices on the north side, 2 on the east side, 2 on the west side, a conference room, and an IT services office. Those rooms are basically our slices, all with different services. 

<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/Mappa_Mesiano_completa.jpeg" width="200%" height="150%"><br>

### How it works 

At the beginning all hosts can communicate with each others, all slices are active.
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/All_Active.jpeg" width="100%" height="100%"><br> 
Test bandwidth:
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/Normal_Bnd" width="100%" height="100%"><br>

In the Ryu controller we can deactivate the slice we want to shut off to give the possibility of more bandwidth to others:
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/Deactive1" width="100%" height="100%"><br>
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/Slice1_off.jpeg" width="100%" height="100%"><br>
Test bandwidth:
<br><img src="https://github.com/Erikascaltrito/On_Demand_Slicing/blob/42b61aaf5cbb420cac25ff4b6c7ebffad6af1df6/Slicing_scenarios/High_BND" width="100%" height="100%"><br>
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
2. Navigate to the project directory: `cd On_Demand_SDN_Slices`

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
