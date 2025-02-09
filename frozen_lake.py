# (0,0) (0,1) (0,2) (0,3)
# (1,0) (1,1) (1,2) (1,3)
# (2,0) (2,1) (2,2) (2,3)
# (3,0) (3,1) (3,2) (3,3)


STATES = [(i, j) for i in range(4) for j in range(4)]
GOAL = (3, 3)
TERM = [(1, 1), (1, 3), (2, 3), (3, 0), GOAL]


# Probability of going from src to dst through action
def p(src, dst, act):
    if src in TERM:
        if dst == src:
            return 1
        return 0
    if act == "U":
        exp = (max(0, src[0] - 1), src[1])
        a = (src[0], max(0, src[1] - 1))
        b = (src[0], min(3, src[1] + 1))
    elif act == "D":
        exp = (min(3, src[0] + 1), src[1])
        a = (src[0], max(0, src[1] - 1))
        b = (src[0], min(3, src[1] + 1))
    elif act == "L":
        exp = (src[0], max(0, src[1] - 1))
        a = (max(0, src[0] - 1), src[1])
        b = (min(3, src[0] + 1), src[1])
    elif act == "R":
        exp = (src[0], min(3, src[1] + 1))
        a = (max(0, src[0] - 1), src[1])
        b = (min(3, src[0] + 1), src[1])
    return (int(dst == exp) + int(dst == a) + int(dst == b)) / 3


randomly = [
    ["R", "L", "D", "U"],
    ["L", " ", "R", " "],
    ["U", "D", "U", " "],
    [" ", "R", "D", " "],
]

go_get_it = [
    ["R", "R", "D", "L"],
    ["D", " ", "D", " "],
    ["R", "R", "D", " "],
    [" ", "R", "R", " "],
]

careful = [
    ["L", "U", "U", "U"],
    ["L", " ", "U", " "],
    ["U", "D", "L", " "],
    [" ", "R", "R", " "],
]

adversarial = [
    ["U", "U", "U", "U"],
    ["U", " ", "U", " "],
    ["L", "L", "L", " "],
    [" ", "L", "L", " "],
]
import copy

policy = adversarial
cnt = 0
while True:
    v = {k: 0.0 for k in STATES}
    q = {k: {"L": 0.0, "R": 0.0, "U": 0.0, "D": 0.0} for k in STATES}

    for _ in range(800):
        new_v = dict(v)
        for src in STATES:
            vv = 0
            for dst in STATES:
                move = policy[src[0]][src[1]]
                r = 1 if dst == (3, 3) and src == (3, 2) else 0
                vv += p(src, dst, move) * (r + v[dst])
            new_v[src] = vv
        v = new_v

    for src in STATES:
        for move in ["L", "R", "U", "D"]:
            vv = 0
            for dst in STATES:
                r = 1 if dst == (3, 3) and src == (3, 2) else 0
                vv += p(src, dst, move) * (r + v[dst])
            q[src][move] = vv

    new_policy = copy.deepcopy(policy)
    changed = False
    for k in STATES:
        if k not in TERM:
            policy_move = policy[k[0]][k[1]]
            best_move = "L"
            best_move_val = q[k][best_move]
            for move in ["R", "U", "D"]:
                if q[k][move] > best_move_val:
                    best_move_val = q[k][move]
                    best_move = move
            if best_move != policy_move:
                changed = True
                new_policy[k[0]][k[1]] = best_move
    policy = new_policy
    print("Iter", cnt)
    cnt += 1
    if not changed:
        break

print("Done!")
print(policy)
