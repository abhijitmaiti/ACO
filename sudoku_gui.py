import tkinter as tk
from tkinter import messagebox
import json
import time
import os
from aco_solver import ACOSudokuSolver


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver with ACO")
        self.entries = []

        # Create 9x9 grid of entry boxes
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(root, width=2, font=('Arial', 18), justify='center',
                                 bg="red")  # Default background color
                entry.grid(row=i, column=j, padx=5, pady=5)
                row.append(entry)
            self.entries.append(row)

        # Solve button
        solve_button = tk.Button(root, text="Solve", command=self.solve_puzzle)
        solve_button.grid(row=10, column=0, columnspan=9, pady=10)

        # Label for showing the time taken
        self.time_label = tk.Label(root, text="Time taken: 0.0 seconds", font=('Arial', 12))
        self.time_label.grid(row=12, column=0, columnspan=9, pady=10)

        # Automatically load the puzzle from the JSON file in the current directory
        self.load_puzzle()

    def read_grid(self):
        """Read the Sudoku grid from the GUI."""
        grid = []
        for row in self.entries:
            grid.append([int(entry.get() or 0) for entry in row])
        return grid

    def display_grid(self, grid):
        """Display a Sudoku grid in the GUI."""
        for i in range(9):
            for j in range(9):
                value = grid[i][j]
                entry = self.entries[i][j]
                entry.delete(0, tk.END)
                entry.insert(0, str(value))
                if value != 0:
                    entry.config(bg="green")  # Color filled cells green
                else:
                    entry.config(bg="red")  # Empty cells are red

    def is_valid_grid(self, grid):
        """Validate the Sudoku grid input."""
        for i in range(9):
            row = [num for num in grid[i] if num != 0]
            if len(row) != len(set(row)):
                return False

            col = [grid[j][i] for j in range(9) if grid[j][i] != 0]
            if len(col) != len(set(col)):
                return False

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subgrid = [
                    grid[x][y]
                    for x in range(i, i + 3)
                    for y in range(j, j + 3)
                    if grid[x][y] != 0
                ]
                if len(subgrid) != len(set(subgrid)):
                    return False

        return True

    def solve_puzzle(self):
        """Solve the Sudoku puzzle using ACO."""
        grid = self.read_grid()
        if not self.is_valid_grid(grid):
            messagebox.showerror("Invalid Input", "The input grid is invalid or unsolvable.")
            return

        solver = ACOSudokuSolver()

        # Record the start time
        start_time = time.time()

        # Solve the puzzle using ACO
        solution = solver.solve(grid)

        # Record the end time
        end_time = time.time()

        # Calculate the time taken
        time_taken = end_time - start_time

        # Display the solution in the grid
        if solution:
            self.display_grid(solution)
        else:
            messagebox.showerror("Error", "ACO could not solve the puzzle.")

        # Update the time label with the time taken
        self.time_label.config(text=f"Time taken: {time_taken:.4f} seconds")

    def load_puzzle(self):
        """Load Sudoku puzzle from a JSON file in the current directory."""
        # Get the current directory path
        current_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_dir, "puzzle.json")  # Assuming the file is named sudoku_puzzle.json

        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    grid = data.get('grid', [])
                    if grid and len(grid) == 9 and all(len(row) == 9 for row in grid):
                        self.display_grid(grid)
                    else:
                        messagebox.showerror("Invalid Puzzle", "The loaded puzzle is invalid.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the file: {e}")
        else:
            messagebox.showerror("File Not Found",
                                 f"Could not find the 'sudoku_puzzle.json' file in the current directory.")

#main
if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()


