#!/usr/bin/env python2.7

from gi.repository import Gtk
from ui.MainWindow import MainWindow
from ui.sound_menu import SoundMenuControls
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


class RaveCool:

    def __init__(self):
        self.window = self.loadMainWindow(DATA_DIR)
        self.window.show_all()

    def loadMainWindow(self, path=""):
        return MainWindow(path)


if __name__ == '__main__':
    ravecool = RaveCool()
    Gtk.main()
