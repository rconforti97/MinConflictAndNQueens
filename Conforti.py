# =============================================================================
# Rachel Conforti - Project: Local Search NQueens
# =============================================================================

import random, time

class NQueens():
    
    def __init__(self, size):
        # Make it create a board
        self.size = size
        self.board = []
        
        # Automatically creates a random board everytime you create a NQueens object
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append('_')
            self.board.append(row)
            # randomly pick and place a queen
            random_queen = int(random.random() * self.size) - 1
            self.board[i][random_queen] = 'Q'
            
        self.print_board('I')
    
    # iterate through the size and print it out 
    def print_board(self, option):
        #  print either inital or final board above the board
        if option == ('I'):
            print('Initial board:')
        else:
            print('\nFinal board:')
        
        for i in range(self.size):
            # this create the board into the rows
            if i != 0:
                print("")
            # This prints out the value
            for j in range(self.size):
                print('{0}  '.format(self.board[i][j]), end = '')
        print("")
    
    
    # swaps the locations
    def swap_positions(self, x_1, y_1, x_2, y_2):
        self.board[x_1][y_1] = ('_')
        self.board[x_2][y_2] = ('Q')

            
    # This is checking if there are any conflicts in the board with the queen
    def num_of_conflicts(self, board_position):
        board_x, board_y = board_position
        num_of_conflicts = 0
        
        # the first four are the diagional, the next two are doing the row checks,
        # and the last two are the column checks 
        direcitons = [(1,1), (1, -1), (-1, 1), (-1, -1), (1,0), (-1, 0), (0, -1), (0,1)]
        
        # For each option in the directions I will save them 
        for d in direcitons: 
            # hold a value in the list like 1,1 | 1, -1 | -1, 1| etc...
            d_x, d_y = d
            # Since adding the board value itself messes it up, I used these
            new_x, new_y = board_x, board_y
            
            while True:
                # add the directions to the current board position to test it out
                # this resets everytime
                new_x += d_x
                new_y += d_y
                
                # checking to make sure its in the size of board 
                if abs(new_x) >= self.size or abs(new_y) >= self.size or new_x < 0 or new_y < 0:
                    break
                
                # if theres a Queen there then its a conflict!
                if self.board[new_x][new_y] == ('Q'):
                    num_of_conflicts += 1
        
        return num_of_conflicts
        

    def min_conflict(self, max_steps=100000):
        steps = 0
        
        for i in range(max_steps):
            # dictionary to hold conflicts 
            conflicted = {}
            
            # list to hold the positions that need to be tie broken 
            new_pos = []
            
            for i in range(self.size):
                for j in range(self.size):
                    # this is so we can get the position in the board and check for conflicts
                    if(self.board[i][j] == 'Q' and self.num_of_conflicts((i, j)) != 0):
                        # equal to zero because the value of the pair is not important here
                        conflicted[(i, j)] = 0
                        
            # checking if current_state is a solution of csp
            if len(conflicted) == 0:
                 break
             
            # getting the randomly chosen variable from the set of conflicted variables
            var_x, var_y = random.choice(list(conflicted))
            
            # empty out put the dictionary 
            conflicted.clear()
            
            # this finds the conflicts with the random value and c
            for c in range(self.size):
                conflicted[(var_x, c)] = self.num_of_conflicts((var_x, c))
                
            # Sort the dictionary by smallest value to largest value 
            sorted_conflicted = dict(sorted(conflicted.items(), key = lambda x: x[1]))
            
            # save the minimum conflict value to min_value by grabbing the
            # lowest value in the SORTED dictionary 
            min_value = next(iter((sorted_conflicted.items())))[1]
    
            # This will search the whole dirctionary and save the lowest
            # min values to a list. Because we sorted the dicionary by min
            # value it is just gathering lowest values that need a tie broken
            # The elif statement is there because this can quickly get us into
            # a local minima so adding a random location can help get us out of 
            # it. It is randomly generating a number between 0 and 1 and if its
            # less then 0.1 it will be added 
            for key, v in sorted_conflicted.items():
                if v == min_value:
                    new_pos.append(key)
                elif (random.random() < 0.1):
                    new_pos.append(key)
                    
            # If there is only 1 option in the list it will "randomly" choose it
            # if there are more then one option this is breaking the time randomly
            new_x, new_y = random.choice(new_pos)
            
            # Swap the positions 
            self.swap_positions(var_x, var_y, new_x, new_y)
            
            # add one to the step counter
            steps +=1
            
        # If my program is unsuccessful, it will print how many attempts it made
        if len(conflicted) != 0:
            print("Unable to solve the board in %s steps" %max_steps)
         
        # If my program is succuessful, it will print the following
        else:
            self.print_board('F')
            print('Total Steps:', steps)
            
        return steps
    
def main():
    # so I can time my program
    total_time = 0
    for t in range(50):
        print("====================================")
        start_time = time.time()
        # creating the NQueens object that creates the random board
        queen = NQueens(8)
        # solves the board 
        steps = queen.min_conflict()
        # prints the time
        program_time = time.time() - start_time
        print("Total run time: %s seconds" % program_time)
        total_time += program_time
        steps += steps 
    
    t += 1
    average_steps = steps  / t 
    average_time = total_time / t
    
    print("\n**************************************")
    print('The average time for the %s boards: ' %t, average_time)
    print('\nThe average steps for the %s boards: ' %t, average_steps)
    print("**************************************")
        

if __name__ == '__main__':
    main()