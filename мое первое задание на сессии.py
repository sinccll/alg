import sys
import time
import random
from array import array
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

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
            return
        
        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(value)
                    break
                current = current.right

def find_paths_recursive(node, target_length, current_path, flat_results):
    current_path.append(node.value)
    
    if node.left is None and node.right is None:
        if len(current_path) == target_length:
            flat_results.extend(current_path)
    else:
        if node.left:
            find_paths_recursive(node.left, target_length, current_path, flat_results)
        if node.right:
            find_paths_recursive(node.right, target_length, current_path, flat_results)
            
    current_path.pop()

def get_paths_equal_length(tree, target_length):
    current_path = array('i')
    flat_results = array('i')
    
    if tree.root is not None:
        find_paths_recursive(tree.root, target_length, current_path, flat_results)
    
    if target_length > 0:
        count = len(flat_results) // target_length
    else:
        count = 0
        
    return target_length, flat_results, count

def generate_random_tree(size):
    t = Tree()
    values = array('i', (random.randint(0, 100000) for _ in range(size)))
    for v in values:
        t.insert(v)
    return t

def benchmark():
    sizes = array('i', range(100, 10100, 500))
    times = array('d')
    
    target_len = 15 

    for n in sizes:
        tree = generate_random_tree(n)
        
        start_time = time.perf_counter()
        get_paths_equal_length(tree, target_len)
        end_time = time.perf_counter()
        
        times.append(end_time - start_time)
        
    return sizes, times

def print_example():
    t = Tree()
    t.insert(10)
    t.insert(5)
    t.insert(15)
    t.insert(1) 
    t.insert(8) 
    t.insert(20)

    target = 3
    length, flat_paths, count = get_paths_equal_length(t, target)
    
    print(f"Count: {count}")
    print(f"Flat paths: {flat_paths}")
    
    for i in range(count):
        start_index = i * length
        end_index = start_index + length
        p = flat_paths[start_index : end_index]
        print(f"Path {i+1}: {p}")

if __name__ == "__main__":
    print_example()
    
    sizes, measured_times = benchmark()
    
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, measured_times, label='Practical Time', marker='o')
    
    if sizes[-1] > 0:
        k = measured_times[-1] / sizes[-1]
    else:
        k = 0
    theoretical_times = array('d', (k * x for x in sizes))
    
    plt.plot(sizes, theoretical_times, label='Theoretical O(N)', linestyle='--')
    
    plt.xlabel('Number of Nodes (N)')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    
    plt.savefig('complexity_plot.png')
