#!/usr/bin/env bash

# cleanup
echo "cleanup"
sudo rm -rf build
sudo rm -rf deb_dist
sudo rm -rf dist
sudo rm -rf indicator_ip.egg-info
sudo rm -rf tmp
sudo rm -rf indicator-ip-*.tar.gz

# build
echo "#########"
echo "# build #"
echo "#########"
python setup.py --command-packages=stdeb.command bdist_deb

# source package
echo "###########################################"
echo "# create launchpad compliant source package"
echo "###########################################"
mkdir tmp
cd tmp
dpkg-source -x ../deb_dist/indicator-ip_*.dsc
sed -i 's/unstable/bionic/g' indicator-ip*/debian/changelog
cd indicator-ip*/
debuild -S -sa

# push to launchpad
# dput -f ppa:nico-marcq/indicator-ip indicator-ip_*_source.changes

