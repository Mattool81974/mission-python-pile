# EN : All the code is in french, because i'm french. All this project is dedicated to my computer science teacher. If you're not him, please leave.
# FR : Le code est français, parce que je suis français. Ce projet est destiné à mon professeur de NSI. Si vous n'êtes pas lui, s'il vous plaît partez.

import implementation as pile #Importation des méthodes pour la pile
from mlib import * #Importation de ma bibliothèque graphique (version 2.0.0)

def constructeur_pile(chaine: str):
    """Retourne une liste tel que la valeur à l'index i est ce qu'il faut rajouter à la pile pour effectuer la mission.
       Par exemple, "+(" signifie qu'il faudra rajouter un "(" à la pile et "+[" qu'il faudra rajouter un "[".
       "-(" signifie qu'il faudra enlever un "(" à la pile et "-[" qu'il faudra enlever un "["."""
    
    retour = [] #Liste à retourner
    for i in range(len(chaine)):
        if chaine[i] == "(":
            retour.append("+(")
        elif chaine[i] == "[":
            retour.append("+[")
        elif chaine[i] == ")":
            retour.append("-(")
        elif chaine[i] == "]":
            retour.append("-[")
        else:
            retour.append("") #Rien à ajouter/enlever
    return retour

def est_parenthese(chaine: str):
    """Retourne si la chaine est bien parenthésée ou non grâce à une pile"""

    constructeur = constructeur_pile(chaine)
    pileAAnalyser = pile.pile_vide()
    for i in constructeur:
        if len(i) > 0: #Si la chaîen n'est pas vide
            if i[0] == "+": #Si il faut ajouter une valeur à la pile
                pile.empiler(pileAAnalyser, i[1])
            elif i[0] == "-": #Si il faut enlever une valeur à la pile
                if pile.taille(pileAAnalyser) > 0 and pile.consulter(pileAAnalyser) == i[1]:
                    pile.depiler(pileAAnalyser)
                else:
                    return False
                
    if pile.taille(pileAAnalyser) > 0: #SI la pile n'est pas vide (parenthèse/crochet ouvert)
        return False
    
    return True

interfaceGraphique = True #Booléen qui indique si la fenêtre graphique doit s'afficher ou non (il est conseillé de laisser à True)

