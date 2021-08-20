from bibliotheque_puissance_4 import *

def test():
    win = test_win(TABLEAU)
    if win == JOUEUR:
        stdout.write("Victoire du joueur !!!\n")
        return False
    if win == IA:
        stdout.write("Victoire de l'IA!!!\n")
        return False
    if test_fin(HAUTEUR):
        stdout.write("Match nul !!!\n")
        return False
    return True
def tour():
    if T == 1:
        joueur_tour()
        afficher_jeu(TABLEAU)
        if test() == False: return False
        ia_tour()
        afficher_jeu(TABLEAU)
    if T == 2:
        ia_tour()
        afficher_jeu(TABLEAU)
        if test() == False: return False
        joueur_tour()
        afficher_jeu(TABLEAU)
    return test()

def joueur_tour():
    ERREUR = True
    # Tour Joueur
    while ERREUR:
        stdout.write("> \n")
        try : 
            x = int(stdin.readline()) - 1
        except:
            x = -1
        if poser_jeton(x,JOUEUR,HAUTEUR,TABLEAU):
            # Poser un jeton en x
            ERREUR = False
    
    return True

def ia_tour():
    # Tour ia
    tableau = deepcopy(TABLEAU)
    hauteur = deepcopy(HAUTEUR)
    x = best_mouv(tableau,hauteur)
    poser_jeton(x,IA,HAUTEUR,TABLEAU)
    
def main():
    global TABLEAU,HAUTEUR, T, IA, JOUEUR
    TABLEAU = [[VIDE for y in range(DIM_Y)]+[BORDURE] for x in range(DIM_X)] + [[BORDURE for _ in range(DIM_X+1)]]
    HAUTEUR = [0 for x in range(DIM_X+1)]
    
    # Premier au deuxième joueur ?
    stdout.write("Joueur 1 ou 2 ? > \n")
    T = ""
    while not(T == "1\n" or T == "2\n"):
        T = stdin.readline()
    T = int(T)
    
    # Jeux
    afficher_jeu(TABLEAU)
    while tour():
        pass
    
stdout.write("PUISSANCE 4 - Emett\n")    
while True:
    main()
