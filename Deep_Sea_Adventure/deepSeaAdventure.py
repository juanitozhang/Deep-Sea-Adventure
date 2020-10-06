"""DEEP SEA ADVENTURE

This is a text based implementation of a modified version of the board game
Deep Sea Adventure (KAITEITANKEN) by Jun Sasaki and Goro Sasaki. 

It also includes a computer intelligence desgined to play one round against
a human player. 

by Juanito Zhang Yang.
CS 111, Spring 2019
"""


import random
import os

class TextInterface:
    """Text based interface for Deep Sea game. Most of the user interaction
    happens through one of these methods"""
    
    def roundEnd(self, turn, playerlist):
        """After the round ends, prints the scoreboard, who starts next and
        informs that the board has changed. 
        Keyword parameters:
        turn -- integer
        playerlist -- list of Player type objects
        """
        os.system("clear")
        print("-----ROUND HAS ENDED-----\n")
        print("Board has been modified!!\n")
        print("-- Scoreboard --\n")
        for player in playerlist:
            print(player, "has", player.getPoints(), "points.")
        print("\n" + str(playerlist[turn]), "Starts Next Round!")
        input("\nPRESS ENTER TO CONTINUE")
    
    def setUpPlayers(self):
        """Asks the user how many players there are and asks for the specified
        amount of names. Returns a list of Player type objects with those
        names in the order they were given.
        """
        playerList = []
        takenNames = [] #Since __eq__ is not in Player() and...
        
        os.system("clear")
        numPlayers = 0
        numTimes = 0
        while not 2 <= numPlayers <= 6:
            if numTimes == 1:
                print("Invalid input.")
            numPlayers = int(input("How many players? 2-6: ")) 
            numTimes = 1
            
        print("\nThe player who has been most recently to the sea is Player 1")
        print("If there is no one, simply type in randomly.")
        print("Order here will remain throughout the game.\n")
        
        for time in range(1, numPlayers+1):
            
            name = input("Player "+str(time)+", What is your name? ")
            while name in takenNames: #...doing Player in playerList gives always False
                print(name, "has been taken! Please choose another.")
                name = input("Player"+str(time)+" What is your name? ")
            
            playerList.append(Player(name))
            takenNames.append(name)
        
        return playerList
    
    def setUpBotGame(self):
        """Creates the two players for the bot game. Asks whether the human player
        wants to be first or not. Returns a list of the corresponding Player types."""
        os.system("clear")
        decision = ""
        name = "Hal"
        time = 0
        while decision != "N" and decision != "Y":
            if time == 1:
                print("Error, (Y) or (N)")
            print("Do you want to go first?")
            decision = input("(Y)es or (N)o: ")
            time = 1
        while name == "Hal": 
            if time == 0:
                print("Error! Our system's name is Hal")
                print("Please use another name")
            name = input("What is your name? ")
            time = 0
        if decision == "Y":
            return [Player(name), Player("Hal", True)]
        else:
            return [Player("Hal", True), Player(name)]
            
    def facingDesicion(self, player):
        """Asks the player if they want to turn around to the submarine. Then changes 
        the facing instance variable in player object given if user says yes. 
        Keyword parameters:
        player -- A Player type object. 
        """
        decision = ""
        time = 0
        while decision != "Y" and decision != "N":
            if time == 1:
                print("ERROR!, type in Y or N")
            print("Can only be done once per round")
            decision = input("Do you want to turn back? (Y)es or (N)o ")
            time = 1
        
        if decision == "Y":
            player.changeFacing()
            
    def exploreDecison(self, numChips, currChip, blankChip):
        """This method asks for user input about what they want to
        do after they have rolled the dice. Returns '2' if they want to
        pick up chip, '3' to place and '' for nothing. 
        Keyword parameters:
        numChips -- integer, number of chips user has
        currChip -- RuinChip type object, where they are standing
        blankChip -- instance of a 'blank' RuinChip. 
        """
        numTimes = 0
        decision = None
        if type(currChip) == tuple: #If it is more than one chip I can always pick it.
            while decision != "" and decision != "2":
                if numTimes == 1:
                    print("Error!")
                print("Press Enter to Do Nothing")
                print("Type in 2 to Pick up a ruin chip")
                decision = input("Type in your decision: ")
                numTimes = 1
        
        elif numChips > 0 and str(currChip) == str(blankChip): #No __eq__ set up for RuinChip
            while decision != "" and decision != "3":          #Turns out this is enough
                if numTimes == 1:                              #for equality for us. 
                    print("Error!")
                print("Press Enter to Do Nothing")
                print("Type in 3 to Place a Ruin chip")
                decision = input("Type in your decision: ")
                numTimes = 1
        
        elif str(currChip) == str(blankChip):
            print("Ups, can't do anything")
            input("Press ENTER to continue")
            decision = ""
        
        else:
            while decision != "" and decision != "2":
                if numTimes == 1:
                    print("Error!")
                print("Press Enter to Do Nothing")
                print("Type in 2 to Pick up a ruin chip")
                decision = input("Type in your decision: ")
                numTimes = 1
        
        return decision    
    
    def chipChoice(self, player):
        """If the user chose to place a chip, this asks him what chip he wants to place. 
        Returns the index (integer) of the chip in the list that the Player has in its
        instance variables. 
        Keyword parameters:
        Player -- A Player type object. 
        """
        chiplist = player.getChips()
        maxRange = len(chiplist)

        numTimes = 0
        choice = -1
        
        while not 0 <= choice <= maxRange - 1:
            if numTimes == 1:
                print("\nError!")
            print("\nPlease choose which chip to place\n")
            for i in range(maxRange):
                print("Type in", i, "to replace chip of level", chiplist[i])
                if i != maxRange - 1:
                    print("or")
            choice = int(input("\nType in choice: "))
            numTimes = 1
        
        return choice
    
    def gameState(self, board, playerlist):
        """With a lot of formating, this method prints the information about the board:
        the submarine, the chips and where players are. 
        Keyword parameters:
        board -- Board type object. 
        playerlist -- list of Player type objects. 
        """
        print("--BOARD--")
        chiplist = board.getChipline()
        
        print("SUBMARINE:", end =" [" )
        
        string = ""
        for player in playerlist:
            if player.getPosition()== -1:
                string += str(player) + ", " #Note that "being in the submarine"
                                             #is defined indirectly. -1 in the board
        print(string[:-2], end = "] CHIPS:") #would be the last in the chip line. 
        for slot in chiplist: 
            print(" -- ", end="")
            print(slot, end="")
        print("\n")
    
    def playerHUD(self, currPlayer, playerlist, air, roundNum):
        """Designed to be printed before gameState method, shows all relevant information
        to the player. Namely, their own state, and the state of other players. 
        Keyword parameters:
        currPlayer -- Player type object, this is this player's turn. 
        playerlist -- List of all Player type objects in the game. 
        air -- integer, amount of air left. 
        roundNum -- integer, round number
        """
        os.system("clear")
        
        print("--This is", currPlayer, end="'s turn--\n")
        print("AIR LEFT:", air)
        print("ROUND NUM:", str(roundNum) +" out of 3")
        print("TURN:", currPlayer)
        print("TURN ORDER:", playerlist)
        
        print("--INFO--")
        print("GOING:", end=" ")
        if currPlayer.getFacing() == 1:
            print("FORWARD")
        else:
            print("BACK TO SUBMARINE")
        print("CURRENT CHIPS:", currPlayer.getChips(), end="   ")
        print("(AMOUNT OF CHIPS", currPlayer.getAmountChips(), end=")   ")
        print("TOTAL POINTS:", currPlayer.getPoints())
        
        print("--INFO ABOUT ALL PLAYERS--")
        
        for player in playerlist:
            print(player, end=": [")
            print(player.getPoints(), ", ", player.getChips(), end="]  ")
        print("\n")
    
