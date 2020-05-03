# Indicator IP

Ubuntu indicator that displays local and external IP addresses in your task bar.

![screenshoot](indicator_ip/images/screenshot.png)

## Installation

Ubuntu 20.04:
```
sudo add-apt-repository ppa:nico-marcq/indicator-ip
sudo apt-get update
sudo apt-get install python3-indicator-ip
```

Then run
```
indicator-ip
```

## Dev environment installation

Install system packages
```
sudo apt-get install gcc python3-dev python3-gi python3-gi-cairo libcairo2-dev \
libjpeg-dev libgif-dev gir1.2-gtk-3.0 gobject-introspection libgirepository1.0-dev pkg-config gir1.2-appindicator3-0.1
```

Install python package
```
sudo pip install -r requirement.txt
```

You can then execute the entry point
```
python3 indicator-ip.py
```
