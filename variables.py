from imports import *

p1_win = Event()
p2_win = Event()

X_SIGN = 1
O_SIGN = -1

round_done = Event()
game_finished = Event()

line_winner = {'line': None}

monitor = Lock()
identified_o = [[],[],[]]
identified_x = [[],[],[],[]]