from PriorityQueue import PriorityQueue
from Node import Node


class SearchAgent(object):
    """docstring for SearchAgent"""

    def __init__(self, graph={}):
        super(SearchAgent, self).__init__()
        self.__agent_status = "idle"
        self.graph = graph

    ################################################
    ########		Search Algorithms		########
    ################################################

    def breadth_first_search(self):
        source = self.source
        if not self.reserve_agent():
            return

        self.reset_graph()
        fringe = []
        node = source
        fringe.append(node)

        while fringe:
            node = fringe.pop(0)
            if self.is_goal_state(node):
                self.finished("success", node)
                return

            if self.node_state(node) != "visited":
                self.set_node_state(node, "visited")
                for n in self.expand(node):
                    if self.node_state(n) != "visited":
                        fringe.append(n)
                yield

        self.finished("failed", source)

    def depth_first_search(self):
        source = self.source
        if not self.reserve_agent():
            return

        self.reset_graph()
        fringe = []
        node = source
        fringe.append(node)

        while fringe:
            node = fringe.pop()
            if self.is_goal_state(node):
                self.finished("success", node)
                return

            if self.node_state(node) != "visited":
                self.set_node_state(node, "visited")
                for n in self.expand(node):
                    if self.node_state(n) != "visited":
                        fringe.append(n)
                yield

        self.finished("failed", source)

    def depth_limit_search(self, limit):
        source = self.source
        if not self.reserve_agent():
            return

        self.reset_graph()
        fringe = []
        node = source
        fringe.append(node)

        while fringe:
            node = fringe.pop()
            if self.is_goal_state(node):
                self.finished("success", node)
                return

            if self.node_state(node) != "visited":
                self.set_node_state(node, "visited")
            if len(node.path) < limit:
                for n in self.expand(node):
                    if self.node_state(n) != "visited":
                        fringe.append(n)

            yield

        self.finished("failed", source)

    def iterative_deepening_search(self, max_depth_limit):
        for limit in range(1, max_depth_limit):
            source = self.source
            if not self.reserve_agent():
                return

            self.reset_graph()
            fringe = []
            node = source
            fringe.append(node)

            while fringe:
                node = fringe.pop()
                if self.is_goal_state(node):
                    self.finished("success", node)
                    return

                if self.node_state(node) != "visited":
                    self.set_node_state(node, "visited")
                if len(node.path) < limit:
                    for i in self.expand(node):
                        if self.node_state(i) != "visited":
                            fringe.append(i)

                yield

            self.finished("failed", source)

    def uniform_cost_search(self):
        source = self.source
        if not self.reserve_agent():
            return

        self.reset_graph()
        fringe = PriorityQueue()
        node = source
        fringe.add(node, node.cost)

        while fringe.isNotEmpty():
            node = fringe.pop()
            if self.is_goal_state(node):
                self.finished("success", node)
                return
            if self.node_state(node) != "visited":
                self.set_node_state(node, "visited")
                for n in self.expand(node):
                    if self.node_state(n) != "visited":
                        fringe.add(n, n.cost)

            yield

        self.finished("failed", source)

    def greedy_search(self):
        source = self.source
        if not self.reserve_agent():
            return

        self.reset_graph()
        fringe = PriorityQueue()
        node = source
        fringe.add(node, node.heuristic)

        while fringe.isNotEmpty():
            node = fringe.pop()
            if self.is_goal_state(node):
                self.finished("success", node)
                return
            if self.node_state(node) != "visited":
                self.set_node_state(node, "visited")
                for n in self.expand(node):
                    if self.node_state(n) != "visited":
                        fringe.add(n, n.heuristic)

            yield

        self.finished("failed", source)

    def a_star_search(self):
        source = self.source
        if not self.reserve_agent():
            return

        self.reset_graph()
        fringe = PriorityQueue()
        node = source
        fringe.add(node, node.cost + node.heuristic)

        while fringe.isNotEmpty():
            node = fringe.pop()
            if self.is_goal_state(node):
                self.finished("success", node)
                return
            if self.node_state(node) != "visited":
                self.set_node_state(node, "visited")
                for n in self.expand(node):
                    if self.node_state(n) != "visited":
                        fringe.add(n, n.cost + n.heuristic)

            yield

        self.finished("failed", source)

    ################################################
    ########		Utility Functions		########
    ################################################

    @property
    def dimensions(self):
        return self.__dimensions

    @property
    def agent_status(self):
        return self.__agent_status

    @property
    def is_agent_searching(self):
        return self.__agent_status == "searching"

    # Reserve the agent and prevent starting new alogorithms while searching
    def reserve_agent(self):
        if self.__agent_status == "searching":
            return False
        self.__agent_status = "searching"
        return True

    # To reset the grid to its initial state
    def reset_graph(self):
        for node_name, node in self.graph.items():
            self.graph[node_name].state = self.graph[node_name].state if self.graph[node_name].state in [
                "source", "goal"] else "empty"

    # The state of a certain node
    def node_state(self, node):
        return self.graph[node.name].state

    def set_node_state(self, node, state):
        self.graph[node.name].state = state

    # Checks whether the state is the goal state (goal)
    def is_goal_state(self, node):
        return self.node_state(node) == "goal"

    # Expand a node to its valid new states
    def expand(self, node):
        return [Node.copy_from(self.graph[name], cost=node.cost + node.children[name], path=node.path + [node.name]) for name in node.children.keys()]

    # Return actual cost
    def cost(self, node):
        return node.cost

    # Retuen Heuristic
    def heuristic(self, node):
        return node.heuristic

    # Get the source node (start state)
    @property
    def source(self):
        return self.graph[0]

    # Finished with "success" or "failed"
    def finished(self, result, goal):
        self.__agent_status = result
        if result == "failed":
            self.graph[goal.name].state = "source"
            return

        for node_name in goal.path[0:]:
            self.graph[node_name].state = "path"
        self.graph[goal.path[0]].state = "source"
