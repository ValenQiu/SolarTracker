import tkinter
import tkinter as tk
from tkinter import ttk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tkinter import messagebox
from PTZ import PTZ
from Sun import SUN
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GUI:
    """
    The _root is the class object for the GUI
    the _ptz is the class object for the PTZ controller
    The _sun is the class object for the Sun updating function
    """
    _root = None
    _ptz = None
    _sun = None

    # Serial Communication
    entry_COM = None
    entry_baud = None
    button_connect = None
    button_disconnect = None

    # Control Panel Buttons
    button_up_left = None
    button_up = None
    button_up_right = None
    button_left = None
    button_stop = None
    button_right = None
    button_down_left = None
    button_down = None
    button_down_right = None

    # Set Joint Speeds
    tilt_speed = None
    pan_speed = None
    tilt_speed_label = None
    pan_speed_label = None

    # PTZ Joint Positions
    pan_pos = 0.0
    tilt_pos = 0.0

    # PTZ Set Position
    enrty_tilt = None
    entry_pan = None

    # Global variable to track if the button is being pressed
    is_button_pressed = False

    # Flag for tracking the sun
    sun_track_flag = False

    # Buttons of Sun Tracking
    track_on = None
    track_off = None

    ##################################################################################################
    # Class Initialization
    ##################################################################################################
    def __init__(self):
        # Create the main application window
        self._root = tk.Tk()
        self._root.title("Solar Tracker")
        self._root.geometry('960x420+50+150')  # Set the window size
        self._sun = SUN()
        self.load_GUI()
        self.update_solar_position()
        # if self._ptz is not None:
        #     self.update_ptz_position()
        # Create the animation
        # self.ani = FuncAnimation(self._sun.fig, self._sun.update, interval=self._sun.interval, blit=True)
        # for testing
        # num_frames = len(self._sun.get_solar_positions_for_a_day())
        # self.ani = FuncAnimation(self._sun.fig, self._sun.update_a_day, frames=num_frames, interval=self._sun.interval, blit=True)

        self._root.mainloop()

    ##################################################################################################
    # Communication Click Events
    ##################################################################################################
    def connect_button_click(self):
        COM = self.entry_COM.get()
        Baud = self.entry_baud.get()
        # Convert the baud rate to an integer
        try:
            baud_rate = int(Baud)
        except ValueError:
            # Handle the case where the baud rate is not a valid integer
            print("Invalid baud rate. Using default value of 2400.")
            baud_rate = 2400

        # Create the PTZ object with the user-provided values
        self._ptz = PTZ(COM, baud_rate)
        port_state = self._ptz._check
        if port_state == True:
            self.button_connect['state'] = 'disable'
            self.button_disconnect['state'] = 'normal'
            self.enable_frames()
            # self.update_solar_position()
            self.track_off['state'] = 'disable'

        else:
            messagebox.showinfo("Connection Error!", "Can not connect to the device!")

    def disconnect_button_click(self):
        self._ptz.unconnect()
        port_state = self._ptz._check
        # print(port_state)
        if port_state == False:
            self.button_connect['state'] = 'normal'
            self.button_disconnect['state'] = 'disable'
            self.disable_all_frames()
            messagebox.showinfo("Disconnect Successfully!", "Device has been disconnected!")
        else:
            messagebox.showinfo("Disconnect Failed!", "Device has not been disconnected!")

    def connect_ptz(self):
        self._ptz = PTZ()

    def disable_frame(self, frame):
        for child in frame.winfo_children():
            child.config(state='disable')

    def disable_all_frames(self):
        frames = self._root.winfo_children()
        for frame in frames:
            # print(frame.winfo_name())
            if frame.winfo_name() != 'communication':
                if frame.winfo_name() == 'panels':
                    subframes = frame.winfo_children()
                    for subframe in subframes:
                        for child in subframe.winfo_children():
                            child.config(state='disable')
                elif frame.winfo_name() == 'sun':
                    subframes = frame.winfo_children()
                    for subframe in subframes:
                        for child in subframe.winfo_children():
                            child.config(state='disable')
                else:
                    for child in frame.winfo_children():
                        child.config(state='disable')

    def enable_frames(self):
        frames = self._root.winfo_children()
        for frame in frames:
            # print(frame.winfo_name())
            if frame.winfo_name() != 'communication':
                if frame.winfo_name() == 'panels':
                    subframes = frame.winfo_children()
                    for subframe in subframes:
                        for child in subframe.winfo_children():
                            child.config(state='normal')
                elif frame.winfo_name() == 'sun':
                    subframes = frame.winfo_children()
                    for subframe in subframes:
                        for child in subframe.winfo_children():
                            child.config(state='normal')
                else:
                    for child in frame.winfo_children():
                        child.config(state='normal')
        self.track_off['state'] = 'disable'

    ##################################################################################################
    # Controller Click Events
    ##################################################################################################
    def stop_click(self):
        if self._ptz is not None:
            self._ptz.stop()
            print("Stop")
        else:
            print("Error: self._ptz is None")

    def up_left_pressed(self, event):
        self.is_button_pressed = True
        print("Button UP-LEFT is being pressed!")
        self._ptz.move_to_up_left()

    def up_pressed(self, event):
        self.is_button_pressed = True
        print("Button UP is being pressed!")
        self._ptz.move_to_up()

    def up_right_pressed(self, event):
        self.is_button_pressed = True
        print("Button UP-RIGHT is being pressed!")
        self._ptz.move_to_up_right()

    def left_pressed(self, event):
        self.is_button_pressed = True
        print("Button LEFT is being pressed!")
        self._ptz.move_to_left()

    def right_pressed(self, event):
        self.is_button_pressed = True
        print("Button RIGHT is being pressed!")
        self._ptz.move_to_right()

    def down_left_pressed(self, event):
        self.is_button_pressed = True
        print("Button DOWN-LEFT is being pressed!")
        self._ptz.move_to_down_left()

    def down_pressed(self, event):
        self.is_button_pressed = True
        print("Button DOWN is being pressed!")
        self._ptz.move_to_down()

    def down_right_pressed(self, event):
        self.is_button_pressed = True
        print("Button DOWN-RIGHT is being pressed!")
        self._ptz.move_to_down_right()

    def button_released(self, event):
        self.is_button_pressed = False
        self._ptz.stop()
        print("Button is released!")

    ##################################################################################################
    # Set Speed
    ##################################################################################################
    def set_speed(self):
        tilt_speed = self.tilt_speed.get()
        pan_speed = self.pan_speed.get()
        # print("Tilt Speed: ", tilt_speed)
        # print("Pan Speed: ", pan_speed)
        # print("Pan Speed (hex): ", chr(pan_speed))
        tilt_speed = chr(tilt_speed)
        pan_speed = chr(pan_speed)
        self._ptz.set_speed(pan_speed, tilt_speed)

    ##################################################################################################
    # Query position
    ##################################################################################################
    def query_tilt_position(self):
        self._ptz.query_tilt_position()
        position = self._ptz._position['TILT']
        self.tilt_pos.set(position)
        print("Tilt Position: ", position)

    def query_pan_position(self):
        self._ptz.query_pan_position()
        position = self._ptz._position['PAN']
        self.pan_pos.set(position)
        print("Pan Position: ", position)

    ##################################################################################################
    # Set Position
    ##################################################################################################
    def set_tilt_click(self):
        tilt_pos = self.enrty_tilt.get()
        # print("tilt_pos get: ", tilt_pos)
        # print("Type: ", type(tilt_pos))
        tilt_pos = float(tilt_pos)
        # print("tilt_pos get: ", tilt_pos)
        # print("Type: ", type(tilt_pos))
        self._ptz.set_tilt_position(tilt_pos)

    def set_pan_click(self):
        pan_pos = self.entry_pan.get()
        # print("tilt_pos get: ", tilt_pos)
        # print("Type: ", type(tilt_pos))
        pan_pos = float(pan_pos)
        # print("tilt_pos get: ", tilt_pos)
        # print("Type: ", type(tilt_pos))
        self._ptz.set_pan_position(pan_pos)

    ##################################################################################################
    # Tracking Sun
    ##################################################################################################
    def track_sun_on(self):
        self.sun_track_flag = True
        self.track_on['state'] = 'disable'
        self.track_off['state'] = 'normal'

    def track_sun_off(self):
        self.sun_track_flag = False
        self.track_off['state'] = 'disable'
        self.track_on['state'] = 'normal'

    ##################################################################################################
    # GUI Loading
    ##################################################################################################
    def load_GUI(self):
        self.load_communication_frame()
        self.load_button_panel()
        self.load_position_frame()
        self.load_query_frame()
        self.load_scan_frame()
        self.load_sun_position()

    def load_communication_frame(self):
        # Serial Communication Parameters Frame
        # input parameters for serial communication
        frame_c = tkinter.LabelFrame(self._root, text="Communication", name='communication')
        frame_c.place(x=15, y=5, width=300, height=100)
        # COM port setting
        label_port = tk.Label(frame_c, text="Port Name:")
        label_port.grid(row=0, column=0, padx=10, pady=(10, 2), sticky="w")

        # Enter COM port number
        self.entry_COM = tk.Entry(frame_c, width=10)
        self.entry_COM.grid(row=1, column=0, padx=10, pady=(2, 10))
        self.entry_COM.insert(0, 'COM3')

        # Baud rate setting
        label_baud = tk.Label(frame_c, text="Baud Rate:")
        label_baud.grid(row=0, column=1, padx=10, pady=(10, 2), sticky="w")

        # Enter baud rate number
        self.entry_baud = tk.Entry(frame_c, width=10)
        self.entry_baud.grid(row=1, column=1, padx=10, pady=(2, 10))
        self.entry_baud.insert(0, 2400)

        # Create a button to connect
        self.button_connect = tk.Button(frame_c, text="Connect", bg="lightblue", width=10, command=self.connect_button_click)
        self.button_connect.grid(row=0, column=2, columnspan=2, padx=10, pady=1)

        # Create a button to disconnect
        self.button_disconnect = tk.Button(frame_c, text="Disconnect", bg="lightblue", width=10, state="disabled", command=self.disconnect_button_click)
        self.button_disconnect.grid(row=1, column=2, columnspan=2, padx=10, pady=1)

    def load_button_panel(self):
        frame_b = tkinter.LabelFrame(self._root, text="Control Panel", name='panels')
        frame_b.place(x=15, y=105, width=300, height=300)

        # Create a subframe for the buttons
        frame_buttons = tk.Frame(frame_b, name='buttons')
        frame_buttons.grid(row=0, column=0, padx=(45, 3), pady=(3, 3))

        # Create the up-left button
        arrow_up_left = tk.PhotoImage(file='pic/arrow_315.png')
        arrow_up_left = arrow_up_left.subsample(10, 10)
        self.button_up_left = tk.Button(frame_buttons, image=arrow_up_left)
        self.button_up_left.bind("<Button-1>", self.up_left_pressed)
        self.button_up_left.bind("<ButtonRelease-1>", self.button_released)
        self.button_up_left.grid(row=0, column=0, padx=(3, 3), pady=(3, 3))
        self.button_up_left.image = arrow_up_left

        # Create the up button
        arrow_up = tk.PhotoImage(file='pic/arrow_up.png')
        arrow_up = arrow_up.subsample(10, 10)
        self.button_up = tk.Button(frame_buttons, image=arrow_up)
        self.button_up.bind("<Button-1>", self.up_pressed)
        self.button_up.bind("<ButtonRelease-1>", self.button_released)
        self.button_up.grid(row=0, column=1, padx=(3, 3), pady=(3, 3))
        self.button_up.image = arrow_up

        # Create the up-right button
        arrow_up_right = tk.PhotoImage(file='pic/arrow_45.png')
        arrow_up_right = arrow_up_right.subsample(10, 10)
        self.button_up_right = tk.Button(frame_buttons, image=arrow_up_right)
        self.button_up_right.bind("<Button-1>", self.up_right_pressed)
        self.button_up_right.bind("<ButtonRelease-1>", self.button_released)
        self.button_up_right.grid(row=0, column=2, padx=(3, 3), pady=(3, 3))
        self.button_up_right.image = arrow_up_right

        # Create the left button
        arrow_left = tk.PhotoImage(file='pic/arrow_left.png')
        arrow_left = arrow_left.subsample(10, 10)
        self.button_left = tk.Button(frame_buttons, image=arrow_left)
        self.button_left.bind("<Button-1>", self.left_pressed)
        self.button_left.bind("<ButtonRelease-1>", self.button_released)
        self.button_left.grid(row=1, column=0, padx=(3, 3), pady=(3, 3))
        self.button_left.image = arrow_left

        # Create the stop button
        arrow_stop = tk.PhotoImage(file='pic/stop.png')
        arrow_stop = arrow_stop.subsample(10, 10)
        self.button_stop = tk.Button(frame_buttons, image=arrow_stop, command=self.stop_click)
        self.button_stop.grid(row=1, column=1, padx=(3, 3), pady=(3, 3))
        self.button_stop.image = arrow_stop

        # Create the right button
        arrow_right = tk.PhotoImage(file='pic/arrow_right.png')
        arrow_right = arrow_right.subsample(10, 10)
        self.button_right = tk.Button(frame_buttons, image=arrow_right)
        self.button_right.bind("<Button-1>", self.right_pressed)
        self.button_right.bind("<ButtonRelease-1>", self.button_released)
        self.button_right.grid(row=1, column=2, padx=(3, 3), pady=(3, 3))
        self.button_right.image = arrow_right

        # Create the down left button
        arrow_down_left = tk.PhotoImage(file='pic/arrow_225.png')
        arrow_down_left = arrow_down_left.subsample(10, 10)
        self.button_down_left = tk.Button(frame_buttons, image=arrow_down_left)
        self.button_down_left.bind("<Button-1>", self.down_left_pressed)
        self.button_down_left.bind("<ButtonRelease-1>", self.button_released)
        self.button_down_left.grid(row=2, column=0, padx=(3, 3), pady=(3, 3))
        self.button_down_left.image = arrow_down_left

        # Create the down button
        arrow_down = tk.PhotoImage(file='pic/arrow_down.png')
        arrow_down = arrow_down.subsample(10, 10)
        self.button_down = tk.Button(frame_buttons, image=arrow_down)
        self.button_down.bind("<Button-1>", self.down_pressed)
        self.button_down.bind("<ButtonRelease-1>", self.button_released)
        self.button_down.grid(row=2, column=1, padx=(3, 3), pady=(3, 3))
        self.button_down.image = arrow_down

        # Create the down right button
        arrow_down_right = tk.PhotoImage(file='pic/arrow_135.png')
        arrow_down_right = arrow_down_right.subsample(10, 10)
        self.button_down_right = tk.Button(frame_buttons, image=arrow_down_right)
        self.button_down_right.bind("<Button-1>", self.down_right_pressed)
        self.button_down_right.bind("<ButtonRelease-1>", self.button_released)
        self.button_down_right.grid(row=2, column=2, padx=(3, 3), pady=(3, 3))
        self.button_down_right.image = arrow_down_right

        # Create a subframe for the sliders
        frame_sliders = tk.Frame(frame_b, name='sliders')
        frame_sliders.grid(row=1, column=0, padx=(3, 3), pady=(3, 3))

        # Create a label for the tilt speed
        label_tilt = tk.Label(frame_sliders, text='Tilt Speed: ')
        label_tilt.grid(row=0, column=0, padx=(3, 3), pady=(3, 3), sticky="e")

        # Create the slider for tilt speed control
        self.tilt_speed = tk.Scale(frame_sliders, from_=10, to=63, orient=tk.HORIZONTAL, length=75, showvalue=0)
        self.tilt_speed.set(31)  # default value
        self.tilt_speed.grid(row=0, column=1, padx=(3, 3), pady=(3, 3), sticky="w")

        self.tilt_speed_label = tk.Label(frame_sliders, text=self.tilt_speed.get())
        self.tilt_speed_label.grid(row=0, column=2, padx=(3, 3), pady=(3, 3), sticky="w")

        # Create a label for the pan speed
        label_pan = tk.Label(frame_sliders, text='Pan Speed: ')
        label_pan.grid(row=1, column=0, padx=(3, 3), pady=(3, 3), sticky="e")

        # Create the slider for pan speed control
        self.pan_speed = tk.Scale(frame_sliders, from_=10, to=63, orient=tk.HORIZONTAL, length=75, showvalue=0)
        self.pan_speed.set(31)  # default value
        self.pan_speed.grid(row=1, column=1, padx=(3, 3), pady=(3, 3), sticky="w")

        self.pan_speed_label = tk.Label(frame_sliders, text=self.pan_speed.get())
        self.pan_speed_label.grid(row=1, column=2, padx=(3, 3), pady=(3, 3), sticky="w")

        # Create a button to set the speeds
        set_speed = tk.Button(frame_sliders, text="Set", bg="lightblue", width=5, command=self.set_speed)
        set_speed.grid(row=0, column=3, rowspan=2, padx=(10, 3), pady=(3, 3), sticky="w")

        self.disable_frame(frame_buttons)
        self.disable_frame(frame_sliders)

    def load_position_frame(self):
        frame_pos = tkinter.LabelFrame(self._root, text="Set PTZ Position", name='position')
        frame_pos.place(x=330, y=125, width=300, height=110)

        # Create a label
        label_tilt_pos = tk.Label(frame_pos, text='Tilt Position (0-100): ')
        label_tilt_pos.grid(row=0, column=0, padx=(3, 3), pady=3, sticky="w")

        # Enter Tilt Position
        self.enrty_tilt = tk.Entry(frame_pos, width=5)
        self.enrty_tilt.grid(row=0, column=1, padx=10, pady=3, sticky="e")
        self.enrty_tilt.insert(0, '0')

        # Create a button to set the position
        set_tilt = tk.Button(frame_pos, text="Go", bg="lightblue", width=8, command=self.set_tilt_click)
        set_tilt.grid(row=0, column=3, padx=(3, 3), pady=3, sticky="e")

        # Create a label
        label_pan_pos = tk.Label(frame_pos, text='Pan Position (0-360): ')
        label_pan_pos.grid(row=1, column=0, padx=(3, 3), pady=3, sticky="w")

        # Enter Pan Position
        self.entry_pan = tk.Entry(frame_pos, width=5)
        self.entry_pan.grid(row=1, column=1, padx=10, pady=3, sticky="e")
        self.entry_pan.insert(0, '0')

        # Create a button to set the position
        set_pan = tk.Button(frame_pos, text="Go", bg="lightblue", width=8, command=self.set_pan_click)
        set_pan.grid(row=1, column=3, padx=(3, 3), pady=3)

        self.disable_frame(frame_pos)

    def load_query_frame(self):
        frame_q = tkinter.LabelFrame(self._root, text="Query PTZ Position", name='query')
        frame_q.place(x=330, y=5, width=300, height=100)

        # Create a label
        label_tilt_q = tk.Label(frame_q, text='Query Tilt Position: ')
        label_tilt_q.grid(row=0, column=0, padx=(3, 3), pady=3, sticky="w")

        self.tilt_pos = tk.StringVar()
        self.tilt_pos.set(0.0)

        label_tilt_pos = tk.Label(frame_q, textvariable=self.tilt_pos)
        label_tilt_pos.grid(row=0, column=1, padx=10, pady=3, sticky="e")

        # Create a button to query the position
        q_tilt = tk.Button(frame_q, text="Query", bg="lightblue", width=8, command=self.query_tilt_position)
        q_tilt.grid(row=0, column=3, padx=(3, 3), pady=3, sticky="e")

        # Create a label
        label_pan_pos = tk.Label(frame_q, text='Query Pan Position: ')
        label_pan_pos.grid(row=1, column=0, padx=(3, 3), pady=3, sticky="w")

        # Create a variable to hold the pan position
        self.pan_pos = tk.StringVar()
        self.pan_pos.set(0.0)

        label_pan_pos = tk.Label(frame_q, textvariable=self.pan_pos)
        label_pan_pos.grid(row=1, column=1, padx=10, pady=3, sticky="e")

        # Create a button to set the position
        q_pan = tk.Button(frame_q, text="Query", bg="lightblue", width=8, command=self.query_pan_position)
        q_pan.grid(row=1, column=3, padx=(3, 3), pady=3, sticky="e")

        self.disable_frame(frame_q)

    def load_scan_frame(self):
        frame_s = tkinter.LabelFrame(self._root, text="Scan", name='scan')
        frame_s.place(x=330, y=250, width=300, height=155)

        # Create a label
        scan_time_label = tk.Label(frame_s, text='Scan Time (s): ')
        scan_time_label.grid(row=0, column=0, padx=(3, 3), pady=3, sticky="w")

        # Enter Scan Time
        scan_time = tk.Entry(frame_s, width=10)
        scan_time.grid(row=0, column=1, padx=10, pady=3, sticky="e")
        scan_time.insert(0, '5')

        # Create a label
        label_tilt_t = tk.Label(frame_s, text='Tilt Interval (angle): ')
        label_tilt_t.grid(row=1, column=0, padx=(3, 3), pady=3, sticky="w")

        # Enter Tilt Position
        tilt_t = tk.Entry(frame_s, width=10)
        tilt_t.grid(row=1, column=1, padx=10, pady=3, sticky="e")
        tilt_t.insert(0, '5')

        # Create a label
        label_pan_t = tk.Label(frame_s, text='Pan Interval (angle): ')
        label_pan_t.grid(row=2, column=0, padx=(3, 3), pady=3, sticky="w")

        # Enter Pan Position
        pan_t = tk.Entry(frame_s, width=10)
        pan_t.grid(row=2, column=1, padx=10, pady=3, sticky="e")
        pan_t.insert(0, '5')

        # Create a button to save the setting
        set = tk.Button(frame_s, text="Set", bg="lightblue", width=5, command=self.on_button_click())
        set.grid(row=3, column=0, padx=(3, 3), pady=5)

        # Create a button to start the scanning
        start_scan = tk.Button(frame_s, text="Start Scanning", bg="lightblue", width=15, command=self.on_button_click())
        start_scan.grid(row=3, column=1, padx=(3, 3), pady=5)

        self.disable_frame(frame_s)

    def load_sun_position(self):
        frame_sun = tkinter.LabelFrame(self._root, text="Sun", name='sun')
        frame_sun.place(x=645, y=5, width=300, height=400)

        # Create a subframe for the plot
        frame_plot = tk.Frame(frame_sun, name='plot')
        frame_plot.grid(row=0, column=0, padx=(5, 5), pady=(10, 10))
        # Create the canvas to display the animation
        canvas = FigureCanvasTkAgg(self._sun.fig, master=frame_plot)
        canvas.draw()
        canvas.get_tk_widget().configure(width=290, height=290)
        canvas.get_tk_widget().pack()

        # Create a subframe for the buttons
        frame_on_off = tk.Frame(frame_sun, name='state')
        frame_on_off.grid(row=1, column=0, padx=(3, 3), pady=(10, 10))

        label_track = tk.Label(frame_on_off, text='Track')
        label_track.grid(row=0, column=0, padx=(3, 3), pady=3, sticky="w")

        self.track_on = tk.Button(frame_on_off, text="ON", bg="lightblue", width=5, command=self.track_sun_on)
        self.track_on.grid(row=0, column=1, padx=(3, 3), pady=5)

        self.track_off = tk.Button(frame_on_off, text="OFF", bg="lightblue", width=5,state="disabled", command=self.track_sun_off)
        self.track_off.grid(row=0, column=2, padx=(3, 3), pady=5)

        self.disable_frame(frame_on_off)

    def on_button_click(self):
        # user_input = entry_COM.get()
        # if user_input:
        #     label_result.config(text=f"Hello, {user_input}!")
        # else:
        #     messagebox.showwarning("Input Error", "Please enter your name.")
        return 0

    # functions that always active
    def update_solar_position(self):
        self._sun.update(0)
        self._root.after(self._sun.interval, self.update_solar_position)

        print(self.sun_track_flag)
        if self._ptz is None:
            return
        if self.sun_track_flag is not False:
            print("it should track now")
            zenith, azimuth = self._sun.get_solar_position()
            zenith = float(zenith)
            azimuth = float(azimuth)
            print("Zebutg: ", zenith)
            print("Azimuth: ", azimuth)
            self._ptz.set_pan_position(azimuth)
            self._ptz.set_tilt_position(zenith)
        else:
            return

    # def track_sun(self):
    #     print(self.sun_track_flag)
    #     if self.sun_track_flag is not False:
    #         print("it should track now")
    #         zenith, azimuth = self._sun.get_solar_position()
    #         zenith = float(zenith)
    #         azimuth = float(azimuth)
    #         self._ptz.set_pan_position(azimuth)
    #         self._ptz.set_tilt_position(zenith)
    #     else:
    #         return
    #     self._root.after(self._sun.interval, self.track_sun)


    # def update_ptz_position(self):
    #     tilt = self._ptz.query_tilt_position()
    #     pan = self._ptz.query_pan_position()
    #     self._sun.ptz_tilt = tilt
    #     self._sun.ptz_pan = pan
    #     self._sun.update_ptz(0)
    #     self._root.after(self._sun.interval, self.update_ptz_position)


if __name__ == "__main__":
    gui = GUI()