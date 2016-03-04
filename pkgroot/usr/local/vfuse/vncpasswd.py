#!/usr/bin/python

##############################################################################
# Copyright 2016 Joseph Chilcote
# 
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License. You may obtain a copy
#  of the License at
# 
#       http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
##############################################################################

# Based on code originated by Michael Lynn: https://gist.github.com/pudquick/1bff29ea56a93089dcfc
## A python implementation of https://communities.vmware.com/docs/DOC-7535
## "Compute hashed password for use with RemoteDisplay.vnc.key"
# d3des library by Yusuke Shinyama: https://vnc2flv.googlecode.com/svn-history/r2/trunk/vnc2flv/vnc2flv/d3des.py

__author__  = 'Joseph Chilcote (chilcote@gmail.com)'
__version__ = '1.0.0'

from d3des import deskey
import sys, base64, struct

def generate_vncpassword(password):
    # Passwords are 8 characters max, unused bytes are filled with null
    c_password = (password + '\x00'*8)[:8]
    encrypted = deskey(c_password, False)
    # Convert bytes to raw buffer
    encrypted_bytes = struct.pack('i'*32, *encrypted)
    # Convert to base64 encoding
    encrypted_string = base64.b64encode(encrypted_bytes)
    # Print resulting ecrypted string encases in double quotes
    print '"%s"' % encrypted_string

if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print "Usage: vncpasswd.py <passphrase> <output path>"
    else:
        generate_vncpassword(sys.argv[1])
