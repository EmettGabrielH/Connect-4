from sys import stdin,stdout
from copy import deepcopy
from time import time

global deltas_inf,positions,possibilites,DIM_X,DIM_Y, JOUEUR, IA,INF, DEPTH,NB_CASES,TIME_MIN
DIM_X, DIM_Y = 7, 6
JOUEUR, IA,VIDE, BORDURE = "X", "O", " ", "#"
INF = float('inf')
NB_CASES = DIM_X * DIM_Y
DEPTH,TIME_MIN = 8, 1.2
deltas_inf = ((-1,-1), (0,-1), (1,-1), (1,0))

positions = tuple((x,y) for y in range(DIM_Y) for x in range(DIM_X))
possibilites = (3,2,4,1,5,0,6)

# Scores:
GRILLE_SCORE = [[3,4,5,5,4,3],[4,6,8,8,6,4],[5,8,11,11,8,5],[7,10,13,13,10,7],[5,8,11,11,8,5],[4,6,8,8,6,4],[3,4,5,5,4,3]]
a, m= DEPTH-1, 13
for x,y in positions: GRILLE_SCORE[x][y] = (a + GRILLE_SCORE[x][y]/m )/(a+1)
GRILLE_SCORE = tuple(map(tuple, GRILLE_SCORE))
WIN = 42*100

def best_mouv(tableau,hauteur):
    # Trouvez le meilleur mouvement
    global tour, debut_tour
    tour,debut_tour = sum(hauteur),time()
    stdout.write("Tour IA n°"+ str(tour)+"\n")
    if tour < DIM_Y:
        depth = DEPTH
    else:
        depth = DEPTH + hauteur.count(DIM_Y)*2
        
    best_score = -INF
    for x in possibilites:
        y = hauteur[x]
        
        if tableau[x,y] == VIDE:
            if test_win_pos(x,y,IA, tableau):
                score = WIN * depth
            else:
                tableau[x,y] = IA
                hauteur[x] += 1
                score = minimax(tableau,hauteur,depth, -INF, INF,evaluate_score_pos(x,y,tableau),False)
                stdout.write("Reflexion... \n")
                hauteur[x] -= 1
                tableau[x,y] = VIDE
            if score > best_score:
                best_score, best = score, x
    stdout.write("Coup choisi: "+str(best+1)+" | Score:" +str(best_score)+" | Temps: "+ str(round(time()-debut_tour,3)) +"\n")
    return best

def minimax(tableau,hauteur,depth, alpha, beta,valeur,ia):
    # Evaluer le mouvement
    
    

    #Profondeur maximale
    if depth <= 0 and time()-debut_tour > TIME_MIN:
        return valeur
    
    # Match nul
    if tour-depth+DEPTH+1 == NB_CASES:
        return 0
    
    if ia:
        score = -INF
        for x in possibilites:
            y = hauteur[x]
            if tableau[x,y] == VIDE:
                # Coup gagnant
                if test_win_pos(x,y,IA, tableau):
                    return  WIN * depth
                
                tableau[x,y] = IA
                hauteur[x] += 1
                
                score = max(score,minimax(tableau,hauteur,depth - 1, alpha, beta,valeur + evaluate_score_pos(x,y,tableau), False))
                hauteur[x] -= 1
                tableau[x,y] = VIDE
                
                if score >= beta:
                   return score
                alpha = max(alpha, score)
                
        return score
    else:
        score = INF
        for x in possibilites:
            y = hauteur[x]
            if tableau[x,y] == VIDE:
                # Coup gagnant
                if test_win_pos(x,y,JOUEUR, tableau):
                    return  -WIN * depth
                tableau[x,y] = JOUEUR
                hauteur[x] += 1
                
                score = min(score,minimax(tableau,hauteur, depth - 1, alpha, beta,valeur - evaluate_score_pos(x,y,tableau), True))
                hauteur[x] -= 1
                tableau[x,y] = VIDE
                
                if alpha >= score:
                    return score
                beta = min(score,beta)
                
        return score
    
def test_win_pos(x,y,joueur, tableau):
    for d_x,d_y in deltas_inf:
        nb_alignes = 1
        for op in [1,-1]:
            for i in range(1,4):
                n_x, n_y = x+i*op*d_x, y + i*op*d_y
                if nb_alignes >= 4:
                    return True
                if tableau[n_x,n_y] != joueur:
                    break
                nb_alignes += 1
        if nb_alignes >= 4:
            return True
    return False

def evaluate_score_pos(x,y,tableau):
    # Est ce que cette position permet a moi ou l'adversaire d'avoir deux ou trois jetons alignés ?
    score_IA,score_JO = 0, 0
    for d_x,d_y in deltas_inf:
        nb_libre_IA,nb_alignes_IA, continu_IA =1, 1, True
        nb_libre_JO,nb_alignes_JO, continu_JO =1, 1, True
        for op in [1,-1]:
            for i in [1,2,3]:
                n_x, n_y = x+i*op*d_x, y + i*op*d_y
                if continu_IA or continu_JO:
                    case = tableau[n_x,n_y]
                    if continu_IA and (case == IA or case == VIDE):
                        nb_libre_IA += 1
                        if case == IA:
                            nb_alignes_IA += GRILLE_SCORE[n_x][n_y]
                    else:
                        continu_IA = False
                    if continu_JO and (case == JOUEUR or case == VIDE):
                        nb_libre_JO += 1
                        if case == JOUEUR:
                            nb_alignes_JO += GRILLE_SCORE[n_x][n_y]
                    else:
                        continu_JO = False
                else:
                    break
        if nb_libre_IA >= 4 and nb_alignes_IA > 2 and nb_alignes_IA > score_IA:
            score_IA = min(3,nb_alignes_IA)
        if nb_libre_JO >= 4 and nb_alignes_JO > 2 and nb_alignes_JO > score_JO:
            score_JO = min(3,nb_alignes_JO)
    return score_IA + score_JO

def evaluate_score(tableau):
    score = 0
    for x, y in positions:
        joueur = tableau[x,y]
        if joueur == IA:
            score += evaluate_score_pos(x,y,tableau)
        if joueur == JOUEUR:
            score -= evaluate_score_pos(x,y,tableau)
    return score

def poser_jeton(x,joueur,hauteur,tableau):
    if tableau[x,hauteur[x]] == VIDE:
        tableau[x,hauteur[x]] = joueur
        hauteur[x] += 1
        return True
    return False
def test_win(tableau):
    for x, y in positions:
        if tableau[x,y] != VIDE and tableau[x,y] != BORDURE:
            winner = tableau[x,y]
            for d_x,d_y in deltas_inf:
                win = True
                for i in range(1,4):
                    n_x, n_y = x+i*d_x, y + i*d_y
                    if tableau[n_x,n_y] != winner:
                        win = False
                        break
                if win:
                    return winner
    return VIDE
def test_fin(hauteur):
    for h in hauteur[:-1]:
        if h < DIM_Y:
            return False
    return True
def afficher_jeu(tableau):
    stdout.write("---------------\n")
    for y in range(DIM_Y-1,-1,-1):
        ligne = str(y+1)+" "
        for x in range(DIM_X):
            ligne += tableau[x,y]
            if (x+y)%2 == 0:
                 ligne += " " #\f
            else:
                ligne += " "
        stdout.write("%s\n" %ligne)
    stdout.write("  "+" ".join(map(str,range(1,DIM_X+1)))+"\n")
    
