import random
import copy

class ACOSudokuSolver:
    def __init__(self, alpha=1, beta=2, evaporation_rate=0.3, num_ants=20, max_iterations=200):
        self.alpha = alpha  # Pheromone importance
        self.beta = beta    # Heuristic importance
        self.evaporation_rate = evaporation_rate
        self.num_ants = num_ants
        self.max_iterations = max_iterations

        # Initialize pheromone levels (9x9x9 grid)
        self.pheromones = [[[1.0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
        print(f"Initialized ACO solver with alpha={alpha}, beta={beta}, evaporation_rate={evaporation_rate}, "
              f"num_ants={num_ants}, max_iterations={max_iterations}")

    def calculate_fitness(self, row, col, grid):
        """Calculate probabilities for numbers 1-9 for a specific cell."""
        print(f"Calculating fitness for cell ({row}, {col})")
        probabilities = []
        for num in range(1, 10):
            if self.is_valid_placement(grid, row, col, num):
                pheromone = self.pheromones[row][col][num - 1] ** self.alpha
                heuristic = self.heuristic_value(grid, row, col, num) ** self.beta
                probabilities.append(pheromone * heuristic)
            else:
                probabilities.append(0)

        total = sum(probabilities)
        if total == 0:
            print(f"Warning: All probabilities are zero at ({row}, {col}).")
            return [0] * 9  # All probabilities are zero, no valid numbers
        print(f"Probabilities for cell ({row}, {col}): {probabilities}")
        return [p / total for p in probabilities]

    def heuristic_value(self, grid, row, col, num):
        """Prioritize cells with fewer valid options."""
        possible_values = [n for n in range(1, 10) if self.is_valid_placement(grid, row, col, n)]
        return len(possible_values)  # Minimize the number of possibilities

    def is_valid_placement(self, grid, row, col, num):
        """Check if placing a number in a cell is valid according to Sudoku rules."""
        # Check row and column
        if num in grid[row] or num in [grid[r][col] for r in range(9)]:
            return False
        # Check 3x3 subgrid
        subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(subgrid_row, subgrid_row + 3):
            for c in range(subgrid_col, subgrid_col + 3):
                if grid[r][c] == num:
                    return False
        return True

    def solve(self, grid):
        """Solve the Sudoku puzzle using ACO."""
        best_solution = None
        best_score = float('-inf')
        print("Starting ACO solver...")

        for iteration in range(self.max_iterations):
            print(f"Iteration {iteration + 1}/{self.max_iterations}")
            for ant in range(self.num_ants):
                print(f"Ant {ant + 1}/{self.num_ants}")
                # Create a copy of the grid for this ant
                grid_copy = copy.deepcopy(grid)
                success = self.ant_traverse(grid_copy)
                if success:
                    score = self.evaluate_grid(grid_copy)
                    if score > best_score:
                        best_score = score
                        best_solution = grid_copy

            # Update pheromones
            self.evaporate_pheromones()
            self.deposit_pheromones(best_solution)

        print("ACO solver finished.")
        return best_solution

    def ant_traverse(self, grid):
        """Simulate an ant filling the Sudoku grid."""
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:  # Empty cell
                    probabilities = self.calculate_fitness(row, col, grid)
                    if sum(probabilities) == 0:
                        print(f"Error: All probabilities are zero at ({row}, {col}). Trying a random choice...")
                        # Try a random number in this case (for backtracking)
                        num = random.randint(1, 9)
                        grid[row][col] = num
                    else:
                        # Select a number based on probabilities
                        num = random.choices(range(1, 10), probabilities)[0]
                        grid[row][col] = num
        return True

    def evaluate_grid(self, grid):
        """Evaluate the quality of a completed grid."""
        score = 0
        # Reward for correctly filled rows, columns, and subgrids
        for row in grid:
            score += len(set(row))  # Maximize unique numbers in rows
        for col in range(9):
            score += len(set(grid[row][col] for row in range(9)))  # Columns
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                subgrid = [grid[x][y] for x in range(r, r + 3) for y in range(c, c + 3)]
                score += len(set(subgrid))  # Subgrid
        print(f"Evaluating grid score: {score}")
        return score

    def evaporate_pheromones(self):
        """Evaporate pheromones."""
        print("Evaporating pheromones...")
        for row in range(9):
            for col in range(9):
                for num in range(9):
                    self.pheromones[row][col][num] *= (1 - self.evaporation_rate)
                    # Apply a minimum threshold to avoid pheromone decay to zero
                    self.pheromones[row][col][num] = max(self.pheromones[row][col][num], 0.1)

    def deposit_pheromones(self, grid):
        """Deposit pheromones on a solution."""
        if grid:
            print("Depositing pheromones...")
            for row in range(9):
                for col in range(9):
                    num = grid[row][col]
                    if num != 0:
                        self.pheromones[row][col][num - 1] += 1


