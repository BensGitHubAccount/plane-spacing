from spacing import (get_orders_txt,
                    create_state_space, perm_state_space,
                    state_space_to_plane, get_plane_score)
import numpy as np
import pandas as pd
import seaborn as sns
# find the number of iterations until the max score is found
# to find the estimated required number of iterations
num_tests = 100
tests = {}
opt_index = []

orders = get_orders_txt('orders.txt')
ss = create_state_space(orders)    
for i in range(num_tests):
    # now find best layout
    num_iters = 1000
    scores = []
    planes = []
    for j in range(num_iters):
        perm_ss = perm_state_space(ss)
        plane = state_space_to_plane(perm_ss)
        planes.append(plane)
        scores.append(get_plane_score(plane))

    best = np.argmax(scores)
    best_plane = planes[best]
    best_score = scores[best]
    print(f"iter {i}: score {best_score} found at {best}")
    opt_index.append(best)
    tests[i] = [best_plane, best_score]




sns.histplot(data=opt_index, kde=True)
# interesting, it is nearly uniform
# what does this mean ?? that I didn't run it enough times? 

all_scores = [t[1][1] for t in tests.items()]
sns.histplot(data=all_scores, kde=True)
np.mean(all_scores)
np.std(all_scores)
# seems to be almost normal with mean 2143 & sd 8

sns.scatterplot(x=opt_index, y=all_scores)
# this doesn't really tell me anything new
# other that the optimal score can be found at any time

# lets look at a single search

# lets create rolling max to see when it gets updated








