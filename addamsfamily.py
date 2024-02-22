# The following is to be the file for the upcoming spring show
import threading

import m480midi

b = m480midi.Board(1)

b.scenes.extend([b.Scene("1.1.0", [1,2,3,4], "test"),
                 b.Scene("1.1.1", [2, 4], "test2"),
                 b.Scene("1.2.0", [], "test3")])

b.setMutes(range(1,25), False)

b.fetch()

#b.fetch([2], [])
#b.setFaderRange(range(1, 24), 0)
#b.setFader(24, -100)

threading.Thread(target=b.startUI).start()
threading.Thread(target=b.startReading, daemon=True).start()