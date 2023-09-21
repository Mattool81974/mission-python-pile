from random import choice, randint

#PILE WITH LIST

def pile_vide():
    return []

def est_vide(p: list):
    return p == []

def empiler(p, x):
    p.append(x)
    
def depiler(p: list):
    assert not est_vide(p), "p est vide"
    return p.pop()

def consulter(p: list):
    d = depiler(p)
    empiler(p, d)
    return d
    #return depiler(p.copy())

def taille(p: list):
    pile_bis = pile_vide()
    i = 0
    while not est_vide(p):
        i += 1
        d = depiler(p)
        empiler(pile_bis, d)
        
    while not est_vide(pile_bis):
        empiler(p, depiler(pile_bis))
        
    return i

def renverser(p: list):
    pile_bis = pile_vide()
    while not est_vide(p):
        d = depiler(p)
        empiler(pile_bis, d)
        
    pile_ter = pile_vide()
    while not est_vide(pile_bis):
        d = depiler(pile_bis)
        empiler(pile_ter, d)
        
    while not est_vide(pile_ter):
        empiler(p, depiler(pile_ter))
        
    return p

def melange(p1: list, p2: list):
    p3 = pile_vide()
    while not est_vide(p1) and not est_vide(p2):
        empiler(p3, depiler(choice([p1, p2])))
        
    while not est_vide(p1):
        empiler(p3, depiler(p1))
        
    while not est_vide(p2):
        empiler(p3, depiler(p2))
        
    return p3

def couper(p: list):
    autre_p = pile_vide()
    k = randint(0, taille(p) - 1)
    for i in range(k):
        empiler(autre_p, depiler(p))
    
    return autre_p

def gilbreath():
    return "As"