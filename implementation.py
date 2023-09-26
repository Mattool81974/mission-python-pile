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