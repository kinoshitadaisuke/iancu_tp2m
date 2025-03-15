# iancu_tp2m

Some testing codes for the telescope construction project at IANCU.

- test_socket_00_server.py, test_socket_00_client.py
  - one-way communication between server and client using socket
- test_socket_01_server.py, test_socket_01_client.py
  - one-way communication between server and client using socket
  - server keeps waiting for connections from client
- test_socket_02_server.py, test_socket_02_client.py
  - two-way communication between server and client using socket
  - server replys to client after a connection from client
- test_socket_00_server.py, test_socket_00_client.py
  - server handles multiple connections from client using threading
