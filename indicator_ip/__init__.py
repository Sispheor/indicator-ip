
import signal

import gi

from indicator_ip.indicator_ip_menu import IndicatorIPMenu

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk


def main():
    IndicatorIPMenu()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()


if __name__ == "__main__":
    main()
