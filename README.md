# SolarTracker
By Valen Qiu, contact: valen.qiu@connect.polyu.hk

### Preface
OneDrive Folder: https://connectpolyu-my.sharepoint.com/:f:/g/personal/20083971d_connect_polyu_hk/EpspQ4KWl9xGvHiiFKB0CRsBsq69lWfJ5u-4mAkCwqDmDQ
Before using it, please download the `VNC viewer` and `remote. it` (or use `remote.it online`) on your computer and sign up/in an account.

<div align=center>
<img src="IMG/SolarTracker.png" width="300px">
</div>

## I.	Connect methods
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

#### 2. Internet

To connect the raspberry conveniently, you can sign up for a VNC account by email and add the raspberry pi to your Team. After doing this, you can directly connect to your raspberry pi, you do not need to be on the same network. As shown in the image. The detail method can be searched online.

<img src="IMG/internet1.png" width="400px">

#### 3. Remote.it
Besides, it is highly recommended to use Remote.it to detect the internet connection. Besides, it can also get the ethernet IP address. 

<img src="IMG/internet2.png" width="400px">

With the ethernet IP address, you can repeat step 1.4, but input this ethernet IP address, you can also remotely connect the raspberry pi, and no need to connect to the same local network.

<img src="IMG/internet3.png" height="200px">

Link for the video tutorial on applying Remote.it: https://www.youtube.com/watch?v=_B8E1dE5kW4&t=167s. 

Some steps for setting up Remote.it are shown below:

<img src="IMG/internet4.png" height="300px"><img src="IMG/internet5.png" height="300px">

## V. Functions: Scanning, Angle Control, Camera...
After accessing the raspberry pi, click the system_4.0.py on the desktop, and run it.
Remarks: please use Geany to run the code. The system is developed under the Geany, and cannot guarantee that other programmers will not report errors.

<img src="IMG/function1.png" weight="300px">

Since the tracker may need further improvement, the code is not encapsulated into an exe.

<img src="IMG/function2.png" weight="300px">

fter running the program, GUI will come out.

<img src="IMG/function3.png" weight="300px">

#### 1. User manual for the GUI:

<img src="IMG/function4.png" height="200px">

##### SCAN

<img src="IMG/function5.png" height="200px">

Click the `SCAN` button, a window will come out. Click OK for starting, and click Cancel to stop it. The Solar Tracker will start with default settings (10 degrees of Zenith and 6 degrees of Azimuth for each step, scan time is 60s (for testing, only 2s). 

<img src="IMG/function6.png" height="200px">

Click the `STOP` button can quit the scanning mode after the initialization. When it is in the scanning mode, other functions will be forbidden.
“Break Time” is not available now. Input the scan time to adjust the time for scanning (input number should be integer and larger than 0), input the azimuth/zenith interval to adjust the angel interval of each step (azimuth: integer in range 0-360, which preferably 360 can be divisible by the integer; zenith: integer in range 0-90, which preferably 90 can be divisible by the integer).
After inputting the numbers for adjustment, click “SCAN” again, the Solar Tracker will start with the new settings. You can input a specific one/two, and others will keep in the default setting.
The initialization angle is Zenith: 90°, Azimuth: 0°, see the definition of zenith and azimuth in part II.

##### MANUAL

Click the `MANUAL` button, wait it for the initialization, those four buttons on the right side of the GUI will be available, and the Solar Tracker can be controlled by those buttons. Each click of the button will let the Solar Tracker move 2° in the corresponding direction.

<img src="IMG/function7.png" height="200px">

When the Solar Tracker is in the manual control mode, other functions will be forbidden, you can click the `MANUAL` button again to quit the mode, and other functions will become available.


##### CUSTOM

Type the angle you want in the `Angle` input panel, and click the `CUSTOM` button, the Solar Tracker will turn to the angle. However, the user must enter both azimuth and zenith to set the custom angle, otherwise, it will ask you to input an angle and end this function.

##### RESET

Click the `RESET` button will clean all the input and the setting will become back to the default mode.

`Remark: After testing, please go to the code, and change the scan time to 60s for each step (now is 2s).`

#### 2. Camera

The fisheye camera used here is for simulating the sensor, in case you want to access the image of the camera, here is the way to do it.

In the GUI, click the `SCAN IP ADDRESS`, and wait for a while. It will scan the IP address and MAC address of devices which connected to the local network. 

<img src="IMG/function7.png" height="200px">


