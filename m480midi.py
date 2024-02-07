import mido
import threading
import time

# TODO:
# - make dca versions of everything?
# - turn on and off fx bypass
# - set board-local scene?
# - add a fetch mute/fader/fx w/ RQ1
#   - need to test all sysex functions
# - simplify code
# - use observer pattern to decomplicate mutes and scenes?
#   - not necessary probably
# - move mute/unmute/setfaders to channel class?
# - use sysex set for faders, to correct the 127 to -905/100 translation(love u roland)
# - add new features to the passive reading function

class Board:
    def __init__(self, deviceID=1):
        self.deviceID = deviceID
        self.inport = mido.open_input('V-Mixer MIDI IN 0')
        self.outport = mido.open_output('V-Mixer MIDI OUT 1')
        self.channels = []
        for x in range(48):
            self.channels.append(self.Channel())
        self.dcas = []
        for x in range(24):
            self.dcas.append(self.Channel())
        self.fx = []
        for x in range(8):
            self.fx.append(self.FX())
        self.scenes = [self.Scene()]
        self.currentScene = 0

    class Channel:
        mute = True
        fader = 97

    class FX:
        bypassL = True
        bypassR = True

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

    # set a channels fader level, from -905 to 100
    def setFader(self, channel, level): # NEED TO UPDATE TO USING SYSEX MSG
        self.channels[channel-1].fader = level
        if (channel <= 24):
            msg = mido.Message("control_change", channel=0, control=channel, value=level)
        else:
            msg = mido.Message("control_change", channel=1, control=channel-24, value=level)
        self.outport.send(msg)

    # toggle an fx channel's bypass setting
    #def setBypass(self, fx, bypass):
    #    self.fx[fx-1] = bypass
    #    #                                 MID-  DID----------  Model Id--------  RQ1-  Param Addr------------  Data-------  Checksum---------------
    #    msg = mido.Message('sysex', data=(65, self.deviceID, 0, 0, 36, 17, 12, fx-1, 0, 12, int(bypass), '''checksum''')) #recalc checksum
    #    self.outport.send(msg)

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
    
    # starts passively reading updates from the board (will only detect new events)
    def startReading(self):
        while(True):
            msg = self.inport.receive()
            print("Receiving: " + str(msg))
            if ((msg.type == 'control_change') and (msg.control  >= 64) and (msg.control <= 87)):
                if (msg.channel == 0):
                    self.channels[msg.control - 64].mute = bool(msg.value)
                elif (msg.channel == 1):
                    self.channels[msg.control - 64 + 24].mute = bool(msg.value)
            elif ((msg.type == 'control_change') and (msg.control  >= 1) and (msg.control <= 24)):
                if (msg.channel == 0):
                    self.channels[msg.control - 1].fader = msg.value # 127 format
                elif (msg.channel == 1):
                    self.channels[msg.control - 1 + 24].fader = msg.value

    # requests a data transfer from the board for relevant properties. defaults to all
    def fetch(self, channels=range(1,48), fxs=range(1,8), dcas=range(1,8)):
        for channel in channels:
            # mutes                              MAN Device ID------- Model ID- RQ1 Param Addr---------- Size------- Checksum----------------
            msgOut = mido.Message('sysex', data=(65, self.deviceID-1, 0, 0, 36, 17, 4, channel-1, 0, 20, 0, 0, 0, 1, 128-((25+channel-1)%128)))
            print('fetching mute')
            print(msgOut)
            self.outport.send(msgOut)
            isRecieved = False
            while(not isRecieved):
                msgIn = self.inport.receive()
                if (not msgIn.type == 'sysex'):
                    continue
                if (msgIn.data[:5]+msgIn.data[6:10] == msgOut.data[:5]+msgOut.data[6:10]):
                    print('mute response! mute is ' + str(msgIn.data[10]))
                    self.channels[channel-1].mute = bool(msgIn.data[10])
                    isRecieved = True
            # fader                              MAN Device ID------- Model ID- RQ1 Param Addr---------- Size--------- Checksum----------------
            msgOut = mido.Message('sysex', data=(65, self.deviceID-1, 0, 0, 36, 17, 4, channel-1, 0, 22, 0, 0, 0, 127, 128-((153+channel-1)%128)))
            print('fetching fader')
            print(msgOut)
            self.outport.send(msgOut)
            isRecieved = False
            while(not isRecieved):
                msgIn = self.inport.receive()
                if (not msgIn.type == 'sysex'):
                    continue
                if (msgIn.data[:5]+msgIn.data[6:10] == msgOut.data[:5]+msgOut.data[6:10]):
                    print('fader a response! got bin ' + bin(msgIn.data[10]))
                    print('fader b response! got bin ' + bin(msgIn.data[11]))
                    if(msgIn.data[10] == 0):
                        level = msgIn.data[11]
                    else:
                        level = -(((msgIn.data[10] << 7) + msgIn.data[11]) ^ 16383) * .1
                    print('fader level is ' + str(level))
                    isRecieved = True
        
        for fx in fxs: # FX uses weird channel joining. Add compensation for mono input?
            # bypass                              MAN Device ID------- Model ID- RQ1 Param Addr----- Size------- Checksum----------------
            msgOutL = mido.Message('sysex', data=(65, self.deviceID-1, 0, 0, 36, 17, 12, fx-1, 0, 16, 0, 0, 0, 1, 128-((29+fx-1)%128)))
            msgOutR = mido.Message('sysex', data=(65, self.deviceID-1, 0, 0, 36, 17, 12, fx-1, 0, 32, 0, 0, 0, 1, 128-((45+fx-1)%128)))
            print('fetching bypass L')
            print(msgOutL)
            self.outport.send(msgOutL)
            self.outport.send(msgOutR)
            isRecieved = False
            while(not isRecieved):
                msgIn = self.inport.receive()
                if (not msgIn.type == 'sysex'):
                    continue
                if (msgIn.data[:5]+msgIn.data[6:10] == msgOutL.data[:5]+msgOutL.data[6:10]):
                    print('bypass L response! bypass is ' + str(msgIn.data[10]))
                    self.fx[fx-1].bypassL = bool(msgIn.data[10])
                    isRecieved = True
            print('fetching bypass R')
            print(msgOutR)
            isRecieved = False
            while(not isRecieved):
                msgIn = self.inport.receive()
                if (not msgIn.type == 'sysex'):
                    continue
                if (msgIn.data[:5]+msgIn.data[6:10] == msgOutR.data[:5]+msgOutR.data[6:10]):
                    print('bypass R response! bypass is ' + str(msgIn.data[10]))
                    self.fx[fx-1].bypassR = bool(msgIn.data[10])
                    isRecieved = True

        for channel in dcas: # Still need to test
            # mutes                              MAN Device ID------- Model ID- RQ1 Param Addr---------- Size------- Checksum----------------
            msgOut = mido.Message('sysex', data=(65, self.deviceID-1, 0, 0, 36, 17, 11, channel-1, 0, 20, 0, 0, 0, 1, 128-((22+channel-1)%128)))
            print('fetching mute')
            print(msgOut)
            self.outport.send(msgOut)
            isRecieved = False
            while(not isRecieved):
                msgIn = self.inport.receive()
                if (not msgIn.type == 'sysex'):
                    continue
                if (msgIn.data[:5]+msgIn.data[6:10] == msgOut.data[:5]+msgOut.data[6:10]):
                    print('mute response! mute is ' + str(msgIn.data[10]))
                    self.channels[channel-1].mute = bool(msgIn.data[10])
                    isRecieved = True
            # fader                              MAN Device ID------- Model ID- RQ1 Param Addr---------- Size--------- Checksum----------------
            msgOut = mido.Message('sysex', data=(65, self.deviceID-1, 0, 0, 36, 17, 11, channel-1, 0, 22, 0, 0, 0, 127, 128-((160+channel-1)%128)))
            print('fetching fader')
            print(msgOut)
            self.outport.send(msgOut)
            isRecieved = False
            while(not isRecieved):
                msgIn = self.inport.receive()
                if (not msgIn.type == 'sysex'):
                    continue
                if (msgIn.data[:5]+msgIn.data[6:10] == msgOut.data[:5]+msgOut.data[6:10]):
                    print('fader a response! got bin ' + bin(msgIn.data[10]))
                    print('fader b response! got bin ' + bin(msgIn.data[11]))
                    if(msgIn.data[10] == 0):
                        level = msgIn.data[11]
                    else:
                        level = -(((msgIn.data[10] << 7) + msgIn.data[11]) ^ 16383) * .1
                    print('fader level is ' + str(level))
                    isRecieved = True