class Player:
    """An instance of this class represents one user."""
    
    def __init__(self, name, bot = False):
        """Creates an instance of the class Player, its initial state is that
        of a player right before the game starts. 
        Keyword parameters:
        name -- string, the name of the player. 
        bot -- boolean, True if this player is a bot. False predetermined. 
        """
        self.name = name
        self.points = 0 #Throughout the game
        self.position = -1 #Position in the board (-1 is submarine)
        self.chips = [] #The chips (or tuple of chips) I have that round, a list of RuinChip objects
        self.facing = 1 #If I am going forward, +1, -1 if going back. 
        self.bot = bot #Am I a robot? 
    
    def selfAwareness(self):
        """Has Hal discovered its self conscoiusness? Returns a boolean, representing
        wether this player is a robot"""
        return self.bot 
    
    def getPosition(self):
        """Returns an integer, the position of the player at that time."""
        return self.position
    
    def setPosition(self, newPos):
        """Modifies the position to whatever the input is. 
        Keyword parameters:
        newPos -- integer, the new position
        """
        self.position = newPos
        
    def getAmountChips(self):
        """Returns an integer, the amount to chips this player has. Useful for
        reducing air and determining dice values. """
        return len(self.chips)
    
    def getChips(self):
        """Returns the list (this is important) of RuinChip objects this player has."""
        return self.chips
    
    def popChip(self, idx):
        """Removes and returns the chip (could also be a tuple of chips) at idx in the 
        list of chips. 
        Keyword parameters:
        idx -- integer. index of chip in the list
        """
        return self.chips.pop(idx)
    
    def changeFacing(self):
        """Modifies wether player is moving forward or backwards by simply multiplying
        the previous state by -1."""
        self.facing *= -1
        
    def addChip(self, chip):
        """Adds a chip(or tuple of chips) to the list of chips this player has.
        Keyword parameters:
        chip -- RuinChip object or tuple of RuinChip objects. 
        """
        self.chips.append(chip)
        
    def resetChips(self):
        """Sets the chips of a player to an empty list."""
        self.chips = []
    
    def getFacing(self):
        """Returns the facing value of this player, either 1 or -1"""
        return self.facing
    
    def getPoints(self):
        '''Returns the points this player has, an integer.'''
        return self.points
    
    def calculatePoints(self):
        '''Calculates the tolal points in the list of RuinChips assosiated with
        this player and adds it to the points they had before.'''
        for chip in self.chips:
            if type(chip) == tuple: #Sometimes it can be a tuple
                for chipInTuple in chip:
                    self.points += chipInTuple.getValue()
            else:
                self.points += chip.getValue()
    
    def __str__(self):
        '''Returns the string that represents the name of the player.'''
        return self.name

    def __repr__(self):
        '''Returns the string that represents the name of the player. Useful when printing
        the list of players later on.'''
        return self.name
        
