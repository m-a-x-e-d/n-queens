import subprocess
import os
import math

def queens(N):
    def pos(i, j):
        return i * N + j + 1

    clauses = []

    # Row and column constraints
    for i in range(N):
        row = [pos(i, j) for j in range(N)]
        col = [pos(j, i) for j in range(N)]
        # at least one queen per row/column
        clauses.append(row)
        clauses.append(col)
        # at most one queen per row/column
        for x in range(N):
            for y in range(x + 1, N):
                clauses.append([-pos(i, x), -pos(i, y)])
                clauses.append([-pos(x, i), -pos(y, i)])

    # Diagonal constraints
    for d in range(-N + 2, N - 1):
        main_diag = [pos(i, i + d) for i in range(N) if 0 <= i + d < N]
        anti_diag = [pos(i, N - 1 - i + d) for i in range(N) if 0 <= N - 1 - i + d < N]
        for x in range(len(main_diag)):
            for y in range(x + 1, len(main_diag)):
                clauses.append([-main_diag[x], -main_diag[y]])
        for x in range(len(anti_diag)):
            for y in range(x + 1, len(anti_diag)):
                clauses.append([-anti_diag[x], -anti_diag[y]])

    # Write to DIMACS file
    with open(f"nqueens_{N}.cnf", "w") as f:
        f.write(f"p cnf {N*N} {len(clauses)}\n")
        for clause in clauses:
            print(clause)
            f.write(" ".join(map(str, clause)) + " 0\n")

    with open(f"nqueens_{N}.cnf", "r") as f: 
        return f"nqueens_{N}.cnf", f.read()



def run_minisat(filename):
    try:
        # Run MiniSat using subprocess.run to capture both output and exit code
        result = subprocess.run(["minisat", filename, "output.txt"], text=True, capture_output=True, check=False)
        
        # Check if the result was successful, or a specific valid exit code occurred
        if result.returncode == 0 or result.returncode == 10 or result.returncode == 20:
            print("MiniSat ran successfully or returned a valid exit code.")
            print(result.stdout)
            return result.stdout
        else:
            # Handle other non-zero exit codes as errors
            print(f"Error: MiniSat exited with unexpected code {result.returncode}")
            print(result.stderr)
            return result.stderr
    except subprocess.CalledProcessError as e:
        # Handle unexpected subprocess errors
        print(f"MiniSat failed with {e.returncode}, output: {e.output}")
        return e.output


def create_assignment_array():
    with open("output.txt", 'r') as f:
        sat = f.readline()
        if not 'UNSAT' in sat: 
            assignment = f.readline().strip().split(" ")[:-1]
            n = int(math.sqrt(int(assignment[-1])*(-1)))
            return_array = []
            for x in assignment:
                if int(x) > 0:
                    return_array.append(int(x))
            return return_array, n
        else:
            return [], 0
    