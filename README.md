# MIMIC ROS driver
This ROS package serves as the driver for the Modular Intelligent Manufacturing and Inspection Cell (MIMIC) located at Nuclear AMRC. The cell aims to showcase the future of automated fabrication by combining:
* Robotic welding: A KUKA KR16 robot arm mounted on a 3-axis gantry for precise and efficient welding tasks. Both the KR16 and the gantry are controlled by a KRC4 extended controller, acting as the slave robot within the KUKA system.
* Robotic Inspection: A KUKA KR20 robot arm located on the floor for thorough and reliable inspection of fabricated parts. The KR20 is controlled by a separate KRC4 controller, designated as the master robot in the KUKA system. This KRC4 master also controls a turntable situated in the middle of the cell, used for precise positioning, turning, and tilting of workpieces.
  
![Full MIMIC.](/docs/media/full_mimic.png)
## Organisation
This repository is comprised of multiple ROS packages, each with different functionalities:

**mimic_support**: MIMIC support package, following [ROS-Industrial's robot support package format](https://wiki.ros.org/Industrial/Tutorials/WorkingWithRosIndustrialRobotSupportPackages)

    mimic_support
    ├── config
    ├── launch                 # contains load and test launch files for all components of the cell. 
    ├── meshes
    │   ├── collision          # *.stl files for each joint collision
    │   ├── visual             # *.dae files for each joint visualisation
    └── urdf

**mimic_driver**: MIMIC driver for setting up Kuka RSI communication and quick control of Kuka robots with ROS

    mimic_driver
    ├── config
    └── launch                 # contains load and test launch files for all components of the cell. 

## Setup
1. Install ROS and create a catkin workspace in your home directory:
```
mkdir -p ~/catkin_ws/src
```
2. Clone this repository into the catkin workpace's source folder (src):
```
git clone https://github.com/farisnafiah/mimic.git
```
3. Clone dependencies.

For controlling the MIMIC cell using ROS: 
* kuka_experimental: Make sure to clone my kuka_experimental repository [here](https://github.com/farisnafiah/kuka_experimental.git), instead of the official Kuka ROS experimental one. The branch that was tested most recently is _test/hw_interface_slave_

For connection with Twinality/Unity: 
* ros_unity
* ros_tcp_endpoint: [https://github.com/Unity-Technologies/ROS-TCP-Endpoint.git](https://github.com/Unity-Technologies/ROS-TCP-Endpoint.git)

4. Build it
```
mkdir -p ~/catkin_ws/
catkin_make
```
## Setup
You can get started with launching the simulator.
```
roslaunch mimic_driver mimic_driver.launch
```
With that running, you can move the joint angles using rqt.

 
