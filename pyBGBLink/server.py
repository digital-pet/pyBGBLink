# pyBGBLink/server.py
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

from .peers import Peer, ProxyPeer

class Server:
    def __init__(self, host, port, peerClass = Peer):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.host = host
        self.port = port
        self.PeerClass = peerClass
        self.peers = {}
        self.connLock = asyncio.Lock()
        self.nextID = 0

    async def _on_client_connected(self, reader, writer):
        
        async with self.connLock:
            i = self.nextID
            self.nextID += 1
        newPeer = self.PeerClass(reader, writer, i)
        self.peers[i] = newPeer
        self.logger.info('Client id %s (%s) connected',newPeer.id, newPeer.name)


        loop = asyncio.get_event_loop()
        rtask = loop.create_task(newPeer._read_loop())
        wtask = loop.create_task(newPeer._write_loop())
        
        while not rtask.done():
            await asyncio.sleep(0.1)
        
        wtask.cancel()
        self.logger.info('Client id %s (%s) disconnected',newPeer.id, newPeer.name)
        del self.peers[i]

    def send_packet(self, raw_packet, peerID = None, invert = False):
        if peerID == None:
            for i in self.peers:
                self.peers[i].send_packet(raw_packet)
        elif invert == True:
            for i in self.peers:
                if i != peerID:
                    self.peers[i].send_packet(raw_packet)
        else:
            self.peers[peerID].send_packet(raw_packet)

    async def start(self):
        await asyncio.start_server(self._on_client_connected, self.host, self.port)
        self.logger.info('Server listening on %s:%s',self.host,self.port)
        
class ProxyServer(Server):
    def __init__(self, host, port, peerClass = ProxyPeer):
        super().__init__(host, port, peerClass)