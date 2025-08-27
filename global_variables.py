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

epsilon_values = [[],[]]
reward_vector_p1 = []
reward_vector_p2 = []
draw_vector = []
lost_rounds = []
action_table = np.zeros([3, 3], dtype=np.int8)

actions_p = {
        'actions_p1': np.zeros(9),
        'actions_p2': np.zeros(9),
}

# TRAIN VARIABLES //
n_episodes = 1_00
start_epsilon = 1.
epsilon_decay = start_epsilon / (n_episodes / 2)
final_epsilon = .00001
