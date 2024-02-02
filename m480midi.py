import mido
import threading
import numpy as np

# TODO:
# - test muting second rows
# - add get faders and add faders to reading
#   - get mutes also?
#     - wait nevermind this is python
# - add set faders
#   - make sure control msg is right
# - make dcu versions of everything?
# - turn on and off fx bypass
# - set board-local scene?
# - nest some more classes for neatness

class Board:
    inport = mido.open_input('V-Mixer MIDI IN 0')
    outport = mido.open_output('V-Mixer MIDI OUT 1')

    # create an array to represent each channel's mute
    mutes = []
    for x in range(48):
        mutes.append(True)

    # create an array to represent each channel's fader
    faders = []
    for x in range(48):
        faders.append(97)
    
    # creates an array containing each of the possible values a fader can assume, as defined in roland's m480 midi implementation paper
    faderValues = np.array([float('-inf'), -80.0, -76.7, -73.3, -70.0, -66.7, -63.3, -60.0, -58.6, -57.1, -55.7, -54.3, -52.9, -51.4, -50.0,
                   -48.9, -47.8, -46.7, -45.6, -44.4, -43.3, -42.2, -41.1, -40.0, -39.2, -38.5, -37.7, -36.9, -36.2, -35.4, -34.6,
                   -33.8, -33.1, -32.3, -31.5, -30.8, -30.0, -29.3, -28.7, -28.0, -27.3, -26.7, -26.0, -25.3, -24.7, -24.0, -23.3,
                   -22.7, -22.0, -21.3, -20.7, -20.0, -19.3, -18.7, -18.0, -17.3, -16.7, -16.0, -15.3, -14.7, -14.0, -13.3, -12.7, -12.0,
                   -11.3, -10.7, -10.3, -10.0, -9.7, -9.3, -9.0, -8.7, -8.3, -8.0, -7.7, -7.3, -7.0, -6.7, -6.3, -6.0, -6.7, -5.3, -5.0
                   -4.7, -4.3, -4.0, -3.7, -3.3, -3.0, -2.7, -2.3, -2.0, -1.7, -1.3, -1.0, -0.7, -0.3, 0.0, 0.3, 0.7, 1.0, 1.3, 1.7,
                   2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0, 4.3, 4.7, 5.0, 5.3, 5.7, 6.3, 6.7, 7.0, 7.3, 7.7, 8.0, 8.3, 8.7, 8.0, 8.3, 8.7,
                   9.0, 9.3, 9.7, 10.0]) # YOU MISSED 2 OF THEM GHUHDJGFO

    # creates an array to contain each scene (label, mics, and queue), scene 0.0.0 is always empty. the first index of the inner list is that scene's label
    scenes = [['0.0.0', [], '']]
    currentScene = 0

    # mute a channel
    def mute(self, channel):
        self.mutes[channel-1] = True
        if (channel <= 24):
            msg = mido.Message("control_change", channel=0, control=63+channel, value=1)
        else:
            msg = mido.Message("control_change", channel=1, control=63+channel-24, value=1)
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
            msg = mido.Message("control_change", channel=1, control=63+channel-24, value=0)
        self.outport.send(msg)

    # unmute channels 1-48
    def unmuteRange(self, channels):
        for x in channels:
            self.unmute(x)

    def unmuteAll(self):
        for i in range(48):
            self.unmute(i+1)

    # mutes all specified channels and unmutes all others, channels 1-48
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

    # set a channels fader level, converting from the -inf to 10 scale
    def setFader(self, channel, level):
        level = np.where(self.faderValues == self.faderValues.flat[np.abs(self.faderValues - level).argmin()])[0][0]
        self.faders[channel-1] = level
        if (channel <= 24):
            msg = mido.Message("control_change", channel=0, control=channel, value=level)
        else:
            msg = mido.Message("control_change", channel=1, control=channel-24, value=level)
        self.outport.send(msg)
    
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
            if ((msg.type == 'control_change') and (msg.control  >= 64) and (msg.control <= 87)):
                print("Receiving: " + str(msg))
                if (msg.channel == 0):
                    self.mutes[msg.control - 64] = bool(msg.value)
                elif (msg.channel == 1):
                    self.mutes[msg.control - 64 + 24] = bool(msg.value)
            elif ((msg.type == 'control_change') and (msg.control  >= 1) and (msg.control <= 24)):
                if (msg.channel == 0):
                    self.faders[msg.control - 1] = msg.value
                elif (msg.channel == 1):
                    self.faders[msg.control - 1 + 24] = msg.value