class RuinChip:
    """An isntance of this class represents a chip of the board, it has two isntances:
    its level, and its value. """
    
    def __init__(self, level, value):
        """Initiates an instance of this class. Within the logic of the game, a blank is
        of level 0 and value 0. For levels 1 , 2 , 3, 4 they have determined values. 
        Keyword parameters:
        level -- integer, level of chip (what faces up)
        values -- integer, values of chip points (what faces down)"""
        self.level = level
        self.value = value
        
    def getValue(self):
        """Return an integer, the value of the chip"""
        return self.value
    
    def getLevel(self):
        """Return an integer, the level of the chip"""
        return self.level
    
    def __str__(self):
        """Returns a string, the level of the chip"""
        return str(self.level)
    
    def __repr__(self):
        """Returns a string, the level of the chip, useful for tuples of chips."""
        return str(self.level)
    
class BoardSlot:
    '''Each "place" of the board is represented by an instance of this class. It can up to 3 chips and 1 player'''
    
    def __init__(self, chip, chip1 = None, chip2 = None):
        """Initiates an instance of the class BoardSlot. It initially only holds the chips in the board slot.
        Notice there is no representation of the 'empty' slot, we simply delete the BoardSlots we want to. 
        Keyword parameters:
        chip -- RuinChip object, the first chip.
        chip1 -- RuinChip object, the second chip, if there is
        chip2 -- RuinChip object, the third chip, if there is. 
        """
        self.chip = chip 
        self.chip1 = chip1
        self.chip2 = chip2
        self.player = None
    
    def getChip(self):
        """Returns the RuinChip in the first chip slot or a tuple of RuinChips if the others slots are defines"""
        if self.chip1 == None: #The reason I didn't set __eq__ for RuinChip is this. 
            return self.chip
        elif self.chip2 == None:
            return self.chip, self.chip1
        else:
            return self.chip, self.chip1, self.chip2
    
    def getPlayer(self):
        """Returns the player instance variable, it will be a Player type object or None."""
        return self.player
    
    def setChip(self, chip):
        """Takes in a RuinChip or tuple of RuinChip objects and places them in the corresponding
        instance variables. 
        Keyword parameters:
        chip -- RuinChip or tuple of RuinChips.
        """
        if type(chip) == tuple:
            if len(chip) == 2:
                self.chip = chip[0]
                self.chip1 = chip[1]
            if len(chip) == 3:
                self.chip = chip[0]
                self.chip1 = chip[1]
                self.chip2 = chip[2]
        else:
            self.chip = chip
            
    def __eq__(self, other):
        """For us, we only need to know if two board slots are the same if they both have blank chips, see 
        the removeBlanks method of Board class for more info. Returns a boolean. """
        return str(other.getChip()) == str(self.getChip()) #For us, it is enough for chips to be the same 
                                                           #if their string is the same
    def setPlayer(self, player):
        """Sets the player instance variable to a player, in other words, there is a player standing on this
        spot. 
        Keyword parameters:
        player -- Player type object."""
        self.player = player
    
    def __str__(self):
        """Returns two different strings depending on wether there is a player. This method is designed thinking
        on the gameState method in TextInterface class."""
        if self.player != None:
            return "( " + str(self.getChip()) + " ) ["+str(self.player)+"]" #Formated for gameState method in 
        else:                                                               #TextInterface class. 
            return "( " + str(self.getChip()) + " ) []" #So that it doesn't print 'None' 
        
    def __repr__(self):
        """Returns the tuple of the chips and player in this slot. Helpful while designing the game, since the board
        is a list of BoardSlots."""
        return str((self.getChip(), self.player))
    
