import mido

# TODO:
# - add fader levels to scenes?
#   - likely will not be very useful. not necessary.
# - make dca setters?
#   - dca cant use channel class as is. the midi out is for regular ch
#   - expand setters to include dcas as >48?
# - turn on and off fx bypass?
#   - not needed, possibly at a later date
# - add a fetch mute/fader w/ RQ1
#   - still need dca of this
# - add good error messages and catching
#   - out of range for literally any setter, fetcher, and the cli
#   - failure to send/recieve

inport = mido.open_input('V-Mixer MIDI IN 0')
outport = mido.open_output('V-Mixer MIDI OUT 1')

class Board:
    def __init__(self, deviceID=1):
        self.deviceID = deviceID
        self.channels = []
        for x in range(48):
            self.channels.append(self.Channel(x+1))
        self.dcas = []
        for x in range(24):
            self.dcas.append(self.Channel(x+1))
        self.scenes = [self.Scene()]
        self.currentScene = 0

    class Channel:
        def __init__(self, num, mute=True, fader=0):
            self.num = num
            self.mute = mute
            self.fader = fader
        def setMute(self, status=True):
            self.mute = status
            if (self.num <= 24):
                msg = mido.Message("control_change", channel=0, control=63+self.num, value=int(status))
            else:
                msg = mido.Message("control_change", channel=1, control=63+self.num-24, value=int(status))
            outport.send(msg)
        def setFader(self, level=0):
            self.fader = level
            level = int(level * 10) # roland uses 3 digit integers for board level
            if level < -905:
                dataA, dataB = 64, 0
            elif level >= 0:
                level = 100 if level > 100 else level
                dataA = 0
                dataB = level
            else:
                data = (abs(level) ^ 0b11111111111111) + 1
                dataA = data >> 7
                dataB = data - (dataA << 7)
            #                                 MID DID------------- Model Id- DT1 Param Addr---------- Data--------- Checksum-------------------------------
            msg = mido.Message('sysex', data=(65, self.deviceID-1, 0, 0, 36, 18, 4, self.num-1, 0, 22, dataA, dataB, 128-(26+dataA+dataB+self.num-1)%128))
            print(msg)
            outport.send(msg)

    class Scene:
        def __init__(self, label="0.0.0", active=[], queue=""):
            self.label = label
            self.active = active
            self.queue = queue

    # provide a list of channels and their desired mute status
    def setMutes(self, channels, status=True):
        for channel in channels:
            self.channels[channel-1].setMute(status)

    # provide a list of channels to be unmuted. all excluded channels will be muted
    def setActive(self, channels):
        for i in range(48):
            isInScene = False
            if not self.channels[i].mute:
                for channel in channels:
                    if channel == i+1:
                        isInScene = True
                        break
                if not isInScene:
                    self.channels[i].setMute(True)
            else:
                for channel in channels:
                    if channel == i+1:
                        isInScene = True
                        break
                if isInScene:
                    self.channels[i].setMute(False)

    # provide a list of channels and a singular desired fader level
    def setFaders(self, channels, level):
        for channel in channels:
                self.setFader(channel, level)

    # set the board to reflect one of the saved scenes via its index
    def setScene(self, sceneNum):
        self.currentScene = sceneNum
        print('Scene ' + self.scenes[sceneNum].label)
        self.setActive(self.scenes[sceneNum].active)
        print('Next scene at: ' + self.scenes[sceneNum].queue)
    
    # start a rudimentary scene swapping user input loop
    def startUI(self):
        print('Press ENTER to proceed to the next scene. Type a scene label to jump to a specific scene. Type "m" to mute all and "u" to restore scene.')
        while True:
            cin = input()
            if  cin == '':
                self.setScene(self.currentScene + 1)
            elif cin == 'exit':
                exit()
            else:
                i = 0
                for scene in self.scenes:
                    if scene.label == cin:
                        self.setScene(i)
                        break
                    i += 1
    
    # start passively reading updates from the board
    def startReading(self):
        while True:
            msgIn = inport.receive()
            print("Receiving: " + str(msgIn))
            # verifies source is the registered m480 (other roland boards will have a different sequence of values here)
            if msgIn.type == 'sysex' and msgIn.data[:6] == (65, self.deviceID-1, 0, 0, 36, 18):
                if msgIn.data[6:7]+msgIn.data[8:10] == (4, 0, 20): # ch mute
                    self.channels[msgIn.data[7]].mute = bool(msgIn.data[10])
                    print('recieved mute ' + str(msgIn.data[10]) + ' on ch ' + str(msgIn.data[7]))
                elif msgIn.data[6:7]+msgIn.data[8:10] == (4, 0, 22): # ch fader
                    if msgIn.data[10] == 0:
                        level = msgIn.data[11]
                    else:
                        # uses twos complement to convert negatives
                        data = (msgIn.data[10]<<7) + msgIn.data[11]
                        level = (((data - 1) ^ 0b11111111111111) * -1) * 0.1
                    print('recieved fader ' + str(level) + ' on ch ' + str(msgIn.data[7]))
                    self.channels[msgIn.data[7]].fader = level 

    # requests a data transfer from the board for relevant properties. defaults to all ch and dca
    def fetch(self, channels=range(1,49), dcas=range(1,25)):
        for channel in channels:
            # mutes                              MAN Device ID------- Model ID- RQ1 Param Addr---------- Size------- Checksum----------------
            msgOut = mido.Message('sysex', data=(65, self.deviceID-1, 0, 0, 36, 17, 4, channel-1, 0, 20, 0, 0, 0, 1, 128-((25+channel-1)%128)))
            print('fetching mute')
            print(msgOut)
            outport.send(msgOut)
            # fader                              MAN Device ID------- Model ID- RQ1 Param Addr---------- Size--------- Checksum----------------
            msgOut = mido.Message('sysex', data=(65, self.deviceID-1, 0, 0, 36, 17, 4, channel-1, 0, 22, 0, 0, 0, 127, 128-((153+channel-1)%128)))
            print('fetching fader')
            print(msgOut)
            outport.send(msgOut)

        for channel in dcas: # Still need to test
            # mutes                              MAN Device ID------- Model ID- RQ1 Param Addr---------- Size------- Checksum----------------
            msgOut = mido.Message('sysex', data=(65, self.deviceID-1, 0, 0, 36, 17, 11, channel-1, 0, 20, 0, 0, 0, 1, 128-((22+channel-1)%128)))
            print('fetching dca  mute')
            print(msgOut)
            outport.send(msgOut)
            # fader                              MAN Device ID------- Model ID- RQ1 Param Addr---------- Size--------- Checksum----------------
            msgOut = mido.Message('sysex', data=(65, self.deviceID-1, 0, 0, 36, 17, 11, channel-1, 0, 22, 0, 0, 0, 127, 128-((160+channel-1)%128)))
            print('fetching dca fader')
            print(msgOut)
            outport.send(msgOut)