# SampleClient.py
#
#Copyright 2020 @digital-pet
#
#Permission is hereby granted, free of charge, for anyone to use, distribute, or
#sell the compiled binaries, source code, and documentation (the "Software")
#provided they grant all contributors to this project immortality.
#
#The Software is provided in the hope that some will find it useful, but the
#Software comes under NO WARRANTY, EXPRESS OR IMPLIED, and the authors of the
#Software are NOT LIABLE IN THE EVENT OF LOSSES, DAMAGES OR MISUSE relating to
#the Software.

import pyBGBLink
import asyncio
import logging
import os

########################################################################
# This script is a sample showing how to use this library
# It will send a ~25ms long down button press to the connected
# BGB instance roughly every second until it is killed.
#
# You should launch your BGB instance with the command line:
#   "bgb64.exe -listen 127.0.0.1:12800"
########################################################################

logging.basicConfig(filename='test.log', encoding='utf-8', level=logging.DEBUG)

client = pyBGBLink.Client()

async def send_button_forever(client):
    #instantiate the packets
    DownPacket = pyBGBLink.JoypadPacket()
    UpPacket = pyBGBLink.JoypadPacket()

    #set the packet flags appropriately
    DownPacket.button = DownPacket.defines.B_DOWN
    UpPacket.button = UpPacket.defines.B_DOWN
    DownPacket.isPressed = True

    while True:
        await asyncio.sleep(1)
        client.send_packet(DownPacket.assemble())
        await asyncio.sleep(0.025)
        client.send_packet(UpPacket.assemble())

#main program code
async def main():
    await asyncio.gather(
        client.connect('127.0.0.1',12800),
        send_button_forever(client))

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Ctrl-C received, quitting immediately')
    logging.critical('Ctrl-C received, quitting immediately')
    os._exit(1)
except Exception:
    logging.error("Fatal error in main loop", exc_info=True)
    os._exit(2)
