#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system

"""
An implementation of Minimax AI Algorithm in Tic Tac Toe,
using Python.
This software is available under GPL license.
Author: Clederson Cruz
Year: 2017
License: GNU GENERAL PUBLIC LICENSE (GPL)
"""

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def evaluate(state):
    """
    Função para avaliação heurística do estado.
     : param state: o estado do quadro atual
     : return: +1 se o computador vencer; -1 se o humano vencer; 0 empate
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    305/5000
Esta função testa se um jogador específico vence. Possibilidades:
     * Três linhas [X X X] ou [O O O]
     * Três colunas [X X X] ou [O O O]
     * Duas diagonais [X X X] ou [O O O]
     : param state: o estado do quadro atual
     : param player: um humano ou um computador
     : return: True se o jogador vencer
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    Esta função testa se o humano ou o computador vence
     : param state: o estado do quadro atual
     : return: True se o humano ou o computador vencer
    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    Cada célula vazia será adicionada à lista de células
     : param state: o estado do quadro atual
     : return: uma lista de células vazias
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    Uma movimentação é válida se a célula escolhida estiver vazia
     : param x: coordenada X
     : param y: coordenada Y
     : return: True se o quadro [x] [y] estiver vazio
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    Defina a mudança a bordo, se as coordenadas forem válidas
     : param x: coordenada X
     : param y: coordenada Y
     : param player: o jogador atual
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    Função AI que escolha a melhor jogada
     : param state: estado atual do quadro
     : param depth: índice do nó na árvore (0 <= depth <= 9),
     mas nunca nove neste caso (consulte a função iaturn ())
     : param player: um humano ou um computador
     : return: uma lista com [a melhor linha, melhor col, melhor pontuação]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def clean():
    """
    limpa o console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    """
   Imprimir o quadro no console
     : param state: estado atual do quadro
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    """
    Ele chama a função minimax se a profundidade <9,
     caso contrário, ele escolhe uma coordenada aleatória.
     : param c_choice: escolha do computador X ou O
     : param h_choice: escolha humana X ou O
     :Retorna:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)


def human_turn(c_choice, h_choice):
    """
    O humano joga escolhendo uma jogada válida.
     : param c_choice: escolha do computador X ou O
     : param h_choice: escolha humana X ou O
     : return: m h_choice: escolha humana X ou O
     :Retorna:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('pessimo movimento')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('tchau')
            exit()
        except (KeyError, ValueError):
            print('pessima escolha')


def main():
    """
    Função principal que chama todas as funções
    """
    clean()
    h_choice = ''  # X ou O
    c_choice = ''  # X ou O
    first = ''  # se o humano for o primeiro

    # humano escolhe entre X ou O para começar
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Escolha X ou O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('tchau')
            exit()
        except (KeyError, ValueError):
            print('pessima escolha')

    # Definir a escolha do computador
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # O ser humano pode começar primeiro
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('primeiro a começar?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('tchau')
            exit()
        except (KeyError, ValueError):
            print('pessima escolha')

    # loop principal do jogo
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # mensagem de game over
    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('VOCE GANHOU :)')
    elif wins(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('VOCE PERDEU :(')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()
