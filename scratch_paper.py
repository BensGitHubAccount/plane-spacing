import numpy as np
# optimally place people in aircraft so they are maxmimally apart

# pretend aircraft is single aisle, w/ 30 rows and 6 seats per row
seats = np.zeros((30,7)) # 30 rows x (6 seats + isle)

num_bus_rows = 5
num_prem_rows = 5
num_econ_rows = 20
total_rows = num_bus_rows + num_prem_rows + num_econ_rows
# how tf do I define the state space
state_space = [[[0]*2*num_bus_rows, [0]*2*num_bus_rows, [0]*2*num_bus_rows],
               [[0]*2*num_prem_rows, [0]*2*num_prem_rows, [0]*2*num_prem_rows],
               [[0]*2*num_econ_rows, [0]*2*num_econ_rows, [0]*2*num_econ_rows],]

# users can purchase windows, middle, or aisle seat
orders = []
order1 = (0,0) # bus class and window seat
order2 = (0,1) # bus class and middle seat
order3 = (0,2) # bus class and aisle seat

order4 = (2,0) # econ class and window seat
order5 = (2,1) # econ class and middle seat
order6 = (2,2) # econ class and aisle seat

orders = [order1, order2, order3, order4, order5, order6]

for o in orders:
    state_space[o[0]][o[1]][0] = 1
    
# I guess I need to think about the neccessary conditions 
# and then work backwards

# everyone gets their seat 'type' they selected
# can I assume that seats are not oversold?
# this can be handled by the purchasing software so I will

# how tf am I going to differentiate the sides of the plane ?? 
# I need to create a mapping from the list/tuple state space 
# to the distance state space
# this needs to be defined using code for reuseablity
plane = np.zeros((total_rows, 6))
class_num = 0
for cl in state_space: # cl states for class (taken by python)
    # classes are bus/prem/econ
    type_num = 0
    for ty in cl: # ty stands for type (also taken) 
        # types are window/middle/aisle
        seat_num = 0
        for seat in ty:
            if seat == 1:
                if seat_num/2 < len(ty): # left side of the plane
                    plane[class_num+seat_num, ty] = 1
                else:
                    plane[class_num+seat_num, type_num+3] = 1
            seat_num += 1
        type_num +=1
    class_num += seat_num # keep track of how many seats in previous classes
    
# solve a simplified version of the problem
# where no one gets to choose their seats and they're randomly assigned

# two possible ways to go about this are:
# use a genetic algorithm of some sort to assign seats
# or
# using one of the curves that TVs use to increase the density of pixels
# because there are a finite number of seats and depending on the number
# of people booked, the density of seats would change

# the simplest hueristic would be to line all seats up in a line and then
# divide the number of seats by people booked and then skip that many seats
# when assigning
# This would work for people standing in a line but because plane seats
# aren't linear it doesn't work


# anyways

# so I have 3*3=9 types of seats in my initial sample
# this means I have 9 groups, each with their own size of potential 
# spots. How do I start off with an initial condition 

# one assumption I am making is that no one is flying with a child
# or anyone who MUST sit next to them.



# sample distance calcualtion for passenger A1
seats = np.array([   [1, 0],
                     [0, 0],
                     [0, 0],
                     [0, 1],
                     [1, 0],])

dist =np.array([ [0, 2],
                 [1, 3],
                 [2, 4],
                 [3, 5],
                 [4, 6],])



# To Do:
    # write function to calculate total distance
    # write optimization algorithm for assigning 1's to a set of 0's
    # I think the hardest part of all this is that the number of 1's
    # has to always be the same, they're just in different places
    
    # assign seats randomly and then calculate the distance score
    # do this a bunch of times and then spit out the one with the best
    
    # don't worry about optimizing the search now
    # that can come later
    # right now just calcualte the heuristics
    
    # add custom variables for defining horizontal 
    # and verticale distances between seats
    # 
    
    # this could also be applied to trains
    # then it would be nice to be able to choose
    # to be 'close' to someone
    # this could be done by forcing them to purchase
    # two tickets in the same class and then assigning their 
    # seats one after another 
    
    # potential improvements
    # better distance metrics
        # don't let people sit next to one another
    # better 'learning' algos
    
