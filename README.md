# SolarTracker

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

