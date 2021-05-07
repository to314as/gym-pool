import logging
from gym.envs.registration import register
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

logger = logging.getLogger(__name__)

register(
    id='Pool-v0',
    entry_point='gym_pool.envs:PoolEnv'
)

register(
    id='Pool_continuous-v0',
    entry_point='gym_pool.envs:PoolEnvCon'
)

register(
    id='Pool_angle-v0',
    entry_point='gym_pool.envs:PoolEnvAng'
)

register(
    id='Pool3-v0',
    entry_point='gym_pool.envs:PoolEnv3'
)

register(
    id='Pool-v1',
    entry_point='gym_pool.envs:PoolEnvNew'
)

#register(
#    id='SoccerAgainstKeeper-v0',
#    entry_point='gym.envs:SoccerAgainstKeeperEnv',
#    timestep_limit=1000,
#    reward_threshold=8.0,
#    nondeterministic = True,
#)
