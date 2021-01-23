import os
from pathlib import Path

import gi

from indicator_ip.net_utils import NetUtils

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, AppIndicator3, Gdk, Notify, GObject
from configparser import ConfigParser

HOME = str(Path.home())
CONFIG_FILE_PATH = HOME + os.sep + ".config/indicator-ip/config.ini"


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

        # create config file if not exist

        # load the configuration
        config = self.load_config_file()
        self.refresh_freq = config.get('main', 'refresh_freq')

        # an object that memory interface timeout
        self.do_iteration_timer = None
        self.refresh()
        self.last_clicked_interface = config.get('main', 'last_clicked_interface')

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
        group_interface = None
        for interface in NetUtils.get_all_interface():
            new_radio = Gtk.RadioMenuItem.new_with_label_from_widget(label=str(interface),
                                                                     group=group_interface)
            new_radio.connect("toggled", self.on_clicked_item, interface)
            new_radio.show()
            if group_interface is None:
                group_interface = new_radio.get_group()[0]
            menu.append(new_radio)

        # separator
        sep1 = Gtk.SeparatorMenuItem()
        sep1.show()
        menu.append(sep1)

        # auto refresh sub menu
        item_auto_refresh = Gtk.MenuItem(label='Auto refresh')
        menu.append(item_auto_refresh)
        refresh_sub_menu = Gtk.Menu()
        item_auto_refresh.set_submenu(refresh_sub_menu)
        # options in sub menu
        selected_refresh_option = None
        for refresh_time in ["Disabled", "15 sec", "1 min", "1 hour"]:
            refresh_radio = Gtk.RadioMenuItem.new_with_label_from_widget(label=str(refresh_time),
                                                                         group=selected_refresh_option)
            refresh_radio.connect("toggled", self.on_clicked_refresh_timer, refresh_time)
            refresh_radio.show()
            if selected_refresh_option is None:
                selected_refresh_option = refresh_radio.get_group()[0]
            refresh_sub_menu.append(refresh_radio)

        # separator
        sep2 = Gtk.SeparatorMenuItem()
        sep2.show()
        menu.append(sep2)

        # quit item
        item_quit = Gtk.MenuItem(label='Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    @staticmethod
    def quit(_):
        Gtk.main_quit()

    def refresh(self):
        print("Refreshing")
        self.indicator.set_menu(self.create_menu())
        # set by default the public IP as label
        self.indicator.set_label(str(NetUtils.get_public_interface().ip),
                                 str(NetUtils.get_public_interface().ip))

    def enable_auto_refresh(self):
        self.save_key_in_config_file("refresh_freq", str(self.refresh_freq))
        refresh_frequency_millisecond = self.refresh_freq * 1000
        self.do_iteration_timer = GObject.timeout_add(refresh_frequency_millisecond, self.refresh)

    def disable_auto_refresh(self):
        GObject.source_remove(self.do_iteration_timer)
        self.do_iteration_timer = None

    def on_clicked_refresh_timer(self, button, refresh_time):
        if button.get_active():
            # print(refresh_time)
            if refresh_time == "Disabled":
                self.disable_auto_refresh()
                self.save_key_in_config_file("refresh_freq", "0")
            else:
                if refresh_time == "15 sec":
                    self.refresh_freq = 15
                elif refresh_time == "1 min":
                    self.refresh_freq = 60
                elif refresh_time == "1 hour":
                    self.refresh_freq = 60*60
                self.enable_auto_refresh()

    def on_clicked_item(self, button, interface):
        if button.get_active():
            if interface.name != self.last_clicked_interface or self.last_clicked_interface is None:
                # copy to clipboard the ip
                self.clipboard.set_text(interface.ip, -1)
                # print("'%s' copied to clipboard" % interface.ip)
                # update the label so we see the selected ip
                self.indicator.set_label(str(interface.ip), str(interface.ip))
                self.show_notification(str(interface.ip), "copied to clipboard")
                self.last_clicked_interface = interface.name
                self.save_key_in_config_file("last_clicked_interface", self.last_clicked_interface)

    @staticmethod
    def show_notification(title, message):
        Notify.init('indicator-ip')
        n = Notify.Notification.new(title, message)
        n.show()

    @staticmethod
    def load_config_file():
        """
        Load the config file.
        Create the config file if not exist
        """
        config_folder = os.path.dirname(CONFIG_FILE_PATH)
        if not os.path.exists(config_folder):
            # create folders
            path = Path(config_folder)
            path.mkdir(parents=True)

        if not os.path.isfile(CONFIG_FILE_PATH):
            # Create the configuration file as it doesn't exist yet
            config = ConfigParser()
            config.add_section('main')
            config.set('main', 'refresh_freq', '0')
            config.set('main', 'last_clicked_interface', 'public')
            with open(CONFIG_FILE_PATH, 'w') as config_file:
                config.write(config_file)

        config = ConfigParser()
        config.read(CONFIG_FILE_PATH)
        return config

    @staticmethod
    def save_key_in_config_file(key, value):
        config = ConfigParser()
        config.read(CONFIG_FILE_PATH)
        config.set('main', key, value)
        with open(CONFIG_FILE_PATH, 'w') as config_file:
            config.write(config_file)
