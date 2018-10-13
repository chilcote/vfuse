vfuse
====

This script takes a never-booted DMG and converts it to a VMware Fusion VM.

The germ of this idea came about, as all good ideas, and germs, do: while drinking beer. Specifically, I was tossing back drinks and tossing around ideas with [Gilbert Wilson](https://twitter.com/boyonwheels), and he mentioned that he uses the VMware CLI tools to convert DMGs to VMDKs based on a [blog post](http://hazenet.dk/2013/07/17/creating-a-never-booted-os-x-template-in-vsphere-5-1/6/) he'd read.  Intrigued, I asked Gil to email me the specifics.  After seeing how potentially cool this was, I wrapped it up in this here terribly illegible, queasingly unpythonic script.

My thanks to [Rich Trouton](https://twitter.com/rtrouton) for testing this script for me and providing feedback. He is a saint among humans.

Requirements
------------

+ VMware Fusion 10.x Professional
+ OS X 10.9.5+
+ A never-booted image created with [AutoDMG](https://github.com/magervalp/autodmg).
+ (optional) [Packer](https://packer.io) 1.1.1 (or above) for building a vagrant box.
+ (optional) [qemu-img](https://en.wikibooks.org/wiki/QEMU/Installing_QEMU)

Usage
-----

    usage: vfuse [-h] [-i INPUT] [-o OUTPUT] [-n NAME] [-w HW_VERSION]
                [-m MEM_SIZE] [-s [SERIAL]] [-t TEMPLATE] [-e] [-p PACKER] [-d D]
                [--hw-model HW_MODEL] [--start [START]] [--stop STOP]
                [--reset RESET] [--use-qemu] [--recovery] [--snapshot]
                [--snapshot-name SNAPSHOT_NAME] [-c CHECKSUM]

    Create and monitor VM from source DMG.

    optional arguments:
    -h, --help            show this help message and exit
    -i INPUT, --input INPUT
                            /path/to/dmg
    -o OUTPUT, --output OUTPUT
                            /path/to/output/dir
    -n NAME, --name NAME  Use a custom name
    -w HW_VERSION, --hw-version HW_VERSION
                            VMware hardware version
    -m MEM_SIZE, --mem-size MEM_SIZE
                            Memory Size in MB
    -s [SERIAL], --serial [SERIAL]
                            Custom Serial number
    -t TEMPLATE, --template TEMPLATE
                            Use a template
    -e, --esx             Create pre-allocated ESX-type VMDK
    -p PACKER, --packer PACKER
                            Populate a packer template
    -d D                  Path to CD/DVD ISO path
    --hw-model HW_MODEL   Custom hardware model
    --start [START]       Start monitoring of VM
    --stop STOP           Stop monitoring of VM
    --reset RESET         Reset monitored VM
    --use-qemu            Use qemu-img intead of the Fusion CLI tools
    --recovery            Boot into Recovery HD
    --snapshot            Create initial snapshot
    --snapshot-name SNAPSHOT_NAME
                            Custom name for the initial snapshot
    -c CHECKSUM, --checksum CHECKSUM
                            Generate checksum of a DMG

Creating a VM
-------------

Running `vfuse` does not necessarily require sudo rights, but if you don't want to be prompted in the GUI for an admin password, run it with `sudo`. Escalated privileges is required to run the `vmware-vdiskmanager` binary, which `vfuse` uses.

The only required argument is `-i` aka `--input`. Run thusly, it will create a vm called `macos-vm.vmwarevm` in the current working directory:

    /usr/local/vfuse/bin/vfuse -i /path/to/dmg

See the [wiki](https://github.com/chilcote/vfuse/wiki) for more on how to use `vfuse`.

Monitoring a VM
---------------

If you wish to utilize `vfused` to monitor and manage VMs, create a separate pkg for the LaunchAgent in the extras folder. This is no longer included in the `vfuse` pkg since LaunchAgents are better left to config management anyway.

Caveats
-------

`vfuse` is meant to be used with never-booted disk images created with [AutoDMG](https://github.com/magervalp/autodmg). That said, you should be able to use `vfuse` with a dmg created with Disk Utility. Be aware, however, that testing has shown that it is best if you use the "Disk Image from Folder" method rather than "Disk Image from (Select a Device)" in Disk Utility, as the latter may result in errors when converting the disk to a vmdk.

License
-------

    Copyright 2016-Present Joseph Chilcote
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
