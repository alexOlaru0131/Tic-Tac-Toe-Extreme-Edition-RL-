###### main.py ######
# -> the file where the main function is located
# -> here you can run the training or start the game

###### IMPORTS ######
from imports import *
from process_game import *
from variables import *
from agent_q_learning import *
from agent_sarsa import *
###### END IMPORTS ######

###### TRAINING ######
action_table = np.zeros([3, 3], dtype=np.int8)

# AGENT VARIABLES //
n_episodes = 1_00
start_epsilon = 1.
epsilon_decay = start_epsilon / (n_episodes / 2)
final_epsilon = .00001

# ENVIRONMENT //
env = gym.wrappers.RecordEpisodeStatistics(gym.make("TicTacToe"))

# AGENT 1: he's very dedicated to learning, but very stupid //
agent_1 = Agent_Q_Learning(
        env = env,
        learning_rate = .0001,
        initial_epsilon = start_epsilon,
        epsilon_decay = epsilon_decay,
        final_epsilon = final_epsilon,
        discount_factor = .0001,
)

# AGENT 2: he's clever, but shy //
agent_2 = Agent_SARSA(
        env = env,
        learning_rate = .0001,
        initial_epsilon = start_epsilon,
        epsilon_decay = epsilon_decay,
        final_epsilon = final_epsilon,
        discount_factor = .0001,
)

# TRAIN FUNCTION -> GETS THE AGENTS IN TRAINING AND EXPLORING //
reward_vector = []
reward_vector_p1 = []
reward_vector_p2 = []
draw_vector = []

def train():
        process_game = Thread(target=process_game_thread, args=(action_table,))
        process_game.start()
        gui = GUI(pygame)

        total_reward = reward_p1 = reward_p2 = total_reward_p1 = total_reward_p2 = draws =  0

        for episode in tqdm(range(n_episodes)):
                observation, _ = env.reset()
                gui.reset(total_reward_p1, total_reward_p2, episode)

                done = terminated = truncated = False
                action_2 = None

                while not done:
                        monitor.acquire()
                        count = 0
                        print(f'Im here! 4: {done} {count}\n')
                        time.sleep(0.1)

                        for i in range(3):
                                for j in range(3):
                                        if action_table[i][j] != 0: count += 1

                        if count % 2 == 1:
                                count = 0
                                round_done.set()
                                monitor.release()
                                break
                        
                        monitor.release()
                        monitor.acquire()
                        print(f'Im here! 8: {done} {count}\n')
                        if count == 8 and line_winner['line'] == "none":
                                print(f'Im here! 5: {done} {count}\n')
                                action_1 = np.where(np.array(observation) == 0)[0][0]
                                print(f'Im here! 7: {done} {count}\n')
                                gui.update("X", gui._action[action_1])

                                print(f'Im here! 6: {done} {count}\n')

                        if count < 8 and line_winner['line'] == "none":
                                action_1 = agent_1.get_action(observation)
                                next_action_2 = agent_2.get_action(observation)
                                while observation[action_1] != 0:
                                        action_1 = agent_1.get_action(observation)
                                while observation[next_action_2] != 0 or action_1 == next_action_2:
                                        next_action_2 = agent_2.get_action(observation)
                                if action_2 is None:
                                        action_2 = next_action_2
                                
                                gui.update("X", gui._action[action_1])
                                gui.update("O", gui._action[next_action_2])

                        monitor.release()
                        monitor.acquire()
                        next_observation, reward, terminated, truncated, _ = env.step(action = (int(action_1), int(next_action_2)))

                        if reward != 0:
                                reward_p1 = 1 if reward == X_SIGN else -1
                                reward_p2 = 1 if reward == O_SIGN else -1
                                total_reward_p1 += reward_p1 if reward_p1 > 0 else 0
                                total_reward_p2 += reward_p2 if reward_p2 > 0 else 0
                                reward_vector_p1.append(total_reward_p1)
                                reward_vector_p2.append(total_reward_p2)
                
                        agent_1.update(observation, action_1, reward_p1, terminated, next_observation)
                        agent_2.update(observation, action_2, reward_p2, terminated, next_action_2, next_observation)

                        done = terminated or truncated or count == 9

                        print(f'Im here! 1: {done} {count}\n')
                        
                        if done:
                                print(f'Im here! 2: {done} {count}\n')
                                if not line_winner['line'] == "none":
                                        draw_vector.append(draws)
                                        gui.winner(gui._winner_lines[line_winner['line']], reward)
                                        round_done.set()
                                        time.sleep(0.1)
                                else:
                                        draws += 1
                                        draw_vector.append(draws)
                                        round_done.set()

                        print(f'Im here! 3: {done} {count}\n')
                                        
                        observation = next_observation
                        action_2 = next_action_2
                        p1_win.clear()
                        p2_win.clear()
                        monitor.release()

                total_reward += reward
                reward_vector.append(total_reward)
                agent_1.decay_epsilon()
                agent_2.decay_epsilon()
###### END TRAINING ######

###### PLOTTING RESULTS ######
def get_moving_avgs(arr, window, convolution_mode):
        return np.convolve(
                np.array(arr).flatten(),
                np.ones(window),
                mode = convolution_mode,
        )
###### END PLOTTING RESULTS ######

###### MAIN ######
if __name__ == "__main__":

        train()

        game_finished.set()

        rolling_length = 500
        fig, axs = plt.subplots(ncols = 3, nrows = 2, figsize = (11, 7))

        axs[0, 0].set_title("Episode rewards")
        axs[0, 0].plot(range(len(reward_vector)), reward_vector)
        axs[0, 0].set_ylabel("Average reward")
        axs[0, 0].set_xlabel("Step")

        axs[0, 1].set_title("Draws")
        length_moving_average = get_moving_avgs(
                env.length_queue,
                rolling_length,
                "valid",
        )
        axs[0, 1].plot(range(len(draw_vector)), draw_vector)
        axs[0, 1].set_ylabel("Draws")
        axs[0, 1].set_xlabel("Step")

        axs[1, 0].set_title("Training error - Agent 1")
        training_error_moving_average = get_moving_avgs(
                agent_1.training_error,
                rolling_length,
                "same",
        )
        axs[1, 0].plot(range(len(training_error_moving_average)), training_error_moving_average)
        axs[1, 0].set_ylabel("Temporal difference error")
        axs[1, 0].set_xlabel("Step")

        axs[1, 1].set_title("Training error - Agent 2")
        training_error_moving_average = get_moving_avgs(
                agent_2.training_error,
                rolling_length,
                "same",
        )
        axs[1, 1].plot(range(len(training_error_moving_average)), training_error_moving_average)
        axs[1, 1].set_ylabel("Temporal difference error")
        axs[1, 1].set_xlabel("Step")

        axs[0, 2].set_title("Agent 1 rewards")
        axs[0, 2].plot(range(len(reward_vector_p1)), reward_vector_p1)
        axs[0, 2].set_ylabel("Average reward")
        axs[0, 2].set_xlabel("Step")

        axs[1, 2].set_title("Agent 2 rewards")
        axs[1, 2].plot(range(len(reward_vector_p2)), reward_vector_p2)
        axs[1, 2].set_ylabel("Average reward")
        axs[1, 2].set_xlabel("Step")

        plt.tight_layout()
        plt.show()
###### END MAIN ######