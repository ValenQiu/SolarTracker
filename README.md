# SolarTracker
By Valen Qiu, contact: valen.qiu@connect.polyu.hk

### Preface
OneDrive Folder: https://connectpolyu-my.sharepoint.com/:f:/g/personal/20083971d_connect_polyu_hk/EpspQ4KWl9xGvHiiFKB0CRsBsq69lWfJ5u-4mAkCwqDmDQ
Before using it, please download the `VNC viewer` and `remote. it` (or use `remote.it online`) on your computer and sign up/in an account.

<div align=center>
<img src="IMG/SolarTracker.png" width="300px">
</div>

## I.	Connect method
  1.	Direct connection: 
    Connect the raspberry pi with the monitor, mouse, and keyboard
  2.	Remote connection via local network: 
    Connect your computer and raspberry pi to the same local network, download & open the VNC viewer and connect it by inputting the IP address of raspberry pi; or connect the computer to the switch in the plastic case (use cable), and do the above step
  3.	Remote connection via Internet: 
    Find a way to access the raspberry pi first, open the VNC server, sign in with your VNC account, and add it to your Team. After finishing it, you can remote connect the raspberry pi through any internet environment (if and only if the raspberry pi is turned on and connected to the internet, Lol)

## II.	Solar Tracker Introduction
The solar tracker is developed based on Raspberry Pi 4B, and the operating system is Raspbian OS (Linux). The raspberry pi is powered up by a rechargeable lithium battery, allowing the device to work for around 2-3 hours even when the power goes out. 

All power and network are provided by the white plastic box connected to the tracker. A switch and router (very old, provided by Mr. Yuen KO, not stable, lol) are placed inside the box for networking, and the IP address is fixed (depends on which port you connect). 

There are only two servo motors as actuators; one is a 360-degree rotatable 25kg*cm servo motor for controlling the azimuth angle (θ). The other is a 180-degree rotatable 60kg*cm servo motor (the torque is large because the camera/sensor is heavy) for controlling zenith angle (φ). Both motors have a certain waterproof ability. 

<div align=center>
<img src="IMG/angle.png" height="150px"><img src="IMG/rotation.jpg" height="150px">
</div>

The tracker has a certain waterproof ability, but it has not been specifically tested, and it is recommended not to use it in extreme weather or rain. If it must be used in the above weather, it is recommended to take additional waterproof measures.

## III.	Cables connection
The cables are shown in below images. To use it, please connect the wires following the right hand side image, which just need to connect the ethernet cable and power source with the tracker.

<div align=center>
<img src="IMG/cable1.png" height="250px"><img src="IMG/cable2.jpg" height="250px">
</div>

## IV.	Connect Solar Tracker
#### 1.	Local Network
1.1.	Connect a monitor to raspberry pi and connect it to the internet. You can also connect your computer to the switch inside the box (highly recommended so that you can know whether the router is working normally, if the router is not well, reboot it until your computer can connect to the Internet). Click the terminal icon (or use `Ctrl + Alt + T`) to open the terminal.

<img src="IMG/terminal1.png" width="300px">

Input:
```
ifconfig
```
The IP address will appear; in this case, the IP address is 192.168.1.23

<img src="IMG/terminal2.png" width="300px">

1.2.	Open the `VNC viewer`.

<img src="IMG/vnc1.png" width="100px">

1.3.	Right-click and choose `“New Connection”`.

<img src="IMG/vnc2.png" width="300px">

1.4.	Input the IP address you get (192.168.1.23 in this case) to the VNC Server, and then click OK. If you want to specify the connection, you can input the name you wish to in the Name.

<img src="IMG/vnc3.png" width="300px">

As shown in the image below, a new connection has been successfully created.

<img src="IMG/vnc4.png" width="300px">

1.5.	Double-click the connection icon you just created, input the user name and password into the window, and click OK.
```
Username: pi
Password: 0
```
<img src="IMG/vnc5.png" width="300px">

1.6.	Connect successfully!

<img src="IMG/vnc6.png" width="300px">

