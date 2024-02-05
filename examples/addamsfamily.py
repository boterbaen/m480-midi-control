import threading

import m480midi

b = m480midi.Board(1)

b.scenes.extend([b.Scene("1.1.0", [1,2,3,4], [], [], "test"),
                 b.Scene("1.1.1", [2, 4], [], [], "test2"),
                 b.Scene("1.2.0", [2, 4], [], [], "test2")])

b.muteRange(range(23)+1)

threading.Thread(target=b.startUI).start()
threading.Thread(target=b.startReading).start()