from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.vertex_list = vertices
        self.V = len(vertices)
        self.graph = defaultdict(list)
        self.coordinate_of_vertices = {}
        self.init_coordinates()

    def init_coordinates(self):
        for vertex in self.vertex_list:
            self.coordinate_of_vertices[vertex[0]] = (vertex[1], vertex[2])

    def add_edge(self, u, v, w):
        self.graph[u].append((v, w))

    def shortest_path(self, s, d):
        connection_exist = False
        explored = []
        all_paths = []

        # Queue for traversing the graph in the BFS
        queue = [[s, 0]]

        # If the desired node is reached
        if s == d:
            message = "You are already in that node:)"
            return False, message

        # Loop to traverse the graph with the help of the queue
        while queue:
            path = queue.pop(0)
            node = path[-2]

            # Find all the neighbours of the node
            neighbours = self.graph[node]

            # Loop to iterate over the neighbours of the node
            for neighbour in neighbours:
                if neighbour[0] not in explored:
                    # Get the path without the total weight
                    new_path = list(path[:-1])
                    # Append the current neighbour to the path
                    new_path.append(neighbour[0])
                    # Update the total weight of the path
                    new_path.append(path[-1] + neighbour[1])
                    queue.append(new_path)

                    # Condition to check if the neighbour node is the destination
                    if neighbour[0] == d:
                        connection_exist = True
                        all_paths.append(new_path)
                    explored.append(node)
        # Condition when the nodes are not connected
        if not connection_exist:
            message = "So sorry, but a connecting path doesn't exist :("
            return False, message
        else:
            shortest_path = all_paths[0]
            for path in all_paths:
                if path[-1] < shortest_path[-1]:
                    shortest_path = path
            return True, shortest_path

    def __str__(self):
        return self.graph