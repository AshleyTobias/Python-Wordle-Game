import tkinter as tk
import random

window = tk.Tk()
window.resizable(False,False) # Stops the window from being able to be resized
window.title('Wordle') # Changes the title to 'Wordle'

def get_word():
    global words
    file = open('word_list.txt') # Opens the file
    words = [word[:-1] for word in file] # List comprehension that iterates through the file
    file.close() # Closes the file
    return random.choice(words) # Returns a random word from the 'words' list

def enter_letter(event):
    global current_word_guess
    if len(current_word_guess) == 5: # A guard clause to ensure that the user will not enter a word longer than 5 characters
        return
    input_letter = event.char.lower()
    current_word_guess += input_letter
    update_board()

def delete_letter(event):
    global current_word_guess
    if len(current_word_guess) == 0: # A guard clause to ensure that the user will not enter a word longer than 5 characters
        return
    current_word_guess = current_word_guess[:-1]
    update_board()

def get_tile_label(letter,colour):
    if colour == None:
        colour = background_colour
    return tk.Label(window,height=Height,width=Width,text=letter.upper(),bg=colour,fg=font_colour,borderwidth=border_size,highlightbackground=border_colour,relief='sunken',font=Font)

def update_board(): # Updates the board
    tiles = [] # Creates a list that will contain all the tile objects
    for word in guessed_words:
        tiles += get_scoring(word) # Creates a list comprehension of all the letters of each guessed word and adds it to the 'tiles' list
    tiles += [get_tile_label(letter,None) for letter in current_word_guess] # Creates a list comprehension of each letter in the current word being guessed
    while len(tiles) != 35: 
        tiles.append(get_tile_label(" ",None)) # Creates empty labels until there are 35 labels in total
    for index,tile in enumerate(tiles):
        Column = index % 5
        Row = index // 5
        tile.grid(row=Row+1,column=Column)

def get_scoring(word):
    labels = []
    for index,letter in enumerate(list(word)):
        if letter not in random_word:
            labels.append(get_tile_label(letter,'#737373'))
        elif letter == random_word[index]:
            labels.append(get_tile_label(letter,'#66ff66'))
        elif letter != random_word[index] and word.count(letter) > random_word.count(letter):
            labels.append(get_tile_label(letter,'#737373'))
        elif letter != random_word[index]:
            labels.append(get_tile_label(letter, '#ffff66'))
    return labels

def alert(error):
    alert_box = tk.Label(window, text=error.upper(), width=Width*3,height=int(round(Height*1.5,0)),font=Font,bg='#ff4d4d', fg='white')
    alert_box.grid(rowspan=3,columnspan=5,row=3)
    window.after(1000, lambda: alert_box.grid_remove())

def enter(event):
    global current_word_guess
    if len(current_word_guess) != 5:
        alert('Not enough letters!')
        return
    elif current_word_guess not in words:
        alert('That is not a word!')
        return
    guessed_words.append(current_word_guess)
    current_word_guess = ""
    update_board()
    if guessed_words[-1] == random_word:
        end_game('win')
    elif len(guessed_words) == 7:
        end_game('loss')

def end_game(end):
    if end == 'loss':
        end_text = 'You lose!\nThe correct word was: '+random_word.upper()
        end_colour = '#ff471a'
        end_font = 'white'
    elif end == 'win':
        end_text = 'You win!\nYou found the word '+random_word.upper() + ' in ' + str(len(guessed_words)) + ' tries!'
        end_colour = '#39e600'
        end_font = 'black'
    end_text_box = tk.Label(window, text=end_text, width=Width*5,height=Height*5,font=Font,bg=end_colour, fg=end_font)
    end_text_box.grid(columnspan=5,rowspan=7,row=1)
    for letter in alphabet:
        window.unbind("<"+letter+">")
    window.unbind("<BackSpace>")
    window.unbind("<Return>")

def boot(): # Starts the program
    global random_word
    title = tk.Label(window,text='Wordle\nCreated by Ashley Tobias'.upper(),width=50,font=Font)
    title.grid(columnspan=5,row=0)
    random_word = get_word() # Gets a random word from the get_word function that the user will try to guess
    update_board()


# Key binding
alphabet = "abcdefghijklmnopqrstuvwxyz"
for letter in alphabet:
    window.bind("<"+letter+">",enter_letter) # Loops through each letter of the alphabet to create a keybinds
    window.bind("<"+letter.upper()+">",enter_letter) # Loops through each letter of the alphabet to create a keybinds
window.bind("<BackSpace>",delete_letter) # Creates a key bind to remove the last-entered letter
window.bind("<Return>",enter)

# Global variables
guessed_words = []
current_word_guess = ""

# Styling variables
Height = 5
Width = 10
background_colour = 'white'
border_size = 2
font_colour = 'black'
border_colour = '#c7c7c7'
Font = ('Verdana',12)

boot()

window.mainloop()




