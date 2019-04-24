import netifaces
import requests

from indicator_ip.interface import Interface


class NetUtils(object):

    current_public_ip = None
    NO_IP = '---.---.---.---'
    DEFAULT_PROVIDER = "https://checkip.amazonaws.com"

    @classmethod
    def get_all_interface(cls):
        returned_list = list()

        all_interface = netifaces.interfaces()
        for interface_name in all_interface:
            addrs = netifaces.ifaddresses(interface_name)
            if netifaces.AF_INET in addrs and addrs[netifaces.AF_INET] is not None:
                interface_ip = addrs[netifaces.AF_INET][0]["addr"]
                netmask = addrs[netifaces.AF_INET][0]["netmask"]
                cidr = sum(bin(int(x)).count('1') for x in netmask.split('.'))
                returned_list.append(Interface(name=interface_name,
                                               ip=interface_ip,
                                               cidr=cidr))

        returned_list.append(cls.get_public_interface())

        return returned_list

    @classmethod
    def get_public_interface(cls):
        return Interface(name="public", ip=cls.get_public_ip())

    @classmethod
    def get_public_ip(cls):

        if cls.current_public_ip is None:
            try:
                r = requests.get(cls.DEFAULT_PROVIDER, timeout=5)
                cls.current_public_ip = r.text.rstrip("\n\r")
                return cls.current_public_ip
            except requests.exceptions.Timeout:
                return cls.NO_IP
        else:
            return cls.current_public_ip
