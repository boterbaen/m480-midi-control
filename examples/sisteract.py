import mido
import threading

import m480midi

board = m480midi.Board()

board.muteAll()

board.addScene('1.1.0', [1, 15, 19], 'start of new scene') # deloris michelle tina  *DANCERS MIGHT BE DIFFERENT (charlotte? no other one?)
board.addScene('1.1.1', [1, 11, 12, 13, 14, 17], 'take me to heaven - deloris') # deloris, curtis, tj, joey, pablo, ernie
board.addScene('1.1.2', [1, 15, 19], 'curtis exits') # deloris michelle tina

board.addScene('1.2.0', [11, 12, 13, 14, 17], 'start of new scene') # curtis ernie tj pablo joey
board.addScene('1.2.1', [1, 11, 13], 'gun shoots') # deloris curtis joey

board.addScene('1.3.0', [], 'chase') # chase scene

board.addScene('1.4.0', [1, 10, 18, 19, 24], 'start of new scene') # deloris cop eddie hookier (18 or 19 for hooker?)
board.addScene('1.4.1', [1, 10], 'thats not my name - eddie') # deloris eddie

board.addScene('1.5.0', [2, 3, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'start of new scene') # nuns mother monsignor
board.addScene('1.5.1', [2, 3], 'nuns exit') # mother monsignor
board.addScene('1.5.2', [1, 2, 3, 10], 'monsignor gets the door') # mother monsignor deloris eddie
board.addScene('1.5.3', [1, 2], 'eddie exits') # mother deloris <DO REVERB? DELAY?>
#board.addScene('1.5.4', [1, 2, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24]) # deloris mother nuns

board.addScene('1.6.0', [2, 4, 5, 6], 'start of new scene') # patrick robert lazarus mother
board.addScene('1.6.1', [1, 2, 4, 5, 6], 'nuns sit') # patrick robert lazarus mother deloris
board.addScene('1.6.2', [1, 2, 4, 6, 8, 9], 'sit down - mother superior') # patrick lazarus martin theresa mother deloris
board.addScene('1.6.3', [1, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'mother superior exits') # deloris patrick lazarus theresa martin robert nuns (mother?)

board.addScene('1.7.0', [1, 2], 'start of new scene') # deloris mother
board.addScene('1.7.1', [1, 5], 'mother superior exits') # deloris robert
board.addScene('1.7.2', [1, 4, 5], 'deloris exits') # robert patrick

board.addScene('1.8.0', [10, 11, 12, 13, 14, 24], 'start of new scene') # curtis joey pablo tj cop eddie *MAKE SURE COP IS CORRECT*
board.addScene('1.8.1', [11, 12, 13, 14], 'eddie exits') # curtis joey tj pablo

board.addScene('1.9.0', [11, 12, 13, 14], 'start of new scene') # curtis joey pablo tj

board.addScene('1.10.0', [1, 12, 13, 14, 18, 21, 22, 23], 'start of new scene') # patrons(all?) tj pablo joey deloris waitress player
board.addScene('1.10.1', [1, 4, 5, 21, 22, 23], 'everyone is so nice! it is good to be a nun! - deloris') # deloris robert patrick patrons(all?) player
board.addScene('1.10.2', [1, 4, 13, 17], 'only a nickel - mary patrick') # deloris patrick joey drag

board.addScene('1.11.0', [2, 4, 5], 'start of new scene') # mother patrick robert
board.addScene('1.11.1', [1, 2, 10], 'patrick and robert exit') # deloris mother eddie
board.addScene('1.11.2', [10], 'mother and deloris exit') # eddie
board.addScene('1.11.3', [10, 15, 16, 18, 19, 23], 'homeless start clapping') # eddie homeless

board.addScene('1.12.0', [1, 2], 'start of new scene') # deloris mother
board.addScene('1.12.1', [2, 3], 'deloris exits') # mother monsignor

board.addScene('1.13.0', [1, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'start of new scene') # deloris robert patrick martin lazarus nuns(all?) *REWORK?*

board.addScene('1.14.0', [1, 2, 3, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'start of new scene') # deloris mother monsignor patrick robert lazarus nuns(all?)
board.addScene('1.14.1', [1, 2, 4, 5, 6, 8, 9, 10, 15, 16, 18, 19, 20, 21, 22, 24], 'hoo hoo hoo - nuns') # mother nuns(all?) eddie
board.addScene('1.14.2', [1, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'get her out now! - mother superior') # nuns

board.addScene('2.1.0', [1, 2], 'start of new scene') # deloris mother
board.addScene('2.1.1', [1, 2, 3], 'monsignor enters') # deloris mother monsignor

board.addScene('2.2.0', [3], 'start of new scene') # monsignor
board.addScene('2.2.1', [3, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'thermometer is brought in') # monsignor nuns(all)
board.addScene('2.2.2', [1, 2, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'crix pix crisifix shticks - mary theresa') # deloris mother nuns(all)
board.addScene('2.2.3', [1, 2, 3, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'mother superior finishes her song') # deloris monsignor nuns(all)
board.addScene('2.2.4', [1, 10], 'mary patrick exits') # deloris eddie
board.addScene('2.2.5', [1, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'eddie exits') # deloris nuns
board.addScene('2.2.6', [2, 3, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'that miracles can happen! - mary robert') # mother monsig nuns
board.addScene('2.2.7', [1, 2, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'after pope paul the sixth') # deloris mother nuns
board.addScene('2.2.8', [1, 2, 3, 4, 5, 6, 8, 9, 10, 15, 16, 18, 19, 20, 21, 22, 24], 'that sunday fever - deloris') # deloris mother monsig eddie nuns

board.addScene('2.3.0', [11, 12, 13, 17], 'start of new scene') # curtis tj joey cab
board.addScene('2.3.1', [1, 4, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 24], 'i know that song - curtis') # deloris curtis tj joey pablo nuns(all?) newscaster(sarah?)
board.addScene('2.3.2', [11, 12, 13, 14], 'newscaster and nuns exit') # curtis tj joey pablo *ADD SCENE FOR SONG*

board.addScene('2.4.0', [2], 'start of new scene') # mother

board.addScene('2.5.0', [1, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'start of new scene') # deloris nuns(all)
board.addScene('2.5.1', [], 'dancing') # dance break 
board.addScene('2.5.2', [1, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'stops dancing') # deloris nuns(all)
board.addScene('2.5.3', [1, 2, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'mother superior enters') # deloris mother nuns(all)

board.addScene('2.6.0', [1, 5], 'start of new scene') # deloris robert
board.addScene('2.6.1', [1, 5, 10], 'take it anyway. you might need some extra help - mary robert') # deloris robert eddie
board.addScene('2.6.2', [5], 'eddie and deloris exit') # robert

board.addScene('2.7.0', [1, 10], 'start of new scene') # deloris eddie
board.addScene('2.7.1', [1], 'eddie exits (on second exit)') # deloris
board.addScene('2.7.2', [1, 15, 18, 19], 'gay boys! - deloris') # deloris dancers
board.addScene('2.7.3', [1, 2, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'me, im fabulus baby') # deloris dancers(michelle tina) nuns(all)
board.addScene('2.7.4', [1], 'stop! - deloris') # deloris

board.addScene('2.8.0', [11, 12, 13, 14], 'start of new scene') # curtis tj joey pablo
board.addScene('2.8.1', [11], 'thugs exit') # curtis

board.addScene('2.9.0', [2, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'start of new scene') # mother nuns(all)
board.addScene('2.9.1', [1, 2, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'deloris! - mary robert') # deloris mother nuns(all)
board.addScene('2.9.2', [1, 2, 5], 'i am impressed and frankly a little surprised - mother superior') # deloris mother robert

board.addScene('2.10.0', [6, 13], 'start of new scene') # lazarus joey
board.addScene('2.10.1', [8, 14], 'pablo enters') # martin pablo
board.addScene('2.10.2', [1, 11], 'curtis fires') # deloris curtis
board.addScene('2.10.3', [1, 2, 11], 'and you sure as hell aint no nun - curtis') # deloris mother curtis *scene for sweet sosters scene?*
board.addScene('2.10.4', [1, 2, 4, 5, 6, 8, 9, 11, 15, 16, 18, 19, 20, 21, 22, 24], 'get out of my way - curtis') # deloris mother curtis nuns(all)
board.addScene('2.10.5', [1], 'and no one on earth can change that fact - deloris') # deloris
board.addScene('2.10.6', [1, 10, 11], 'im not afraid of you, curtis. none of us are - deloris') # delolris curtis eddie
board.addScene('2.10.7', [1, 2, 4, 5, 6, 8, 9, 10, 11, 15, 16, 18, 19, 20, 21, 22, 24], 'after youre nothing youre nobody from curtis') # deloris mother eddie nuns(all)
board.addScene('2.10.8', [1, 2], 'eddie exits') # deloris mother

board.addScene('2.11.0', [3], 'start of new scene') # monsignor
board.addScene('2.11.1', [4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'give it up for pope paul VI! - monsignor') # nuns(all)
board.addScene('2.11.2', [1, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'deloris enters') # deloris nuns(all?)
board.addScene('2.11.3', [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24], 'men enter') # deloris nuns men
board.addScene('2.11.4', [1, 2, 4, 5, 6, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24], 'men enter audience') # deloris mother nuns

print(board.scenes)

threading.Thread(target=board.startUI).start()
threading.Thread(target=board.startReading).start()