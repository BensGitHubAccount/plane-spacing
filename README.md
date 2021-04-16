# Plane Spacing

## Background

This past week I bought a plane ticket for the first time in a year. After purchasing a ticket I was asked to choose my seat as usual. After trying to find the optimally distanced seat, I thought there had ot be a better way let people choose the type of seat they want and then assign seats based on distance.

## The Solution
Customers are allowed to choose from 3 classes (business, premium, or economy) and 3 types of seats (window, aisle, or middle). These options can be changed and configured with minimal effort. The algorithm could even be configure for other vehicles like busses or planes.

## Assumptions
- There is currently no way for two or more passengers to choose to sit next to each other. This could be done manually or implemented in the algorithm.
- Order types aren't overbooked. This could be added easily with come checks but for now I'll assume the front end does that.

## Future Improvements
- Optimize the search
  - At the moment, the search is random. There may a way to search in the right direction. I will study this.
- Better distance calculations
  - horizontal space is further than vertical space
    - b/c sitting in front is better than beside
- Add in distance calculation for aisle

## To Do
- now just need to do some examples and put on github
- also should write more comments
- make bencraver.com/github redirect to my github account
- https://google.github.io/styleguide/pyguide.html
- explanation of state space shape

### To Done
- do some meta analysis on number of iterations needed to find best_plane
  - could see how this changes when the number of passengers increases
- total_rows and num_bus_row calculations inside of functions

## Sample order list
# users can purchase windows, middle, or aisle seat
orders = []
order1 = (0,0) # bus class and window seat
order2 = (0,1) # bus class and middle seat
order3 = (0,2) # bus class and aisle seat

order4 = (2,0) # econ class and window seat
order5 = (2,1) # econ class and middle seat
order6 = (2,2) # econ class and aisle seat

# aircraft is single aisle, w/ 30 rows and 6 seats per row
seats = np.zeros((30,7)) # 30 rows x (6 seats + isle)

num_bus_rows = 5 # 5 business rows
num_prem_rows = 5 # 5 premium rows
num_econ_rows = 20 # 20 economy rows
total_rows = num_bus_rows + num_prem_rows + num_econ_rows

state_space = [[[0]*2*num_bus_rows, [0]*2*num_bus_rows, [0]*2*num_bus_rows],
               [[0]*2*num_prem_rows, [0]*2*num_prem_rows, [0]*2*num_prem_rows],
               [[0]*2*num_econ_rows, [0]*2*num_econ_rows, [0]*2*num_econ_rows],]
