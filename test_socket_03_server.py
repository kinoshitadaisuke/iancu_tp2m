#!/usr/pkg/bin/python3.13

#
# Time-stamp: <2025/03/14 12:37:54 (UT+08:00) daisuke>
#

###########################################################################

#
# importing modules
#

# importing argparse module
import argparse

# importing socket module
import socket

# importing threading module
import threading

# importing time module
import time

###########################################################################

###########################################################################

#
# parameters
#

# file to store telescope status
file_status = 'status.txt'

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
# functions
#

def is_valid_command (command):
    # initialisation of parameter 'valid'
    valid = False
    # splitting command
    list_command = command.split ()
    # checking command
    match list_command[0]:
        case 'gohome' | 'goflatscreen' | 'pointing' | 'status' | 'tracking':
            valid = True
        case _:
            valid = False
    # return validity of command
    return valid

def write_status (filename, telescope_status):
    with open (filename, 'w') as fh_w:
        fh_w.write (f'{telescope_status}\n')
    return (0)

def read_status (filename):
    with open (filename, 'r') as fh_r:
        telescope_status = fh_r.read ()
    return (telescope_status)

def execute_gohome (command):
    print (f'Now, going to home position...')
    write_status (file_status, f'status: busy (moving to home position)\n')
    time.sleep (15)
    write_status (file_status, f'status: idling\n')
    print (f'Finished going to home position!')
    return (0)

def execute_goflatscreen (command):
    print (f'Now, going to flatfield screen...')
    write_status (file_status, f'status: busy (moving to flatfield screen)\n')
    time.sleep (15)
    write_status (file_status, f'status: idling\n')
    print (f'Finished going to flatfield screen!')
    return (0)

def execute_pointing (command):
    print (f'Now, pointing telescope to the target...')
    write_status (file_status, f'status: busy (pointing target object)\n')
    time.sleep (15)
    write_status (file_status, f'status: idling\n')
    print (f'Finished pointing telescope to the target!')
    return (0)

def execute_status (command):
    print (f'Now, checking telescope status')
    # checking telescope status
    telescope_status = read_status (file_status)
    print (f'Finished checking telescope status!')
    return (telescope_status)

def execute_tracking (command):
    print (f'Now, changing tracking mode...')
    write_status (file_status, f'status: busy (changing tracking mode)\n')
    time.sleep (5)
    write_status (file_status, f'status: idling\n')
    print (f'Finished changing tracking mode!')
    return (0)

def process_request_from_client (connection, address):
    # connecting with client
    with connection:
        # receiving message from client
        data_from_client_byte = connection.recv (maxlength)
        # converting message from client into UTF-8 string
        data_from_client_str = data_from_client_byte.decode ('utf-8')
        # printing received message
        print (f'Message received from client:')
        print (f'{data_from_client_str}')
        # checking validity of command
        valid = is_valid_command (data_from_client_str)
        # message sent back to client
        if (valid):
            message_str = f'following command received:\n' \
                + f'{data_from_client_str}\n'
        else:
            message_str = f'command is invalid!\n' \
                + f'{data_from_client_str}'
        # conversion from string into byte
        message_byte = message_str.encode ()
        # sending a message back to client
        connection.sendall (message_byte)
        # executing command
        list_command = data_from_client_str.split ()
        match list_command[0]:
            case 'gohome':
                execute_gohome (data_from_client_str)
            case 'goflatscreen':
                execute_goflatscreen (data_from_client_str)
            case 'pointing':
                execute_pointing (data_from_client_str)
            case 'status':
                telescope_status = execute_status (data_from_client_str)
                telescope_status_byte = telescope_status.encode ()
                connection.sendall (telescope_status_byte)
            case 'tracking':
                execute_tracking (data_from_client_str)
                
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
    # waiting for connection from client
    while (True):
        # accepting connection
        connection, address = skt.accept ()
        # starting a new thread and processing request from client
        thread = threading.Thread (target=process_request_from_client, \
                                   args=(connection, address) )
        thread.start ()

###########################################################################
