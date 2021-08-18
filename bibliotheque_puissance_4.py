from sys import stdin,stdout
from copy import deepcopy

global deltas_inf,positions,DIM_X,DIM_Y, JOUEUR, IA,INF, DEPTH,NB_COUPS
DIM_X, DIM_Y = 7, 6
JOUEUR, IA,VIDE = "X", "O", " "
INF = float('inf')
NB_COUPS = DIM_X * DIM_Y
DEPTH = 5
deltas = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
deltas_inf = [(-1,-1), (0,-1), (1,-1), (1,0)]
positions = [(x,y) for y in range(DIM_Y) for x in range(DIM_X)]

# Scores:
WIN = 42*7

def libre_pos(x, hauteur):
    return (0 <= x < DIM_X and hauteur[x] < DIM_Y)
def poser_jeton(x,joueur,hauteur,tableau):
    if libre_pos(x, hauteur):
        tableau[x][hauteur[x]] = joueur
        hauteur[x] += 1
        return tableau,hauteur
    return (False,False)
def depiler_jeton(x,hauteur,tableau):
    hauteur[x] -= 1
    tableau[x][hauteur[x]] = VIDE
    return tableau,hauteur

def valide_pos(x,y):
    return (0 <= x < DIM_X and 0 <= y < DIM_Y)
def test_win(tableau):
    for x, y in positions:
        if tableau[x][y] != VIDE:
            winner = tableau[x][y]
            for d_x,d_y in deltas_inf:
                win = True
                for i in range(1,4):
                    n_x, n_y = x+i*d_x, y + i*d_y
                    if not(valide_pos(n_x,n_y) and tableau[n_x][n_y] == winner):
                        win = False
                if win:
                    return winner
    return VIDE

def test_fin(hauteur):
    FIN = True
    for h in hauteur:
        if h < DIM_Y:
            FIN = False
    return FIN
  
def game_over(tableau,hauteur):
    return (test_win(tableau) or test_fin(hauteur))

def evaluate_score(joueur,tableau):
    # Evaluer la situation
    score = 0
    for x, y in positions:
        if tableau[x][y] == VIDE or tableau[x][y] == joueur:
            for d_x,d_y in deltas_inf:
                bonus = 0
                nb_jeton_ok = 0
                for i in range(DIM_X):
                    n_x, n_y = x+i*d_x, y + i*d_y
                    bonus += 1
                    if valide_pos(n_x,n_y) and tableau[x][y] == joueur:
                        nb_jeton_ok += 1
                    if not(valide_pos(n_x,n_y) and (tableau[x][y] == VIDE or tableau[x][y] == joueur)):
                        break
                if nb_jeton_ok >= 2 and bonus>= 4:
                    score += bonus
    return score 
def best_mouv(tableau,hauteur):
    # Trouvez le meilleur mouvement
    best_score = -INF
    for x in range(DIM_X):
        if libre_pos(x, hauteur):
            tableau,hauteur=poser_jeton(x,IA,hauteur,tableau)
            score = minimax(tableau,hauteur,NB_COUPS, -INF, INF,False)
            tableau,hauteur=depiler_jeton(x,hauteur,tableau)
            if score > best_score:
                best_score = score
                best = x
    print(best, best_score)
    return best
    
def minimax(tableau,hauteur,depth, alpha, beta,ia):
    # Evaluer le mouvement
    #print(tableau,depth)
    # Match gagnant
    if test_win(tableau) == IA:
        return WIN * depth
    if test_win(tableau) == JOUEUR:
        return -WIN * depth
    # Match nul
    if depth <= (NB_COUPS - DEPTH):
        return evaluate_score(IA, tableau) - evaluate_score(JOUEUR, tableau)
    if test_fin(hauteur):
        return 0
    
    if ia:
        score = -INF
        for x in range(DIM_X):
            if libre_pos(x, hauteur):
                tableau,hauteur=poser_jeton(x,IA,hauteur,tableau)
                score = max(score,minimax(tableau,hauteur, depth - 1, alpha, beta, False))
                tableau,hauteur=depiler_jeton(x,hauteur,tableau)
                
                if score >= beta:
                   return score
                alpha = max(alpha, score)
                
        return score
    else:
        score = INF
        for x in range(DIM_X):
            if libre_pos(x, hauteur):
                tableau,hauteur=poser_jeton(x,JOUEUR,hauteur,tableau)
                score = min(score,minimax(tableau,hauteur, depth - 1, alpha, beta, True))
                tableau,hauteur=depiler_jeton(x,hauteur,tableau)
                if alpha >= score:
                    return score
                beta = min(score,beta)
                
        return score
