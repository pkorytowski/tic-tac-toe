import pygame as pg


def comp_move(board):
    best_score = -10000  # -inf
    best_move = -1
    possible_moves = [x for x, sign in enumerate(board) if sign[1] == 'empty']
    for k in possible_moves:
        board[k][1] = 'circle'
        score = minimax(board, 0, False)
        board[k][1] = 'empty'
        if score > best_score:
            best_score = score
            best_move = k

    return best_move


# Checks if 3 arguments are equal and belong to player
def equals3(a, b, c):
    return a == b and b == c and a != 'empty'


# Checks who won (rect/circle/tie/no_winners)
def check_winner(board):
    winner = 'no_winners'
    # Checking for rows
    for k in range(0,7,3):
        if equals3(board[k][1],board[k+1][1], board[k+2][1]):
            winner = board[k][1]
    # Checking columns
    for k in range(3):
        if equals3(board[k][1], board[k+3][1], board[k+6][1]):
            winner = board[k][1]
    # Crosswise
    if equals3(board[0][1], board[4][1], board[8][1]):
        winner = board[0][1]
    if equals3(board[2][1], board[4][1], board[6][1]):
        winner = board[2][1]
    is_full = True
    for x in board:
        if x[1] == 'empty':
            is_full = False
            break
    if winner is 'no_winners' and is_full:
        return 'tie'
    else:
        return winner


# needed for minimax
scores = {'rect': -1, 'circle': 1, 'tie': 0}


def minimax(board, depth, is_maximizing):
    result = check_winner(board)
    if result != 'no_winners':
        return scores[result]

    if is_maximizing:
        best_score = -10000
        possible_moves = [x for x, sign in enumerate(squares) if sign[1] == 'empty']
        for k in possible_moves:
            squares[k][1] = 'circle'
            score = minimax(board, depth+1, False)
            squares[k][1] = 'empty'
            if score > best_score:
                best_score = score
        return best_score
    else:
        best_score = 10000
        possible_moves = [x for x, sign in enumerate(squares) if sign[1] == 'empty']
        for k in possible_moves:
            squares[k][1] = 'rect'
            score = minimax(board, depth + 1, True)
            squares[k][1] = 'empty'
            if score < best_score:
                best_score = score
        return best_score


def text_info(board):
    font = pg.font.SysFont('Comic Sans MS', 40)
    text = font.render(check_winner(board) + ' won', True, (255, 0, 0), (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (275, 275)
    win.blit(text, text_rect)

# preparing window
pg.init()
win = pg.display.set_mode((550, 550))

pg.display.set_caption('Tic-Tac-Toe')

# preparing board
squares = []
for i in range(3):
    for j in range(3):
        squares.append([pg.draw.rect(win, (255, 255, 255), (25 + j*175, 25 + i*175, 150, 150)), 'empty'])

run = True
draw_object = 'rect'  # Flag which decides what shape should be drawn


# Main game loop
while run:
    for event in pg.event.get():
        # clicking quit button
        if event.type == pg.QUIT:
            run = False
        if check_winner(squares) == 'no_winners':
            # player clicks and it's his turn
            if event.type == pg.MOUSEBUTTONUP and draw_object == 'rect':
                pos = pg.mouse.get_pos()
                for element in squares:
                    if element[0].collidepoint(pos):
                        pg.draw.rect(win, (0, 255, 0), (element[0].x + 25, element[0].y + 25, 100, 100))
                        draw_object = 'circle'
                        element[1] = 'rect'
            # it's "computers" turn
            elif draw_object == 'circle':
                pos = comp_move(squares)
                pg.time.delay(400)
                pg.draw.circle(win, (0, 0, 255), (squares[pos][0].x + 75, squares[pos][0].y + 75), 50)
                draw_object = 'rect'
                squares[pos][1] = 'circle'
        else:
            text_info(squares)

    pg.display.update()
pg.quit()

