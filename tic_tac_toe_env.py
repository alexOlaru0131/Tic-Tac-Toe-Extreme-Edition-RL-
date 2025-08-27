###### tic_tac_toe_end.py ######
# -> the environment for the model
# -> it is built from the Gymnasium library provided by OpenAI (see comments in the code for explanations)

###### IMPORTS ######
from imports import *
from global_variables import *
###### END IMPORTS ######

###### ENVIRONMENT CLASS ######
class TicTacToe(gym.Env):
        def __init__(self):

                # -> action space it's where you describe the argument (count) of the possible actions
                self.action_space = spaces.Tuple((
                        # -> 9 possible actions for the player 1
                        spaces.Discrete(9),
                        # -> 9 possible actions for the player 2
                        spaces.Discrete(9),
                ))
                
                # -> the game table as a matrix (for init all cells are 0)
                self.action_table = np.zeros([3, 3], dtype = np.int8)

                # -> observation space for agents
                # -> maximum value on table = 1 (action from player 1), lowest value on table = -1 (action from player 2)
                self.observation_space = gym.spaces.Box(
                        low = -1,
                        high = 1,
                        shape = (9,),
                        dtype = np.int8
                )

                # -> possible actions
                # -> each action represents a placement of a X or O on the table in the coordinates corresponding to the action index
                self._action = {
                        0: (0, 0),
                        1: (0, 1),
                        2: (0, 2),
                        3: (1, 0),
                        4: (1, 1),
                        5: (1, 2),
                        6: (2, 0),
                        7: (2, 1),
                        8: (2, 2),
                }

        # -> function that returns the observation space (action table) as an array
        def _get_obs(self):
                return self.action_table.flatten()\
                                        .copy()
        
        # -> this function resets the environment, in our case the action table has all cells reset to 0
        # -> in order for it to work we need to return observation, info !!!!! 
        # (otherwise the library won't manage it well - it is a must)
        # -> input parameters must be the same
        def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
                super().reset(seed = seed)

                self.action_table = np.zeros([3, 3])

                observation = self._get_obs()

                # -> return observation, info
                return observation, {}
        
        # -> this functions iterates through states and actions and provides rewards after each iteration
        # -> in order for it to work we need to return observation, reward, terminated, truncated, info !!!!!
        # (otherwise the library won't manage it well - it is a must)
        ## FIND HOW TO MAKE IT WORK WITH A TUPLE
        # -> if you return more parameters as a tuple, array or anything else it might be unstable
        # -> input parameters must be the same, be careful when giving a tuple as an argument (in my case I mapped my input to ints and shared it)
        def step(self, action):

                action_p1, action_p2 = map(int, action)

                pos1 = self._action[action_p1]
                pos2 = self._action[action_p2]
                reward = 0
                truncated = False
                terminated = False

                if self.action_table[pos1] == 0:
                        self.action_table[pos1] = X_SIGN
                if self.action_table[pos2] == 0:
                        self.action_table[pos2] = O_SIGN
                
                # -> if there is a winner end the game
                if p1_win.is_set():
                        terminated = True
                        reward = X_SIGN
                        p1_win.clear()

                elif p2_win.is_set():
                        terminated = True
                        reward = O_SIGN
                        p2_win.clear()

                else:
                        reward = 0

                # -> if the number of turns is too much end the simulation
                ## FINISH OR FIND OUT IF IT UPDATES
                truncated = False
                
                obs = self._get_obs()

                # -> return observation, reward, terminated, truncated, info
                return obs, reward, terminated, truncated, {}
###### END ENVIRONMENT CLASS ######

###### REGISTER ENVIRONMENT ######
register (
        id = "TicTacToe",
        entry_point="main:TicTacToe",
        max_episode_steps = 100_000_000,
)
###### END REGISTER ENVIRONMENT ######