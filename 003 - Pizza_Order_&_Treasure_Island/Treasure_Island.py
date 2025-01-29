print(r'''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\ ` . "-._ /_______________|_______
|                   | |o ;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/_____ /
*******************************************************************************
''')
def game_over(message):
    print(message)
    print("Game Over.")
    exit()

print("Welcome to Treasure Island.")
print("Your mission is to find the treasure.")

choice1 = input('You\'re at a cross road. Where do you want to go? Type "left" or "right": ').lower()
if choice1 != "left":
    game_over("You fell into a hole.")

choice2 = input('You\'ve come to a lake. There is an island in the middle of the lake. '
                'Type "wait" to wait for a boat. Type "swim" to swim across: ').lower()
if choice2 != "wait":
    game_over("You get attacked by an angry trout.")

choice3 = input('You arrive at the island unharmed. There is a house with 3 doors. '
                'One red, one yellow and one blue. Which colour do you choose? ').lower()

if choice3 == "red":
    game_over("It's a room full of fire.")
elif choice3 == "blue":
    game_over("You enter a room of beasts.")
elif choice3 == "yellow":
    print("You found the treasure! You Win!")
else:
    game_over("You chose a door that doesn't exist.")
