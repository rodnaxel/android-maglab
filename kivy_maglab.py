'''usbserial4a example with UI.

This example directly works on Android 6.0+ with Pydroid App.
And it also works on main stream desktop OS like Windows, Linux and OSX.
To make it work on Android 4.0+, please follow the readme file on
https://github.com/jacklinquan/usbserial4a
'''

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.clock import mainthread
from kivy.utils import platform

import threading
import sys
import time

if platform == 'android':
    from usb4a import usb
    from usbserial4a import serial4a
else:
    from serial.tools import list_ports
    from serial import Serial

kv = '''
BoxLayout:
    id: box_root
    orientation: 'vertical'

    Label:
        size_hint_y: None
        height: '50dp'
        text: 'Monitor Sensor Data'
        canvas.before:
            Color:
                rgba: 0, 0.5, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size

    ScreenManager:
        id: sm
        on_parent: app.uiDict['sm'] = self

        Screen:
            name: 'screen_scan'
            BoxLayout:
                orientation: 'vertical'
                spacing: 20
                Button:
                    id: btn_scan
                    on_parent: app.uiDict['btn_scan'] = self
                    size_hint_y: None
                    height: '50dp'
                    text: 'Scan USB Device'
                    on_release: app.on_btn_scan_release()

                ScrollView:
                    BoxLayout:
                        id: box_list
                        orientation: 'vertical'
                        on_parent: app.uiDict['box_list'] = self
                        size_hint_y: None
                        height: max(self.minimum_height, self.parent.height)

                Button:
                    id: btn_switch
                    on_parent: app.uiDict['btn_switch'] = self
                    size_hint_y: None
                    height: '50dp'
                    text: 'Monitor'
                    on_release: app.on_btn_switch()
    
        Screen:
            name: 'screen_test'
            GridLayout:
                cols:2
                spacing: 10
               
                Label:
                    id: label_roll
                    text: 'Roll:'
                Label:
                    id: txtInput_roll
                    on_parent: app.uiDict['txtInput_roll'] = self
                    font_size: self.height * 0.65
                    halign: 'center'
                    valign: 'center'
                    text: '-'
                    color: 0,0,0,1
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size   
                    on_text: self.color = [0,0,0,1] if (float(self.text) < 1.0 and float(self.text) > - 1.0 ) else [1,0,0,1]

                Label:
                    id: label_pitch
                    text: 'Pitch:'                 
                Label:
                    id: txtInput_pitch
                    on_parent: app.uiDict['txtInput_pitch'] = self
                    font_size: self.height * 0.65
                    multiline: False
                    readonly: True
                    halign: 'center'
                    valign: 'center'
                    text: '-'
                    color: 0,0,0,1
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size   
                    on_text: self.color = [0,0,0,1] if (float(self.text) < 1.0 and float(self.text) > - 1.0 ) else [1,0,0,1]

                Label:
                    id: label_course
                    text: 'Heading:'
                Label:
                    id: txtInput_course
                    on_parent: app.uiDict['txtInput_course'] = self
                    font_size: self.height * 0.65
                    multiline: False
                    readonly: True
                    halign: 'center'
                    valign: 'center'
                    text: '-'
                    color: 0,0,0,1
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size   
                             
                Label:
                    id: label_bx
                    text: 'Bx, uT:'
                Label:
                    id: txtInput_bx
                    on_parent: app.uiDict['txtInput_bx'] = self
                    font_size: self.height * 0.65
                    multiline: False
                    readonly: True
                    halign: 'center'
                    valign: 'center'
                    text: '-'
                    color: 0,0,0,1
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size   
                
                Label:
                    id: label_by
                    text: 'By, uT:'
                Label:
                    id: txtInput_by
                    on_parent: app.uiDict['txtInput_by'] = self
                    font_size: self.height * 0.65
                    multiline: False
                    readonly: True
                    halign: 'center'
                    valign: 'center'
                    text: '-'
                    color: 0,0,0,1
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size   

                Label:
                    id: label_bz
                    text: 'Bz, uT:'
                Label:
                    id: txtInput_bz
                    on_parent: app.uiDict['txtInput_bz'] = self
                    font_size: self.height * 0.65
                    multiline: False
                    readonly: True
                    halign: 'center'
                    valign: 'center'
                    text: '-'
                    color: 0,0,0,1
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size   

                Button:
                    id: btn_write
                    on_parent: app.uiDict['btn_write'] = self
                    text: 'Device'
                    on_release: app.on_btn_back()
                
                Button:
                    id: btn_reset
                    on_parent: app.uiDict['btn_reset'] = self
                    text: 'Reset'
                    background_color: .7, .7, 1, 1
                    on_release: app.on_btn_reset_sensor()
                
                Label:
                    id: txtStatus
                    on_parent: app.uiDict['txtStatus'] = self
                    text: 'Status: None'
                    size_hint_y: None
                    height: '50dp'
'''

