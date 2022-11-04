# Push to PPA

Install required packages
```
apt-get install python3-stdeb build-essential devscripts dh-python
```

Build
```
python3 setup.py --command-packages=stdeb.command bdist_deb
```

Launchpad reject a build that contains both source and binary. We need to generate only the source package
```
mkdir tmp
cd tmp
dpkg-source -x ../deb_dist/indicator-ip_1.0-1.dsc
```

Update the version
```
sed -i 's/unstable/jammy/g' debian/changelog
```

Build and sign the source package
```
debuild -S -sa
```

Push to ppa
```
dput -f ppa:nico-marcq/indicator-ip tmp/indicator-ip_1.0-1_source.changes
```

The GPG key that signed the package need to be available on Ubuntu key servers
```
gpg --keyserver keyserver.ubuntu.com --send-key <key id>
```