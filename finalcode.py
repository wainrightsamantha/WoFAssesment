from numpy import append
from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = ["dictionary.txt"]
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
consonants = {"b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"}
roundstatus = ""
finalroundtext = ""

###


# In[115]:


def readDictionaryFile():
    global dictionary
    dict_file = open("dictionary.txt", "r")
    dictionary = dict_file.read().splitlines()
    dict_file.close()

###


# In[116]:


def readTurnTxtFile():
    global turntext
    turn_file = open("turntext.txt", "r")
    turntext = turn_file.read()

    #read in turn intial turn status "message" from file
    
###


# In[117]:


def readFinalRoundTxtFile():
    global finalroundtext   
    final_file = open("finalround.txt", "r")
    finalroundtext = final_file.read()
    final_file.close()
    

    #read in turn intial turn status "message" from file

###


# In[118]:


def readRoundStatusTxtFile():
    global roundstatus
    status_file = open("roundstatus.txt", "r")
    roundstatus = status_file.read()
    
    # read the round status the Config roundstatusloc file location
    
###


# In[119]:


def readWheelTxtFile():
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location
    wheel_file = open("wheeldata.txt", "r")
    wheellist = wheel_file.read().splitlines()
    wheel_file.close()


###


# In[120]:


def getPlayerInfo(): #display player info throughout game
    global players

    # print("Players, enter your name:")
    # three_players = False
    # i = 0
    # while (not three_players):
    #         print(f"Player {i + 1}, enter your name:")
    #         name = input(f"name: ")
    #         players[i]['name'] = name
    #         i += 1
    #         if (i == 3):
    #             print("\n all three players are added, now we can play")
    #             three_players = True
    players[0]["name"] = input(f"Player 1, enter your name: ")
    players[1]["name"] = input(f"Player 2, enter your name: ")
    players[2]["name"] = input(f"Player 3, enter your name: ")




###


# In[ ]:

def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile()

###


# In[ ]:


def getWord():
    global dictionary
    global roundWord
    global roundUnderscoreWord

    roundWord = random.choice(dictionary).lower()
    
# make a list of the word with underscores instead of letters
    roundUnderscoreWord = ['_'] * len(roundWord)

    return roundWord, roundUnderscoreWord

###


# In[132]:


def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    # Set round total for each player = 0
    players[0]["roundtotal"] = 0
    players[1]["roundtotal"] = 0
    players[2]["roundtotal"] = 0
    
    # Return the starting player number (random)
    initPlayer = random.choice([0,1,2])
    
    # Use getWord function to retrieve the word and the underscore word (blankWord)
    roundWord, blankWord = getWord()
    
    return initPlayer

###


# In[135]:


def spinWheel(playerNum):
    global wheellist
    global players
    global consonants
    stillinTurn = True
    valid_guess = False
    
# Get random value for wheellist
    spin_value = random.choice(wheellist)
    print(f"Your spin came up as {spin_value}.")
    
    
# Check for bankrupcy, and take action.
    if spin_value == "bankrupt":
        print("Your round total returns to $0.")
        players[playerNum]["roundtotal"] = 0
        
        stillinTurn = False
        
# Check for lose turn
    elif spin_value == "lose turn":
        print("You lost your turn.")
        
        stillinTurn = False
        
# Get amount from wheel if not loose turn or bankruptcy
    else:
        spin_value.isdigit() == True
            
# Ask user for letter guess
        print(f"{players[playerNum]['name']}, what is your letter guess?")
        letter_guess = str(input(f"What is your letter guess?: ")).lower()
        if letter_guess in vowels:
            print(f"Enter a consonant")
        elif (len(letter_guess) != 1):
            print(f"Enter a single letter.")
        elif (not letter_guess.isalpha()):
            print(f"Input a letter.")
        else:
            valid_guess, count = guessletter(letter_guess)

# Use guessletter function to see if guess is in word, and return count
        stillinTurn, count = guessletter(letter_guess)

# Change player round total if they guess right.
        if valid_guess:
            players[playerNum]["roundtotal"] += count * int(spin_value)
            print(f"Valid guess ${spin_value} was added to your total.")
            print(blankWord)
            stillinTurn = True

        else:
            stillinTurn = False
            print(f"{letter_guess} is not in the word.")

        return stillinTurn


###


# In[125]:


def guessletter(letter): 
    global players
    global blankWord
# parameters:  take in a letter guess and player number
    
    goodGuess = False
    count = 0
    
# Change position of found letter in blankWord to the letter instead of underscore
    for i, letterCorrect in enumerate(roundWord):
        if letter !="_" and letter == letterCorrect:
            roundUnderscoreWord[i] = letterCorrect
            
# return goodGuess= true if it was a correct guess
            goodGuess = True

# return count of letters in word.
            count += 1
# ensure letter is a consonante

    return goodGuess, count

###


# In[126]:


def buyVowel(playerNum):
    global players
    global vowels
    global roundWord
    global blankWord
    
# Take in a player number
# Ensure player has 250 for buying a vowelcost
    stillinTurn = True
    goodGuess = False
    count = 0

    if players[playerNum]["roundtotal"] >= vowelcost:
        print(f"{players[playerNum]['name']}, what is your vowel guess?")
        vowel_guess = str(input(f"What is your letter guess?: ")).lower()
        players[playerNum]["roundtotal"] -= count * vowelcost

        if vowel_guess in vowels: 
            valid_guess = guessletter(vowel_guess)
            print(f"Valid guess. ${vowelcost} was deducted from your roundtotal.")
            print(blankWord)
            stillinTurn = True

        elif vowel_guess in consonants:
            print(f"Enter a vowel")

        elif (len(vowel_guess) != 1):
            print(f"Enter a single letter.")

        elif (not vowel_guess.isalpha()):
            print(f"Input a letter.")

        else:
            print(f"That vowel isn't in the word")
            stillinTurn = False
    else:
        print(f"You only have ${players[playerNum]['roundtotal']} that's not enough to buy a vowel.")
        stillinTurn = False

