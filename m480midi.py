import mido
import threading
import time

# TODO:
# - test muting second rows
# - make dca versions of everything?
# - turn on and off fx bypass
# - set board-local scene?
# - add a fetch mute/fader/fx w/ RQ1
#   - need to test all sysex functions
# - make scenes a tuple?
# - checksum read/calc function
# - use observer pattern to decomplicate mutes and scenes?
#   - not necessary probably
# - move mute/unmute/setfaders to channel class
# - look into using the -900 100 format thing instead of 127 for faders
#   - setting will be complicated but getting will be soo much easier

class Board:
    def __init__(self, deviceID=1):
        self.deviceID = deviceID
        self.inport = mido.open_input('V-Mixer MIDI IN 0')
        self.outport = mido.open_output('V-Mixer MIDI OUT 1')
        self.channels = []
        for x in range(48):
            self.channels.append(self.Channel())
        self.dcas = []
        for x in range(8):
            self.dcas.append(self.Channel())
        self.fx = []
        for x in range(8):
            self.fx.append(False)
        self.scenes = [self.Scene()]
        self.currentScene = 0

    class Channel:
        mute = True
        fader = 97

    class Scene:
        def __init__(self, label="0.0.0", active=[], faders=[[], []], bypassFx=[], queue=""):
            self.label = label
            self.active = active
            self.faders = faders
            self.bypassFx = bypassFx
            self.queue = queue

    # mute a channel
    def mute(self, channel):
        self.channels[channel-1].mute = True
        if (channel <= 24):
            msg = mido.Message("control_change", channel=0, control=63+channel, value=1)
        else:
            msg = mido.Message("control_change", channel=1, control=63+channel-24, value=1)
        self.outport.send(msg)

    # mute channels 1-48
    def muteRange(self, channels):
        for x in channels:
            self.mute(x)

    # unmute a channel
    def unmute(self, channel):
        self.channels[channel-1].mute = False
        if (channel <= 24):
            msg = mido.Message("control_change", channel=0, control=63+channel, value=0)
        else:
            msg = mido.Message("control_change", channel=1, control=63+channel-24, value=0)
        self.outport.send(msg)

    # unmute channels 1-48
    def unmuteRange(self, channels):
        for x in channels:
            self.unmute(x)

    # mutes all specified channels and unmutes all others, channels 1-48
    def setMutes(self, channels):
        for i in range(48):
            if (not self.channels[i].mute):
                isInScene = False
                for x in channels:
                    if (x == i+1):
                        isInScene = True
                        break
                if (not isInScene):
                    self.mute(i+1)
            else:
                isInScene = False
                for x in channels:
                    if (x == i+1):
                        isInScene = True
                        break
                if (isInScene):
                    self.unmute(i+1)

    # set a channels fader level, converting from the -inf to 10 scale
    def setFader(self, channel, level):
        self.channels[channel-1].fader = level
        if (channel <= 24):
            msg = mido.Message("control_change", channel=0, control=channel, value=level)
        else:
            msg = mido.Message("control_change", channel=1, control=channel-24, value=level)
        self.outport.send(msg)

    # toggle an fx channel's bypass setting
    def setBypass(self, fx, bypass):
        self.fx[fx-1] = bypass
        #                                 MID-  DID----------  Model Id--------  RQ1-  Param Addr------------  Data-------  Checksum---------------
        msg = mido.Message('sysex', data=(0x41, self.deviceID, 0x00, 0x00, 0x24, 0x11, 0x0C, fx-1, 0x00, 0x10, int(bypass), 128-((25+channel-1)%128))) #recalc checksum
        self.outport.send(msg)
    
    def setScene(self, sceneNum):
        self.currentScene = sceneNum
        print('Scene ' + self.scenes[sceneNum].label)
        self.setMutes(self.scenes[sceneNum].active)
        print('Next scene at: ' + self.scenes[sceneNum].queue)
    
    # starts a rudimentary scene swapping user input loop
    def startUI(self):
        print('Press ENTER to proceed to the next scene. Type a scene label to jump to a specific scene. Type "m" to mute all and "um" to unmute all.')
        while(True):
            cin = input()
            if (cin == ''):
                self.setScene(self.currentScene + 1)
            elif (cin == 'exit'):
                exit()
            elif (cin == 'm'):
                self.muteAll
            elif (cin == 'u'):
                self.setScene(self.currentScene)
            else:
                i = 0
                for x in self.scenes:
                    if (x[0] == cin):
                        self.setScene(i)
                        break
                    i += 1

    # requests a data transfer from the board for relevant properties of a channel
    def fetch(self, channel):
        # mutes                           MID-  DID----------  Model Id--------  RQ1-  Param Addr-----------------  Size------------------  Checksum---------------
        msg = mido.Message('sysex', data=(0x41, self.deviceID, 0x00, 0x00, 0x24, 0x11, 0x04, channel-1, 0x00, 0x14, 0x00, 0x00, 0x00, 0x01, 128-((25+channel-1)%128)))
        self.outport.send(msg)
        isRecieved = False
        while(not isRecieved):
            msg = self.inport.receive()
            if (not msg.type == 'sysex'):
                continue
            if (msg.data[:10] != (0x41, self.deviceID, 0x00, 0x00, 0x24, 0x12, 0x04, channel-1, 0x00, 0x14)):
                self.channels[channel-1].mute = bool(msg.data[10])
        
        # faders                          MID-  DID----------  Model Id--------  RQ1-  Param Addr-----------------  Size------------------  Checksum---------------
        msg = mido.Message('sysex', data=(0x41, self.deviceID, 0x00, 0x00, 0x24, 0x11, 0x04, channel-1, 0x00, 0x16, 0x00, 0x00, 0x00, 0x01, 128-((25+channel-1)%128))) # recalc checksum
        self.outport.send(msg)
        isRecieved = False
        while(not isRecieved):
            msg = self.inport.receive()
            if (not msg.type == 'sysex'):
                continue
            if (msg.data[:10] != (0x41, self.deviceID, 0x00, 0x00, 0x24, 0x12, 0x04, channel-1, 0x00, 0x14)):
                print('wip') # add binary to temp var
        
        # faders part 2                   MID-  DID----------  Model Id--------  RQ1-  Param Addr-----------------  Size------------------  Checksum---------------
        msg = mido.Message('sysex', data=(0x41, self.deviceID, 0x00, 0x00, 0x24, 0x11, 0x04, channel-1, 0x00, 0x17, 0x00, 0x00, 0x00, 0x01, 128-((25+channel-1)%128))) # recalc checksum
        self.outport.send(msg)
        isRecieved = False
        while(not isRecieved):
            msg = self.inport.receive()
            if (not msg.type == 'sysex'):
                continue
            if (msg.data[:10] != (0x41, self.deviceID, 0x00, 0x00, 0x24, 0x12, 0x04, channel-1, 0x00, 0x14)):
                print('wip') # append binary to right of temp var and resolve to 127 format?


    # starts passively reading updates from the board (will only detect new events)
    def startReading(self):
        while(True):
            msg = self.inport.receive()
            if ((msg.type == 'control_change') and (msg.control  >= 64) and (msg.control <= 87)):
                print("Receiving: " + str(msg))
                if (msg.channel == 0):
                    self.channels[msg.control - 64].mute = bool(msg.value)
                elif (msg.channel == 1):
                    self.channels[msg.control - 64 + 24].mute = bool(msg.value)
            elif ((msg.type == 'control_change') and (msg.control  >= 1) and (msg.control <= 24)):
                if (msg.channel == 0):
                    self.channels[msg.control - 1].fader = msg.value #is this 100 or 127 format?
                elif (msg.channel == 1):
                    self.channels[msg.control - 1 + 24].fader = msg.value # roland why are you like this