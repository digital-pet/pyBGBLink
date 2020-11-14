# pyBGBLink/peers.py
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
#

import asyncio

from .protocol import BGBProtocol, VersionPacket, StatusPacket

class Peer(BGBProtocol):
    """A basic BGBLink-compatible peer.

    Args:
        reader (asyncio.streams.Reader): The reader associated with this connection.
        writer (asyncio.streams.Writer): The writer associated with this connection.
        PeerID (int or None): The ID of this peer when in server mode

    Inherits:
        BGBProtocol
    """
    def __init__(self, reader, writer, PeerID):
        self.active = True
        super().__init__()
        self.reader = reader
        self.writer = writer
        self.id = PeerID
        self.name = writer.get_extra_info('peername')
        self.ownstatus = self.defines.S_SUPPORT_WANTDISCONNECT
        self.peerstatus = None
        self.outQ = asyncio.Queue()

        # version packet should be sent immediately
        version = VersionPacket()
        self.send_packet(version)        

    async def _read_loop(self):
        """The asynchronous read loop.
        """
        while self.active:
            try:
                buffer = await self.reader.readexactly(8)
                self._on_packet_received(buffer)
            except asyncio.exceptions.IncompleteReadError:
                self.logger.error('IncompleteReadError encountered from peer id %s (%s).', self.id, self.name)
                break
            except ConnectionResetError:
                self.logger.error('Connection reset unexpectedly with peer id %s (%s).', self.id, self.name)
                break
        self.writer.close()
        self.active = False
        
    async def _write_loop(self):
        """The asynchronous write loop.
        """
        while self.active:
            raw_packet = await self.outQ.get()
            self.writer.write(raw_packet)
            await self.writer.drain()
            self.outQ.task_done()

    def _on_version(self, packet):
        """The handler for VersionPacket packets

        Args:
            packet (pyBGBLink.protocol.VersionPacket): A VersionPacket object
        """
        super()._on_version(packet)
        if (packet.b1 != self.defines.MAJOR_VER) or (packet.b2 != self.defines.MINOR_VER):
            self.logger.error('Incompatible version of protocol (MAJOR:%s, MINOR:%s) used by peer id %s (%s).', packet.b1, packet.b2, self.id, self.name)
            self.active = False

        status = StatusPacket()
        status.b1 = self.ownstatus
        self.send_packet(status)

    def _on_status(self, packet):
        """The handler for StatusPacket packets

        Args:
            packet (pyBGBLink.protocol.StatusPacket): A StatusPacket object
        """
        super()._on_status(packet)
        self.peerstatus = packet.b1

    def send_packet(self, raw_packet):
        """Schedules a packet to be sent to the connected peer.

        Args:
            raw_packet (Bytes): An assembled BGBLink packet
        """
        self.outQ.put_nowait(raw_packet)

class ProxyPeer(Peer):
    """ProxyPeer: A more advanced BGBLink Peer which proxies data to an associated peer if one if provided.

    Args:
        reader (Object, asyncio.streams.Reader): The reader associated with this connection.
        writer (Object, asyncio.streams.Writer): The writer associated with this connection.
        PeerID (int or None): The ID of this peer when in server mode

    Inherits:
        Peer
    """
    def __init__(self, reader, writer, PeerID):    
        super().__init__(reader, writer, PeerID)
        self.peer = None

    def _on_sync1(self, packet):
        """_on_sync1: The handler for Sync1Packet packets

        Args:
            packet (Object, pyBGBLink.protocol.Sync1Packet): A Sync1Packet object
        """
        super()._on_sync1(packet)
        if self.peer:
            self.peer.send_packet(packet)

    def _on_sync2(self, packet):
        """_on_sync2: The handler for Sync2Packet packets

        Args:
            packet (Object, pyBGBLink.protocol.Sync2Packet): A Sync2Packet object
        """
        super()._on_sync2(packet)
        if self.peer:
            self.peer.send_packet(packet)

    def _on_sync3(self, packet):
        """_on_sync3: The handler for Sync3Packet packets

        Args:
            packet (Object, pyBGBLink.protocol.Sync3Packet): A Sync3Packet object
        """
        super()._on_sync3(packet)
        if self.peer:
            self.peer.send_packet(packet)

    def _on_status(self, packet):
        """_on_status: The handler for StatusPacket packets

        Args:
            packet (Object, pyBGBLink.protocol.StatusPacket): A StatusPacket object
        """
        super()._on_status(packet)
        if self.peer:
            self.peer.send_packet(packet)
    
    def _on_want_disconnect(self, packet):
        """_on_want_disconnect: The handler for WantDiscoonectPacket packets

        Args:
            packet (Object, pyBGBLink.protocol.WantDisconnectPacket): A WantDisconnectPacket object
        """
        super()._on_want_disconnect(packet)
        if self.peer:
            self.peer.send_packet(packet)
            
    async def connect(self, peer):
        """connect: Connects two peers together to start proxying data

        Args:
            peer (Object, pyBGBLink.peers.Peer): A connected and active peer object
        """
        self.peer = peer
        status = StatusPacket()
        status.b1 = self.peerstatus or self.ownstatus
        self.peer.send_packet(status)
        asyncio.create_task(self._maintain_connection())
        
    async def _maintain_connection(self):
        """_maintain_connection: Asynchronously monitors the connection between peers
        """
        while self.peer:
            if not self.peer.active:
                self.peer = None
            asyncio.sleep(0.1)