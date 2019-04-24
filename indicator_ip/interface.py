

class Interface(object):
    """
    Abstract base class that represents a network interface.
    """

    def __init__(self, ip=None, name=None, cidr=None) -> None:
        super().__init__()

        self.name = name
        self.ip = ip
        self.cidr = cidr

    def __str__(self):
        if self.cidr is not None:
            return "{0}: {1}/{2}".format(self.name, self.ip, self.cidr)
        else:
            return "{0}: {1}".format(self.name, self.ip)
