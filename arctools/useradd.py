#!/usr/bin/python3

import sys
import textwrap
from optparse import OptionParser, OptionError
import requests
import json
from base64 import encodebytes

consul_server = 'localhost'
consul_port = '8500'


def main():
    try:
        usage = textwrap.dedent("""
           %prog [OPTIONS] uniquename

           eg: %prog -a brockp -s flux -u 12345 -g 54321 -m -c "Brock Palen" -s "/bin/tcsh"
           """)
        parser = OptionParser(usage=usage)
        parser.add_option("-a", "--arcuser", dest="arcuser",
                          help="Username for user eg: brockp")
        parser.add_option("--service", dest="service",
                          help="Service to add user to Eg: flux")
        parser.add_option("-u", "--uid", dest="uid",
                          help="The unix user ID")
        parser.add_option("-g", "--gid", dest="gid",
                          help="The group ID (not name) to add the user to")
        parser.add_option("-c", "--comment", dest="comment",
                          help="The user's full name")
        parser.add_option("-s", "--shell", dest="shell",
                          default="/bin/bash",
                          help="User Shell Default: /bin/bash")
        parser.add_option("-b", "--base-dir", dest="basedir",
                          default="/home",
                          help="Base path for $HOME Default: %default")
        parser.add_option("-m", "--create-home", action="store_true",
                          dest="verbose")
        (options, args) = parser.parse_args()
        to_consul(options, args)

    except OptionError as err:
        print(err)
        parser.print_help()
        sys.exit(2)


def to_consul(options, args):
    # See: https://www.consul.io/api/txn.html
    prefix = "arcusers/users/"+options.arcuser
    payload = []
    payload.append(consul_payload(
                   prefix+"/common/commonName",
                   options.comment))
    payload.append(consul_payload(
                   prefix+"/common/uid",
                   options.uid))
    payload.append(consul_payload(
                   prefix+"/"+options.service+"/gid",
                   options.gid))
    payload.append(consul_payload(
                   prefix+"/"+options.service+"/homedir",
                   options.basedir+"/testuser"))
    payload.append(consul_payload(
                   prefix+"/"+options.service+"/shell",
                   options.shell))

    server_addr = "http://"+consul_server+":"+consul_port+"/v1/txn"
    r = requests.put(server_addr, data=json.dumps(payload))
    print(r.text)


def consul_b64encoded(string):
    encoded = encodebytes(str.encode(string))
    return encoded.decode('utf-8')


def consul_payload(key, value):
    payload = {"KV":
               {
                "Verb": "set",
                "Key": key,
                "Value": consul_b64encoded(value)
               }
               }

    return payload


if __name__ == "__main__":
    main()
