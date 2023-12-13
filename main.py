class Queen:

    def __init__(self, column, size):
        self.column = column
        self.size = size
        self.row = -1  # Inicialmente la reina está fuera del tablero

    def is_safe(self, queens):
        for other_queen in queens:
            if (other_queen.row == self.row or abs(other_queen.row - self.row)
                    == abs(other_queen.column - self.column)):
                return False
        return True

    # def show_queens(self, queens):
    #     for queen in queens:
    #         print(queen.row, ", ", queen.column)


def print_queens_info(queens):
    for queen in queens:
        print(f"Reina en columna {queen.column}: Fila {queen.row}")


def solve_n_queens_backtracking(size, queens, solutions):
    # print("Reinas:", queens.row, ", ", queens.column)
    if len(queens) == size:
        # Se han colocado todas las reinas, hemos encontrado una solución
        solutions.append(queens.copy())
        # if len(solutions) == 3:
        #     # Se encontraron tres soluciones, terminamos la búsqueda
        #     return solutions

    for row in range(size):
        queen = Queen(len(queens), size)
        queen.row = row
        if queen.is_safe(queens):
            # La reina actual es segura en la posición actual
            solve_n_queens_backtracking(size, queens + [queen], solutions)

    print_queens_info(queens)
    return solutions


def print_solution(queens):
    board = [['.' for _ in range(len(queens))] for _ in range(len(queens))]
    for queen in queens:
        board[queen.row][queen.column] = 'Q'

    for row in board:
        print(' '.join(row))


# Ejemplo de uso
size = 4
solutions = solve_n_queens_backtracking(size, [], [])

if solutions:
    for i, solution in enumerate(solutions):
        print(f"Solución {i + 1}:")
        print_solution(solution)
        print()
else:
    print("No se encontró ninguna solución.")
