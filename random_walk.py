import random


class State:
    def __init__(self):
        self.s = 3

    def action(self, act):
        if self.s == 6 or self.s == 0:
            return (0, True)
        else:
            if random.random() < 0.5:
                self.s += 1
            else:
                self.s -= 1
            if self.s == 6:
                return (1, True)
            if self.s == 0:
                return (0, True)
            return (0, False)


def trajectory():
    s = State()
    done = False
    traj = []
    while True:
        act = "L"
        curr = s.s
        (reward, done) = s.action(act)
        nxt = s.s
        traj.append((curr, act, nxt, reward))
        if done:
            return traj
        if len(traj) >= 20:
            traj = []
            s = State()


def monte_carlo(num_episodes=50000, gamma=0.99):
    v = [0 for _ in range(7)]
    for ec in range(num_episodes):
        tr = trajectory()
        visited = [False for _ in range(7)]
        for i, (s, _, _, _) in enumerate(tr):
            if visited[s]:
                continue
            visited[s] = True
            G = sum([(gamma**j) * exp[3] for (j, exp) in enumerate(tr[i:])])
            v[s] = v[s] + (1 / (ec + 1)) * (G - v[s])
    return v


print(monte_carlo())
