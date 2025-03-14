#!/usr/pkg/bin/python3.13

#
# Time-stamp: <2025/03/14 12:37:13 (UT+08:00) daisuke>
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
descr  = f'server program for socket communication'
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

# parsing arguments
args = parser.parse_args ()

# arguments
server_address = args.server
server_port    = args.port
maxlength      = args.maxlength

###########################################################################

###########################################################################

#
# communication with client using socket
#

# opening socket
with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as skt:
    # binding socket
    skt.bind ( (server_address, server_port) )
    # starting to listen to client
    skt.listen ()
    # accepting connection
    connection, address = skt.accept ()
    # receiving message from client
    data_from_client_byte = connection.recv (maxlength)
    # converting message from client into UTF-8 string
    data_from_client_str = data_from_client_byte.decode ('utf-8')
    # printing received message
    print (f'Message received from client:')
    print (f'{data_from_client_str}')

###########################################################################
