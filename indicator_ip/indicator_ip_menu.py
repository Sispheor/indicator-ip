import os
import gi

from indicator_ip.net_utils import NetUtils

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, AppIndicator3, Gdk, Notify, GObject

class IndicatorIPMenu(object):

    def __init__(self) -> None:
        super().__init__()

        icon = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'images', 'ip_white.png')

        self.app_id = 'ip-indicator'

        self.indicator = AppIndicator3.Indicator.new(self.app_id,
                                                     icon,
                                                     AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        # prepare the clipboard to receive copied IPs
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        self.refresh_freq = 0
        self.doIterationTimer = None

        self.refresh(None)

        self.last_clicked_interface = None


    def create_menu(self):
        menu = Gtk.Menu()
        # manual refresh
        item_refresh = Gtk.MenuItem(label='Refresh')
        item_refresh.connect('activate', self.refresh)
        menu.append(item_refresh)

        # separator
        sep = Gtk.SeparatorMenuItem()
        sep.show()
        menu.append(sep)

        # get all interface
        group = None
        for interface in NetUtils.get_all_interface():
            new_radio = Gtk.RadioMenuItem.new_with_label_from_widget(label=str(interface), group=group)
            new_radio.connect("toggled", self.on_clicked_item, interface)
            new_radio.show()
            if group is None:
                group = new_radio.get_group()[0]
            menu.append(new_radio)

        # separator
        sep = Gtk.SeparatorMenuItem()
        sep.show()
        menu.append(sep)


        # get all refresh timer
        group = None
        for refresh_time in ["[OFF] autorefresh", "15 sec", "1 min", "1 hour"]:
            refresh_radio = Gtk.RadioMenuItem.new_with_label_from_widget(label=str(refresh_time), group=group)
            refresh_radio.connect("toggled", self.on_clicked_refresh_timer, refresh_time)
            refresh_radio.show()
            if group is None:
                group = refresh_radio.get_group()[0]
            menu.append(refresh_radio)

        # separator
        sep = Gtk.SeparatorMenuItem()
        sep.show()
        menu.append(sep)

        # quit item
        item_quit = Gtk.MenuItem(label='Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    @staticmethod
    def quit(_):
        Gtk.main_quit()

    def refresh(self, w=None):
        if w is None:
            self.indicator.set_menu(self.create_menu())
        else:
            self.doIterationTimer = GObject.timeout_add(self.refresh_freq, self.refresh, True)
        # set by default the public IP as label
        self.indicator.set_label(str(NetUtils.get_public_interface().ip),
                                 str(NetUtils.get_public_interface().ip))

    def on_clicked_refresh_timer(self, button, refresh_time):
        if button.get_active():
            print("refresh_time %s" % refresh_time)

            if refresh_time == "[OFF] autorefresh":
                GObject.source_remove(self.doIterationTimer)
                self.doIterationTimer = None
                return

            if refresh_time == "15 sec":
                self.refresh_freq = 15*1000
            elif refresh_time == "1 min":
                self.refresh_freq = 60*1000
            elif refresh_time == "1 hour":
                self.refresh_freq = 60*60*1000

            if self.doIterationTimer is not None:
                GObject.source_remove(self.doIterationTimer)
                self.doIterationTimer = None
            self.doIterationTimer = GObject.timeout_add(self.refresh_freq, self.refresh, True)

    def on_clicked_item(self, button, interface):
        if button.get_active():
            if interface != self.last_clicked_interface or self.last_clicked_interface is None:
                # copy to clipboard the ip
                self.clipboard.set_text(interface.ip, -1)
                # print("'%s' copied to clipboard" % interface.ip)
                # update the label so we see the selected ip
                self.indicator.set_label(str(interface.ip), str(interface.ip))
                self.show_notification(str(interface.ip), "copied to clipboard")
                self.last_clicked_interface = interface

    @staticmethod
    def show_notification(title, message):
        Notify.init('indicator-ip')
        n = Notify.Notification.new(title, message)
        n.show()