def kang2dec(kang, signed=True):
    return round(int.from_bytes(kang, byteorder='little', signed=signed) * 359.9 / 65536.0, 1)

def gauss2tesla(gauss):
    return round(int.from_bytes(gauss, byteorder='little', signed=True) * 750.0 / 65536.0, 1)


class MainApp(App):
    def __init__(self, *args, **kwargs):
        self.uiDict = {}
        self.device_name_list = []
        self.serial_port = None
        self.read_thread = None
        self.port_thread_lock = threading.Lock()

        self.counter_msg = 0
        self.counter_error = 0

        super(MainApp, self).__init__(*args, **kwargs)

    def build(self):
        return Builder.load_string(kv)

    def on_stop(self):
        if self.serial_port:
            with self.port_thread_lock:
                self.serial_port.close()

    def on_btn_switch(self):
        self.uiDict['sm'].current = 'screen_test'

    def on_btn_back(self):
        self.uiDict['sm'].current = 'screen_scan'
    
    def on_btn_reset_sensor(self):
        if self.serial_port and self.serial_port.is_open:
            req = "0d0a7e7201040c"
            message = bytearray.fromhex(req)
            self.serial_port.write(message)
            self.uiDict['txtStatus'].text = 'Status: Reset Sensor'

    def on_btn_scan_release(self):
        self.uiDict['box_list'].clear_widgets()
        self.device_name_list = []
        
        if platform == 'android':
            usb_device_list = usb.get_usb_device_list()
            self.device_name_list = [
                device.getDeviceName() for device in usb_device_list
            ]
        else:
            usb_device_list = list_ports.comports()
            self.device_name_list = [port.device for port in usb_device_list]
        
        for device_name in self.device_name_list:
            btnText = device_name
            button = Button(text=btnText, size_hint_y=None, height='100dp')
            button.bind(on_release=self.on_btn_device_release)
            self.uiDict['box_list'].add_widget(button)
        
    def on_btn_device_release(self, btn):
        device_name = btn.text
        
        if platform == 'android':
            device = usb.get_usb_device(device_name)
            if not device:
                raise SerialException(
                    "Device {} not present!".format(device_name)
                )
            if not usb.has_usb_permission(device):
                usb.request_usb_permission(device)
                return
            self.serial_port = serial4a.get_serial_port(
                device_name, 9600, 8, 'N', 1, timeout=0.03
            )
        else:
            self.serial_port = Serial(
                device_name, 9600, 8, 'N', 1, timeout=0.03
            )
        
        if self.serial_port.is_open and not self.read_thread:
            self.read_thread = threading.Thread(target = self.read_msg_thread)
            self.read_thread.start()
        
        self.uiDict['sm'].current = 'screen_test'

    def on_btn_write_release(self):
        self.uiDict['txtStatus'].text = 'Status: {}'.format("on_btn_release")
        
    def recv(self):
        buf = b''
        while self.serial_port.in_waiting:
            buf = self.serial_port.read(1)
            if buf != b'~':
                continue
            buf += self.serial_port.read(21)       
        return buf 

    def handler_dorient(self, data_bytes):
        fields = [data_bytes[2 * i : 2 * (i+1) ] for i in range(9)]

        roll = kang2dec(fields[0])
        pitch = kang2dec(fields[1])
        course = kang2dec(fields[2], signed=False)
        magb = gauss2tesla(fields[6])
        magc = gauss2tesla(fields[7])
        magz = gauss2tesla(fields[8])
        
        return roll, pitch, course, magb, magc, magz

    def read_msg_thread(self):
        while True:
            try:
                with self.port_thread_lock:
                    if not self.serial_port.is_open:
                        break

                    msg = self.recv()

                if msg and len(msg) > 21:   
                    mid = msg[1]
                    msize = msg[2]
                    data = msg[3:-1]
                    checksum = msg[-1]      
                    dorient_data = self.handler_dorient(data)
                    self.counter_msg += 1
                    self.display_received_msg(dorient_data)
                else:
                    self.counter_error += 1
                time.sleep(0.1)

            except Exception as ex:
                raise ex
                
    @mainthread
    def display_received_msg(self, msg):
        r,p,h,bx,by,bz = msg
        self.uiDict['txtInput_roll'].text =  str(r)
        self.uiDict['txtInput_pitch'].text =  str(p)
        self.uiDict['txtInput_course'].text =  str(h)
        self.uiDict['txtInput_bx'].text =  str(bx)
        self.uiDict['txtInput_by'].text =  str(by)
        self.uiDict['txtInput_bz'].text =  str(bz)

        self.uiDict['txtStatus'].text = 'Recieved: {} Error: {}'.format(self.counter_msg, self.counter_error)

if __name__ == '__main__':
    MainApp().run()

