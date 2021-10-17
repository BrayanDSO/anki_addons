# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from aqt import mw
from . import pyqtkeybind

def add_card():
    mw.onAddCard()

def browser():
    mw.onBrowse()

class WinEventFilter(QtCore.QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0

cfg = mw.addonManager.getConfig(__name__)

pyqtkeybind.keybinder.init()
unregistered = False

pyqtkeybind.keybinder.register_hotkey(mw.winId(), cfg["add_card"], add_card)
pyqtkeybind.keybinder.register_hotkey(mw.winId(), cfg["browser"], browser)

# Install a native event filter to receive events from the OS
win_event_filter = WinEventFilter(pyqtkeybind.keybinder)
event_dispatcher = QtCore.QAbstractEventDispatcher.instance()
event_dispatcher.installNativeEventFilter(win_event_filter)
