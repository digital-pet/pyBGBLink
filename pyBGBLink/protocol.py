# pyBGBLink/protocol.py
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

import logging
from types import SimpleNamespace
from struct import *
from uint import Int as FixedInt

defines = SimpleNamespace(
            # version numbering
            MAJOR_VER                   = FixedInt(0x01, 8),
            MINOR_VER                   = FixedInt(0x04, 8),
            # valid commands
            C_VERSION                   = FixedInt(0x01, 8),
            C_JOYPAD                    = FixedInt(0x65, 8),
            C_SYNC1                     = FixedInt(0x68, 8),
            C_SYNC2                     = FixedInt(0x69, 8),
            C_SYNC3                     = FixedInt(0x6A, 8),
            C_STATUS                    = FixedInt(0x6C, 8),
            C_WANTDISCONNECT            = FixedInt(0x6D, 8)
            #button values (bits 0-2)
            B_RIGHT                     = FixedInt(0x00, 8),    #b'000'
            B_LEFT                      = FixedInt(0x01, 8),    #b'001'
            B_UP                        = FixedInt(0x02, 8),    #b'010'
            B_DOWN                      = FixedInt(0x03, 8),    #b'011'
            B_A                         = FixedInt(0x04, 8),    #b'100'
            B_B                         = FixedInt(0x05, 8),    #b'101'
            B_SELECT                    = FixedInt(0x06, 8),    #b'110'
            B_START                     = FixedInt(0x07, 8),    #b'111'
            #button pressed flag
            B_ISPRESSED                 = FixedInt(0x08, 8),    #bit 3
            #status bits
            S_ISRUNNING                 = FixedInt(0x01, 8),    #bit 0 
            S_ISPAUSED                  = FixedInt(0x02, 8),    #bit 1
            S_SUPPORT_WANTDISCONNECT    = FixedInt(0x04, 8))    #bit 2