if interfaceGraphique:
    """L'objectif de cette interface graphique est de créer une partie pour rentrer un texte, une partie afficher pendant l'analyse et une partie qui affiche
       les résultats sous forme d'image scrollable avec le même design que le croquis présent dans l'énoncé."""

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
    fenetreResultat = MWidget(0, 100, TAILLE[0], TAILLE[0] - 100, mapp) #Définition de la fenêtre qui contiendra le résultat de l'analyse
    titreResultat = MText("", 0, 0, fenetreResultat.getWidth(), 50, fenetreResultat) #Définition du texte qui indiquera si la chaîne est bien ortographié ou non
    conteneurResultat = MWidget(0, 0, 0, 300, fenetreResultat) #Définition du widget qui contiendra précisement le résultat
    bordureResultat = MFrame(49, 49, (fenetreResultat.getWidth() - 100) + 2, conteneurResultat.getHeight() + 19, fenetreResultat)
    scrolleurResultat = MScrollArea(conteneurResultat, 1, 1, bordureResultat.getWidth() - 2, bordureResultat.getHeight() - 2, bordureResultat) #Définition du widget qui permettra de scroll dans conteneurResultat
    contenuResultat = [] #Liste de tous les éléments qui seront générés dans conteneurResultat

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
    entreeTexte.setSelectionTextColor((255, 255, 255))

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

    fenetreResultat.setBackgroundColor((0, 0, 0, 0))

    titreResultat.antiAnaliasing = False #Variable ajouter hors mlib suite à un bug inrésolvable à cause de l'horaire
    titreResultat.setBackgroundColor((0, 0, 0, 0))
    titreResultat.setFontSize(23)
    titreResultat.setTextHorizontalAlignment(1)

    bordureResultat.setFrameWidth(1)
    #Fin des modification purement esthétique des éléments graphiques (voir documentation graphique)

    fenetreActuel = 0 #Contient le numéro de la fenêtre actuellement affiché (0 pour fenetreEntreeTexte)
    texteAAnalyser = "" #Définition du texte à analyser

    def consuitreAnalyse(chaine: str):
        pass

    def setFenetre(fenetre: int): #Permet de mettre une certaine fenêtre facilement en montrant la fenêtre designée par "fenetre" et en cachant les autres
        global fenetreActuel
        
        if fenetre == 0: #Si fenetre == 0, mettre fenetreEntreeTexte
            fenetreActuel = fenetre
            fenetreAnalyse.setVisible(False)
            fenetreEntreeTexte.setVisible(True)
            fenetreResultat.setVisible(False)
            mapp.promoveChild(fenetreEntreeTexte)

            erreurEntreeTexte.setVisible(False)
        elif fenetre == 1: #Si fenetre == 1, mettre fenetreAnalyse
            fenetreActuel = fenetre
            fenetreAnalyse.setVisible(True)
            fenetreEntreeTexte.setVisible(False)
            fenetreResultat.setVisible(False)
            mapp.promoveChild(fenetreAnalyse)
        elif fenetre == 2: #Si fenetre == 2, mettre fenetreResultat
            fenetreActuel = fenetre
            fenetreAnalyse.setVisible(False)
            fenetreEntreeTexte.setVisible(False)
            fenetreResultat.setVisible(True)
            mapp.promoveChild(fenetreResultat)

            if est_parenthese(texteAAnalyser): #Actualiser le texte du titre de résultat selon si le texte est bien parenthésé ou non
                titreResultat.setText("Le texte est bien parenthésé.")
            else:
                titreResultat.setText("Le texte n'est pas bien parenthésé.")

            constructeurPile = constructeur_pile(texteAAnalyser) #Liste des modifications à éxécuter dans la pile
            erreur = "" #Contient l'erreur si il y en a une
            pileActuelle = [] #Contenu de la pile à l'étape actuelle
            for i in range(len(constructeurPile)): #Générer le descriptif du fonctionnement de la pile
                element = constructeurPile[i]
                
                if element != "":
                    if element[0] == "+": #Remplir la pile comme dans est_parenthese
                        pileActuelle.append(element[1])
                    elif element[0] == "-":
                        if len(pileActuelle) == 0: #Si la pile est vide
                            erreur = "vide"
                        else:
                            if element[1] == pileActuelle[-1]:
                                pileActuelle.pop()
                            else: #Si le crochet se ferme sur une parenthèse ou vice verse
                                erreur = "mauvais retrait"

                caseLargeur = 75 #Largeur d'une case du conteneur
                conteneurResultat.setWidth(5 + ((i + 1) * caseLargeur) + ((i + 1) * 5)) #Réajuster la taille du conteneur
                xCase = 5 + ((i) * caseLargeur) + ((i) * 5) #Position x de chaque éléments de cette case

                for j in range(len(pileActuelle)): #Parcourir chaque élément de la pile actuelle
                    charactere = pileActuelle[j] #Définir le caractère à afficher

                    case = MText(charactere, xCase, 35 + 30 * j, caseLargeur, 30, conteneurResultat) #Création de la case qui contient le contenu de la piel actuelle
                    case.setFontSize(23)
                    case.setFrameWidth(1)
                    case.setTextHorizontalAlignment(1)
                    case.setTextVerticalAlignment(1)
                    if erreur == "mauvais retrait" and j == len(pileActuelle) - 1:
                        case.setTextColor((255, 0, 0))
                    contenuResultat.append(case)

                if erreur == "vide": #Si il y a une erreur "vide"
                    case = MText("Vide", xCase, 35 + 30 * len(pileActuelle), caseLargeur, 30, conteneurResultat) #Création de la case qui contient le contenu de la piel actuelle
                    case.setFontSize(23)
                    case.setTextColor((255, 0, 0))
                    case.setTextHorizontalAlignment(1)
                    case.setTextVerticalAlignment(1)
                    contenuResultat.append(case)

                lettre = MText(texteAAnalyser[i], xCase, 0, caseLargeur, 30, conteneurResultat) #Texte qui indique la lettre actuelle
                lettre.setFontSize(23)
                lettre.setFrameWidth(1, 2)
                lettre.setTextHorizontalAlignment(1)
                lettre.setTextVerticalAlignment(1)
                if erreur != "": #Si il y a une erreur, afficher la lettre en rouge
                    lettre.setTextColor((255, 0, 0))
                contenuResultat.append(lettre)

                if erreur != "":  #Si il y a une erreur, arrêter la génération
                    break
            
            if len(pileActuelle) > 0 and erreur == "":
                caseLargeur = 200 #Largeur d'une case du conteneur
                xCase = conteneurResultat.getWidth() #Position x des éléments dans la case du conteneur

                conteneurResultat.setWidth(conteneurResultat.getWidth() + caseLargeur + 5) #Réajuster la taille du conteneur

                caseTexte = "Parenthèse ouverte" #Texte affiché par la case qui indique "parenthèse/crochet ouvert"
                if pileActuelle[-1] == "[":
                    caseTexte = "Crochet ouvert"
                case = MText(caseTexte, xCase, 35, caseLargeur, 30, conteneurResultat) #Création de la case qui indique "parenthèse/crochet ouvert"
                case.setFontSize(23)
                case.setTextColor((255, 0, 0))
                case.setTextHorizontalAlignment(1)
                case.setTextVerticalAlignment(1)
                contenuResultat.append(case)

                lettre = MText("Fin", xCase, 0, caseLargeur, 30, conteneurResultat) #Texte qui indique "fin"
                lettre.setFontSize(23)
                lettre.setFrameWidth(1, 2)
                lettre.setTextHorizontalAlignment(1)
                lettre.setTextVerticalAlignment(1)
                lettre.setTextColor((255, 0, 0))
                contenuResultat.append(lettre)

            scrolleurResultat.reLoad()

    setFenetre(0)

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
        elif fenetreActuel == 1: #Si nous sommes sur la fenêtre d'analyse (pendant une frame seulement)
            setFenetre(2)

        mapp.frameGraphics() #Faire les mise à jour graphique de mlib (voir documentation)
        pygame.display.flip()
else:
    texte = str(input("Rentrez une chaîne de caractère : ")) #Demander à l'utilisateur une chaîne de caractère
    if est_parenthese(texte):
        print("Cette chaîne est bien parenthésé.")
    else:
        print("Cette chaîne n'est pas bien parenthésé.")