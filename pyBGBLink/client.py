# pyBGBLink/client.py
#
#Copyright 2020 @digital-pet
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import asyncio
import logging

from .peers import Peer

class Client:
    """A simple BGBLink compatible client.
    """
    def __init__(self, peerClass = Peer):
        """Initializes the Client class.

        Args:
            peerClass (Peer, optional): The peer class to be used for this connection. Defaults to Peer.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.PeerClass = peerClass
        self.peer = None

    def send_packet(self, raw_packet):
        """Sends a single packet to the connected peer, or discards it if no peers are connected.

        Args:
            raw_packet (Bytes): An assembled BGBLink packet
        """
        if self.peer:
            self.peer.send_packet(raw_packet)
            
    async def connect(self, host, port):
        """Connects to a server.

        Args:
            host (str): Server hostname or IP address
            port (int): Server port number
        """
        self.host = host
        self.port = port
        while not self.peer:
            self.logger.info('Connecting to server %s:%s', self.host, self.port)
            try:
                reader, writer = await asyncio.open_connection(host, port)
                self.peer = self.PeerClass(reader, writer, None)                
            except ConnectionRefusedError:
                self.logger.info('Connection refused, trying again in 1 second')
                await asyncio.sleep(1)
        self.logger.info('Client connected to server %s', self.peer.name)

        loop = asyncio.get_event_loop()
        rtask = loop.create_task(self.peer._read_loop())
        wtask = loop.create_task(self.peer._write_loop())

        while not rtask.done():
            await asyncio.sleep(0.1)

        wtask.cancel()
        self.logger.info('Client disconnected from server %s', self.peer.name)
        self.peer = None