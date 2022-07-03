# -*- coding: utf-8 -*-
from aqt.qt import *
from aqt import mw
from aqt.utils import tooltip

from . import pyqtkeybind



def add_card():
    dialog = mw.onAddCard()
    dialog.show()


def browser():
    dialog = mw.onBrowse()
    dialog.show()


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


if qtmajor == 5:
	cfg = mw.addonManager.getConfig(__name__)

	pyqtkeybind.keybinder.init()
	unregistered = False

	scut_add = cfg.get("add_card")
	if scut_add:
		pyqtkeybind.keybinder.register_hotkey(mw.winId(), scut_add, add_card)
	scut_browse = cfg.get("browser")
	if scut_browse:
		pyqtkeybind.keybinder.register_hotkey(mw.winId(), scut_browse, browser)

	# Install a native event filter to receive events from the OS
	win_event_filter = WinEventFilter(pyqtkeybind.keybinder)
	event_dispatcher = QAbstractEventDispatcher.instance()
	event_dispatcher.installNativeEventFilter(win_event_filter)
else:
	tooltip("the add-on global hotkeys only works with pyqt5 at the moment", period=5000)