class Board: 
    """This represents the line of board slots. It doesn't inclue, however, the submarine"""
    
    def __init__(self):
        """Initiates an instance of this class. The line of chips is, for now, simply an empty
        list."""
        self.chipline = [] #This is going to be a list of boardslots, but it doesn't 
                           #I doesn't include the submarine, which is technically part
    def getChipline(self): #Of the board.
        """Returs the list of boardslots. """
        return self.chipline
    
    def getPlayerInSlot(self, idx):
        """Returns the Player object (or None if applicable) in the slot that is at idx in the
        chip line. 
        Keyword parameters:
        idx -- integer, index of slot we want to look at. 
        """
        return self.chipline[idx].getPlayer()
    
    def getChipLineLen(self):
        """Returns the length (integer) of the chip line. This and the previous method are useful
        when moving the player around. """
        return len(self.chipline)
    
    def getChipInSlot(self, idx):
        """Returns the RuinChip object (or tuple of chips if applicable) in the slot that is at
        idx in the chip line.
        Keyword parameters:
        idx -- integer, index of slot we want to look at. 
        """
        return self.chipline[idx].getChip()
    
    def addPlayerInSlot(self, idx, player):
        """Adds a player type object in the slot at idx in the chip line.
        Keyword parameters:
        idx -- integer, index of slot we want to add player at.
        player -- Player type object
        """
        self.chipline[idx].setPlayer(player)
        
    def addSlot(self, slot):
        """Adds a slot to the end of the chip line. 
        Keyword parameters:
        slot -- instance of BoardSlot class. 
        """
        self.chipline.append(slot)
        
    def removeBlanks(self):
        """Removes all of the slots that have a blank chip on them."""
        blank = BoardSlot(RuinChip(0,0))
        while blank in self.chipline:   #This is why __eq__ in BoardSlot is useful (and enough)
            self.chipline.remove(blank) #For our purposes.
        
    def replaceChip(self, idx, chip):
        """Changes the chip (or tuple of chips) in the slot at idx in the list to the input chip 
        (or tuple of chips)
        Keyword parameters:
        idx -- integer, index of slot we want to look at. 
        chip -- RuinChip object or tuple of RuinChip objects. 
        """
        self.chipline[idx].setChip(chip)
        
    def createBoard(self):
        """Creates the chip line as it is at the start of the first round. Please refer to Preparations
        in Instruction Manual"""
        for level in range(1, 5):
            
            possibleValues = list(range((level - 1)*4 , (level-1)*4 + 4)) * 2 
            
            for i in range(8):
                
                value = random.choice(possibleValues)
                possibleValues.remove(value)
                self.addSlot(BoardSlot(RuinChip(level, value)))
                
    def resetBoard(self, lostChips):
        """Takes a list of RuinChips (some/all of them can be tuples of chips) and leaves
        them at the end of the chip line in groups of three, randomly. Refer to 'Players
        who didn't make it back to submarine' in Manual and consider my comment in texts/mods.txt.
        Keyword parameters:
        lostChips -- a list of RuinChips or tuple of RuinChips. 
        """
        justChips = [] # If there are tuples, I will 'unzip' them and append them here
        for item in lostChips:
            if type(item) == tuple:
                for chip in item:
                    justChips.append(chip)
            else:
                justChips.append(item)
        
        random.shuffle(justChips)
        while len(justChips) % 3 != 0: 
            justChips.append(None) #If it is not a multiple of 3, append None types until it is
        
        for i in range(0, len(justChips), 3):
            chip = justChips[i] 
            chip1 = justChips[i+1]
            chip2 = justChips[i+2] 
            self.addSlot(BoardSlot(chip, chip1, chip2)) #The None types will not matter beacuse of
                                                        # the way BoardSlot is designed. 
    def removePlayers(self):
        """Removes any players that are in the slots of the chip line. """
        for boardslot in self.chipline:
            boardslot.setPlayer(None)
                
