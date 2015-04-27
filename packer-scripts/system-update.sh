#/bin/bash

# fork of Tim Sutton's osx-vm-template script:
# https://github.com/timsutton/osx-vm-templates/blob/master/scripts/system-update.sh

if [ "$UPDATE_SYSTEM" != "true" ] && [ "$UPDATE_SYSTEM" != "1" ]; then
  exit
fi

echo "Downloading and installing system updates..."
softwareupdate -i -a
