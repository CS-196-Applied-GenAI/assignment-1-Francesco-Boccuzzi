# Route Planning System with Pseudocode

# Function 1: Fully written in pseudocode
# ----------------------------------------
# Define function process_route_data(data)
#     Initialize empty dictionary route_map
#     For each entry in data:
#         Extract 'starting_point', 'destination', and 'distance'
#         Store 'starting_point' as key and a list of (destination, distance) tuples as value in route_map
#     Return route_map


def process_route_data(data):
    """
    Process route data and organize it into a dictionary structure.
    
    Parameters
    ----------
    data : list of dict
        List of route entries, each containing 'starting_point', 'destination', and 'distance'
    
    Returns
    -------
    dict
        Dictionary where keys are starting points and values are lists of (destination, distance) tuples
    """
    route_map = {}
    
    for entry in data:
        starting_point = entry['starting_point']
        destination = entry['destination']
        distance = entry['distance']
        
        if starting_point not in route_map:
            route_map[starting_point] = []
        
        route_map[starting_point].append((destination, distance))
    
    return route_map



# Function 2: Function header with brief pseudocode
# --------------------------------------------------
def find_shortest_route(start, destination, route_map):
    """
    Find the shortest route between two locations.
    - Use a pathfinding algorithm to determine the optimal route.
    - Return the route and estimated distance.
    """
    import heapq
    
    # Initialize distances and path tracking
    distances = {node: float('inf') for node in route_map}
    distances[start] = 0
    previous = {node: None for node in route_map}
    
    # Priority queue: (distance, current_node)
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        # If we reached the destination, reconstruct the path
        if current_node == destination:
            path = []
            node = destination
            while node is not None:
                path.append(node)
                node = previous[node]
            path.reverse()
            return (path, distances[destination])
        
        # Check all neighbors
        if current_node in route_map:
            for neighbor, distance in route_map[current_node]:
                new_distance = current_distance + distance
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))
    
    # No route found
    return None


# Pseudocode block 1: No function title, just high-level steps
# ------------------------------------------------------------
# Read user input for starting location and destination
# Validate that both locations exist in the route map
# If both are valid, call the shortest route function and return the result
# If not, return an error message

def get_route_query(route_map):
    """
    Read user input for starting location and destination, validate locations.
    
    Parameters
    ----------
    route_map : dict
        Dictionary mapping starting points to destinations
    
    Returns
    -------
    tuple or None
        (start, destination) if valid, None if invalid
    """
    start = input("Enter starting location: ").strip()
    destination = input("Enter destination: ").strip()
    
    if start not in route_map:
        print(f"Error: Starting location '{start}' not found in route map.")
        return None
    
    if destination not in [dest for dest, _ in route_map.get(start, [])]:
        print(f"Error: Destination '{destination}' is not reachable from '{start}'.")
        return None
    
    return (start, destination)

# Pseudocode block 2: Another missing function title
# --------------------------------------------------
# Allow the system to handle multiple route calculations in a loop
# - Continue accepting input from the user
# - Provide the shortest route for each query
# - Allow the user to exit by typing 'quit'

def main_route_loop(route_map):
    """
    Main application loop for route planning system.
    
    Parameters
    ----------
    route_map : dict
        Dictionary mapping starting points to destinations
    """
    while True:
        user_input = input("Enter 'quit' to exit or press Enter to continue: ").strip().lower()
        
        if user_input == 'quit':
            print("Exiting route planning system.")
            break
        
        result = get_route_query(route_map)
        
        if result:
            start, destination = result
            route_result = find_shortest_route(start, destination, route_map)
            if route_result:
                print(f"Shortest route from {start} to {destination}: {route_result}")
            else:
                print(f"No route found from {start} to {destination}.")


# BLANK SPACE: Students will continue writing the route planning implementation from here
# - Calculate the estimated travel time based on distance and average speed
# - Implement a function to suggest alternative routes if the shortest route is unavailable
# - Design a function that calculates the total fuel cost for a given route based on fuel efficiency

def calculate_travel_time(distance, average_speed=60):
    """
    Calculate the estimated travel time based on distance and average speed.
    
    Parameters
    ----------
    distance : float
        Total distance in kilometers
    average_speed : float
        Average speed in km/h (default: 60 km/h)
    
    Returns
    -------
    float
        Estimated travel time in hours
    """
    if average_speed <= 0:
        raise ValueError("Average speed must be positive.")
    
    travel_time = distance / average_speed
    return travel_time

def suggest_alternative_routes(start, destination, route_map, num_alternatives=3):
    """
    Suggest alternative routes if the shortest route is unavailable.
    
    Parameters
    ----------
    start : str
        Starting location
    destination : str
        Destination location
    route_map : dict
        Dictionary mapping starting points to destinations
    num_alternatives : int
        Number of alternative routes to find (default: 3)
    
    Returns
    -------
    list
        List of alternative routes, each as (path, distance) tuple
    """
    alternatives = []
    visited_routes = set()
    
    # Generate alternative routes by exploring different paths
    def dfs(current, target, path, distance, max_depth=5):
        if len(alternatives) >= num_alternatives:
            return
        
        if current == target:
            route_key = tuple(path)
            if route_key not in visited_routes:
                visited_routes.add(route_key)
                alternatives.append((path.copy(), distance))
            return
        
        if max_depth <= 0:
            return
        
        if current in route_map:
            for neighbor, edge_distance in route_map[current]:
                if neighbor not in path:  # Avoid cycles
                    path.append(neighbor)
                    dfs(neighbor, target, path, distance + edge_distance, max_depth - 1)
                    path.pop()
    
    dfs(start, destination, [start], 0)
    
    # Sort alternatives by distance
    alternatives.sort(key=lambda x: x[1])
    return alternatives

def calculate_fuel_cost(route, fuel_efficiency=8, fuel_price_per_liter=1.5):
    """
    Calculate the total fuel cost for a given route based on fuel efficiency.
    
    Parameters
    ----------
    route : tuple
        Tuple of (path, distance) where path is list of locations and distance is total km
    fuel_efficiency : float
        Fuel efficiency in km/liter (default: 8 km/liter)
    fuel_price_per_liter : float
        Fuel price per liter in currency units (default: 1.5)
    
    Returns
    -------
    float
        Total fuel cost for the route
    """
    if fuel_efficiency <= 0:
        raise ValueError("Fuel efficiency must be positive.")
    if fuel_price_per_liter < 0:
        raise ValueError("Fuel price cannot be negative.")
    
    path, distance = route
    liters_needed = distance / fuel_efficiency
    total_cost = liters_needed * fuel_price_per_liter
    
    return round(total_cost, 2)

def load_route_data(filename):
    """
    Load route data from a file.
    
    Parameters
    ----------
    filename : str
        Path to the file containing route data
    
    Returns
    -------
    list
        List of dictionaries containing route information
    """
    route_data = []
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                parts = [part.strip() for part in line.split(',')]
                if len(parts) >= 3:
                    try:
                        route_entry = {
                            'starting_point': parts[0],
                            'destination': parts[1],
                            'distance': float(parts[2])
                        }
                        route_data.append(route_entry)
                    except ValueError:
                        print(f"Warning: Could not parse distance value in line: {line}")
        
        return route_data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

if __name__ == "__main__":
    import os
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    routes_file = os.path.join(script_dir, "routes.txt")
    
    route_data = load_route_data(routes_file)
    
    if route_data:
        route_map = process_route_data(route_data)
        print("Route system initialized successfully.")
        print(f"Available routes: {route_map}")
        # Uncomment the line below to start the interactive route planning loop
        # main_route_loop(route_map)