class Game:
    """Represents a game of Deep Sea Adventure. """
    
    def __init__(self):
        """Creates an instance of the game. It sets five instance variables. One for the board, a list of 
        players, their states, the interface, and a Bot. """
        self.board = Board() 
        self.playerlist = []
        self.playerstates = [] #Although this information is somewhat redundant, I think it is more
        self.interface = TextInterface() #Convenient to access it this way. 
        self.bot = None # To hold a Bot object, if necessary.  
    
    def updateStates(self):
        """Updates the playerstates instance variable with the positions of the players. """
        self.playerstates = []
        for player in self.playerlist:
            self.playerstates.append(player.getPosition())
        
    def setPlayers(self, bot = False):
        """Creates the player list (and thus the players also) by asking for user input
        Keyword parameters:
        bot -- Boolean, True if this is a bot game. False is default. 
        """
        if bot:
            self.playerlist = self.interface.setUpBotGame()
        else:
            self.playerlist = self.interface.setUpPlayers()
    
    def endRound(self):
        """Determines if a player made it back to the submarine or not. If yes, counts the points
        gained from the chips (or tuple) they have. If no, removes the chips (or tuple) they had and
        appends them to a list. Returns that list. For more info refer to Round Conclusion in Manual."""
        lostChips = [] 
        for player in self.playerlist:
            if player.getPosition() != -1: 
                lostChips += player.getChips()
                player.resetChips()
            else: 
                player.calculatePoints()
                player.resetChips()
        return lostChips
    
    def determineFirst(self, lastPlayerInSubIdx, numPlayers): # I pass numPlayers just to not call len again. 
        '''Determines what the first player in the next round should be. Returns the index of that player in
        the playerlist. Refer to Round Conclusion in Manual for more information. 
        Keyword parameters:
        lastPlayerInSubIdx -- integer, index of the player that was last in the sub, if any. 
        numPlayers -- number of players in the game, integer
        '''
        if self.playerstates != [-1] * numPlayers: 
            maxPos = -1
            maxIdx = 0
            for idx in range(len(self.playerlist)):
                pos = self.playerlist[idx].getPosition()
                if pos > maxPos:
                    maxPos = pos
                    maxIdx = idx
            return maxIdx
            
        else:
            return lastPlayerInSubIdx
    
    def resetPlayers(self):
        """Prepares the players for the next round, it sets their facing to be forward and their position to
        -1."""
        for player in self.playerlist:
            player.setPosition(-1)
            if player.getFacing() == -1:
                player.changeFacing()
        
        self.playerstates = []
                    
    def aRound(self, turn, roundNum, numPlayers):
        """Plays one round of the game. The first player depends on the input. Returns an integer, the index of 
        the last player that was in the sub, if any. 
        Keyword parameters:
        turn -- integer, index of player that starts in the list
        roundNum -- integer, number of round
        numPlayers -- integer, number of players. 
        """
        air = 25
        lastPlayerInSubIdx = None
        firstRound = 0 # Garantees that everyone can get a turn if they are in the sub (for the while loop). 
        endstate = [-1] * numPlayers
        while self.playerstates != endstate and air > 0: # The first time, player states is an empty list
                                                                  # So while the first time everyone is in the sub,
            currPlayer = self.playerlist[turn % numPlayers]       # because of this the while loop is true. 
            
            if currPlayer.getPosition() != -1 or firstRound < numPlayers: # You cannot return in your first turn
                                                                          # So everyone gets a turn. 
                air -= currPlayer.getAmountChips()
                
                self.turn(currPlayer, air, roundNum)

                if currPlayer.getPosition() == -1:
                    lastPlayerInSubIdx = turn % numPlayers # If someone gets back gets the index until someone else
                                                           # does. 
                self.updateStates() 
                
            firstRound += 1
            turn += 1
        return lastPlayerInSubIdx
            
    def turn(self, currPlayer, air, roundNum):
        '''Turn progression for one player: declaring facing decision, Roll dice and move and Search (manipulating chips). 
        Please refer to Turn Progress in Manual. 
        Keyword parameters:
        currPlayer -- Player type object. this is their turn
        air -- integer, air left
        roundNum -- integer, number of round
        '''
        currPos = currPlayer.getPosition()
        
        self.interface.playerHUD(currPlayer, self.playerlist, air, roundNum)
        self.interface.gameState(self.board, self.playerlist)
        
        if currPos != -1 and currPlayer.getFacing() == 1: # The first boolean expression refers to that you cannot
            if currPlayer.selfAwareness():                # Change facing decision in first turn. 
                changefunc = self.bot.directionDecision   # The second, that it can only be done once 
                decision = self.bot.decisionFunction(air, currPlayer, \
                                                  self.playerlist, self.board, changefunc)
                if decision == "Y":
                    currPlayer.changeFacing()
                    print("Hal has decided to go back")
                else:
                    print("Hal has decided to keep going forward")
                input("PRESS ENTER TO CONTINUE")
            else:
                self.interface.facingDesicion(currPlayer)
        
        self.playerMove(currPlayer, air, roundNum)
        
        self.playerExplore(currPlayer, air)
        
        if not currPlayer.getPosition() == -1:
            self.interface.playerHUD(currPlayer, self.playerlist, air, roundNum)
            self.interface.gameState(self.board, self.playerlist)
            print("ACTION EXECUTED. TURN HAS ENDED.")
            input("PRESS ENTER TO CONTINUE")
        
    def playerMove(self, currPlayer, air, roundNum):
        """Determines the dice value and moves the player accordingly. Refer to number three on Turn Progression
        Keyword parameters:
        currPlayer -- Player type object, this is their turn
        air -- integer, air left
        roundNum -- integer, number of round
        """
        currPos = currPlayer.getPosition()
        numChips = currPlayer.getAmountChips()
        
        if not currPlayer.selfAwareness(): # Computers roll their own dice
            input("Hit Enter to Roll Dice")
                        
        dice1 = random.randint(1,3)
        dice2 = random.randint(1,3)

        dicesum = dice1 + dice2 - numChips
        
        if dicesum < 0:
            dicesum = 0
        
        self.interface.playerHUD(currPlayer, self.playerlist, air, roundNum)
        
        print("DICES:", dice1, "and", dice2, "Total (minus num of chips):", dicesum, "\n")
        
        if currPos != -1:
            self.board.addPlayerInSlot(currPos, None) # The player disappears from the board
        
        dif = currPlayer.getFacing()
        
        while dicesum > 0: 
            while dif + currPos < self.board.getChipLineLen() and self.board.getPlayerInSlot(currPos + dif) != None: 
                currPos += dif # This is when we can skip a player, and we skip as much as we can. 
            if dif + currPos < self.board.getChipLineLen() and self.board.getPlayerInSlot(dif + currPos) == None: 
                currPos += dif 
            while self.board.getPlayerInSlot(currPos) != None: 
                currPos -= 1 # Beacuse of how the first while loop is setup, we must account for the case where
            dicesum -= 1     # Everyone piles up at the end. 
        
        if currPos < -1:
            currPos = -1
        
        currPlayer.setPosition(currPos) 
        
        
        if currPos > -1:
            self.board.addPlayerInSlot(currPos, currPlayer) # As said earlier, if player is in submarine,
                                                            # then they don't come back to the board.  
        self.interface.gameState(self.board, self.playerlist)
        
        if currPos == -1 and not currPlayer.selfAwareness():
            input("YOU GOT BACK TO THE SUBMARINE! \nPRESS ENTER TO CONTINUE")
        
        if currPlayer.selfAwareness():
            if currPos != -1:
                input("Hal has rolled his die.\nPRESS ENTER TO CONTINUE")
            else: 
                input("Hal rolled his die and got back to the submarine.\nPRESS ENTER TO CONTINUE")
        
    def playerExplore(self, currPlayer, air):
        '''Depending on the situation, the player can either pick up or place a chip or do nothing. This
        method takes care of all of this. For more information look at search in Manual.
        Keyword parameters:
        currPlayer -- Player type object, this is their turn
        air -- integer, air left
        '''
        currPos = currPlayer.getPosition()
        
        if currPos != -1: # In case they got back to the submarine in this turn. 
            numChips = currPlayer.getAmountChips()
            blankChip = RuinChip(0,0)
            currChip = self.board.getChipInSlot(currPos)
            
            if not currPlayer.selfAwareness():
                decision = self.interface.exploreDecison(numChips, currChip, blankChip)

            else:
                if str(currChip) != str(blankChip) or type(currChip) == tuple:
                    expfunc = self.bot.pickUpDecision
                    decision = self.bot.decisionFunction(air, currPlayer, \
                                                      self.playerlist, self.board, expfunc)
                else:
                    decision = ""
                
                if decision == "2":
                    input("Hal has decided to pick up this chip \nPRESS ENTER TO CONTINUE")
                else:
                    print("Hal has decided to do nothing")
                    input("PRESS ENTER TO CONTINUE")
                      
            if decision == "2":
                currPlayer.addChip(currChip)
                self.board.replaceChip(currPos, (blankChip, None, None)) # The None, None are in case it
                                                                         # was a tuple they picked up. 
            if decision == "3":
                choice = self.interface.chipChoice(currPlayer)
                newChip = currPlayer.popChip(choice)
                self.board.replaceChip(currPos, newChip) # Here the replaced chip is always a blank. 
                
    def endGame(self):
        '''Determines and prints the winner of the game.'''
        os.system("clear")
        print("---GAME HAS ENDED---\n")
        
        scoreboard = {}
        
        for player in self.playerlist:
            points = player.getPoints()
            print(player, "got", str(points), "points.")
            if points in scoreboard:
                scoreboard[points].append(player)
            else:
                scoreboard[points] = [player]
                
        winner = scoreboard[max(scoreboard)]
        if len(winner) == 1:
            print(end = "\n")
            print(winner[0], "WINS!!")
        else:
            print("\nTHERE IS A TIE BETWEEN", str(winner)[1:-1])
            
        input("\n\nPRESS ENTER TO CONTINUE")
    
    def play(self, bot = False):
        """Plays a game of Deep Sea Adventure, if all humans: three rounds from 2 to 6 players.
        if robot, only one round with one human player and one bot. 
        Keyword parameters:
        bot -- Boolean, True if there is a bot. Default is False. 
        """
        self.setPlayers(bot)
        numPlayers = len(self.playerlist)
        self.board.createBoard()
        
        turn = 0
        roundrange = 4
        if bot:
            self.bot = Bot()
            roundrange = 2
        
        for roundNum in range(1, roundrange):
            
            lastPlayerInSubIdx = self.aRound(turn, roundNum, numPlayers)
            
            lostChips = self.endRound()
            
            if bot:
                return self.endGame()
            if roundNum < 3:
                
                self.board.resetBoard(lostChips)
                turn = self.determineFirst(lastPlayerInSubIdx, numPlayers)
                self.interface.roundEnd(turn, self.playerlist)
                self.board.removeBlanks()
                self.board.removePlayers()
                self.resetPlayers()
                 
        self.endGame()

