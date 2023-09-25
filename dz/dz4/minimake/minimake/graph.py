def topological_sort(graph, inverted=False):
    def dfs(node, visited, stack):
        visited[node] = True
        if node in graph:
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    dfs(neighbor, visited, stack)
        stack.insert(0, node)

    visited = {node: False for node in graph}
    stack = []

    for node in graph:
        if not visited[node]:
            dfs(node, visited, stack)

    if inverted:
        return stack[::-1]

    return stack


if __name__ == "__main__":
    # Example usage:
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D', 'E'],
        'D': ['E'],
        'E': []
    }

    result = topological_sort(graph)
    print(result)
