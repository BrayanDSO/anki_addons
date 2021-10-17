# -*- coding: utf-8 -*-
'''
The MIT License (MIT)

Copyright (c) 2016-2018 Arun Mahapatra

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import ctypes
from ctypes import windll
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

from .keycodes import KeyTbl, ModsTbl


def keys_from_string(keys):
    keysequence = QKeySequence(keys)
    ks = keysequence[0]

    # Calculate the modifiers
    mods = Qt.NoModifier
    qtmods = Qt.NoModifier
    if (ks & Qt.ShiftModifier == Qt.ShiftModifier):
        mods |= ModsTbl.index(Qt.ShiftModifier)
        qtmods |= Qt.ShiftModifier.real
    if (ks & Qt.AltModifier == Qt.AltModifier):
        mods |= ModsTbl.index(Qt.AltModifier)
        qtmods |= Qt.AltModifier.real
    if (ks & Qt.ControlModifier == Qt.ControlModifier):
        mods |= ModsTbl.index(Qt.ControlModifier)
        qtmods |= Qt.ControlModifier.real

    # Calculate the keys
    qtkeys = ks ^ qtmods
    try:
        keys = KeyTbl[qtkeys]
        if keys == 0:
            keys = _get_virtual_key(qtkeys)
    except ValueError:
        keys = _get_virtual_key(qtkeys)
    except IndexError:
        keys = KeyTbl.index(qtkeys)
        if keys == 0:
            keys = _get_virtual_key(qtkeys)


    return mods, keys


def _get_virtual_key(qtkeys):
    """Use the system keyboard layout to retrieve the virtual key.

    Fallback when we're unable to find a keycode in the mappings table.
    """
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    thread_id = 0

    # Key table doesn't have an entry for this keycode
    # Attempt to retrieve the VK code from system
    keyboard_layout = user32.GetKeyboardLayout(thread_id)
    virtual_key = windll.user32.VkKeyScanExW(qtkeys, keyboard_layout)
    if virtual_key == -1:
        keyboard_layout = user32.GetKeyboardLayout(0x409)
        virtual_key = windll.user32.VkKeyScanExW(qtkeys, keyboard_layout)
    # Key code is the low order byte
    keys = virtual_key & 0xff

    return keys
