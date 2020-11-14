# PyBGBLink
A python implementation of the [BGB gameboy emulator](https://bgb.bircd.org/)'s link protocol using asyncio.  
 
Based on existing [protocol documentation](https://bgb.bircd.org/bgblink.html) and a healthy amount of trial and error.  

## Current functionality:  
Server class accepts client connections and handshakes, then holds connection open and sends injected packets (generally joypad packets)  
Client class connects to server and handshakes, and then holds connection open and sends injected packets  

## Planned functionality:  
ProxyServer class will automatically match connected ProxyPeer clients, while still allowing for packet injection  
  
## Possible future projects:  
DMG-07 4-player link cable emulation 

## Versioning
This project follows the tradition of "funny numbers" rather than any formalized versioning system. Numbers will count up, bigger numbers mean newer.