class Bot:
    """The computer intelligence designed to play one round of this game against a human"""
    
    def __init__(self):
        """Initiates an instance of this class. The two variables represent what I need
        to remember from turn to turn."""
        self.facestate = 0 #How many times it has asked me to decide on facing
        self.pickstate = 0 #If this is one, I really want to pick this chip. 
    
    def decisionFunction(self, air, bot, playerlist, board, functype):
        """Asks the bot to make a decision, returns that decision in a form of a string
        The decision depends on the input. 
        Keyword parameters: 
        air -- integer, air left
        bot -- the current Player, who we know is a bot,
        playerlist -- a list of Player type obejcts.
        board -- a Board type object. 
        functype -- a Bot method, either direction or pick Decision. 
        """
        for player in playerlist:
            if str(bot) != str(player):
                enemy = player
        ibot = self.rawPlayer(bot) #i stands for info,  since it only holds
        ienemy = self.rawPlayer(enemy) #the raw info i need, without messy instance
        iboard = self.rawBoard(board) #variables and methods. 
        
        decision = functype(air, ibot, ienemy, iboard)
        return decision
    
    def rawBoard(self, board):
        """Returns a list of integers representing the levels of board. 
        Keyword parameters:
        board -- Board type object. 
        """
        infoList = []
        for boardslot in board.getChipline(): 
            chip = boardslot.getChip()
            level = chip.getLevel()
            infoList.append(level) 
       
        return infoList
            
    def rawPlayer(self, player):
        """Returns a list of integers that represents the position, amount of
        chips and facing of input. 
        Keyword parameters:
        player -- Player type object.
        """
        infoList = []
        infoList.append(player.getPosition())
        infoList.append(player.getAmountChips())
        infoList.append(player.getFacing())
        return infoList
    
    def directionDecision(self, air, ibot, ienemy, iboard):
        """Asks the bot to decide on wether to turn back or not. 
        Keyword parameters: 
        air -- integer, air left
        ibot -- list of integers, the state of bot,
        ienemy -- list of integers, the state of enemy.
        iboard -- list of integers, the levels of board.
        """
        
        self.facestate += 1
        
        if ibot[1] > 0: #TURN BACK AS SOON AS YOU PICK CHIP. 
            return "Y"
        elif self.facestate == 1: #Never let your first chip be a level 1. 
            return "N"
        elif self.facestate == 2:
            if 14 < ibot[0]:
                if ienemy[0] < 8: # I am far ahead on the board
                    self.pickstate = 1 # So I can risk it and pick the next chip
                    return "N" # Also I am pretty close to the level 3's (within one
                                # expected value.)
                if ienemy[2] == -1: #If the enemy is turning back with no chips.
                    if ienemy[1] == 0: #Not redcuing air and he could go back
                        return "N" #To sub soon. 
                return "Y"
            elif ibot[0] < 8: #I don't like a level 1
                return "N"
            else:
                self.pickstate = 1 #According to strategy. 
                return "N"
        else:
            if ibot[0] >= 8: 
                if ibot[0] == 15: #I am right in the border
                    if ienemy[0] > ibot[0]:
                        if ienemy[1] == 0: #Enemy is not doing enything
                            self.pickstate = 1 #I could just greed
                            return "N"
                    if ienemy[0] < 12: #Enemy is close to sub
                        if enemy[1] == 0: #Not doing anything
                            return "N"
                        if enemy[2] == -1: #He is not affecting anything. 
                            return "N"
            return "Y"
                
    def pickUpDecision(self, air, ibot, ienemy, iboard):
        """Asks the bot to decide on wether to pick up a chip or not. 
        Keyword parameters: 
        air -- integer, air left
        ibot -- list of integers, the state of bot,
        ienemy -- list of integers, the state of enemy.
        iboard -- list of integers, the levels of board.
        """
        if self.pickstate == 1:
            return "2"
        
        elif ibot[1] == -1 and ibot[2] == 0: #If somehow am turning back with
            return "2" #No chips, I must pick up one as soon as possible. 
        
        elif self.facestate == 0: #I don't want these chips. 
            return ""
        elif ibot[2] == 1: #If still going forward, 
            if self.facestate == 1:
                if 11 < ibot[0]: #By the second turn I am already ahead,
                    if air > 20: #I could risk it. 
                        return ""
                if 8 > ibot[0]: # I don't like level 1's
                    return ""
                return "2" #All other scenarios: stick to  plan. 
            elif self.facestate == 2:
                if 16 > ibot[0] >= 8:
                    if ibot[0] > 14: # I have a chance to greed
                        if ienemy[0] < 8: #Without getting punished to much
                            return "" 
                    if ienemy[2] == -1: 
                        if ienemy[1] == 0: #The enemy is turning back with
                            return "" #No chips????
                    return "2"
                elif 16 >= ibot[0]: #This is very lucky. 
                    return "2"
                else:
                    return ""

            else:
                return "2" # It's too late, I must pick and go. 
        
        else: # We can assume I am turning back
            weight = ibot[1] + ienemy[1] #Measure of total air consumed per turn
            if ibot[0] == 1:
                if ibot[0] == 1: #This is the I am close to sub so I can greed. 
                    if weight > 0 and air//weight >1:
                        return "2" 
            if ibot[0] == 0:
                if ibot[0] == 2: #air//weight measures what is the chance
                    if weight > 0 and air//weight >2: #That I will play again. 
                        return "2"
                    if weight == 0:
                        return "2"
            if ienemy[0] > ibot[0]:
                if ibot[0] < 12: #I bot is close to sub but enemy is not
                    if weight >0  and air//weight > 2:    
                        return "2" #We can greed. 
            if ibot[0] - 3 >= 0 and iboard[:ibot[0]-3].count(0) > 3:
                if air//weight > 2: #This counts that there are too many
                    if ibot[0] < 10: #Blanks ahead, so I secure one chip now. 
                        return "2"
            return "" #I really shouldn't greed. 
        
