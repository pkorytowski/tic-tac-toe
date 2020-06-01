import pygame as pg


def comp_move(board):
    best_score = float("-inf")  # -inf
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
    for k in range(0, 7, 3):
        if equals3(board[k][1], board[k+1][1], board[k+2][1]):
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


def text_objects(text, font):
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface, text_surface.get_rect()


def reset_board(draw_object):
    winner = check_winner(squares)
    if winner == 'rect':
        draw_object = 'rect'
    elif winner == 'circle':
        draw_object = 'circle'

    win.fill((0, 0, 0))
    for element in squares:
        pg.draw.rect(win, (255, 255, 255), (element[0].x, element[0].y, 120, 120))
        element[1] = 'empty'
    return draw_object

def counter(result, PC_score, player_score):

    if result == 'tie':
        PC_score += 1
        player_score += 1
    if result == 'circle':
        PC_score += 1
    if result == 'rect':
        player_score += 1
    
    return PC_score, player_score

def button(window, PC_score, player_score, draw_object):
    color = (219, 48, 165)
    x = 125
    y = 170
    w = 200
    h = 50

    pg.draw.rect(window, color, (x, y, w, h))
    small_text = pg.font.SysFont("comicsansms", 40)
    text_surf, text_rect = text_objects("New Game", small_text)
    text_rect.center = ((x+(w/2)), (y+(h/2)))
    window.blit(text_surf, text_rect)
    click = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()
    if click[0]:
        if x <= mouse_pos[0] <= x+w and y <= mouse_pos[1] <= y+h:
            PC_score, player_score = counter(check_winner(squares), PC_score, player_score)
            draw_object = reset_board(draw_object)

    return PC_score, player_score, draw_object


def text_info(board, window, PC_score, player_score, draw_object):
    font = pg.font.SysFont('Comic Sans MS', 40)
    text = font.render(check_winner(board) + ' won!', True, (255, 0, 0), (255, 255, 255))

    if check_winner(board) == 'tie':
        text = font.render('It\'s a tie!', True, (255, 0, 0), (255, 255, 255))

    text_rect = text.get_rect()
    text_rect.center = (225, 300)
    win.blit(text, text_rect)
    PC_score, player_score, draw_object = button(window, PC_score, player_score, draw_object)
    return PC_score, player_score, draw_object


def draw_turn(window, draw_object):
    x = 200
    y = 75
    w = 200
    h = 50

    str = ''
    if draw_object=='rect':
        str = 'Your turn'
    else:
        str = "AI's turn"
    pg.draw.rect(window, (0, 0, 0), (x, y, w, h))
    font = pg.font.SysFont('Comic Sans MS', 40)
    text = font.render(str, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (x+w/2, y+h/2)
    window.blit(text, text_rect)


def score_board(window, PC_score, player_score):
    font = pg.font.SysFont('Comic Sans MS', 40)
    
    PC = font.render('PC: ' + str(PC_score),  True, (255, 255, 255), (0, 0, 0))
    player = font.render('Player: ' + str(player_score), True, (255, 255, 255), (0, 0, 0))

    PC_pos = PC.get_rect()
    PC_pos.center = (50, 25)

    player_pos = player.get_rect()
    player_pos.center = (300, 25)

    window.blit(PC, PC_pos)
    window.blit(player, player_pos)


# preparing window
pg.init()
win = pg.display.set_mode((450, 600))
pg.display.set_caption('Tic-Tac-Toe!')



# preparing board
squares = []
for i in range(3):
    for j in range(3):
        squares.append([pg.draw.rect(win, (255, 255, 255), (25 + j*140, 140 + i*140, 120, 120)), 'empty'])

run = True
draw_object = 'rect'  # Flag which decides what shape should be drawn

PC_score = 0
player_score = 0
clock = pg.time.Clock()

# Main game loop
while run:
    
    score_board(win, PC_score, player_score)
    draw_turn(win, draw_object)
    for event in pg.event.get():
        # clicking quit button
        if event.type == pg.QUIT:
            run = False
        if check_winner(squares) == 'no_winners':
            # player clicks and it's his turn
            if event.type == pg.MOUSEBUTTONDOWN and draw_object == 'rect':
                pos = pg.mouse.get_pos()
                for element in squares:
                    if element[0].collidepoint(pos) and element[1] == 'empty':
                        pg.draw.rect(win, (0, 255, 0), (element[0].x + 20, element[0].y + 20, 80, 80))
                        draw_object = 'circle'
                        element[1] = 'rect'
            # it's "computers" turn
            elif draw_object == 'circle':
                pos = comp_move(squares)
                pg.time.delay(400)
                pg.draw.circle(win, (0, 0, 255), (squares[pos][0].x + 60, squares[pos][0].y + 60), 40)
                draw_object = 'rect'
                squares[pos][1] = 'circle'
        else:
            PC_score, player_score, draw_object = text_info(squares, win, PC_score, player_score, draw_object)

    pg.display.update()
    clock.tick(60)

pg.quit()
