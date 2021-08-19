from sys import stdin,stdout
from copy import deepcopy

global deltas_inf,deltas_sup,positions,possibilites,DIM_X,DIM_Y, JOUEUR, IA,INF, DEPTH,NB_COUPS,GRILLE_SCORE
DIM_X, DIM_Y = 7, 6
JOUEUR, IA,VIDE = "X", "O", " "
INF = float('inf')
NB_CASES = DIM_X * DIM_Y
DEPTH = 8
deltas_inf = [(-1,-1), (0,-1), (1,-1), (1,0)]
deltas_sup = [(1,1), (0,1), (-1,1), (-1,0)]

positions = [(x,y) for y in range(DIM_Y) for x in range(DIM_X)]
possibilites = [3,2,4,1,5,0,6]

# Scores:
GRILLE_SCORE = [(3,4,5,5,4,3),(4,6,8,8,6,4),(5,8,11,11,8,5),(7,10,13,13,10,7),(5,8,11,11,8,5),(4,6,8,8,6,4),(3,4,5,5,4,3)]
WIN = 42*100

def libre_pos(x, hauteur):
    return (0 <= x < DIM_X and hauteur[x] < DIM_Y)
def valide_pos(x,y):
    return (0 <= x < DIM_X and 0 <= y < DIM_Y)

def poser_jeton(x,joueur,hauteur,tableau):
    if libre_pos(x, hauteur):
        tableau[x][hauteur[x]] = joueur
        hauteur[x] += 1
        return True
    return False


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

def test_win_pos(x, tableau, hauteur):
    y = hauteur[x]-1
    joueur = tableau[x][y]
    for d_x,d_y in deltas_inf:
        nb_alignes = 1
        for op in [1,-1]:
            for i in range(1,4):
                n_x, n_y = x+i*op*d_x, y + i*op*d_y
                if not(valide_pos(n_x,n_y) and tableau[n_x][n_y] == joueur):
                    break
                nb_alignes += 1
        if nb_alignes >= 4:
            return True
    return False
            
def test_fin(hauteur):
    for h in hauteur:
        if h < DIM_Y:
            return False
    return True

def evaluate_score(joueur,tableau):
    # Evaluer la situation
    score = 0
    non_joueur = JOUEUR if joueur == IA else IA
    for x, y in positions:
        if tableau[x][y] == joueur :
            score += GRILLE_SCORE[x][y]
        elif tableau[x][y] == non_joueur:
            score -= GRILLE_SCORE[x][y]
    return score

def best_mouv(tableau,hauteur):
    # Trouvez le meilleur mouvement
    tour = sum(hauteur)
    best_score = -INF
    for x in possibilites:
        if libre_pos(x, hauteur):
            tableau[x][hauteur[x]] = IA
            hauteur[x] += 1
            score = minimax(x,tableau,hauteur,tour,DEPTH, -INF, INF,False)
            hauteur[x] -= 1
            tableau[x][hauteur[x]] = VIDE
            
            if score > best_score:
                best_score = score
                best = x
    print(best+1, best_score)
    return best
    
def minimax(x,tableau,hauteur,tour,depth, alpha, beta,ia):
    # Evaluer le mouvement
    
    # Coup gagnant
    if test_win_pos(x,tableau,hauteur):
        if ia: return -WIN * depth
        else:  return  WIN * depth

    #Profondeur maximale
    if depth == 0:
        return evaluate_score(IA, tableau)
    
    # Match nul
    if tour == NB_CASES:
        return 0
    
    if ia:
        score = -INF
        for x in possibilites:
            if libre_pos(x, hauteur):
                tableau[x][hauteur[x]] = IA
                hauteur[x] += 1
                score = max(score,minimax(x,tableau,hauteur,tour+1,depth - 1, alpha, beta, False))
                hauteur[x] -= 1
                tableau[x][hauteur[x]] = VIDE
                
                if score >= beta:
                   return score
                alpha = max(alpha, score)
                
        return score
    else:
        score = INF
        for x in possibilites:
            if libre_pos(x, hauteur):
                tableau[x][hauteur[x]] = JOUEUR
                hauteur[x] += 1
                score = min(score,minimax(x,tableau,hauteur,tour+1, depth - 1, alpha, beta, True))
                hauteur[x] -= 1
                tableau[x][hauteur[x]] = VIDE
                
                if alpha >= score:
                    return score
                beta = min(score,beta)
                
        return score
  
def game_over(tableau,hauteur):
    return (test_win(tableau) or test_fin(hauteur))

def evaluate_score2(joueur,tableau):
    # Evaluer la situation
    score = 0
    non_joueur = IA if joueur == IA else JOUEUR
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
                    if not(valide_pos(n_x,n_y) and tableau[x][y] != non_joueur):
                        break
                if nb_jeton_ok >= 2 and bonus>= 4:
                    score += nb_jeton_ok*2 + bonus
    return score 
