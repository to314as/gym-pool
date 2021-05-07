import numpy as np
import gym_pool.envs.gamestate_angle as gamestate
import gym_pool.envs.collisions as collisons
import gym_pool.envs.event as event
import gym
from gym import error, spaces
from gym import utils as gym_utils
from gym.utils import seeding
import logging


class ActionSpace:
    def __init__(self, ranges):
        self.ranges = ranges
        self.buckets = None
        self.is_discrete = False

    @property
    def n(self):
        if self.is_discrete:
            return self.buckets
        else:
            return len(self.ranges)

    def set_buckets(self, buckets):
        self.buckets = buckets
        self.is_discrete = True

    def sample(self):
        if self.is_discrete:
            return [np.random.choice(bucket) for bucket in self.buckets]
        else:
            return [np.random.rand() * (mx - mn) + mn for mn, mx in self.ranges]

    def get_action(self, action):
        if self.is_discrete:
            real_action = []
            #print('no', action)
            # Map discrete buckets to continuous values
            #print(action)
            for i, a in enumerate(action):
                bucket = self.buckets[i]
                l, u = self.ranges[i]

                v = (a / bucket) * (u - l) + l
                real_action.append(v)
            #print('after', real_action)
            return real_action
        else:
            return action

    def encode(self, action):
        """
        Deprecated.
        """
        t = 1
        encoded_action = 0
        for i, a in enumerate(action):
            encoded_action += t * a
            t *= self.buckets[i]
        return encoded_action

    def decode(self, action):
        """
        Deprecated.
        """
        decoded_action = []
        for bucket in self.buckets:
            decoded_action.append(action % bucket)
            action //= bucket
        return decoded_action

class StateSpace:
    def __init__(self, m, size):
        self.states=7
        self.m = m
        self.w = size[0]
        self.h = size[1]
        diagonal=np.sqrt(self.w**2+self.h**2)
        self.buckets = None
        self.bin_limits = np.array([[[(0,1)]for j in range(self.states)]for i in range(self.m-1)]).reshape((self.m-1)*self.states,2)
        self.num_bins = tuple(np.array([[32] for i in range((self.m-1)*self.states)]).flatten())
        self.is_discrete = False

    @property
    def n(self):
        if self.is_discrete:
            return self.num_bins
        else:
            return (self.m-1)*self.states

    def set_buckets(self, buckets):
        self.buckets = self.num_bins
        self.is_discrete = True

    def sample(self):
        if self.is_discrete:
            return np.random.choice(self.n)
        else:
            return [(np.random.rand() * self.w, np.random.rand() * self.h) for _ in range(self.m)]

    def get_discrete_state(self,state):
        #print(state)
        #print(self.num_bins)
        #print(self.bin_limits)
        #print(state)
        ratios = [(state[i] + abs(self.bin_limits[i][0])) / (self.bin_limits[i][1] - self.bin_limits[i][0]) for i in range(len(state))]
        #print("Ratios:",ratios)
        s = [int(round((self.num_bins[i] - 1) * ratios[i])) for i in range(len(state))]
        s = [min(self.num_bins[i] - 1, max(0, s[i])) for i in range(len(s))]
        return tuple(s)

    def get_state(self, observation):
        #print(observation)
        observation=np.asarray(observation, dtype=np.float64)
        if not self.is_discrete:
            #observation = np.asarray(observation, dtype=np.float64)
            return observation
        else:
            ds=self.get_discrete_state(observation)
            #print(ds)
            #state = [(0, 0)] * len(observation)
            #bucket_x, bucket_y = self.buckets
            #lx, ux = 0, self.w
            #ly, uy = 0, self.h

            # Map continuous values to discrete buckets
            #for i, (x, y) in enumerate(observation):
            #    sx = 0 if x <= lx else (bucket_x - 1 if x >= ux else int(((x - lx) / (ux - lx) * bucket_x)))
            #    sy = 0 if y <= ly else (bucket_y - 1 if y >= uy else int(((y - ly) / (uy - ly) * bucket_y)))

             #   state[i] = (sx, sy)

            # Encode state into consecutive state space
            #unit_size = bucket_x * bucket_y
            #encoded_state = 0
            #for i, (sx, sy) in enumerate(state):
            #    encoded_state += (sy * bucket_y + sx) * (unit_size ** i)

            return ds

class PoolEnvAng(gym.Env, gym_utils.EzPickle):
    def __init__(self, num_balls=2, visualize=False, single = True):
        self.num_balls = num_balls
        self.visualize = visualize
        self.singlePlayer = single

        # Two actions: angle, force
        # In the range of `ranges` in the game
        self.action_space = ActionSpace([(0, 1), (0, 1)])

        # State: a list of `m` ball (x,y) coordinates
        # Representing a table of (w, h) size
        self.state_space = StateSpace(num_balls, [1000, 1000])

        # Reward
        self.ball_in_reward = 500
        self.white_ball_punishment = -5
        self.no_ball_punishment = -1
        self.hole_distance = 100#3
        self.occlusion = 1
        self.eight_ball_punishment = 0

        # Init
        self.current_obs = None
        self.current_state = None
        self.gamestate = None
        self.reset()

    @property
    def max_reward(self):
        # Small bug here, should be (self.num_balls - 1) * self.ball_in_reward, but doesn't matter
        return self.num_balls * self.ball_in_reward

    @property
    def min_reward(self):
        return self.no_collision_penalty

    def set_buckets(self, action=None, state=None):
        if action is not None:
            self.action_space.set_buckets(action)
        if state is not None:
            self.state_space.set_buckets(state)

    def reset(self):
        self.gamestate = gamestate.GameState(self.num_balls, self.visualize, self.singlePlayer)
        self.current_obs = self.gamestate.return_ball_state_dict()
        self.current_state = self.state_space.get_state(self.current_obs)/self.state_space.bin_limits[:,1]
        return self.current_state

    def step(self, action):
        real_action = self.action_space.get_action(action) # deal with discretized action
        game = self.gamestate
        ball_pos, holes_in, collision_count, white_in, eight_in, smallest_distance, total_distance, done = game.step(game, real_action[0],real_action[1])
        full_state=ball_pos#/self.state_space.bin_limits[:,1]
        self.current_state = self.state_space.get_state(full_state)
        reward = self.ball_in_reward * holes_in + self.no_ball_punishment * collision_count + self.white_ball_punishment * white_in + self.eight_ball_punishment * eight_in + smallest_distance * self.hole_distance + total_distance * self.hole_distance
        #print("current state:",self.current_state)
        return self.current_state, reward, done
