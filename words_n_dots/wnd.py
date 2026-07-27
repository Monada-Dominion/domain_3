#It is a game with a card deck
#Thus, we firstly make something to imitate a card deck 
#Card deck must contatin 72 cards
#Each card is a word taken form the list of English words
#The game counts the number of letters and hides them into stars 
#This is to symbolically represent the card and lightning dots


import random
import sys

#make a file with 72 unique words 

#let's create a function that will create a card deck

def makedeck():
    file = open('words.txt') #open a list of English words downloaded from the web
    wordlist = list(file) 

    gamelist = random.choices(wordlist, k = 72) #randomly pick 72 words from the list

    #remove \n from the list (initially words come with '\n' at the end of each word)
    converted_list = []

    for element in gamelist:
        converted_list.append(element.strip())

    return converted_list

output = makedeck()

#print(f'These are all the words to be connected to the dots: \n\n{output}')

makedeck


allcards = len(output) #return a number of cards in a deck
print(f'\nThere are {allcards} cards with English words! \n')

while allcards > 0:

    choosecard = int(random.uniform(1,72)) #randomly choose a number between 1 and 72
    chosencard = list(output[choosecard]) #connect this number to an appropriate word in the list
    wordlength = len(chosencard) #return wordlength


    print(f'You randomly picked a card with a word of {wordlength} letters - guess them all!')

    #print(f'This is a 4th letter in the chosen word: {chosencard[3]}')
    wordcopy = list.copy(chosencard)
    
    #create a function that will return letters as '*' and allow user to guess
    #also counts fails and guesses

    def hideNcount():
        
        count = 0

        for x in wordcopy:
            if x != "1":
                wordcopy[count] = "*"
            
            count = count +1



        return wordcopy

    returnstars = hideNcount()
    print(returnstars)


    print("\nGuess all characters")
    
    guesses = ''
    
    # any number of turns can be used here
    turns = wordlength
    
    
    while turns > 0:
        
        # counts the number of times a user fails
        failed = 0
        
        # all characters from the input
        # word taking one at a time.
        for char in chosencard:
            
            # comparing that character with
            # the character in guesses
            if char in guesses:
                print(char, end=" ")
                
            else:
                print('*', end=" ")
                print("_")
                
                # for every failure 1 will be
                # incremented in failure
                failed += 1
                
    
        if failed == 0:
            # user will win the game if failure is 0
            # and 'You Win' will be given as output
            print("You Win")
            
            # this print the correct word
            print("The word is: ", chosencard)
            break
        
        # if user has input the wrong alphabet then
        # it will ask user to enter another alphabet
        print()
        guess = input("Input letter:")
        
        # every input character will be stored in guesses
        guesses += guess
        
        # check input with the character in word
        if guess not in chosencard:
            
            turns -= 1
            
            # if the character doesn’t match the word
            # then “Wrong” will be given as output
            print("Wrong")
            
            # this will print the number of
            # turns left for the user
            print("You have", + turns, 'more guesses')
            
            
            if turns == 0:
                print("You Loose")

    allcards = allcards - 1
    print("You have", +allcards, "cards left.")
    #end