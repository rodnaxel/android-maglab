'''usbserial4a example with UI.

This example directly works on Android 6.0+ with Pydroid App.
And it also works on main stream desktop OS like Windows, Linux and OSX.
To make it work on Android 4.0+, please follow the readme file on
https://github.com/jacklinquan/usbserial4a
'''

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.clock import mainthread
from kivy.utils import platform

from kivy.clock import Clock

import threading
import sys
import time

from queue import Queue

if platform == 'android':
    from usb4a import usb
    from usbserial4a import serial4a
else:
    from serial.tools import list_ports
    from serial import Serial


__version__ = "0.0.1"

kv = '''

#:set green_color (27/255, 94/255, 32/255, 1)
#:set darkgrey_color (32/255, 32/255, 33/255,1)
#:set red_color (213/255, 0, 0, 1)

BoxLayout:
    id: box_root
    orientation: 'vertical'

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: '50dp'
        Label:
        #    height: '50dp'
            text: 'Sensor'
            canvas.before:
                Color:
                    rgba: green_color
                Rectangle:
                    pos: self.pos
                    size: self.size
        Label:
            id: txtCal
            on_parent: app.uiDict['txtCal'] = self
            text: ''
            #size_hint_x: None
            #width: '200dp'
            halign: 'right'
            valign: 'middle'
            canvas.before:
                Color:
                    rgba: green_color
                Rectangle:
                    pos: self.pos
                    size: self.size
        Label:
            id: txtStatus
            on_parent: app.uiDict['txtStatus'] = self
            text: ''
            #size_hint_x: None
            #width: '200dp'
            halign: 'right'
            valign: 'middle'
            canvas.before:
                Color:
                    rgba: green_color
                Rectangle:
                    pos: self.pos
                    size: self.size

    TabbedPanel:
        id: sm
        on_parent: app.uiDict['sm'] = self
        do_default_tab: False

        TabbedPanelItem:
            name: 'screen_scan'
            text: 'Scan'
            BoxLayout:
                orientation: 'vertical'
                spacing: 20
                padding: 100
                Button:
                    id: btn_scan
                    on_parent: app.uiDict['btn_scan'] = self
                    size_hint_y: None
                    height: '50dp'
                    text: 'Scan USB Device'
                    on_release: app.on_btn_scan_release()            

                RecycleView:
                    BoxLayout:
                        id: box_list
                        spacing: 20
                        orientation: 'vertical'
                        on_parent: app.uiDict['box_list'] = self
                        #size_hint_y: None
                        height: max(self.minimum_height, self.parent.height)

        TabbedPanelItem:
            name: 'screen_test'
            text: "Monitor"
            BoxLayout:
                orientation: 'vertical'
                #padding:100
                GridLayout:
                    cols:2
                    spacing: 20
                    padding: 50
                    
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
                                rgba: (1,1,1,1) 
                            RoundedRectangle:
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
                            RoundedRectangle:
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
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size   
                                    
                    Label:
                        id: label_bxh
                        text: 'Bxh, uT:'
                    Label:
                        id: txtInput_bxh
                        on_parent: app.uiDict['txtInput_bxh'] = self
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
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size   
                    
                    Label:
                        id: label_byh
                        text: 'Byh, uT:'
                    Label:
                        id: txtInput_byh
                        on_parent: app.uiDict['txtInput_byh'] = self
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
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size   

                    Label:
                        id: label_bzh
                        text: 'Bzh, uT:'
                    Label:
                        id: txtInput_bzh
                        on_parent: app.uiDict['txtInput_bzh'] = self
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
                            RoundedRectangle:
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
                            RoundedRectangle:
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
                                rgba: 1,1,1,1
                            RoundedRectangle:
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
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size   

                    # Button:
                    #     id: btn_write
                    #     on_parent: app.uiDict['btn_write'] = self
                    #     text: 'Device'
                    #     on_release: app.on_btn_back()
        TabbedPanelItem:
            name: "screen_compensate"
            text: "Compensate"
            BoxLayout:
                orientation: 'vertical'
                padding: 100
                spacing: 20

                Button:
                    id: btn_reset
                    on_parent: app.uiDict['btn_reset'] = self
                    text: 'Reset Sensor'
                    size_hint_y: None
                    height: btn_scan.height
                    background_color: .7, .7, 1, 1
                    on_release: app.on_btn_reset_sensor()

                Button:
                    id: btn_compensate
                    on_parent: app.uiDict['btn_compensate'] = self
                    text: 'Start Compensate'
                    size_hint_y: None
                    height: btn_scan.height
                    background_color: .7, .7, 1, 1
                    on_release: app.on_btn_compensate_sensor()

                Button:
                    id: btn_abort
                    on_parent: app.uiDict['btn_abort'] = self
                    text: 'Abort Compensate'
                    size_hint_y: None
                    height: btn_scan.height
                    background_color: .7, .7, 1, 1
                    on_release: app.on_btn_compensate_sensor_abort()

    # BoxLayout:
    #     id: toolbar
    #     on_parent: app.uiDict['toolbar'] = self
    #     size_hint_y: None
    #     height: '50dp'
    #     spacing: 0
    #     padding:0

    #     ToggleButton:
    #         text: 'Scan'
    #         #background_color: darkgrey_color
    #         group: "toolbar"
    #         state: 'down'
    #         on_release:
    #             sm.current = 'screen_scan'
    #     ToggleButton:
    #         text: 'Monitor'
    #         #background_color: darkgrey_color
    #         group: "toolbar"
    #         on_release:
    #             sm.current = 'screen_test'

    #     ToggleButton:
    #         text: 'Calibrate'
    #         #background_color: darkgrey_color
    #         group: "toolbar"
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
        self.queue = Queue(maxsize=1)

        self.counter_msg = 0
        self.counter_error = 0
        self.counter_reset = 0

        self.calibrate_on = False

        super(MainApp, self).__init__(*args, **kwargs)

    def build(self):
        b =  Builder.load_string(kv)
        
        return b

    def my_callback(self, second):
        if self.queue:
            print("Get: ", self.queue.get())

    def on_stop(self):
        if self.serial_port:
            with self.port_thread_lock:
                self.serial_port.close()

    def on_btn_compensate_sensor(self):
        req = "0d0a7e72010109"
        self.calibrate_on = True
        self.request(req)

    def on_btn_compensate_sensor_abort(self):
        req = "0d0a7e7201030b"
        self.calibrate_on = False
        self.request(req)

    def on_btn_reset_sensor(self):
        req = "0d0a7e7201040c"
        self.request(req)
        
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
        
        if self.device_name_list:
            for device_name in self.device_name_list:
                btnText = device_name
                button = Button(text=btnText, size_hint_y=None, height='50dp')
                button.bind(on_release=self.on_btn_device_release)
                self.uiDict['box_list'].add_widget(button)
        else:
            label = Label(text="Not find USB device")
            self.uiDict['box_list'].add_widget(label)    
    
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
            #self.read_thread = threading.Thread(target = self.read_msg_thread)
            self.read_thread = threading.Thread(target = self.recieve)
            self.read_thread.start()
            #from kivy.clock import Clock
            #Clock.schedule_interval(self.my_callback, 0.1)
        else:
            print("Exception")

        #self.uiDict['sm'].current = 'screen_test'
        self.uiDict['sm'].switch_to(self.uiDict['sm'].tab_list[1]) 

    def on_clear_status(self, event):
        self.uiDict['txtCal'].text = ''

    def request(self, req):
        if self.serial_port and self.serial_port.is_open:
            message = bytearray.fromhex(req)
            self.serial_port.write(message)

    def recieve(self):
        buf = b''
        data = b''
        counter = 0
        state = 0
        
        while True:
            try:
                with self.port_thread_lock:
                    if not self.serial_port.is_open:
                        break

                buf = self.serial_port.read(1)
                if state == 0: 
                    if buf == b'~':
                        state = 1
                elif state == 1:
                    mid = buf.hex()
                    state = 2
                elif state == 2:
                    msize = int.from_bytes(buf, byteorder="little")
                    state = 3
                elif state == 3:
                    if counter < msize:
                        data += buf
                        counter += 1
                    else:
                        #self.queue.put((mid, data))
                        if mid == '70':
                            dorient_data = self.handler_dorient(data)
                            self.display_received_msg(dorient_data)
                        elif mid == '72':
                            dmcal = self.handler_dmcal(data)
                            self.display_compensate(dmcal)
                        self.counter_msg += 1
                        state = 0
                        counter = 0   
                        data = b''

            except Exception as ex:
                print("<Exception>")
                self.read_thread = None
                raise ex               

    
    def handler_dmcal(self, data_bytes):
        state = data_bytes[0]
        status_code = data_bytes[1]
        bins = [b for b in data_bytes[2:10]]
        progress = data_bytes[11]
        quality = int.from_bytes(data_bytes[12:13], byteorder='little')    
        return state, status_code, bins, progress, quality

    def handler_dorient(self, data_bytes):
        fields = [data_bytes[2 * i : 2 * (i+1) ] for i in range(9)]
        roll = kang2dec(fields[0])
        pitch = kang2dec(fields[1])
        course = kang2dec(fields[2], signed=False)
        magbh = gauss2tesla(fields[3])
        magch = gauss2tesla(fields[4])
        magzh = gauss2tesla(fields[5])
        magb = gauss2tesla(fields[6])
        magc = gauss2tesla(fields[7])
        magz = gauss2tesla(fields[8])
        return roll, pitch, course, magb, magc, magz, magbh, magch, magzh

    @mainthread
    def display_compensate(self, data):
        state, scode, bins, progress, quality = data

        if state == 1 and scode == 0:
            self.uiDict['txtCal'].text = "Fill {} from 8".format(sum(bins) % 15)
        if scode == 1:
            self.uiDict['txtCal'].text = "Success"
            Clock.schedule_once(self.on_clear_status, 3)
        elif scode==0 and state == 3:
            self.uiDict['txtCal'].text = "Abort"
            Clock.schedule_once(self.on_clear_status, 3)
        elif state == 0 and scode == 0:
            self.uiDict['txtCal'].text = "Revert"
            Clock.schedule_once(self.on_clear_status, 3)
                
    @mainthread
    def display_received_msg(self, msg):
        r,p,h,bx,by,bz, bxh ,byh, bzh = msg
        self.uiDict['txtInput_roll'].text =  str(r)
        self.uiDict['txtInput_pitch'].text =  str(p)
        self.uiDict['txtInput_course'].text =  str(h)
        self.uiDict['txtInput_bx'].text =  str(bx)
        self.uiDict['txtInput_by'].text =  str(by)
        self.uiDict['txtInput_bz'].text =  str(bz)

        self.uiDict['txtStatus'].text = 'Rx: {} Tx: {}'.format(self.counter_msg % 1000000, 0 % 1000000 )

if __name__ == '__main__':
    MainApp().run()



'''
    def recv(self):
        """ Deprecated """
        buf = b''
        while self.serial_port.in_waiting:
            buf = self.serial_port.read(1)
            if buf != b'~':
                continue
            buf += self.serial_port.read(21)       
        return buf 

    def read_msg_thread(self):
        """ Deprecated """
        while True:
            try:
                with self.port_thread_lock:
                    if not self.serial_port.is_open:
                        break

                    msg = self.recv()
                    if self.calibrate_on:
                        print(msg.hex())

                if msg and len(msg) > 21:   
                    mid = msg[1]
                    msize = msg[2]
                    data = msg[3:-1]
                    checksum = msg[-1]      
                    dorient_data = self.handler_dorient(data)
                    self.counter_msg += 1
                    self.display_received_msg(dorient_data)
                elif msg and len(msg) > 12:
                    mid = msg[1]
                    msize = msg[2]
                    self.counter_reset += 1
                else:
                    self.counter_error += 1
                time.sleep(0.1)

            except Exception as ex:
                raise ex

'''
