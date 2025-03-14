#!/usr/pkg/bin/python3.13

#
# Time-stamp: <2025/03/14 12:37:38 (UT+08:00) daisuke>
#

###########################################################################

#
# importing modules
#

# importing argparse module
import argparse

# importing socket module
import socket

###########################################################################

###########################################################################

#
# command-line argument analysis
#

# initialising a parser object
descr  = f'client program for socket communication'
parser = argparse.ArgumentParser (description=descr)

# default values
default_server    = '192.168.29.50'
default_port      = 12345
default_maxlength = 256

# adding arguments
parser.add_argument ('-s', '--server', default=default_server, \
                     help=f'IP address of server (default: {default_server})')
parser.add_argument ('-p', '--port', default=default_port, \
                     help=f'port number on server (default: {default_port})')
parser.add_argument ('-l', '--maxlength', default=default_maxlength, \
                     help=f'maximum length of message (default: {default_maxlength})')
parser.add_argument ('command', nargs='+', \
                     help=f'command to be sent to server')

# parsing arguments
args = parser.parse_args ()

# arguments
server_address = args.server
server_port    = args.port
maxlength      = args.maxlength
list_command   = args.command

###########################################################################

#
# constructing a command to be sent to server
#

# initialisation of command to be sent to server
command_to_server_str = ''

# making a command
for i in range ( len (list_command) ):
    command_to_server_str = f'{command_to_server_str} {list_command[i]}'

# removing leading white space
command_to_server_str = command_to_server_str.lstrip ()

# conversion from string into byte
command_to_server_byte = command_to_server_str.encode ()

###########################################################################

###########################################################################

#
# communication with server using socket
#

# opening socket
with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as skt:
    # connecting to server
    skt.connect ( (server_address, server_port) )
    # sending a message to server
    skt.sendall (command_to_server_byte)

###########################################################################