def create_state_space(orders):
    state_space = [[[0]*2*num_bus_rows, [0]*2*num_bus_rows, [0]*2*num_bus_rows],
               [[0]*2*num_prem_rows, [0]*2*num_prem_rows, [0]*2*num_prem_rows],
               [[0]*2*num_econ_rows, [0]*2*num_econ_rows, [0]*2*num_econ_rows],]
    for o in orders:
        for i in range(len(state_space[o[0]][o[1]])):
            if state_space[o[0]][o[1]][i] == 0:
                state_space[o[0]][o[1]][i] = 1
                break
    return state_space

ss = create_state_space(orders)

def perm_state_space(state_space):
    perm_ss = []
    for cl in state_space:
        new_row = []
        for row in cl:
            new_row.append(list(np.random.permutation(row)))
        perm_ss.append(new_row)
    return perm_ss

perm_ss = perm_state_space(ss)

def state_space_to_plane(state_space):
    plane = np.zeros((total_rows, 6))
    class_num = 0
    for cl in state_space: # cl states for class (taken by python)
        # classes are bus/prem/econ
        type_num = 0
        for ty in cl: # ty stands for type (also taken) 
            # types are window/middle/aisle
            seat_num = 0
            for seat in ty:
                if seat == 1:
                    if seat_num < len(ty)/2: # left side of the plane
                        plane[class_num+seat_num, type_num] = 1
                    else:
                        plane[int(class_num+seat_num/2), type_num+3] = 1
                seat_num += 1
            type_num +=1
        class_num += int(seat_num/2)
    return plane

plane = state_space_to_plane(perm_ss)

def calc_distance(dist, seats):
    temp = np.multiply(dist, seats)
    return temp.sum()

# So far I have 
# taken all the orders andadded them to a state space
# randomized that state space
# mapped state space to plane

# now I need to 
# calc score of plane
    # find individual
    # calc each individual score 
        # create distance matrix for individual
        # multiply it and sum
    # sum individual score
from scipy.spatial import distance
 
def get_total_distance(ri, ci):
    total = 0
    for r in range(plane.shape[0]):
        for c in range(plane.shape[1]):
            if plane[r, c] == 1 and (r, c) != (ri, ci):
                # normal distance wasn't best measure
                # could log root base
                # log means that the algo focuses on keeping people at
                # least a few seats apart
                # without this, it would put everyone in the corners
                total += np.log(distance.euclidean((r, c), (ri, ci)))/np.log(100)
    return total
        
def get_plane_score(plane):
    total = 0
    for r in range(plane.shape[0]):
        for c in range(plane.shape[1]):
            if plane[r, c] == 1:
                total += get_total_distance(r, c)
    return total
# print(get_plane_score(plane))

def get_orders_txt(file_path):
    orders = []
    with open(file_path, 'r') as file:
        for line in file:
            orders.append([int(x) for x in line.split(',')])
    # print(orders)
    return orders
orders = get_orders_txt('orders.txt')

# now find best layout
num_iters = 10000
scores = []
planes = []
ss = create_state_space(orders)
for i in range(num_iters):
    perm_ss = perm_state_space(ss)
    plane = state_space_to_plane(perm_ss)
    planes.append(plane)
    scores.append(get_plane_score(plane))

best = np.argmax(scores)
best_plane = planes[best]
best_score = scores[best]

print(best_plane)
# now just need to do some examples and put on github
# also should write a readme
# also should write more comments



# do some meta analysis on number of iterations needed to find best_plane
# could see how this changes when the number of passengers increases
# import orders from text file ?