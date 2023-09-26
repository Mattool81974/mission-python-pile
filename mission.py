# EN : All the code is in french, because i'm french. All this project is dedicated to my computer science teacher. If you're not him, please leave.
# FR : Le code est français, parce que je suis français. Ce projet est destiné à mon professeur de NSI. Si vous n'êtes pas lui, s'il vous plaît partez.

import implementation as pile
from mlib import *

interfaceGraphique = True #Booléen qui indique si la fenêtre graphique doit s'afficher ou non (il est conseillé de laisser à True)

if interfaceGraphique:
    TAILLE = (600, 600) #Taille de la fenêtre graphique

    fenetre = display.set_mode(TAILLE) #Définition de la fenêtre python

    mapp = MApp(fenetre, "Pile", TAILLE[0], TAILLE[1], console=False, printFps=True) #Définition de la fenêtre mlib
    titre = MText("Pile", 0, 0, TAILLE[0], 100, mapp) #Définition du titre principale de la fenêtre
    fenetreEntreeTexte = MWidget(0, 100, TAILLE[0], TAILLE[0] - 100, mapp) #Définition de la fenêtre qui contiendra tous les éléments nécessaires à l'entrée du texte
    entreeTexte = MText("", 50, 50, fenetreEntreeTexte.getWidth() - 100, fenetreEntreeTexte.getHeight() - 150, fenetreEntreeTexte) #Définition de l'entrée texte du texte à analyser
    erreurEntreeTexte = MText("Erreur", 50, 0, fenetreEntreeTexte.getWidth() - 100, 40, fenetreEntreeTexte) #Définition d'un texte d'erreur si le texte n'est pas correct
    boutonValiderEntreeTexte = MButton("Valider", 50, entreeTexte.getWidth() - 75, (TAILLE[0] - 120) / 2, 50, fenetreEntreeTexte) #Définition du bouton pour valider le texte à analyser
    fenetreAnalyse = MWidget(0, 100, TAILLE[0], TAILLE[0] - 100, mapp) #Définition de la fenêtre qui contiendra les éléments à montrer pendant l'analyse
    titreAnalyse = MText("Analyse en cours...", 0, 0, fenetreAnalyse.getWidth(), fenetreAnalyse.getHeight() - 50, fenetreAnalyse) #Définition du titre à montrer pendant l'analyse

    #Modification purement esthétique des éléments graphiques (voir documentation graphique)
    mapp.setBackgroundColor((209, 204, 59))

    titre.setBackgroundColor((0, 0, 0, 0))
    titre.setFontSize(50)
    titre.setTextHorizontalAlignment(1)
    titre.setTextVerticalAlignment(1)

    fenetreEntreeTexte.setBackgroundColor((0, 0, 0, 0))

    entreeTexte.setDynamicTextCut(True)
    entreeTexte.setFontSize(23)
    entreeTexte.setFrameWidth(2)
    entreeTexte.setInput(True)

    erreurEntreeTexte.antiAnaliasing = False #Variable ajouter hors mlib suite à un bug inrésolvable à cause de l'horaire
    erreurEntreeTexte.setBackgroundColor((0, 0, 0, 0))
    erreurEntreeTexte.setFontSize(23)
    erreurEntreeTexte.setTextHorizontalAlignment(1)
    erreurEntreeTexte.setTextColor((255, 0, 0))
    erreurEntreeTexte.setVisible(False)

    boutonValiderEntreeTexte.setChangeBackgroundColorOnOnOverflight(True)

    fenetreAnalyse.setBackgroundColor((0, 0, 0, 0))

    titreAnalyse.setBackgroundColor((0, 0, 0, 0))
    titreAnalyse.setFontSize(43)
    titreAnalyse.setTextHorizontalAlignment(1)
    titreAnalyse.setTextVerticalAlignment(1)
    #Fin des modification purement esthétique des éléments graphiques (voir documentation graphique)

    fenetreActuel = 0 #Contient le numéro de la fenêtre actuellement affiché (0 pour fenetreEntreeTexte)

    def setFenetre(fenetre: int): #Permet de mettre une certaine fenêtre facilement en montrant la fenêtre designée par "fenetre" et en cachant les autres
        if fenetre == 0: #Si fenetre == 0, mettre fenetreEntreeTexte
            fenetreAnalyse.setVisible(False)
            fenetreEntreeTexte.setVisible(True)
            mapp.promoveChild(fenetreEntreeTexte)

            erreurEntreeTexte.setVisible(False)
        elif fenetre == 1: #Si fenetre == 1, mettre fenetreAnalyse
            fenetreAnalyse.setVisible(True)
            fenetreEntreeTexte.setVisible(False)
            mapp.promoveChild(fenetreAnalyse)

    setFenetre(0)

    texteAAnalyser = "" #Définition du texte à analyser

    while True:
        mapp.frameEvent() #Faire les mise à jour évènements de mlib (voir documentation)

        if fenetreActuel == 0: #Si nous somme sur la fenêtre fenetreEntreeTexte
            if boutonValiderEntreeTexte.isGettingLeftClicked(): #Si le bouton de validation du texte est clické
                texteAAnalyser = entreeTexte.getText()
                if texteAAnalyser == "": #Si le texte est vide
                    erreurEntreeTexte.setText("Erreur : texte vide")
                    erreurEntreeTexte.setVisible(True)
                else:
                    setFenetre(1)

        mapp.frameGraphics() #Faire les mise à jour graphique de mlib (voir documentation)
        pygame.display.flip()