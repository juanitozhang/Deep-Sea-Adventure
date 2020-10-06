in directory: 
deepSeaAdventure.py
readme.txt
    in /images:
        hud.png
        hudimage.jpeg
        manual.png
    in /texts:
        intelligence.txt
        mods.txt
        usefulText.txt

--- DEEP SEA ADVENTURE ---

For explanations on intelligence, please check out texts/intelligence.txt

This module implements most of the charasteristics of the Deep Sea
Adventure board game. Instructions for the game are found at images/
manual.png . It is completely text based, it prints a player HUD, where
all of the useful information available is shown for an informed decision. 
It also prints a sort of "Board", with the chipline ordered from left to right
and subsequently from top to bottom. Information about the interface is at
the images directory. This implementation also counts with a main menu, instructions
for the game can also be accessed from here. The game, and all its features
are can be runned throught the command line. 

As for the game itself, it is the 3 round, 32 chips, 2-6 player version, no others
are allowed as of yet. 


I think the Player and RuinChip objects speak for themselves, they are the
most abvious classes in term of necessities. The Player class allows me to
remember to the information I need from each user. Since RuinChips have two
important characteristics: level and value, a class is also useful to represent 
them. 

Next comes the BoardSlot and Board classes. The Board class needs to somehow 'hold'
chips and players at the same time in the same place and sometimes hold more than one 
chip or no player at all. Then simply adding Player and RuinChip instances to a list will not do, 
especially since this game has complicated manipulations (at least in my opinion). 
Thus, it is useful to create a Class that can hold my instances and have methods that are useful. 

As for the Board class, it might seem a bit redundant to have a separate class just to
hold a list, when we could simply have one more instance variable in the Game class. 
But Game class already had very long and complicated methods, so I decided to separate
the Board fromt he Game, since it also has somewhat complicated manipulations that are proper
to it (for example, resetting and removing blanks after a round). 
 
Also, the interface.py from HW11 made me think that classes can also be a collection of methods
with a similar concept rather than  object oriented programming. That is why TextInterface class is
so helpful. It can group all of the methods with long and tedious print and input statements, so that
Game can seem a bit easier to read. Thus, most of the user interaction happens through this class. 
Some methods do some work though. (Like the one that changes the facing)

The Bot class, since it only needs one instance can be refered to by a instance variable
of Game, which can help while calling. 
The Bot class has two instance variables, that help me remeber what I have been doing
since my two main strategical decisions (picking and returning) must be related. 

As for how the game actually works: 
    The most important thing to figure out is movement and representation (what does it mean to
    be in the chip line or submarine).
    
    There is two ways about thinking about position. What the instance variable in Player says and if
    a BoardSlot holds a reference to Player and where that is in the Board (index of a list). 
    
    Thus we define that if position in Player is -1 I am in submarine. Only if it is greater
    I will be in the chip line (the list) and I will have a meaningful index. (-1 is actually the
    last spot in a list so we must be careful). 
    
    Then moving around is a manipulation of the posistion variable inside Player and seeing wether 
    I can move around the board by checking indexes inside of chip line. When a final position has been
    determined, I erase the reference of Player in the original spot and create a new reference in the
    new spot. 
    
    That was the hardest part. The other is how chips can be in stacks as well. For that we use tuples. 
    Although in BoardSlot it is three separate variables, the methods that return the chips always do so
    in tuples, and there are methods that receive tuples as well. This allows me to have tuples outside 
    of the BoardSlot class but multiple individual RuinChips inside. This allows easy manipulation but
    they count as one outside of the slot, which is what we want. 
    
    Equality between classes. 
        For two instances to be equal I only consider some things about them, not all. 
        For RuinChip and BoardSlot espacially there are a lot of comparisons. Since we should'nt know
        their value, we only consider their level. That is why we use str (we could also have used
        getLevel, but it is easier to right and in the end the same thing, since we don't allow that
        many values anyways (only 4))
        The only instances where this doesn't work and it matters (there is a tuple),  we do account for
        in exploreDecision. 
        

Status of program: 
    As for the game itself, I think I am pretty satisfied with what turned out, in terms of goals
    I accomplished them all. I was able to play several games to completion. Any bugs should be very
    special cases and relatively easy to fix. 
    If any, they should probably be beacuse of last minute modifications (espcially around Bot)
    
    As for the intelligence I am very disappointed. Creating a winning strategy was very hard, much 
    more than expected. I spent all weekend working on this with little results. The problem is that
    I was trying to be as good as possible and I kept loosing myself in an infinitude of Booleans. The
    Bot is not a good representation of how I think you should play the game. 
    
    Extra features I wish I had added: 
    graphics. 
    a highscore board. 
    a way to save games (what a pain to have the game suddenly crash at round 3).
    
--HOW TO RUN--

with the command line in the directory, type python3 deepSeaAdventure.py There is a menu there, should
explain itself. All features are accessible through there. 
My program ran on both my mac and the mac in the cmc labs. (I haven't updated either in a while) It, as
far as I know, should not run on Windows though. 


Techniques not covered in class:
1. The __eq__, __str__, and __repr__ are all talked upon in the
class part in the textbook. I sort of guessed how __repr__ worked
by looking at the cImage module. 
2. I sort of know how os works, since you used in some of the assign-
ments, but os.system("clear") I explicetely looked it up on the Internet
3. The end="" part of print I remember seeing it in one the readinds in
the textbook, I think. I am definetely sure it was somewhere in the 
course. 
4. Setting a default value for a parameter I don't know where I saw 
that. I definetely didn't look it up explicetely. 
5. type(chip) == tuple I discovered on my own, playing around with
classes and dir(__builtins__) while doing the readings. 
6. random.choice was on the documentation you sent us about random 
module in one of the first assignments I think. 
7. I guessed how os.system("open ...") worked by infering from the 
behavior of os.system("clear")