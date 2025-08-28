###### main.py ######
# -> the file where the main function is located
# -> here you can run the training or start the game

###### IMPORTS ######
from imports import *
from process_game import *
from global_variables import *
from agent_q_learning import *
from agent_sarsa import *
from plot_results import *
from train_agents import *
###### END IMPORTS ######

# ENVIRONMENT //
env = gym.wrappers.RecordEpisodeStatistics(gym.make("TicTacToe"))

# AGENT 1 //
agent_1 = Agent_Q_Learning(
        env = env,
        learning_rate = .00001,
        initial_epsilon = start_epsilon,
        epsilon_decay = start_epsilon / (n_episodes / 1.5),
        final_epsilon = final_epsilon,
        discount_factor = .95,
)

# AGENT 2 //
agent_2 = Agent_SARSA(
        env = env,
        learning_rate = .00001,
        initial_epsilon = start_epsilon,
        epsilon_decay = start_epsilon / (n_episodes / 1.5),
        final_epsilon = final_epsilon,
        discount_factor = .95,
)

###### MAIN ######
if __name__ == "__main__":
        # -> thread for processing the game
        process_game = Thread(target=process_game_thread, args=(action_table,))
        process_game.daemon = True
        process_game.start()
        time.sleep(1)

        gui = GUI(pygame)

        train(env, gui, n_episodes, agent_1, agent_2)

        plot_results()
###### END MAIN ######