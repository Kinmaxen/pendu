import random
import os


class Pendu:
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
                "V", "W", "X", "Y", "Z"]

    filePath = "dico.txt"

    every = "*"

    extension = ".txt"

    settings_tag = [True, 0]

    # In order: Show word at defeat, show none/fist/last/random letter

    def dessinPendu(self, nb):
        tab = [
            """
               +-------+
               |
               |
               |
               |
               |
            ==============
            """,
            """
               +-------+
               |       |
               |       O
               |
               |
               |
            ==============
            """
            ,
            """
               +-------+
               |       |
               |       O
               |       |
               |
               |
            ==============
            """,
            """
               +-------+
               |       |
               |       O
               |      -|
               |
               |
            ==============
            """,
            """
               +-------+
               |       |
               |       O
               |      -|-
               |
               |
            ==============
            """,
            """
               +-------+
               |       |
               |       O
               |      -|-
               |      |
               |
            ==============
            """,
            """
               +-------+
               |       |
               |       O
               |      -|-
               |      | |
               |
            ==============
            """
        ]
        return tab[nb]

    def raw_look(self, looker):
        with open(self.filePath, "r", encoding="UTF-8") as f:
            lines = f.readlines()
        result = {}
        for line in lines:
            # Select the biggest and the smaller string
            if len(line) > len(looker):
                big = line
                small = looker
            else:
                big = looker
                small = line
            # Put the maximum of difference possible
            difference = len(big)
            # Each time in the loop, we go 1 char further in the big string
            for i in range(len(big) - len(small)):
                # Reset current difference
                current = 0
                for char in range(len(small)):
                    # If there is a big difference add 1
                    if str.lower(big[i + char]) != str.lower(small[char]):
                        current += 1
                    # If there is a low difference add one third
                    elif big[i + char] != small[char]:
                        current += 1 / 3
                # Set the difference to the current one if it is smaller
                difference = current if difference > current else difference
            # Put in the final list if at least the score if half good
            if difference < len(small) * 0.2:
                result[line] = difference
        # Sorting the dictionary (the dictionary is turning into a list of tuples)
        result = sorted(result.items(), key=lambda x: x[1])
        return result

    def wrong_file_path(self):
        while True:
            # Ask for new path
            new_path = input(
                "Le chemin d'accès est invalide, veuillez rentrer un nouveau valide sans extension avant de continuer : ")
            new_path = new_path + "." + self.extension
            # Check if it's correct
            try:
                with open(new_path, 'a', encoding="UTF-8") as f:
                    f.write("")
            except FileNotFoundError:
                print("Ce chemin est toujours invalide, veuillez recommencer.")
                continue
            # Set in memory data
            self.filePath = new_path
            # Set in .py data
            with open("Pendu.py", "r", encoding="UTF-8") as f:
                new_py = f.readlines()
                for i in range(len(new_py)):
                    # Replace in list only the filePath line
                    if new_py[i].startswith("    filePath ="):
                        new_py[i] = "    filePath = \"" + new_path.replace("\\", "\\\\") + "\"\n"
            with open("Pendu.py", "w", encoding="UTF-8") as f:
                for line in new_py:
                    f.write(line)
            return

    # Method to ask a question with limited/unlimited answer(s):
    def ask(self, question: str, answers):
        # Check if there is at least 1 answer
        if not answers:
            raise ValueError("ask need a fulfilled answer tab")
        while True:
            # Ask the user
            choice = input(question)
            # Check for each possible answer if it is the right one return it
            for i in answers:
                if str.lower(choice) == str.lower(i):
                    return i
                # Check if the list contains the symbol to authorize all answer
                if self.every in answers:
                    return choice
            # If no value is corresponding, advertise the user and redo the loop
            print("Valeur incorrect, veuillez recommencer.")

    # set the game's essentials variables
    def play(self):
        with open("dico.txt", "r") as f:
            mots = f.readlines()

        mot = random.choice(mots)
        mot = mot.strip()
        stade_pendu = 0
        typed = []
        while True:  # ask to the user which letter he wants to select
            choice = self.ask("Veuillez rentrer votre lettre : ", self.alphabet)
            if not str.upper(choice) in self.alphabet:  # set the case if the letter is incorrect
                print("Veuillez rentrer une lettre vailde")
                continue
            if choice in typed:  # set the case if the letter has already been typed
                print("Vous avez déjà utilisé cette lettre")
                continue
            typed.append(str.upper(choice))
            # set the case if the letter is wrong
            if str.upper(choice) not in mot:
                stade_pendu += 1
                print("Cette lettre est incorrecte")
            # set the case if the letter is good
            else:
                print("Cette lettre est correcte")
            print(self.dessinPendu(stade_pendu))
            # set the loose condition
            if stade_pendu > 5:
                print("Vous avez perdu !", end="")
                if self.settings_tag[0]:
                    print("Le mot était " + mot)
                else:
                    print()
                break
            win = True
            for char in mot:
                if char in typed or char == "-":
                    print(char, end="")
                else:
                    print("_", end="")
                    win = False
            print("")
            # sent a message if the user win
            if win:
                print("Bravo, tu as gagné !!")
                break

    # Add the word which the user want to add
    def add(self):
        next_one = ""
        while True:
            word = input(f"Veuillez saisir le mot{next_one} à ajouter. [0] : Sortir : ")
            if word == "0":
                return
            incorrect = False
            for char in word:  # set the exeption if the word taped is incorect
                if str.upper(char) not in self.alphabet:
                    print("Mot incorrect, veuillez recommencer")
                    incorrect = True
                    break
            # set the verification of checking if the word hasn't already been typed
            with open(self.filePath, "r") as f:
                for mot in f.readlines():
                    if mot == str.upper(word):
                        print("Ce mot est déjà dans le dictionnaire")
                        incorrect = True
                        break
            if incorrect:
                continue
            # create a new word in the file
            with open(self.filePath, "a") as f:
                f.write(str.upper(word) + "\n")
                print(f"votre mot <{str.upper(word)}> a bien été ajouté \n")
            next_one = " suivant"

    # Allow you to search and remove a word
    def remove(self):
        while True:
            looker = input("Veuillez rentrer le mot à rechercher. [0] Quitter : ")
            if looker == "0":
                return
            tab = self.raw_look(str.upper(looker))
            if len(tab) == 0:
                print("Aucun mot ne correspond, veuillez recommencer")
                continue
            print("Voici les mots qui correspondent à votre recherche")
            for i in range(len(tab)):
                print(" - " + str(i) + " : " + tab[i][0].removesuffix("\n"))
            index = self.ask("Veuillez rentrer l'index du mot à retirer. [A] Annuler : ",
                             [str(i) for i in range(len(tab))] + ["A"])
            if index == "A":
                continue
            remove = tab[int(index)][0]
            with open(self.filePath, "r") as f:
                words = f.readlines()
            with open(self.filePath, "w") as f:
                for i in range(len(words)):
                    if words[i] == remove + "\n":
                        continue
                    f.write(words[i])
            print(f"Le mot <{remove}> a été retiré")

    def change_file_path(self):
        while True:
            new = self.ask("Veuillez rentrer le nouveau chemin d'accès sans extension. [A] Annuler : ",
                           [self.every, "A"])
            if new == "A":
                return
            new = new + ".txt"
            if new == self.filePath:
                choice = self.ask("Ceci est l'actuelle chemin d'accès, voulez vous continuer? [Y] Oui, [N] Non : ",
                                  ["Y", "N"])
                if choice == "N":
                    continue
            try:
                with open(new, "w") as f:
                    f.write("")
            except FileNotFoundError:
                print("Le chemin d'accès est invalide, veuillez recommencer")
                continue
            transfer = self.ask(
                "Voulez vous transférer toutes les données vers le nouveau chemin d'accès? [Y] Oui, [N] Non : ",
                ["Y", "N"])
            if transfer == "Y":
                with open(self.filePath, 'r') as f:
                    data = f.readlines()
                with open(new, 'w') as f:
                    for line in data:
                        f.write(line)
            delete_past = self.ask("Voulez vous effacer le fichier précédent? [Y] Oui, [N] Non : ", ["Y", "N"])
            if delete_past == "Y":
                os.remove(self.filePath)
            self.filePath = new
            with open("PenduUpgraded.py", "r") as f:
                new_py = f.readlines()
                for i in range(len(new_py)):
                    if new_py[i].startswith("    filePath = \""):
                        new_py[i] = "    filePath = \"" + new.replace("\\", "\\\\") + "\"\n"
            with open("PenduUpgraded.py", "w") as f:
                for line in new_py:
                    f.write(line)
            print("Le nouveau chemin est bien " + new)
            break

    def settings(self):
        while True:
            choix = self.ask(" [0] Quitter\n [1] Afficher le mot à la défaite\n [2] Changer la difficulté",
                             [str(i) for i in range(3)])
            if choix == "0":
                return
            if choix == "1":
                reponse_aff = self.ask("Voulez vous afficher[1] ou supprimer le mot à la défaite[2] ?",
                                       [str(i + 1) for i in range(2)])
                if reponse_aff == "1":
                    print("le mot va etre affiché à la défaite !")
                else:
                    print("Le mot ne va pas être affiché à la défaite")
                self.settings_tag[0] = reponse_aff == "1"
                continue

            if choix == "2":
                reponse_diff = self.ask(
                    "quelle bonus souhaitez vous vous ajouter ?\n [0] Aucune\n [1] La première lettre du mot apparait\n [2] La dernière lettre du mot apparait\n [3] Une lettre aléatoire est ajoutée dans le mot [NE MARCHE PAS] ",
                    [str(i) for i in range(4)])
                self.settings_tag[1] = int(reponse_diff)

    # set the user interface
    def __init__(self):
        try:  # open the file
            with open(self.filePath, 'a', encoding="UTF-8") as f:
                f.write("")
        except FileNotFoundError:  # set the exeption if the file is unfindable
            self.wrong_file_path()
        while True:  # ask the choices each time
            choice = self.ask(
                "Veuillez choisir:\n [0] : Quitter\n [1] Lancer le jeu\n [2] Ajouter un/des mot(s)\n [3] Rechercher/retirer un/des mot(s)\n [4] Changer le chemin du fichier dictionnaire\n [5] Paramètres\n",
                [str(i) for i in range(6)])
            if choice == "0":
                print("Merci d'avoir utilisé le programme. Au revoir")
                return
            elif choice == "1":
                self.play()
            elif choice == "2":
                self.add()
            elif choice == "3":
                self.remove()
            elif choice == "4":
                self.change_file_path()
            elif choice == "5":
                self.settings()


Pendu()
