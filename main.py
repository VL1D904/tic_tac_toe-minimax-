import pygame
import tkinter.messagebox as msg
import numpy
import copy

pygame.init()
pygame.display.set_caption('Крестики Нолики')
screen = pygame.display.set_mode((300, 300))
screen.fill('white')

cross = pygame.image.load('cross.jpg')
circle = pygame.image.load('circle.png')

TABLE = [[' ' for _ in range(3)] for _ in range(3)]

player_check = True

step = 8


class Player:
    def __init__(self):
        pass

    def set_cell(self, pos):
        x, y = pos
        x //= 100
        y //= 100

        screen.blit(cross, (x * 100, y * 100))

        TABLE[y][x] = 'x'


class AI:
    def __init__(self):
        self.benefit_move = []

    def minimax(self, count, table):
        global step

        global_deep_score = 0

        for i in range(0, 3):
            for j in range(0, 3):
                table_copy = copy.deepcopy(table)
                if table_copy[i][j] != ' ':
                    continue

                score = 0
                table_now = table_copy
                table_now[i][j] = 'o' if count % 2 == 1 else 'x'
                table_vector = numpy.ravel(table_now)
                res = check(table_now)
                if count == step or res != 0 or ' ' not in table_vector:
                    score += res
                else:
                    score += self.minimax(count + 1, table_now)

                if count == 1:
                    self.benefit_move.append((score, [i, j]))
                else:
                    global_deep_score += score
        
        return global_deep_score
                


def main():
    global player_check
    for i in range(100, 300, 100):
        pygame.draw.line(screen, 'black', [0, i], [300, i], 2)
        pygame.draw.line(screen, 'black', [i, 0], [i, 300], 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and player_check:
                player.set_cell(event.pos)
                player_check = False

        if check(TABLE) != 0 or ' ' not in numpy.ravel(TABLE):
            msg.showinfo('Игра окончена!', 'Игра окончена!')
            reset()

        if not player_check:
            ai.benefit_move = []
            ai.minimax(1, TABLE)
            y, x = max(ai.benefit_move, key=lambda x: x[0])[1]
            screen.blit(circle, (x * 100, y * 100))
            TABLE[y][x] = 'o'
            player_check = True

        pygame.display.flip()


def reset():
    global TABLE, player_check

    screen.fill('white')
    for i in range(100, 300, 100):
        pygame.draw.line(screen, 'black', [0, i], [300, i], 2)
        pygame.draw.line(screen, 'black', [i, 0], [i, 300], 2)
    TABLE = [[' ' for _ in range(3)] for _ in range(3)]
    player_check = True
    return 0

def check(table):
        winner = 0
        for i in range(0, 3):
            if len(set(table[i])) == 1 and table[i][0] != ' ':
                winner += -1 if list(table[i])[0] == 'x' else 1
                return winner

        for i in range(0, 3):
            t = []
            for j in range(0, 3):
                t.append(table[j][i])

            if len(set(t)) == 1 and t[0] != ' ':
                winner += -1 if list(t)[0] == 'x' else 1
                return winner

        t = set([table[i][i] for i in range(0, 3)])
        if len(t) == 1 and list(t)[0] != ' ':
            winner += -1 if list(table)[0] == 'x' else 1
            return winner

        t = set([table[i][2 - i] for i in range(0, 3)])
        if len(t) == 1 and list(t)[0] != ' ':
            winner += -1 if list(t)[0] == 'x' else 1
            return winner

        return winner


if __name__ == '__main__':
    player = Player()
    ai = AI()
    main()
