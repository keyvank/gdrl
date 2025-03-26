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


Q = {i: {act: 0.0 for act in [LEFT, RIGHT]} for i in range(9)}
eps = 0.1


def select_action(state, eps):
    if random.random() < eps:
        return random.choice([LEFT, RIGHT])
    if Q[state][RIGHT] > Q[state][LEFT]:
        return RIGHT
    else:
        return LEFT


alpha = 0.1
gamma = 1.0
for ep in range(5000):
    s = State()
    prev_act = select_action(s.s, 0.1)
    prev_s = s.s
    (reward, done) = s.action(prev_act)
    while not done:
        new_act = select_action(s.s, 0.1)
        (reward, done) = s.action(new_act)
        new_s = s.s
        td_target = reward + gamma * Q[new_s][new_act] * (not done)
        td_err = td_target - Q[prev_s][prev_act]
        Q[prev_s][prev_act] += alpha * td_err
        prev_act = new_act
        prev_s = new_s

print(Q)
