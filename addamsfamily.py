# The following is to be the file for the upcoming spring show
# TODO:
# note continuous scenes
# add in specific ancestors

from threading import Thread
import m480midi

b = m480midi.Board(1)

b.mutesIgnore.extend(range(25, 49)) # scenes will ignore the 25-48 row when setting values

all = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
ancestors = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
femAnc = [12, 13, 16, 19]

b.scenes.extend([
    b.Scene("1.1.0", [1,2, ancestors], "scene"),
    b.Scene("1.1.1", [1, 2, 3, 4, 5, 6], "Death of a Salesman - gomez"),
    b.Scene("1.1.2", [1, ancestors], "fester wakes the dead"),
    b.Scene("1.1.3", [1, 2, 3, 4, 5, 6, ancestors], "Death Rattle! - gomez"),
    b.Scene("1.1.4", [3, 5, 16], "Back to your crypt - gomez"),
    b.Scene("1.1.5", [3, 5, 11], "lucas enters"),
    b.Scene("1.1.6", [3, ancestors], "lights out on wed + lucas"),
    b.Scene("1.1.7", [3], "ancs disappear"),

    b.Scene("1.2.0", [1, 2], "scene"),
    b.Scene("1.2.1", [1, 2, 5], "wed enters"),
    b.Scene("1.2.2", [1, 5], "mort exits"),
    b.Scene("1.2.3", [1], "wed exits"),
    b.Scene("1.2.4", [1, 2], "mort enters"),
    b.Scene("1.2.5", [1], "mort exits"),

    b.Scene("1.3.0", [5, 6], "scene"),
    b.Scene("1.3.1", [5], "Puppy dogs with droopy faces - wed"),
    b.Scene("1.3.2", [1, 2], "wed exits"),
    b.Scene("1.3.3", [1, 2, 3, 4, 5, 6], "family enters"), # potential drop 3 + 6
    b.Scene("1.3.4", [1, 2, 5], "Normal is an illusion - mort"),

    b.Scene("1.4.0", [9, 10, 11], "scene"),
    b.Scene("1.4.1", [11], "No! - lucas"),
    b.Scene("1.4.2", [3, ancestors], "mal + alice exit"),
    b.Scene("1.4.3", [1, 2, 3, 4, 5, 6, ancestors], "GET! - fester"),
    b.Scene("1.4.4", [1, 2, 3, 4, 5, 6, 9, 10, 11, ancestors], "They'll tend my every need - wed"), # potential drop ancs
                 
    b.Scene("1.5.0", [3], "scene, doorbell rings"),
    b.Scene("1.5.1", [8, 9, 10], "door opens"),
    b.Scene("1.5.2", [9, 10, 11], "Oh, Mal - alice"),
    b.Scene("1.5.3", [1], "gomez enters"),
    b.Scene("1.5.4", [1, 2], "mort enters"),
    b.Scene("1.5.5", [2, 9, 10, 11], "Oh, Gomez! - mort"),
    b.Scene("1.5.6", [1, 2, 5], "Hes tolk lak dis - mort"),
    b.Scene("1.5.7", [1, 10], "Oh look. It's everywhere - mort"),
    b.Scene("1.5.8", [6, 10], "Say hello, Puggles - gomez"),
    b.Scene("1.5.9", [1, 4, 10], "alice puts a coin in the can"),
    b.Scene("1.5.10", [1, 3, 4, 6], "fester enters"),
    b.Scene("1.5.11", [1, 2, 5], "Goodbye! - the addams"),
    b.Scene("1.5.12", [1, 2, 9, 10], "Dad, remember (is cut off) - wed"),
    b.Scene("1.5.13", [2, 10], "gomez begins to exit"),
    b.Scene("1.5.14", [3, ancestors], "mort + alice exit"),
    
    b.Scene("1.6.0", [5, 11], "scene"),
    b.Scene("1.6.1", [3, ancestors], "lucas + wed exit"),

    b.Scene("1.7.0", [1, 9], "scene"),
    
    b.Scene("1.8.0", [2, 10], "scene"),
    b.Scene("1.8.1", [2], "mort solo"),
    b.Scene("1.8.2", [2, 10], "first bus out of town - mort"),
    b.Scene("1.8.3", [], "The dance routine - mort"),
    b.Scene("1.8.4", [2, femAnc], "dance break ends"),

    b.Scene("1.9.0", [1, 11], "scene"),
    b.Scene("1.9.1", [1, 2, 5, 11], "Where did you find him? - gomez"),
    b.Scene("1.9.2", [1, 2], "No, sir - lucas"),
    b.Scene("1.9.3", [1], "mort exits"),
    
    b.Scene("1.10.0", [5, 11], "scene"),
    b.Scene("1.10.1", [5, 6, 11], "You make me so crazy - lucas"),
    
    b.Scene("1.11.0", [6], "scene, wed + lucas exit"),
    b.Scene("1.11.1", [4, 6], "grandma enters"),
    b.Scene("1.11.2", [6], "grandma exits"),

    b.Scene("1.12.0", [1, 2, 5, 6], "scene"),
    b.Scene("1.12.1", [1, 2, 9, 10], "The game IS a good idea - gomez"),
    b.Scene("1.12.2", [1], "gomez recieves the chalice"),
    b.Scene("1.12.3", [1, 2, 3, 4, 6, ancestors], "crazy happy people! - gomez"), # possible drop ancs
    b.Scene("1.12.4", [1], "Yes. Well. - gomez"),
    b.Scene("1.12.5", [1, 2, 3, 5], "(to mort) Full disclosure! - gomez"), # possible revision
    b.Scene("1.12.6", [2, 3, 9, 10], "Awwww - all"),
    b.Scene("1.12.7", [1, 2, 3, 4, 6, 10], "I haven't told her yet - fester"), # possible add ancs
    b.Scene("1.12.8", [2, 4, 5], "And call it fuuuull disclosure!!! - all"),
    b.Scene("1.12.9", [4], "Me! Me! Me! - grandma"),
    b.Scene("1.12.10", [1, 2, 5], "I just peed a little - grandma"),
    b.Scene("1.12.11", [6], "Wheres the chalice? - mort"),
    b.Scene("1.12.12", [1, 2, 4, 5, 6], "Gonna be strange!!! - pugs"), # possible add ancs
    b.Scene("1.12.13", [9, 10, 11], "Nooooo!!!! - pugs"),
    b.Scene("1.12.14", [10], "Mom! - lucas"),
    b.Scene("1.12.15", [8, 10, ancestors], "alice grabs lurch's hand"), # possible drop ancs
    b.Scene("1.12.16", [1, 2, 3, 4, 6], "applause after alice song"), # possible add ancs
    b.Scene("1.12.17", [3, 9], "mal rises"),
    b.Scene("1.12.18", [2, 5], "help your mother off the table - mal"), # change the queue here - line not always used
    b.Scene("1.12.19", [1, 2, 3, 4, 5, 6, 9, 10, 11, ancestors], "What?! - mort"), # possible revision/reduction
    b.Scene("1.12.20", [1, 3, 9, ancestors], "fester freezes the action"),

    b.Scene("2.1.0", [5, 11], "scene"),
    b.Scene("2.1.1", [5, 11, ancestors], "Stop being so scared - wed"),
    b.Scene("2.1.2", [3, ancestors], "lucas exits"),

    b.Scene("2.2.0", [1, 2], "scene"),
    b.Scene("2.2.1", [2], "gomez exits"),
    b.Scene("2.2.2", [2, 15, 18, 21], "Cherry pits - mort"), # add cave, flight, soldier ancs
    b.Scene("2.2.3", [2, 12, 13, 16, 22], "Or even by your daughter - mort"), # add bride, conq, puritan, saloon/flapper ancs
    b.Scene("2.2.4", [], "swiftly on its way - mort dance break"),
    b.Scene("2.2.5", [2, ancestors], "end dance break"), # possible revision. full ancs or ancs present?

    b.Scene("2.3.0", [9, 10], "scene"),

    b.Scene("2.4.0", [3], "scene"),
    b.Scene("2.4.1", [3, femAnc], "Each waning - fester"),# remove
    b.Scene("2.4.2", [3], "fem ancs spread"),# remove
    b.Scene("2.4.3", [3, femAnc], "When the moon says I love you - fester"),
    
    b.Scene("2.5.0", [1, 5], "scene"),
    b.Scene("2.5.1", [1], "Now youve got it - gomez"),
    b.Scene("2.5.2", [1, 5], "You had to go and grow up - gomez"),
    b.Scene("2.5.3", [1], "Yes and no - gomez"),

    b.Scene("2.6.0", [1, 5, 11], "scene"),
    b.Scene("2.6.1", [5, 11], "gomez exits"),
    b.Scene("2.6.2", [5], "You're crazy - lucas"),
    b.Scene("2.6.3", [5, 11], "or simply move along - wed"),
    b.Scene("2.6.4", [11], "I'd never ask that of you - wed"),
    b.Scene("2.6.5", [5, 11], "wed gives lucas apple"),
    b.Scene("2.6.6", [3, 9], "wed and lucas exit"),
    b.Scene("2.6.7", [9, 10], "fester exits"),
    b.Scene("2.6.8", [5, 9, 10, 11], "Come to mama! - alice"),

    b.Scene("2.7.0", [2, 6], "scene"),
    
    b.Scene("2.8.0", [1], "scene"),
    b.Scene("2.8.1", [1, 8], "lurch enters"),
    b.Scene("2.8.2", [1, 3], "fester re-enters"),
    
    b.Scene("2.9.0", [1, 2], "scene"),
    b.Scene("2.9.1", [1], "like a lawyer - mort"),
    b.Scene("2.9.2", [1, 2], "and dance - gomez (mort rises)"),

    b.Scene("2.10.0", [1], "scene"),
    b.Scene("2.10.1", [1, 9, 10], "alice + mal enter"),
    b.Scene("2.10.2", [2, 5, 11], "longs to hear - gomez"), # add gomez?
    b.Scene("2.10.3", [1, 2], "May you have many children - mort"),
    b.Scene("2.10.4", [1, 2, 4, 5, 6, 9, 10, 11], "Oh the french - gomez"),
    b.Scene("2.10.5", [1, 2, 5, 6], "Welcome to our family! - gomez"),
    b.Scene("2.10.6", [8], "You are a true Addams! - gomez"), # combine with .7?
    b.Scene("2.10.7", [2, 5, ancestors], "And smile - lurch"),
    b.Scene("2.10.8", [1, 2, 5, 8, 9, 10, 11], "Can we learn whats there? - mort + wed"),
    b.Scene("2.10.9", [1, 2, 3, 10], "fester appears"),
    b.Scene("2.10.10", [5, 9, 10, 11], "To the moon, alice. - fester"), # fix numbers in book
    b.Scene("2.10.11", [1, 3], "fester is fully outfitted and ready to go"),
    b.Scene("2.10.12", [all], "fly on wings of love! - gomez"), # narrow the scope of "all" w/ cast list

    b.Scene("3.1.0", [all], "curtain call") # possibly narrow the scope of "all" w/ cast list / boundary mic
])

b.setMutes(range(1,25), True)

b.fetch() # attempt to populate midi variables with board values

Thread(target=b.startUI).start()
Thread(target=b.startReading, daemon=True).start()