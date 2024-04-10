# On Demand SDN Slices in ComNetsEmu Project

This README provides an overview of the "On Demand SDN Slices in ComNetsEmu" project developed for the Networking 2 course.

## Introduction

The objective is to implement a network slicing approach allowing dynamic activation and deactivation of network slices via CLI/GUI commands, the SDN controller used is a RYU. On-demand functionality means users can activate and deactivate various slices as needed. Slice descriptions, possibly in template form, should include identifiers for flows, topology, and percentage of link capacity for each slice.

## Project Description

In traditional networking setups, resources are often statically allocated, leading to underutilization and lack of flexibility. SDN introduces the concept of network slicing, where network resources are dynamically allocated based on application requirements. Our project leverages ComNetsEmu, a network emulation platform, to simulate SDN environments and implement on-demand network slicing.

#How it works 
\begin{figure}[htbp]
\begin{center}

\caption{default}
\label{default}
\end{center}
\end{figure}



## Features

- **Dynamic Resource Allocation**: Utilize SDN principles to dynamically allocate network resources based on application demands.
- **Flexible Networking**: Enable the creation of multiple network slices catering to different application requirements.
- **ComNetsEmu Integration**: Utilize the capabilities of ComNetsEmu for realistic network emulation and testing.

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
