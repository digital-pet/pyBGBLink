# SampleServer.py
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

import pyBGBLink
import asyncio
import logging
import os

########################################################################
# This script is a sample showing how to use this library
# It will send a ~25ms long down button press to all connected
# BGB instances roughly every second until it is killed.
#
# You should launch your BGB instance with the command line:
#   "bgb64.exe -connect 127.0.0.1:12800"
########################################################################

logging.basicConfig(filename='test.log', encoding='utf-8', level=logging.DEBUG)

server = pyBGBLink.Server('127.0.0.1',12800)

async def send_button_forever(server):
    #instantiate the packets
    DownPacket = pyBGBLink.JoypadPacket()
    UpPacket = pyBGBLink.JoypadPacket()
    
    #set the packet flags appropriately
    DownPacket.button = DownPacket.defines.B_DOWN
    UpPacket.button = UpPacket.defines.B_DOWN
    DownPacket.isPressed = True
    
    while True:
        await asyncio.sleep(1)
        server.send_packet(DownPacket.assemble())
        await asyncio.sleep(0.025)
        server.send_packet(UpPacket.assemble())

# standard asyncio code to start the server and the send_button_forever loop
loop = asyncio.get_event_loop()
asyncio.ensure_future(server.start())
asyncio.ensure_future(send_button_forever(server))
try:
    loop.run_forever()
except KeyboardInterrupt:
    print('Ctrl-C received, quitting immediately')
    logging.critical('Ctrl-C received, quitting immediately')
    os._exit(1)
except Exception:
    logging.error("Fatal error in main loop", exc_info=True)
    os._exit(2)