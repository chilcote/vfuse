vfuse
====

This script takes a never-booted DMG and converts it to a VMware Fusion VM.  

The germ of this idea came about, as all good ideas, and germs, do: while drinking beer. Specifically, I was tossing back drinks and tossing around ideas with [Gilbert Wilson](https://twitter.com/boyonwheels), and he mentioned that he uses the VMware CLI tools to convert DMGs to VMDKs based on a [blog post](http://hazenet.dk/2013/07/17/creating-a-never-booted-os-x-template-in-vsphere-5-1/6/) he'd read.  Intrigued, I asked Gil to email me the specifics.  After seeing how potentially cool this was, I wrapped it up in this here terribly illegible, queasingly unpythonic script.  

My thanks to [Rich Trouton](https://twitter.com/rtrouton) for testing this script for me and providing feedback. He is a saint among humans.  

Requirements
------------

+ VMware Fusion 7.x Professional  
+ OS X 10.9.5+ (compatible with 10.10)  
+ A never-booted image created with your [favorite](https://github.com/chilcote/stew) [image creation tool](https://github.com/magervalp/autodmg).  
+ I've only tested with 10.9.5 and 10.10. YMMV  

Usage
-----

    usage: vfuse [-h] [-i INPUT] [-o OUTPUT] [-n NAME] [-w HW_VERSION]
                 [-t TEMPLATE]

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            /path/to/dmg
      -o OUTPUT, --output OUTPUT
                            /path/to/output/dir
      -n NAME, --name NAME  custom name
      -w HW_VERSION, --hw-version HW_VERSION
                            VMware hardware version
      -m MEM_SIZE, --mem-size MEM_SIZE
                            Memory Size in MB
      -t TEMPLATE, --template TEMPLATE
                            use a template

Creating a VM
-------------

Running `vfuse` does not necessarily require sudo rights, but if you don't want to be prompted in the GUI for an admin password, run it with `sudo`. Escalated privileges is required to run the `vmware-vdiskmanager` binary, which `vfuse` uses.

The only required argument is `-i` aka `--input`. Run thusly, it will create a vm called `osx-vm.vmwarevm` in the current working directory:

    sudo ./vfuse -i /path/to/OSX10.9.5_13F34.dmg

If you give it a URL, it will mount the dmg over the network.

    sudo ./vfuse -i http://org.server.com/path/to/dmg

Alternatively, you can redirect the output directory, and/or give your VM a specific name:

    sudo ./vfuse -i ~/Downloads/OSX10.9.5_13F34.dmg -o ~/vmtesting -n osx-mav

To use a custom `virtualHW.version` setting, i.e. for use with ESXi, use the `-w` argument

    sudo ./vfuse -i ~/Downloads/OSX10.9.5_13F34.dmg -o ~/vmtesting -n osx-mav -w 10


Templates
---------

Templates are simple json files that allow for automation and version control.  The templating format is simple:  

    {
        "input": "/path/to/dmg",
        "output": "/path/to/output/dir",
        "name": "custom-name",
        "cache": false,
        "hw_version": 11,
        "mem_size": 2048
    }

If you are using an http resource for the source DMG and cache is `true`, vfuse will cache the DMG in ~/.vfuse/ and will consult that directory before downloading the dmg again.  


License
-------

    Copyright 2014 Joseph Chilcote
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
