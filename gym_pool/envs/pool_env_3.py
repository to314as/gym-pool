import logging
from gym_pool.envs.pool_env import PoolEnv

logger = logging.getLogger(__name__)

class PoolEnv3(PoolEnv):
    """
    SoccerAgainstKeeper initializes the agent most of the way down the
    field with the ball and tasks it with scoring on a keeper.

    Rewards in this task are the same as SoccerEmptyGoal: reward
    is given for kicking the ball close to the goal and extra reward is
    given for scoring a goal.

    """
    def __init__(self):
        super(PoolEnv3, self).__init__(num_balls=4)

    def _configure_environment(self):
        super(PoolEnv3, self).__init__(num_balls=4)
