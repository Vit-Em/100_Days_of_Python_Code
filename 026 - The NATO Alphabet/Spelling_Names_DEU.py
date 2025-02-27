#TODO 1. Create a dictionary in this format:
{"A": "Alfa", "B": "Bravo"}

with open('nato_phonetic_alphabet.csv', 'r') as npa:
    letters = npa.readlines()
    nato_phonetic_dict = {row.split(',')[0]:row.split(',')[1].strip() for row in letters}

#TODO 2. Create a list of the phonetic code words from a word that the user inputs.
with open('DE_Name_Buchstabieren.csv', 'r') as den:
    letters = den.readlines()
    de_dict = {row.split(' wie ')[0]:row.split(' wie ')[1].strip() for row in letters}
user_name = input("Wie heißen Sie? ").upper()
name_buchstabieren = [de_dict[letter] for letter in user_name if letter in de_dict] # Liste der phonetischen Codewörter erstellen
print(name_buchstabieren)