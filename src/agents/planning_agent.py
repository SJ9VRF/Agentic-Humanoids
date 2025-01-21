import numpy as np
import heapq
import random
from scipy.spatial import distance


class PlanningAgent:
    """
    Planning Agent: Handles path planning, navigation, and decision-making for a humanoid robot.
    Utilizes state-of-the-art methods like A*, RRT, and SLAM for efficient and robust pathfinding.
    """

    def __init__(self, name="Planning Agent"):
        self.name = name
        self.environment_map = None  # Placeholder for the map data (2D/3D grid)
        self.position = [0, 0]  # Current position of the robot (x, y in meters)

    def log(self, message):
        """Log messages with the agent's name."""
        print(f"[{self.name}] {message}")

    def set_environment_map(self, environment_map):
        """
        Set the environment map for path planning.
        Args:
            environment_map (np.array): 2D grid representing the map.
        """
        self.environment_map = environment_map
        self.log("Environment map set successfully.")

    def a_star(self, start, goal):
        """
        A* search algorithm for optimal pathfinding in a 2D grid.
        Args:
            start (tuple): Starting position (x, y).
            goal (tuple): Goal position (x, y).

        Returns:
            list: Optimal path as a list of (x, y) tuples.
        """
        self.log(f"Starting A* search from {start} to {goal}...")

        def heuristic(a, b):
            return distance.euclidean(a, b)

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                self.log(f"Goal reached: {goal}. Constructing path...")
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if (0 <= neighbor[0] < self.environment_map.shape[0] and
                        0 <= neighbor[1] < self.environment_map.shape[1] and
                        self.environment_map[neighbor[0], neighbor[1]] == 0):  # 0 = free space
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        self.log("A* search failed to find a path.")
        raise ValueError("No path found using A*.")

    def rrt(self, start, goal, max_iterations=1000, step_size=0.5):
        """
        RRT (Rapidly-exploring Random Tree) algorithm for path planning in 2D space.
        Args:
            start (tuple): Starting position (x, y).
            goal (tuple): Goal position (x, y).
            max_iterations (int): Maximum number of iterations to search.
            step_size (float): Maximum step size towards a random point.

        Returns:
            list: Path from start to goal, or raises an exception if no path is found.
        """
        self.log(f"Starting RRT from {start} to {goal}...")

        class Node:
            def __init__(self, position, parent=None):
                self.position = position
                self.parent = parent

        nodes = [Node(start)]
        goal_reached = False

        for _ in range(max_iterations):
            random_point = (
                random.uniform(0, self.environment_map.shape[0]),
                random.uniform(0, self.environment_map.shape[1])
            )
            nearest_node = min(nodes, key=lambda node: distance.euclidean(node.position, random_point))
            direction = np.array(random_point) - np.array(nearest_node.position)
            new_position = np.array(nearest_node.position) + step_size * (direction / np.linalg.norm(direction))
            new_position = tuple(np.round(new_position).astype(int))

            if (0 <= new_position[0] < self.environment_map.shape[0] and
                    0 <= new_position[1] < self.environment_map.shape[1] and
                    self.environment_map[new_position[0], new_position[1]] == 0):
                new_node = Node(new_position, nearest_node)
                nodes.append(new_node)

                if distance.euclidean(new_position, goal) <= step_size:
                    goal_reached = True
                    nodes.append(Node(goal, new_node))
                    break

        if goal_reached:
            self.log("Goal reached using RRT. Constructing path...")
            path = []
            current_node = nodes[-1]
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]
        else:
            self.log("RRT failed to find a path.")
            raise ValueError("No path found using RRT.")

    def dynamic_path_update(self, current_path, new_obstacle):
        """
        Update path dynamically when a new obstacle is detected.
        Args:
            current_path (list): Current planned path.
            new_obstacle (tuple): Position of the new obstacle.

        Returns:
            list: Updated path after re-planning.
        """
        self.log(f"Dynamic update triggered. New obstacle at {new_obstacle}.")
        self.environment_map[new_obstacle] = 1  # Mark as obstacle
        start = current_path[0]
        goal = current_path[-1]
        return self.a_star(start, goal)

    def perform_task(self, details):
        """
        Perform a planning task based on the provided details.
        Args:
            details (dict): Task details including type and parameters.

        Returns:
            list: Planned path as a list of (x, y) tuples.
        """
        task_type = details.get("task_type", "unknown")
        self.log(f"Performing planning task '{task_type}'...")

        if task_type == "path_planning":
            start = tuple(details.get("start", [0, 0]))
            goal = tuple(details.get("goal", [0, 0]))
            algorithm = details.get("algorithm", "a_star")

            if algorithm == "a_star":
                return self.a_star(start, goal)
            elif algorithm == "rrt":
                return self.rrt(start, goal)
            else:
                self.log(f"Unknown algorithm '{algorithm}'.")
                raise ValueError(f"Invalid algorithm specified: {algorithm}")

        else:
            self.log(f"Task type '{task_type}' is not recognized.")
            raise ValueError(f"Unknown planning task: {task_type}")

