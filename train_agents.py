###### IMPORTS ######
from imports import *
from process_game import *
from global_variables import *
from agent_q_learning import *
from agent_sarsa import *
###### END IMPORTS ######

def train(env, gui, n_episodes, agent_1, agent_2):

        total_reward = 0
        reward_p1 = 0
        reward_p2 = 0
        total_reward_p1 = 0
        total_reward_p2 = 0
        draws =  0

        for episode in tqdm(range(n_episodes)):
                observation, _ = env.reset()
                gui.reset(total_reward_p1, total_reward_p2, episode)

                done = terminated = truncated = False
                action_2 = None

                while not done:
                        monitor.acquire()
                        round_done.clear()
                        count = 0
                        time.sleep(0.1)

                        for i in range(3):
                                for j in range(3):
                                        if action_table[i][j] != 0: count += 1

                        if count % 2 == 1 and count != 9:
                                round_done.set()
                                monitor.release()
                                break
                        
                        if count == 8 and line_winner['line'] == "none":
                                try:
                                        action_1 = np.where(np.array(observation) == 0)[0][0]
                                except:
                                        monitor.release()
                                        break
                                actions_p['actions_p1'][action_1] += 1
                                gui.update("X", gui._action[action_1])

                        if count < 8 and line_winner['line'] == "none":
                                action_1 = agent_1.get_action(observation)
                                while observation[action_1] != 0:
                                        action_1 = agent_1.get_action(observation)
                                actions_p['actions_p1'][action_1] += 1

                                next_action_2 = agent_2.get_action(observation)
                                while observation[next_action_2] != 0 or action_1 == next_action_2:
                                        next_action_2 = agent_2.get_action(observation)
                                actions_p['actions_p2'][action_2] += 1

                                if action_2 is None:
                                        action_2 = next_action_2
                                
                                gui.update("X", gui._action[action_1])
                                gui.update("O", gui._action[next_action_2])

                        next_observation, reward, terminated, truncated, _ = env.step(action = (int(action_1), int(next_action_2)))

                        if reward != 0:
                                reward_p1 = 1 if reward == X_SIGN else -1
                                reward_p2 = 1 if reward == O_SIGN else -1
                                total_reward_p1 += reward_p1 if reward_p1 > 0 else 0
                                total_reward_p2 += reward_p2 if reward_p2 > 0 else 0
                        else:
                                reward_p1 = 0
                                reward_p2 = 0
                
                        agent_1.update(observation, action_1, reward_p1, terminated, next_observation)
                        agent_2.update(observation, action_2, reward_p2, terminated, next_action_2, next_observation)

                        done = terminated or truncated or count == 9
                        
                        if done:
                                if not line_winner['line'] == "none":
                                        gui.winner(gui._winner_lines[line_winner['line']], reward)
                                        round_done.set()
                                        time.sleep(0.1)
                                else:
                                        draws += 1                     
                                        round_done.set()
                                        time.sleep(0.1)
                                        
                        observation = next_observation
                        action_2 = next_action_2
                        p1_win.clear()
                        p2_win.clear()
                        monitor.release()

                draw_vector.append(draws)
                reward_vector_p1.append(total_reward_p1)
                reward_vector_p2.append(total_reward_p2)
                lost_rounds.append((episode - (total_reward_p1 + total_reward_p2 + draws)) > 0)
                total_reward += reward
                epsilon_values[0].append(agent_1.epsilon)
                epsilon_values[1].append(agent_2.epsilon)
                agent_1.decay_epsilon()
                agent_2.decay_epsilon()
        
        game_finished.set()