class BGBProtocol:
    """ BGBProtocol: An implementation of the BGBLink protocol version 1.4 with v1.5 extensions

    Provides a dispatcher method and events for each packet type. This class is not designed to
    be instantiated directly but should be subclassed to provide the necessary functionality.

    Notes:
        Numbering of elements in this implementation starts at zero, while the official 
        protocol specification starts numbering elements at one.
    
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.defines = defines
        self.packets = {
            1 : VersionPacket,
            101 : JoypadPacket,
            104 : Sync1Packet,
            105 : Sync2Packet,
            106 : Sync3Packet,
            108 : StatusPacket,
            109 : WantDisconnectPacket}
        self.handlers = {
            1 : self._on_version,
            101 : self._on_joypad,
            104 : self._on_sync1,
            105 : self._on_sync2,
            106 : self._on_sync3,
            108 : self._on_status,
            109 : self._on_want_disconnect}

    def _on_packet_received(self, raw_packet):
        """_on_packet_received - Unpacks raw bytes objects and calls the relevant event handler

        Args:
            raw_packet (Bytes): A raw BGBLink protocol packet.
        """
        (ptype,) = unpack('=bxxxxxxx',raw_packet)
        packet = self.packets[ptype](raw_packet)
        self.handlers[ptype](packet)

    def _on_version(self, packet, *args, **kwargs):
        """_on_version: Event handler for [packet] packets

        [extended_summary]

        Args:
            packet ([type]): [description]
            *args
            **kwargs
        """
        self.logger.debug('Received VersionPacket: B0: %s B1: %s B2: %s B3: %s i0: %s',packet.b0,packet.b1, packet.b2, packet.b3, packet.i0)
        #do nothing
        pass

    def _on_joypad(self, packet, *args, **kwargs):
        """_on_joypad: Event handler for [packet] packets

        [extended_summary]

        Args:
            packet ([type]): [description]
            *args
            **kwargs
        """
        self.logger.debug('Received JoypadPacket: B0: %s B1: %s B2: %s B3: %s i0: %s',packet.b0, packet.b1, packet.b2, packet.b3, packet.i0)
        #do nothing
        pass

    def _on_sync1(self, packet, *args, **kwargs):
        """_on_sync1: Event handler for [packet] packets

        [extended_summary]

        Args:
            packet ([type]): [description]
            *args
            **kwargs
        """
        self.logger.debug('Received Sync1Packet: B0: %s B1: %s B2: %s B3: %s i0: %s',packet.b0, packet.b1, packet.b2, packet.b3, packet.i0)
        #do nothing
        pass

    def _on_sync2(self, packet, *args, **kwargs):
        """_on_sync2: Event handler for [packet] packets

        [extended_summary]

        Args:
            packet ([type]): [description]
            *args
            **kwargs
        """
        self.logger.debug('Received Sync2Packet: B0: %s B1: %s B2: %s B3: %s i0: %s',packet.b0, packet.b1, packet.b2, packet.b3, packet.i0)
        #do nothing
        pass

    def _on_sync3(self, packet, *args, **kwargs):
        """_on_sync3: Event handler for [packet] packets

        [extended_summary]

        Args:
            packet ([type]): [description]
            *args
            **kwargs
        """
        self.logger.debug('Received Sync3Packet: B0: %s B1: %s B2: %s B3: %s i0: %s',packet.b0, packet.b1, packet.b2, packet.b3, packet.i0)
        #do nothing
        pass

    def _on_status(self, packet, *args, **kwargs):
        """_on_status: Event handler for [packet] packets

        [extended_summary]

        Args:
            packet ([type]): [description]
            *args
            **kwargs
        """
        self.logger.debug('Received StatusPacket: B0: %s B1: %s B2: %s B3: %s i0: %s',packet.b0, packet.b1, packet.b2, packet.b3, packet.i0)
        #do nothing
        pass

    def _on_want_disconnect(self, packet, *args, **kwargs):
        """_on_want_disconnect: Event handler for [packet] packets

        [extended_summary]

        Args:
            packet ([type]): [description]
            *args
            **kwargs
        """
        self.logger.debug('Received WantDisconnectPacket: B0: %s B1: %s B2: %s B3: %s i0: %s',packet.b0, packet.b1, packet.b2, packet.b3, packet.i0)
        #do nothing
        pass
        
class GenericPacket:
    """ GenericPacket [summary]

    [extended_summary]
    
    Args:
        raw_packet (Bytes, optional): A raw BGBLink protocol packet. Defaults to None.    
    """
    def __init__(self, raw_packet = None):
        self.defines = defines
        if not raw_packet:
            self.b0 = FixedIntt(0x00, 8) # command number
            self.b1 = FixedInt(0x00, 8) # data
            self.b2 = FixedInt(0x00, 8) # data
            self.b3 = FixedInt(0x00, 8) # reserved
            self.i0 = FixedInt(0x00, 32) # timestamp
        else:
            (b0, b1, b2, b3, i0) = unpack('=bbbbi',raw_packet)
            self.b0 = FixedInt(b0, 8)
            self.b1 = FixedInt(b1, 8)
            self.b2 = FixedInt(b2, 8)
            self.b3 = FixedInt(b3, 8)
            self.i0 = FixedInt(i0, 8)

    def _assemble(self):
        """assemble Assembles the packet into a Bytes object

        Returns:
            Bytes: a raw BGBLink packet
        """
        return pack('=bbbbi',self.b0, self.b1, self.b2, self.b3, self.i0)
        
    def __bytes__(self):
        return self._assemble()

class VersionPacket(GenericPacket):
    """VersionPacket A version packet.

        The protocol version. A change of these fields indicates a different (incompatible) protocol used.

        b0=int_8:   0x01        - command
        b2=int_8:   varies      - major version byte
        b3=int_8:   varies      - minor version byte
        b4=int_8:   0x00        - reserved
        i0=int_32:  0x00000000  - reserved

    Args:
        raw_packet (Bytes, optional): A raw BGBLink protocol packet. Defaults to None.

    Inherits:
        GenericPacket
    """
    def __init__(self, raw_packet = None):
        super().__init__(raw_packet)
        if not self.b0:
            self.b0 = self.defines.C_VERSION
            self.b1 = self.defines.MAJOR_VER
            self.b2 = self.defines.MINOR_VER

class JoypadPacket(GenericPacket):
    """JoypadPacket A joypad packet.

        Joypad change, for remote control of an emulator. The receiving end can choose to ignore joypad changes, or update its button state accordingly.

        Any bits and fields other than the ones used for a purpose MUST be 0 when sending, and MUST be ignored when receiving.

        b0=int_8:   0x65        - command
        b2= bit0:   button number
              |       |
            bit2:     *
            bit3:   is_pressed
            bit4:   reserved
              |       |
              |       |
            bit7:     *
        b3=int_8:   0x00        - reserved
        b4=int_8:   0x00        - reserved
        i0=int_32:  0x00000000  - reserved

    Args:
        raw_packet (Bytes, optional): A raw BGBLink protocol packet. Defaults to None.
        
    Inherits:
        GenericPacket
    """
    def __init__(self, raw_packet = None):
        super().__init__(raw_packet)
        if not self.b0:
            self.b0 = self.defines.C_JOYPAD
        self.isPressed = bool(self.b1 & self.defines.B_ISPRESSED)
        self.button = self.b1 & 7

    def _assemble(self):
        """assemble Assembles the packet into a Bytes object.

        Returns:
            Bytes: a raw BGBLink packet
        """
        self.b1 = (int(self.isPressed) * self.defines.B_ISPRESSED) | self.button
        return super()._assemble()

class Sync1Packet(GenericPacket):
    """Sync1Packet [summary]

    [extended_summary]

    Inherits:
        GenericPacket
    """
    def __init__(self, raw_packet = None):
        super().__init__(raw_packet)
        if not self.b0:
            self.b0 = self.defines.C_SYNC1
        self.data = self.b1
        self.highspeed = bool(self.b2 & 2)
        self.doublespeed = bool(self.b2 & 4)
        self.timestamp = self.i0
        
    def _assemble(self):
        """assemble Assembles the packet into a Bytes object.
        
        Returns:
            Bytes: a raw BGBLink packet
        """
        self.b1 = FixedInt(self.data, 8)
        #sanity check, bits 1 and 7 of b2 should always be 1
        self.b2 = self.b2 | -127
        #add the highspeed bit
        self.b2 = self.b2 | (int(self.highspeed) * 2)
        #add the doublespeed bit
        self.b2 = self.b2 | (int(self.doublespeed) * 4)
        self.i0 = self.timestamp
        return super()._assemble()
        

class Sync2Packet(GenericPacket):
    """Sync2Packet [summary]

    [extended_summary]

    Inherits:
        GenericPacket
    """
    def __init__(self, raw_packet = None):
        super().__init__(raw_packet)
        if not self.b0:
            self.b0 = self.defines.C_SYNC2
        self.data = self.b1

    def _assemble(self):
        """assemble Assembles the packet into a Bytes object.

        Returns:
            Bytes: a raw BGBLink packet
        """
        self.b1 = FixedInt(self.data, 8)
        #sanity check, b2 should always be 0x80
        self.b2 = FixedInt(0x80, 8)
        return super()._assemble()

class Sync3Packet(GenericPacket):
    """Sync3Packet [summary]

    [extended_summary]

    Inherits:
        GenericPacket
    """
    def __init__(self, raw_packet = None):
        super().__init__(raw_packet)
        if not self.b0:
            self.b0 = self.defines.C_SYNC3

class StatusPacket(GenericPacket):
    """StatusPacket [summary]

    [extended_summary]

    Inherits:
        GenericPacket
    """
    def __init__(self, raw_packet = None):
        super().__init__(raw_packet)
        if not self.b0:
            self.b0 = self.defines.C_STATUS

class WantDisconnectPacket(GenericPacket):
    """WantDisconnectPacket [summary]

    [extended_summary]

    Inherits:
        GenericPacket
    """
    def __init__(self, raw_packet = None):
        super().__init__(raw_packet)
        if not self.b0:
            self.b0 = self.defines.C_WANTDISCONNECT