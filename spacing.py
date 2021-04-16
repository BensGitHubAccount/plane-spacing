import numpy as np
from scipy.spatial import distance

# optimally place people in aircraft so they are maxmimally apart

def create_state_space(orders, num_bus_rows=5,
                             num_prem_rows=5, num_econ_rows=20):
    '''
    Creates state space from list of orders. 
    The first dimension of the state space represents class (business, premium, econ)
    The second dimension represents seat type (windows, middle, aisle)
    The third dimension represents row num (row A, B, C, ...)
        The first half of the third row represents the left side of the plane
        while the second half is the right side of the plane

    Args:
        orders: list of tuples
    
    Returns:
        state space matrix
    '''    
    # 5 business rows
    # 5 premium rows
    # 20 economy rows
    state_space = [[[0]*2*num_bus_rows, [0]*2*num_bus_rows, [0]*2*num_bus_rows],
               [[0]*2*num_prem_rows, [0]*2*num_prem_rows, [0]*2*num_prem_rows],
               [[0]*2*num_econ_rows, [0]*2*num_econ_rows, [0]*2*num_econ_rows],]
    for o in orders:
        for i in range(len(state_space[o[0]][o[1]])):
            if state_space[o[0]][o[1]][i] == 0: # this should be a while loop
                state_space[o[0]][o[1]][i] = 1
                break
    return state_space

def perm_state_space(state_space):
    '''
    Randomly permutates the state space.
    Taken seats are represented by 1's while empty seats are 0's

    Args:
        state_space:

    Returns:
        randomly permutated state space
    '''
    perm_ss = []
    for cl in state_space:
        new_row = []
        for row in cl:
            new_row.append(list(np.random.permutation(row)))
        perm_ss.append(new_row)
    return perm_ss

def state_space_to_plane(state_space, num_bus_rows=5,
                             num_prem_rows=5, num_econ_rows=20):
    '''
    Converts the state space to a matrix representing taken seats in a plane.
    Used for calculating distance as well as visual inspection of state space. 

    Args:
        state_space: 3D matrix of taken seats
    
    Returns
        2D representation of plane
    '''    
    # 5 business rows
    # 5 premium rows
    # 20 economy rows
    #_+______________
    # 30 total rows
    total_rows = num_bus_rows + num_prem_rows + num_econ_rows
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

def get_total_distance(ri, ci, plane):
    '''
    Returns distance score between two patrons.
    Euclidian distance wasn't a good measure.
    By using the log of the distance, it means that the algorithm
    focuses on keeping people at least a few seats apart.
    Without this, it would put everyone in the corners.  

    Args:
        ri: row index of current passenger
        ci: column index of current passenger
        plane: 2D matrix of plane

    Returns:
        sum of log distances for one passenger to all other passengers
    '''
    total = 0
    for r in range(plane.shape[0]):
        for c in range(plane.shape[1]):
            if plane[r, c] == 1 and (r, c) != (ri, ci):
                total += np.log(distance.euclidean((r, c), (ri, ci)))/np.log(100)
    return total
        
def get_plane_score(plane):
    '''
    Returns total distance score of plane.
    The greater the score the more distance between patrons.

    Args:
        plane: 2d matrix of plane, 0's representing empty seats

    Returns:
        total distance score of plane
    '''
    total = 0
    for r in range(plane.shape[0]):
        for c in range(plane.shape[1]):
            if plane[r, c] == 1:
                total += get_total_distance(r, c, plane)
    return total

def get_orders_txt(file_path):
    '''
    Converts text file of orders to a list of tuples.

    Args:
        file_path: filepath to orders text file
    
    Returns
        list of tuples representing order selections
    '''
    orders = []
    with open(file_path, 'r') as file:
        for line in file:
            orders.append([int(x) for x in line.split(',')])
    return orders

if __name__ == '__main__':
        
    orders = get_orders_txt('orders.txt')
    ss = create_state_space(orders)

    # now find best layout
    num_iters = 100
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
    print(best_score)