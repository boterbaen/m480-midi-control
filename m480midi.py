import mido
import threading

class Board:
    inport = mido.open_input('V-Mixer MIDI IN 0')
    outport = mido.open_output('V-Mixer MIDI OUT 1')

    # create an array to represent each channel's mute
    mutes = []
    for x in range(48):
        mutes.append(True)

    # creates an array to contain each scene (label, mics, and queue), scene 0.0.0 is always empty. the first index of the inner list is that scene's label
    scenes = [['0.0.0', [], '']]
    currentScene = 0

    # mute a channel
    def mute(self, channel):
        self.mutes[channel-1] = True
        if (channel <= 24):
            msg = mido.Message("control_change", channel=0, control=63+channel, value=1)
        else:
            msg = mido.Message("control_change", channel=1, control=63+channel, value=1)
        self.outport.send(msg)

    # mute channels 1-48
    def muteRange(self, channels):
        for x in channels:
            self.mute(x)

    def muteAll(self):
        for i in range(48):
            self.mute(i+1)

    # unmute a channel
    def unmute(self, channel):
        self.mutes[channel-1] = False
        if (channel <= 24):
            msg = mido.Message("control_change", channel=0, control=63+channel, value=0)
        else:
            msg = mido.Message("control_change", channel=1, control=63+channel, value=0)
        self.outport.send(msg)

    # unmute channels 1-48
    def unmuteRange(self, channels):
        for x in channels:
            self.unmute(x)

    def unmuteAll(self):
        for i in range(48):
            self.unmute(i+1)

    # sets specific mutes, channels 1-48
    def setMutes(self, channels):
        for i in range(48):
            if (not self.mutes[i]):
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
    
    # adds a scene
    def addScene(self, label, channels, queue):
        scene = [label, channels, queue]
        self.scenes.append(scene)
    
    # recalls a scene from scenes[]
    def setScene(self, scene):
        self.currentScene = scene
        print('Scene ' + self.scenes[scene][0])
        self.setMutes(self.scenes[scene][1])
        print('Next scene: ' + self.scenes[scene+1][2])
    
    # starts the scene swapping user input loop in a new thread
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
            elif (cin == 'um'):
                self.setScene(self.currentScene)
            else:
                i = 0
                for x in self.scenes:
                    if (x[0] == cin):
                        self.setScene(i)
                        break
                    i += 1

    # starts actively reading mutes on the board in a new, adding them to the mutes list
    def startReading(self):
        while(True):
            msg = self.inport.receive()
            if (msg.type == 'control_change' and (msg.value == 1 or msg.value == 0) and (msg.control - 63 > 0)):
                print("Receiving: " + str(msg))
                if (msg.channel == 0):
                    self.mutes[msg.control - 64] = bool(msg.value)
                elif (msg.channel == 1):
                    self.mutes[msg.control - 64 + 24] = bool(msg.value)

