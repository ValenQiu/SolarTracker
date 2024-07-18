import sys
import serial
import serial.tools.list_ports
from threading import Lock
import time
from pynput import keyboard

ports_list = list(serial.tools.list_ports.comports())  # 获取所有串口设备实例
if len(ports_list) <= 0:
    print("无可用的串口设备！")
else:
    print("可用的串口设备如下：")
    for port in ports_list:  # 依次输出每个设备对应的串口号和描述信息
        print(list(port)[0], list(port)[1])  # COM4 USB-SERIAL CH340 (COM4)


class PTZ:
    _device = []
    _command = []
    _check = False
    _position = {
        'PAN': 0,  # Pan position
        'TILT': 0,  # Tilt position
    }

    _speed = {
        # from 0 to 63 (dec) => 0x00 to 0x3F (hex)
        'PAN': '\x1F',   # Pan speed
        'TILT': '\x1F'   # Tilt speed
    }

    # connect
    def __init__(self, port='', baudrate=2400, timeout_=10, address=1):

        if port != '':
            try:
                self.serial_mutex = Lock()
                self.ser = None
                self.timeout = 10
                self._device = serial.Serial(port, baudrate, timeout=timeout_)
                if self._device.isOpen():  # 判断串口是否成功打开
                    print("串口成功打开")
                    print(self._device.name)  # 输出串口号，即COM4
                    self._check = True
                    self._command = Frame(address)
                else:
                    print("串口打开失败")
                    self._check = False
                self.port_name = port
            except:
                print("error")
                self._check = False
        else:
            print('No device is specified for connection')
            self._check = False

    def unconnect(self):
        self.stop()
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        """
               close the serial port.
       """
        if self._device:
            self._device.flushInput()
            self._device.flushOutput()
            self._device.close()
        if self._device.isOpen():  # 判断串口是否关闭
            print("串口未关闭")
        else:
            self._check = False
            print("串口已关闭")

    def exception_on_error(self, error_code, hand_id, command_failed):
        global exception
        exception = None

        if not isinstance(error_code, int):
            ex_message = '[servo #%d on %s@%sbps]: %s failed' % (
            hand_id, self.ser.port, self.ser.baudrate, command_failed)
            msg = 'Communcation Error ' + ex_message
            exception = NonfatalErrorCodeError(msg, 0)
            return

    # PTZ speed setting
    def set_speed(self, pan_speed, tilt_speed):
        # save the speed to the log
        self._speed['PAN'] = pan_speed
        self._speed['TILT'] = tilt_speed

        # # convert the speed to the corresponding format and write it into Frame._frame
        # hex_pan_speed = hex(pan_speed)[2:].zfill(2)
        # hex_pan_speed = bytes.fromhex(hex_pan_speed)
        #
        # hex_tilt_speed = hex(tilt_speed)[2:].zfill(2)
        # hex_tilt_speed = bytes.fromhex(hex_tilt_speed)

        # print('pan speed: ', ord(hex_pan_speed))
        # print('tilt speed: ', ord(hex_tilt_speed))
        self._command._change_speed(pan_speed, tilt_speed)

    # PTZ MOVING (continually)
    # check angle limits
    def check_angle(self):
        '''
            edit it if need
        '''
        # tilt_position = self._position['TILT']
        # # tilt_position = self.convert_tile_angle_to_custom(tilt_position)
        # print(tilt_position)
        #
        # if tilt_position > 90 or tilt_position <= -10:
        #     self.stop()
        #     print("MOTION OUT OF RANGE")
        #     return False
        # else:
        #     return True
        return True

    # These part of codes are used for the bottoms in the GUI to control the angles
    def move_to_side(self, side):
        """ 'DOWN', 'UP'.'LEFT','RIGHT', 'STOP'"""
        cmd = self._command._construct_cmd(command2=side, pan_speed=self._speed['PAN'],
                                           tilt_speed=self._speed['PAN'])
        print("move to side: ", end='')
        for byte in cmd:
            print(f"{byte:02X}", end=' ')
        print()
        self._device.write(cmd)
        time.sleep(0.05)

    def stop(self):
        cmd = self._command._construct_cmd(command2='STOP', pan_speed='\x00', tilt_speed='\x00')
        print("stop: ", end='')
        for byte in cmd:
            print(f"{byte:02X}", end=' ')
        print()
        self._device.write(cmd)

    def move_to_left(self):
        self.move_to_side('LEFT')

    def move_to_right(self):
        self.move_to_side('RIGHT')

    def move_to_up(self):
        state = self.check_angle()
        if state:
            self.move_to_side('UP')

    def move_to_down(self):
        state = self.check_angle()
        if state:
            self.move_to_side('DOWN')

    def move_to_up_left(self):
        state = self.check_angle()
        if state:
            self.move_to_side('UP-LEFT')

    def move_to_up_right(self):
        state = self.check_angle()
        if state:
            self.move_to_side('UP-RIGHT')

    def move_to_down_left(self):
        state = self.check_angle()
        if state:
            self.move_to_side('DOWN-LEFT')

    def move_to_down_right(self):
        state = self.check_angle()
        if state:
            self.move_to_side('DOWN-RIGHT')

    # Query positions
    def convert_position(self, high_byte, low_byte):
        # Combine the high and low bytes into the actual position value
        position = (high_byte << 8) + low_byte
        # print(position)
        position = position / 100
        return position

    # angle converter
    def convert_tile_angle_to_custom(self, tile_angle):
        # edit it if need
        # tile_angle = 360 + tile_angle
        # # normalize
        if tile_angle >= 90:
            tile_angle = tile_angle - 360
        return round(tile_angle, 2)

    def convert_tile_angle_to_default(self, tile_angle):
        # edit it if need
        tile_angle = tile_angle
        if tile_angle <= 0:
            tile_angle = tile_angle + 360
        return round(tile_angle, 2)

    def query_tilt_position(self):
        '''
        Query Tilt Position	            | 0xFF | Address	0x00 |	0x53 |	0x00	        | 0x00	        | SUM |
        Query Tilt Position Response	| 0xFF | Address	0x00 |	0x5B |	Value High Byte	| Value Low Byte| SUM |
        '''
        cmd = self._command._construct_cmd(command2='QUERY-TILT', pan_speed='\x00',
                                           tilt_speed='\x00')
        print("query tilt position: ", end='')
        for byte in cmd:
            print(f"{byte:02X}", end=' ')
        print()
        self._device.write(cmd)
        response = self._device.read(7)
        # print(response)

        # if len(response) == 7 and response[0] == '\x00' and response[1] == '\x59':
        if len(response) == 7 and response[0] == 0xff and response[1] == 0x01 and response[3] == 0x5B:
            tilt_high = response[4]
            tilt_low = response[5]
            # print(type(pan_high))
            tilt_position = self.convert_position(tilt_high, tilt_low)
            # print("original: ", tilt_position)
            tilt_position = self.convert_tile_angle_to_custom(tilt_position)
            print('custom: ', tilt_position)
            self._position['TILT'] = tilt_position

    def set_tilt_position(self, angle):
        """
        Set Pan Position    | 0xFF | Address 0x01 | 0x00 | 0x4D | Value High Byte | Value Low Byte | Checksum |
        """
        """
           Converts an angle (in degrees) into high and low byte values.

           Parameters:
           angle (float): The angle in degrees.

           Returns:
           tuple: A tuple containing the high byte and low byte values.
           """
        angle = self.convert_tile_angle_to_default(angle)

        # Ensure the angle is within the valid range of 0 to 360 degrees
        angle = angle * 100

        # Calculate the high byte and low byte values
        high = int(angle // 256)
        low = int(angle % 256)

        # Convert the MSB and LSB to the correct format
        high_hex = chr(high)
        low_hex = chr(low)

        print("High (hex): ", high_hex)
        print("Low (hex): ", low_hex)

        # self._command._move_to_position(high_hex_byte, low_hex_byte)

        # print("data1: ", self._command._frame['data1'])
        # print("data2: ", self._command._frame['data2'])

        cmd = self._command._construct_cmd(command2='SET-TILT', pan_speed=high_hex,
                                           tilt_speed=low_hex)
        print("set pan position: ", end='')
        for byte in cmd:
            print(f"{byte:02X}", end=' ')
        print()
        self._device.write(cmd)

    def query_pan_position(self):
        '''
        Query Pan Position	        | 0xFF | Address	0x01 |	0x51 |	0x00	        | 0x00	        | SUM |
        Query Pan Position Response	| 0xFF | Address	0x01 |	0x59 |	Value High Byte	| Value Low Byte| SUM |
        '''
        cmd = self._command._construct_cmd(command2='QUERY-PAN', pan_speed='\x00',
                                           tilt_speed='\x00')
        self._device.write(cmd)
        response = self._device.read(7)
        # print(response)

        # if len(response) == 7 and response[0] == '\x00' and response[1] == '\x59':
        if len(response) == 7 and response[0] == 0xff and response[1] == 0x01 and response[3] == 0x59:
            pan_high = response[4]
            pan_low = response[5]
            # print(type(pan_high))
            pan_position = self.convert_position(pan_high, pan_low)
            print(pan_position)
            self._position['PAN'] = pan_position

    def set_pan_position(self, angle):
        """
        Set Pan Position    | 0xFF | Address 0x01 | 0x00 | 0x4B | Value High Byte | Value Low Byte | Checksum |
        """
        """
           Converts an angle (in degrees) into high and low byte values.

           Parameters:
           angle (float): The angle in degrees.

           Returns:
           tuple: A tuple containing the high byte and low byte values.
           """
        # Ensure the angle is within the valid range of 0 to 360 degrees
        angle = angle * 100

        # Calculate the high byte and low byte values
        high = int(angle // 256)
        low = int(angle % 256)

        # Convert the MSB and LSB to the correct format
        high_hex = chr(high)
        low_hex = chr(low)

        print("High (hex): ", high_hex)
        print("Low (hex): ", low_hex)

        # self._command._move_to_position(high_hex_byte, low_hex_byte)

        # print("data1: ", self._command._frame['data1'])
        # print("data2: ", self._command._frame['data2'])

        cmd = self._command._construct_cmd(command2='SET-PAN', pan_speed=high_hex,
                                           tilt_speed=low_hex)
        print("set pan position: ", end='')
        for byte in cmd:
            print(f"{byte:02X}", end=' ')
        print()
        self._device.write(cmd)


# Peclo-D data construction
class Frame:
    # Frame format:		|synch byte|address|command1|command2|data1|data2|checksum|
    # Bytes 2 - 6 are Payload Bytes
    _frame = {
        'synch_byte': '\xFF',  # Synch Byte, always FF		-	1 byte
        'address': '\x00',  # Address			-	1 byte
        'command1': '\x00',  # Command1			-	1 byte
        'command2': '\x00',  # Command2			-	1 byte
        'data1': '\x3F',  # Data1	(PAN SPEED): from 00 to 3F		-	1 byte
        'data2': '\x3F',  # Data2	(TILT SPEED): from 00 to 3F		- 	1 byte
        'checksum': '\x00'  # Checksum:			-       1 byte
    }

    _command2_code = {
        'DOWN': '\x10',
        'UP': '\x08',
        'LEFT': '\x04',
        'RIGHT': '\x02',
        'UP-RIGHT': '\x0A',
        'DOWN-RIGHT': '\x12',
        'UP-LEFT': '\x0C',
        'DOWN-LEFT': '\x14',
        'STOP': '\x00',
        'ZOOM-IN': '\x00',
        'ZOOM-OUT': '\x00',
        'FOCUS-FAR': '\x00',
        'FOCUS-NEAR': '\x00',
        'QUERY-TILT': '\x53',
        'QUERY-PAN': '\x51',
        'SET-PAN': '\x4B',
        'SET-TILT': '\x4D'
    }

    def __init__(self, adress=1):

        self._frame['address'] = chr(adress)
        print("address: ",ord(self._frame['address']))

    def _construct_cmd(self, command1='\x00', command2='\x00', pan_speed='\x00', tilt_speed='\x00'):

        self._frame['command1'] = command1

        if command2 not in self._command2_code:
            if (type(command2) == str and (ord(command2) < 255 and ord(command2) >= 0)):
                self._frame['command2'] = command2
            else:
                print('not command')
        else:
            self._frame['command2'] = self._command2_code[command2]

        self._frame['data1'] = pan_speed
        self._frame['data2'] = tilt_speed

        self._checksum(self._payload_bytes())
        cmd_str = self._frame['synch_byte'] + self._payload_bytes() + self._frame['checksum']
        cmd = bytes('', encoding='utf-8')

        # Error result function bytes('\xFF',encoding = 'utf-8') is b'\xc3\xbf'
        for ch in cmd_str:
            if ch == '\xFF':
                cmd = b'\xFF'
            else:
                # cmd = cmd + bytes(ch, encoding='utf-8')
                cmd = b''.join(bytes(ch, encoding='latin-1') for ch in cmd_str)
        return cmd

    def _payload_bytes(self):
        return self._frame['address'] + self._frame['command1'] + \
               self._frame['command2'] + self._frame['data1'] + \
               self._frame['data2']

    def _checksum(self, payload_bytes_string):
        self._frame['checksum'] = chr(sum(map(ord, payload_bytes_string)) % 256)
        # print(ord(self._frame['checksum']))

    def _change_speed(self, pan_speed, tilt_speed):
        self._frame['data1'] = pan_speed
        self._frame['data2'] = tilt_speed

    def _move_to_position(self, MSB, LSB):
        self._frame['data1'] = MSB
        self._frame['data2'] = LSB

# Error detection
class ChecksumError(Exception):
    def __init__(self, hand_id, response, checksum):
        Exception.__init__(self)
        self.message = 'Checksum received from motor %d does not match the expected one (%d != %d)' \
                       % (hand_id, response[-1], checksum)
        self.response_data = response
        self.expected_checksum = checksum

    def __str__(self):
        return self.message


class FatalErrorCodeError(Exception):
    def __init__(self, message, ec_const):
        Exception.__init__(self)
        self.message = message
        self.error_code = ec_const

    def __str__(self):
        return self.message


class NonfatalErrorCodeError(Exception):
    def __init__(self, message, ec_const):
        Exception.__init__(self)
        self.message = message
        self.error_code = ec_const

    def __str__(self):
        return self.message


class ErrorCodeError(Exception):
    def __init__(self, message, ec_const):
        Exception.__init__(self)
        self.message = message
        self.error_code = ec_const

    def __str__(self):
        return self.message


class DroppedPacketError(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return self.message


