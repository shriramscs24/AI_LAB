import heapq

INITIAL_STATE = (
    2, 8, 3,
    1, 6, 4,
    0, 7, 5
)

GOAL_STATE = (
    1, 2, 3,
    8, 0, 4,
    7, 6, 5
)

# Precompute target positions (row, col) for each tile in the goal state
GOAL_POSITIONS = {tile: (i // 3, i % 3) for i, tile in enumerate(GOAL_STATE)}

def manhattan_distance(state):
    """
    Calculates h(n): sum of Manhattan distances (row_diff + col_diff)
    for all tiles except the blank (0).
    """
    distance = 0
    for i, tile in enumerate(state):
        if tile != 0:
            current_row, current_col = divmod(i, 3)
            goal_row, goal_col = GOAL_POSITIONS[tile]
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def get_neighbors(state):
    """Generates valid next states by sliding adjacent tiles into the blank space."""
    neighbors = []
    blank = state.index(0)
    row, col = divmod(blank, 3)

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for dr, dc in moves:
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            new_blank = r * 3 + c
            state_list = list(state)
            # Swap blank space with neighboring tile
            state_list[blank], state_list[new_blank] = state_list[new_blank], state_list[blank]
            neighbors.append(tuple(state_list))

    return neighbors

def solve_8_puzzle(start_state):
    """Solves the 8-puzzle using A* Search with a Min-Heap priority queue."""
    h_start = manhattan_distance(start_state)
    
    # Priority Queue tuple format: (f_score, g_score, current_state, path)
    # Heap stores items ordered primarily by f_score
    open_set = [(h_start, 0, start_state, [start_state])]
    
    # Tracks the best g_score found for each state to prevent redundant loops
    g_scores = {start_state: 0}

    while open_set:
        # Extract node with smallest f_score in O(log N)
        f, g, current, path = heapq.heappop(open_set)

        if current == GOAL_STATE:
            return path, g

        # Skip if we've already found a strictly cheaper route to this state
        if g > g_scores.get(current, float('inf')):
            continue

        for neighbor in get_neighbors(current):
            tentative_g = g + 1

            if tentative_g < g_scores.get(neighbor, float('inf')):
                g_scores[neighbor] = tentative_g
                h = manhattan_distance(neighbor)
                f_score = tentative_g + h
                
                # Push new candidate node into heap in O(log N)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor, path + [neighbor]))

    return None, -1

def print_board(state):
    """Formats state into a 3x3 grid layout."""
    for i in range(0, 9, 3):
        row = [str(x) if x != 0 else ' ' for x in state[i:i+3]]
        print(" ".join(row))
    print()

# --- Execution ---
path, depth = solve_8_puzzle(INITIAL_STATE)

if path:
    print(f"Optimal solution found in {depth} moves!\n")
    for step, state in enumerate(path):
        h = manhattan_distance(state)
        print(f"Step {step} (g = {step}, h = {h}, f = {step + h}):")
        print_board(state)
else:
    print("No solution found.")
