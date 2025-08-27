###### agent.py ######
# -> here is the structure for the agent

###### IMPORTS ######
from imports import *
###### END IMPORTS ######

###### AGENT ######
class Agent_Q_Learning:
        def __init__(
                      self,
                      env: gym.Env,
                      learning_rate: float,
                      initial_epsilon: float,
                      epsilon_decay: float,
                      final_epsilon: float,
                      discount_factor: float,  
        ):
                self.env = env
                self.q_values = defaultdict(lambda: np.zeros(env.action_space[0].n))
                self.learning_rate = learning_rate
                self.discount_factor = discount_factor
                self.epsilon = initial_epsilon
                self.epsilon_decay = epsilon_decay
                self.final_epsilon = final_epsilon
                
        # -> getting the observation as a tuple for future processing
        def _to_key(self, obs: np.ndarray) -> tuple:
                return tuple(obs.astype(np.int8))

        # -> select an action from action space
        # -> it is a must to send the observation as a parameter and BE AN ARRAY!!!!
        # -> it is also a must to return an action else it will not work!!!!
        # -> this is an epsilon greedy inspired algorithm
        def get_action(self, obs: np.ndarray) -> int:
                obs_key = self._to_key(obs)
                # -> exploring randomly
                if np.random.random() < self.epsilon:
                        return int(self.env.action_space.spaces[0].sample())
                # -> else go for the greedy action
                return int(np.argmax(self.q_values[obs_key]))
        
        # -> update the state of the agent after executing an action
        # -> it is a must to sent as parameters observation, action, reward, terminated and next observation
        def update(
                self,
                obs: np.ndarray,
                action: int,
                reward: float,
                terminated: bool,
                next_obs: np.ndarray,
        ):
                observation = tuple(obs.astype(np.int8))
                next_observation = tuple(next_obs.astype(np.int8))

                future_q_value = (not terminated) * np.max(self.q_values[next_observation])
                target = reward + self.discount_factor * future_q_value
                td_error = target - self.q_values[observation][action]

                self.q_values[observation][action] += self.learning_rate * td_error
        
        # -> it's a function that makes the agent less explorative and more conversative 
        # (the epsilon is decreased by epsilon decay parameter)
        def decay_epsilon(self):
                self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)
###### END AGENT ######
                