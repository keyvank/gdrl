import random

LEFT = -1
RIGHT = 1


class State:
    def __init__(self):
        self.s = 4

    def action(self, act):
        if self.s == 8 or self.s == 0:
            return (0, True)
        else:
            rand = random.random()
            if rand < 1 / 2:
                self.s += act
            elif rand > 5 / 6:
                self.s -= act
            if self.s == 8:
                return (1, True)
            elif self.s == 0:
                return (0, True)
            return (0, False)


def policy(state: State):
    return RIGHT


def trajectory(policy, eps=0):
    s = State()
    done = False
    traj = []
    while True:
        act = policy(s)
        if random.random() < eps:
            act = random.choice([LEFT, RIGHT])
        curr = s.s
        (reward, done) = s.action(act)
        nxt = s.s
        traj.append((curr, act, nxt, reward))
        if done:
            return traj
        if len(traj) >= 20:
            traj = []
            s = State()


Q = {i: {act: 0.0 for act in [LEFT, RIGHT]} for i in range(9)}
eps = 0.1
for ep in range(5000):
    visited = set()
    traj = trajectory(policy, eps)
    for i, (prev, act, nxt, rew) in enumerate(traj):
        if (prev, act) in traj:
            continue
        else:
            rest = traj[i:]
            discounted_reward = sum([(0.99**i) * e[3] for i, e in enumerate(rest)])
            alpha = 0.01
            Q[prev][act] += alpha * (discounted_reward - Q[prev][act])
            visited.add((prev, act))

print(Q)
