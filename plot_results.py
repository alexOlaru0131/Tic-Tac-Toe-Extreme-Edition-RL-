###### IMPORTS ######
from imports import *
from process_game import *
from global_variables import *
###### END IMPORTS ######

def plot_results():

        _, axs = plt.subplots(ncols = 2, nrows = 2, figsize = (13, 8))

        axs[0, 0].set_title("Epsilon decay")
        axs[0, 0].plot(range(len(epsilon_values[0])), epsilon_values[0], label = 'Epsilon - P1')
        axs[0, 0].plot(range(len(epsilon_values[1])), epsilon_values[1], label = 'Epsilon - P2')
        axs[0, 0].legend()
        axs[0, 0].set_ylabel("Epsilon")
        axs[0, 0].set_xlabel("Epsiode")

        axs[0, 1].set_title("Round evolution")
        axs[0, 1].plot(range(len(draw_vector)), draw_vector, label = 'Draws')
        axs[0, 1].plot(range(len(reward_vector_p1)), reward_vector_p1, label = 'Points P1')
        axs[0, 1].plot(range(len(reward_vector_p2)), reward_vector_p2, label = 'Points P2')
        axs[0, 1].plot(range(len(lost_rounds)), lost_rounds, label = 'Lost rounds')
        axs[0, 1].legend()
        axs[0, 1].set_ylabel("Draws")
        axs[0, 1].set_xlabel("Episode")

        axs[1, 0].set_title("Number of actions taken")
        actions = ['(1,1)', '(1,2)', '(1,3)',
                   '(2,1)', '(2,2)', '(2,3)',
                   '(3,1)', '(3,2)', '(3,3)',]
        
        x = np.arange(len(actions))
        width = 0.25
        multiplier = 0
        actions_p['actions_p2'] = actions_p['actions_p2'] // 2

        for attribute, measurement in actions_p.items():
                offset = width * multiplier
                rects = axs[1, 0].bar(x + offset, measurement, width, label=attribute)
                axs[1, 0].bar_label(rects, padding=3)
                multiplier += 1
        axs[1, 0].set_xticks(x + width, actions)
        axs[1, 0].legend(loc='upper right')

        axs[1, 1].set_title("Agent rewards")
        axs[1, 1].plot(range(len(reward_vector_p1)), reward_vector_p1, label = 'Reward P1')
        axs[1, 1].plot(range(len(reward_vector_p2)), reward_vector_p2, label = 'Reward P2')
        axs[1, 1].legend()
        axs[1, 1].set_ylabel("Reward")
        axs[1, 1].set_xlabel("Episode")

        plt.tight_layout()
        plt.show()