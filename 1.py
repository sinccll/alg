import time
import random
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(20000)

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None
        self.found_paths = []

    def add_node(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._add_recursion(self.root, value)

    def _add_recursion(self, current, value):
        if value < current.value:
            if current.left is None:
                current.left = Node(value)
            else:
                self._add_recursion(current.left, value)
        else:
            if current.right is None:
                current.right = Node(value)
            else:
                self._add_recursion(current.right, value)

    def find_paths_range(self, a, b):
        self.found_paths = []
        if self.root is not None:
            self._dfs(self.root, [], a, b)
        return self.found_paths
    
    def _dfs(self, node, current_path, a, b):
        current_path.append(node.value)

        if node.left is None and node.right is None:
            path_length = len(current_path) - 1
            if a <= path_length <= b:
                self.found_paths.append(list(current_path))
        if node.left:
            self._dfs(node.left, current_path, a, b)
        if node.right:
            self._dfs(node.right, current_path, a, b)
        
        current_path.pop()

def run_performance_test():
    ns = []
    times = []

    step = 500
    max_nodes = 5000
    
    for n in range(step, max_nodes + step, step):
        tree = Tree()
        random_vals = [random.randint(0, 1000000) for _ in range(n)]
        for v in random_vals:
            tree.add_node(v)
            
        start_time = time.perf_counter()

        tree.find_paths_range(0, n) 

        end_time = time.perf_counter()
        
        elapsed = end_time - start_time
        ns.append(n)
        times.append(elapsed)
        print(f"Обработано {n} узлов за {elapsed:.6f} сек")

    plt.figure(figsize=(10, 6))
    plt.plot(ns, times, 'o-', linewidth=2, label='Практическое время')

    k = times[-1] / ns[-1]
    theoretical_times = [k * x for x in ns]
    plt.plot(ns, theoretical_times, 'r--', label='Теория O(N)')

    plt.xlabel('Количество узлов N')
    plt.ylabel('Время (сек)')
    plt.title('Сложность алгоритма DFS')
    plt.legend()
    plt.grid(True)

    plt.savefig('my_graph.png')

if __name__ == "__main__":
    t = Tree()
    values = [5, 6 , 10, 12, 15, 2, 4]

    for n in values:
        t.add_node(n)

    print("--- Тест: Пути длины от 2 до 3 ---")
    paths = t.find_paths_range(2, 3)
    for p in paths:
        print(f"Путь: {p}, Длина: {len(p) - 1}")

    print("\n--- Построение графика ---")
    run_performance_test()