# Use guessLetter function to see if the letter is in the file
    stillinTurn, count = guessletter(vowel_guess)
# Ensure letter is a vowel
# If letter is in the file let goodGuess = True
    goodGuess = True

    return goodGuess

###


# In[127]:


def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    
# Take in player number
# Ask for input of the word and check if it is the same as wordguess
# Fill in blankList with all letters, instead of underscores if correct     
    
    print(f"{players[playerNum]['name']}, what is your word guess?")
    word_guess = str(input(f"What is your word guess?: ")).lower()
    if word_guess == roundWord:
        for i in range(0, len(word_guess)):
            roundUnderscoreWord[i] = word_guess[i]
        print(f"You guessed the word. The word was {roundWord}.")
    else:
        print(f"{word_guess} is not correct.")
# return False ( to indicate the turn will finish)  
    
    return False

###


# In[128]:


def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players

    print(f"It is {playerNum+1}'s turn. {players[playerNum]['name']} currently have ${players[playerNum]['roundtotal']} \n{roundUnderscoreWord}")

# take in a player number. 
# use the string.format method to output your status for the round
# and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
# Keep doing all turn activity for a player until they guess wrong
# Do all turn related activity including update roundtotal 
    
    stillinTurn = True

    while stillinTurn:

        for key, info in players.items():
            print("\nPlayer ID:", key) 
            for key in info:
                print(key + ':', info[key])
        
        choice = str(input(f"Would you like to (S)pin the wheel, (B)uy a vowel, or (G)uess the word?:  ")).upper()
# use the string.format method to output your status for the round
# Get user input S for spin, B for buy a vowel, G for guess the word     
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")        
    
# Check to see if the word is solved, and return false if it is,
        if roundWord == ''.join(blankWord):
            stillinTurn = False
            break


#make a variable == true if variable == false break if the guess = round word retufn false
#just return false 
# Or otherwise break the while loop of the turn. 
#literally what does this even mean

    game_over = ''.join(blankWord)
    if game_over == roundWord:
        players[playerNum]["gametotal"] += players[playerNum]["roundtotal"]
        return False
    else:
        return True

###


# In[129]:


def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    initPlayer = wofRoundSetup()
    current_player = initPlayer
    
    continue_game = True
    while continue_game:

# Keep doing things in a round until the round is done ( word is solved)
# While still in the round keep rotating through players
# Use the wofTurn fuction to dive into each players turn until their turn is done.
        continue_game = wofTurn(current_player)
        if continue_game == False:
            break
        
        if current_player == 2:
            current_player = 0
        else:
            current_player += 1
# Print roundstatus with string.format, tell people the state of the round as you are leaving a round.
    print(f"This round has eneded. The word was {roundWord} \nThe current state of the game is as follows:")
    for key, info in players.items():
        print("\nPlayer ID:", key) 
        for key in info:
            print(key + ':', info[key])

###


# In[130]:


def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    global players
    winplayer = 0
    
# Find highest gametotal player.  They are playing.
    for i in range(1, len(players)):
        if players[i]['gametotal'] > players[winplayer]['gametotal']:
            winplayer = i
    
# Print out instructions for that player and who the player is.
    print(f"Welcome to the final round, {players[winplayer]['name']}.")
    print(finalroundtext)

# Use the getWord function to reset the roundWord and the blankWord (word with the underscores)
    roundWord, blankWord = getWord()

# Use the guessletter function to check for {'R','S','T','L','N','E'}
    for i in ("r", "s", "t", "l", "n", "e"):
        guessletter(i)

# Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    print(f"Here is your hint: {(''.join(blankWord))}")

# Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    print(f"You may guess 3 consonants and a vowel.")

    c_guess = 0
    v_guess = 0
    total_in = False

    while not total_in:

        letter = str(input(f"What is your letter guess?: ")).lower()
        if letter not in vowels and c_guess < 3:
            c_guess += 1
            guessletter(letter)
            print(blankWord)

        elif letter not in vowels and c_guess >= 3:
            print("You already guessed 3 consonants.")
        elif letter in vowels and v_guess < 1:
            v_guess += 1
            guessletter(letter)
            print(blankWord)
        elif (len(letter) != 1):
            print(f"Enter a single letter.")
        elif (not letter.isalpha()):
            print(f"Input a letter.")

        if roundWord == ''.join(blankWord):
            total_in = True
            break
        elif c_guess == 3 and v_guess == 1:
            break
# Print out the current blankWord again
    print(f"Here is your updated hint: {(''.join(blankWord))}")

# Remember guessletter should fill in the letters with the positions in blankWord
# Get user to guess word
# If they do, add finalprize and gametotal and print out that the player won

    final_guess = str(input(f"What is your final word guess?: ")).lower()
    if final_guess == roundWord:
        players[winplayer]['gametotal'] += finalprize
        print(f"{final_guess} is correct. You've won ${finalprize}. Congratulations.")

    else:
        print(f"The word was actually {roundWord}. Better luck next time.")

###


# In[ ]:


def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()

