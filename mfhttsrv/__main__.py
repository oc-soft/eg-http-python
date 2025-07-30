import http.server
import socket
from .request.handler import Handler


port_number = 8000

addres_info_list = socket.getaddrinfo(None, port_number)



# http.server.ThreadingHttpServer.address


# vi: se ts=4 sw=4 et:
