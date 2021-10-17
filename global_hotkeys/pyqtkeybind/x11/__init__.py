# -*- coding: utf-8 -*-
'''
The MIT License (MIT)

Copyright (c) 2016-2018 Arun Mahapatra

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import sys
from collections import defaultdict

from PyQt5.QtX11Extras import QX11Info
import xcffib
import xcffib.xproto
from xcffib import ffi
from struct import unpack
import sip

from .keybindutil import *

# class X11KeyBinder(KeyBinder):
class X11KeyBinder(object):
    conn = None

    def init(self):
        # Get the X11 connection and update keyboard mappings
        qt_conn = QX11Info.connection()
        ptr = sip.unwrapinstance(qt_conn)
        self.conn = xcffib.wrap(ptr)
        update_keyboard_mapping(self.conn, None)

    def register_hotkey(self, wid, key_string, callback):
        if wid is None:
            wid = QX11Info.appRootWindow()

        return bind_global_key(self.conn, "KeyPress", key_string, callback)

    def unregister_hotkey(self, wid, key_string):
        if wid is None:
            wid = QX11Info.appRootWindow()

        return unbind_global_key(self.conn, wid, key_string)

    def handler(self, eventType, message):
        e = self._parse_keypress_event(message)

        if e.is_valid():
            return run_keybind_callbacks(e)
        return False

    def _parse_keypress_event(self, message):
        # Try unpack the message as a xcb_key_press_event.
        # Each xcb event is 36 bytes, last 4 bytes are padding for keypress,
        # hence set the size to be unpacked as 32.
        message.setsize(32)
        return X11KeyPressEvent(message.asstring())

class X11KeyPressEvent(object):
    def __init__(self, data):
        self.response_type, self.detail, self.sequence, self.time,\
            self.root, self.event, self.child, self.root_x, self.root_y,\
            self.event_x, self.event_y, self.state,\
            self.same_screen = unpack("=BBHIIIIhhhhHBx", data)

    def is_valid(self):
        # Response type of a KeyPress event is 2, KeyRelease event has a
        # response type 3
        return self.response_type == 0x2