def gameMenu(title):
    """Game menu. Asks for user input to start a game. 
    Keyword paramaters:
    title: string, the name of the game.
    """
    os.system("clear")
    print(title, end="\n\n")
    print("--GAME MENU--\n")
    print("FOR A NORMAL HUMAN GAME PRESS ENTER")
    print("TO GO BACK TO MENU PRESS M")
    print("FOR A BOT 1V1 INPUT ANY OTHER KEY")
    decision = input("\n-->")
    if decision == "":
        Game().play()
    elif decision == "M":
        return mainMenu(title)
    else:
        Game().play(True)
    os.system("clear")
    print(title, end="\n\n")
    print("PRESS ENTER TO EXIT")
    print("TO GO TO TITLE INPUT ANYTHING ELSE")
    decision = input("\n-->")
    if decision == "":
        exit()
    else:
        main()
    
def mainMenu(title):
    """Prints the main menu. From here we can go to the game menu, title or instruction menu.
    Keyword paramaters:
    title: string, the name of the game.
    """
    os.system("clear")
    print(title, end="\n\n")
    print("--MAIN MENU--\n")
    print("TO GO TO GAME MENU, SIMPLY PRESS ENTER")
    print("TO EXIT, PRESS E")
    print("TO GO TO TITLE, PRESS T")
    print("TO READ INSTRUCTIONS (RECOMMENDED), INPUT ANY OTHER KEY")
    decision = input("\n-->")
    if decision == "":
        gameMenu(title)
    elif decision =="E":
        exit()
    elif decision =="T":
        main()
    else:
        instructionMenu(title)
        
