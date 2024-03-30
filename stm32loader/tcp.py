# Author: Floris Lambrechts, Jeroen van Straten
# GitHub repository: https://github.com/florisla/stm32loader
#
# This file is part of stm32loader.
#
# stm32loader is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3, or (at your option) any later
# version.
#
# stm32loader is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with stm32loader; see the file LICENSE.  If not see
# <http://www.gnu.org/licenses/>.

"""
Handle remote RS-232 serial communication through a serial-to-network
interface.

Toggling RESET and BOOT0 is not possible this way, but stubs are provided for
compatibility with SerialConnection.
"""

# Note: this file not named 'serial' because that name-clashed in Python 2


import socket


class TcpConnection:
    """Wrap a TCP connection."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, address):
        """Construct a TcpConnection (not yet connected)."""
        self.address = address

        self.swap_rts_dtr = False
        self.reset_active_high = False
        self.boot0_active_low = False

        # don't connect yet; caller should use connect() separately
        self.tcp_connection = None

        self._timeout = 5

    @property
    def timeout(self):
        """Get timeout."""
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        """Set timeout."""
        self._timeout = timeout
        if self.tcp_connection:
            self.tcp_connection.settimeout(self._timeout)

    def connect(self):
        """Connect to the UART serial port."""
        self.tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip, port = self.address.rsplit(':', maxsplit=1)
        ip = ip.strip('[]')
        port = int(port)
        self.tcp_connection.settimeout(self._timeout)
        self.tcp_connection.connect((ip, port))

    def disconnect(self):
        """Close the connection."""
        if not self.tcp_connection:
            return

        self.tcp_connection.close()
        self.tcp_connection = None

    def write(self, *args, **kwargs):
        """Write the given data to the serial connection."""
        return self.tcp_connection.send(*args, **kwargs)

    def read(self, amount=1):
        """Read the given amount of bytes from the serial connection."""
        data = b''
        while len(data) < amount:
            new_data = self.tcp_connection.recv(amount - len(data))
            if not new_data:
                break
            data += new_data
        return data

    def enable_reset(self, enable=True):
        pass

    def enable_boot0(self, enable=True):
        pass

    def flush_imput_buffer(self):
        pass
