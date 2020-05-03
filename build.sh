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
python3 setup.py --command-packages=stdeb.command bdist_deb

# source package
echo "###########################################"
echo "# create launchpad compliant source package"
echo "###########################################"
mkdir tmp
cd tmp
dpkg-source -x ../deb_dist/indicator-ip_*.dsc

# update info to be Ubuntu ready
sed -i 's/unstable/focal/g' indicator-ip*/debian/changelog

# add system dependencies
sed -i 's/Depends: ${misc:Depends}, ${python3:Depends}/Depends: ${misc:Depends}, ${python3:Depends}, gir1.2-appindicator3-0.1/g' indicator-ip*/debian/control

# final build
cd indicator-ip*/
debuild -S -sa

# push to launchpad
# dput -f ppa:nico-marcq/indicator-ip indicator-ip_*_source.changes