def instructionMenu(title):
    """Prints the instruction manual and according to user input shows
    important information about the game
    Keyword paramaters:
    title: string, the name of the game.
    """
    os.system("clear")
    print(title, end="\n\n")
    print("--INSTRUCTION MENU--\n")
    print("FOR AN EXPLANATION ON THE HUD INPUT H")
    print("TO SEE THE INSTRUCTION MANUAL INPUT I")
    print("TO GO BACK TO MAIN MENU PRESS ENTER")
    decision = input("\n-->")
    if decision == "H":
        os.system("open images/hud.png")
        os.system("open images/hudimage.jpeg")
        os.system("clear")
        print("hudimage.jpeg is an image of the real game. \nPlease use your imagination!")
    if decision == "I":
        os.system("open images/manual.png")
        textfile = textfile = open("texts/mods.txt")
        os.system("clear")
        for line in textfile: 
            print(line , end = "")
        print("\n")
    if decision == "":
        return mainMenu(title)
    input("\n\nPRESS ENTER TO GO BACK")
    instructionMenu(title)
    
def main():
    '''Main function, runs the title and main menu '''
    title = "------------DEEP SEA ADVENTURE-------------"
    os.system("clear")
    textfile = open("texts/usefulText.txt")
    for line in textfile: 
        print(line , end = "")
    input("\n\nPRESS ENTER TO CONTINUE")
    mainMenu(title) 

if __name__ == "__main__":
    main()