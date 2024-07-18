import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
import time
import pvlib
import pytz
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


class SUN:
    # For Sun Data
    latitude = 22.30327  # HK纬度
    longitude = 114.17933  # HK经度
    altitude = 35  # HK海拔
    timezone = 'Asia/Hong_Kong'  # 时区
    start_date = '2024-06-01'

    # for animation
    # Animation parameters
    interval = 10000  # Interval between frames in milliseconds (0.1 seconds)

    # Initialize the figure and 3D axes
    fig = plt.figure(figsize=(5, 5), dpi=75)
    ax = fig.add_subplot(111, projection='3d')

    # Set the background to be transparent
    fig.patch.set_alpha(0.0)

    # Show the positive and negative x-y-z axes and hide the grips
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(-1, 1)
    ax.set_zlim3d(0, 1)
    ax.set_xlabel('West-East')
    ax.set_ylabel('North-South')
    ax.set_zlabel('Zenith')
    ax.set_title('Solar Position')
    ax.grid(False)

    # Add thick, semi-transparent, straight lines for the x, y, and z axes
    ax.plot([-1, 1], [0, 0], [0, 0], 'g-', alpha=0.5, linewidth=3, zorder=1)
    ax.plot([0, 0], [-1, 1], [0, 0], 'b-', alpha=0.5, linewidth=3, zorder=1)
    ax.plot([0, 0], [0, 0], [0, 1], 'r-', alpha=0.5, linewidth=3, zorder=1)

    # Initialize the PTZ angles
    ptz_tilt = 0
    ptz_pan = 0

    # Initialize the plot elements
    sun, = ax.plot([], [], [], 'ro', markersize=10, label='Sun')
    azimuth_line, = ax.plot([], [], [], 'b-', linewidth=2, label='Azimuth')
    zenith_line, = ax.plot([], [], [], 'g-', linewidth=2, label='Zenith')

    # ptz_line, = ax.plot([], [], [], 'k', linewidth=4, label='PTZ Line')
    # ptz, = ax.plot([], [], [], 'ko', markersize=10, label='PTZ')

    def get_solar_position(self):
        now = datetime.datetime.now(pytz.timezone(self.timezone))
        solar_position = pvlib.solarposition.get_solarposition(
            time=now,
            latitude=self.latitude,
            longitude=self.longitude,
            altitude=self.altitude
        )
        zenith = solar_position['zenith'].values[0]
        azimuth = solar_position['azimuth'].values[0]
        print("current time: ", now)
        return zenith, azimuth

    def update(self, frame):
        zenith, azimuth = self.get_solar_position()
        x = np.sin(np.radians(zenith)) * np.cos(np.radians(azimuth))
        y = np.sin(np.radians(zenith)) * np.sin(np.radians(azimuth))
        z = np.cos(np.radians(zenith))
        self.sun.set_data_3d(x, y, z)
        self.azimuth_line.set_data_3d([0, x], [0, y], [0, 0])
        self.zenith_line.set_data_3d([0, x], [0, y], [0, z])

        # # Update the PTZ
        # self.ptz, self.ptz_line = self.update_ptz(frame)

        print(f"Solar Zenith Angle: {zenith:.2f} degrees")
        print(f"Solar Azimuth Angle: {azimuth:.2f} degrees")
        print('-' * 40)
        # return self.sun, self.azimuth_line, self.zenith_line, self.ptz, self.ptz_line
        return self.sun, self.azimuth_line, self.zenith_line

    # def update_ptz(self, frame):
    #     tilt = self.ptz_tilt
    #     pan = self.ptz_pan
    #     print("Pan angle: ", pan)
    #     x = 0.5 * np.sin(np.radians(tilt)) * np.cos(np.radians(pan))
    #     y = 0.5 * np.sin(np.radians(tilt)) * np.sin(np.radians(pan))
    #     z = 0.5 * np.cos(np.radians(tilt))
    #     self.ptz.set_data_3d(x, y, z)
    #     self.ptz_line.set_data_3d([0, x], [0, y], [0, z])
    #     print(f"PTZ Tilt Angle: {tilt:.2f} degrees")
    #     print(f"PTZ Pan Angle: {pan:.2f} degrees")
    #     print('-' * 40)
    #     return self.ptz, self.ptz_line

    # for testing the animation
    def get_solar_positions_for_a_day(self):
        if isinstance(self.start_date, str):
            start_date = datetime.datetime.strptime(self.start_date, "%Y-%m-%d").date()

        end_date = start_date + datetime.timedelta(days=1)
        times = pd.date_range(
            start=datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0,
                                    tzinfo=pytz.timezone(self.timezone)),
            end=datetime.datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59,
                                  tzinfo=pytz.timezone(self.timezone)),
            freq='10T'
        )
        solar_positions = pvlib.solarposition.get_solarposition(
            time=times,
            latitude=self.latitude,
            longitude=self.longitude,
            altitude=self.altitude
        )

        return solar_positions

    def update_a_day(self, frame):
        solar_positions = self.get_solar_positions_for_a_day()
        time = solar_positions.index[frame]
        zenith = solar_positions['zenith'].iloc[frame]
        azimuth = solar_positions['azimuth'].iloc[frame]
        x = np.sin(np.radians(zenith)) * np.cos(np.radians(azimuth))
        y = np.sin(np.radians(zenith)) * np.sin(np.radians(azimuth))
        z = np.cos(np.radians(zenith))

        # Update the 3D plot elements
        self.sun.set_data_3d(x, y, z)
        self.azimuth_line.set_data_3d([0, x], [0, y], [0, 0])
        self.zenith_line.set_data_3d([0, x], [0, y], [0, z])

        # print(f"Time: {time}, Solar Zenith Angle: {zenith:.2f} degrees, Solar Azimuth Angle: {azimuth:.2f} degrees")
        # print('-' * 40)
        return self.sun, self.azimuth_line, self.zenith_line


# try:
#     sun = SUN()
#     # Create the animation
#     ani = FuncAnimation(sun.fig, sun.update, interval=sun.interval, blit=True)
#
#     # Display the animation
#     sun.ax.legend()
#     plt.show()
#     # while True:
#     #     zenith, azimuth = sun.get_solar_position()
#     #     print(f"Solar Zenith Angle: {zenith:.2f} degrees")
#     #     print(f"Solar Azimuth Angle: {azimuth:.2f} degrees")
#     #     print('-' * 40)
#     #     time.sleep(3) # 等待30秒
# except KeyboardInterrupt:
#     print("Program interrupted")