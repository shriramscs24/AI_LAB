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

def misplaced_tiles(state):
    """Calculates h(n): count of misplaced tiles (excluding blank 0)."""
    return sum(1 for i in range(9) if state[i] != 0 and state[i] != GOAL_STATE[i])

def get_neighbors(state):
    """Generates valid successor states by moving the blank space."""
    neighbors = []
    blank = state.index(0)
    row, col = divmod(blank, 3)

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for dr, dc in moves:
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            new_blank = r * 3 + c
            state_list = list(state)
            state_list[blank], state_list[new_blank] = state_list[new_blank], state_list[blank]
            neighbors.append(tuple(state_list))

    return neighbors

def solve_8_puzzle(start_state):
    """Solves the 8-puzzle using A* search without using heapq."""
    h_start = misplaced_tiles(start_state)
    
    # Store items as dictionaries inside a standard list
    open_set = [{
        'state': start_state,
        'g': 0,
        'h': h_start,
        'f': h_start,
        'path': [start_state]
    }]
    
    g_scores = {start_state: 0}

    while open_set:
        # Manually find and extract the node with the lowest f score
        best_index = 0
        for i in range(1, len(open_set)):
            if open_set[i]['f'] < open_set[best_index]['f']:
                best_index = i

        current_node = open_set.pop(best_index)
        current = current_node['state']
        g = current_node['g']
        path = current_node['path']

        if current == GOAL_STATE:
            return path, g

        for neighbor in get_neighbors(current):
            tentative_g = g + 1

            if tentative_g < g_scores.get(neighbor, float('inf')):
                g_scores[neighbor] = tentative_g
                h = misplaced_tiles(neighbor)
                
                open_set.append({
                    'state': neighbor,
                    'g': tentative_g,
                    'h': h,
                    'f': tentative_g + h,
                    'path': path + [neighbor]
                })

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
        if step == 0:
            print("Initial State (Depth 0):")
        else:
            h = misplaced_tiles(state)
            print(f"Step {step} (g = {step}, h = {h}, f = {step + h}):")
        print_board(state)
else:
    print("No solution found.")
