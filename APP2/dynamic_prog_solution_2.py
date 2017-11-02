
global cache
cache = {} # We use a hashmap-like collection to store a association between our problem object, and is composition

class Problem:
	def __init__(self, problem, precom=0):
		self.computed = precom # This attribute contain the score that the best subproblems will lead to. Is initilaised with the card value
		self.subpath = None # The path you have to go through to get this score
		self.choice = None
		self.board = problem
		
		self.left, self.right = None, None
		
	def id(self): # This method is used to identifie
		return ",".join([str(c) for c in self.board])
		
		
def pathfinder(problem, is_dog_first):
	if problem.id() not in cache.keys(): # Is it the first time we meet such a problem ?
		if len(problem.board) > 2:
			subproblem = problem.board
			if is_dog_first: # If the opponent plays first, then we just shrink our problem
				subproblem = subproblem[1:] if max(subproblem[0], subproblem[-1]) == subproblem[0] else subproblem[:-1]
				
			problem.left = Problem(subproblem[1:], subproblem[0])
			if not is_dog_first: # If the opponent plays second, then we have to skrink this subproblem...
				problem.left.board = problem.left.board[1:] if max(problem.left.board[0], problem.left.board[-1]) == problem.left.board[0] else problem.left.board[:-1]
			problem.left = pathfinder(problem.left, is_dog_first)
				
			
			problem.right = Problem(subproblem[:-1], subproblem[-1])
			if not is_dog_first: # ... and this one
				problem.right.board = problem.right.board[1:] if max(problem.right.board[0], problem.right.board[-1]) == problem.right.board[0] else problem.right.board[:-1]		
			problem.right = pathfinder(problem.right, is_dog_first)
			
			problem.computed += max(problem.left.computed, problem.right.computed) # we had to our precomputed value, the score of the best subsolution
			problem.choice = 'L' if max(problem.left.computed, problem.right.computed) == problem.left.computed else 'R' # and we store the action that has to be done to reach this problem
			problem.subpath = problem.choice + (problem.left.subpath if max(problem.left.computed, problem.right.computed) == problem.left.computed else problem.right.subpath)
			problem.left, problem.right = None, None # we delete the subproblems as we gathered the information to the current problem
						
		else:
			# Same than for a node, except that we only care about the local data
			problem.choice = 'L' if max(problem.board) == problem.board[0] else 'R'
			problem.subpath = str(problem.choice)
			problem.computed += max(problem.board)		
		
		# We save it in our cache
		cache[problem.id()] = problem	
	
		return problem
	else:
		# We take it from our cache
		return cache[problem.id()]
		
		
# The code below is used to simulate
board = [int(c) for c in raw_input("Board ? ").split(" ")]
tot = sum(board)
		
board = Problem(board)
pathfinder(board, raw_input("Does the oppenent start? ")[0].lower() == "y")
print("The board has %d points" % tot)
for c in board.subpath:
	print("Take the left card" if c == "L" else "Take the right card")
	raw_input()
	
print("... and you should %s with %d points" % ("win" if board.computed > tot/2 else ("lose" if float(board.computed) < float(tot/2) else "draw"), board.computed))


