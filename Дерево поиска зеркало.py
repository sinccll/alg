#Реализуйте класс бинарного дерева Tree с использованием класса узла Node и функцию для проверки, является ли N-нарное дерево бинарным деревом поиска, зеркальным (123->321) по значениям в узлах относительно своего центра (корня). Проверьте работу функции на различных конфигурациях деревьев. Обоснуйте и подтвердите сложность алгоритма (график теор. и практич. времени)

import sys
import time
import random
from array import array
import matplotlib.pyplot as plt

# Увеличиваем лимит рекурсии для глубоких деревьев
sys.setrecursionlimit(20000)

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None

def is_mirrored_bst(node, min_val=float('-inf'), max_val=float('inf')):
    """
    Проверяет, является ли дерево зеркальным бинарным деревом поиска.
    Условие зеркальности (123 -> 321):
    Значения в левом поддереве > Значение узла > Значения в правом поддереве.
    """
    if node is None:
        return True

    # 1. Проверяем текущий узел на соответствие диапазону
    if not (min_val < node.value < max_val):
        return False

    # 2. Рекурсивно проверяем детей с обновленными границами:
    # Для левого ребенка: он должен быть БОЛЬШЕ текущего узла -> нижняя граница node.value
    # Для правого ребенка: он должен быть МЕНЬШЕ текущего узла -> верхняя граница node.value
    return (is_mirrored_bst(node.left, node.value, max_val) and
            is_mirrored_bst(node.right, min_val, node.value))

# --- Вспомогательные функции для генерации деревьев ---

def build_perfect_reverse_bst(start, end):
    """
    Строит идеально сбалансированное Зеркальное BST из диапазона чисел.
    Нужно, чтобы гарантировать проход по ВСЕМ узлам (худший случай для теста времени).
    """
    if start > end:
        return None
    
    mid = (start + end) // 2
    node = Node(mid)
    
    # В зеркальном дереве большие значения слева, меньшие справа
    # Диапазон [mid+1, end] идет влево
    node.left = build_perfect_reverse_bst(mid + 1, end)
    # Диапазон [start, mid-1] идет вправо
    node.right = build_perfect_reverse_bst(start, mid - 1)
    
    return node

def generate_valid_tree(size):
    """Создает дерево размером size, которое ЯВЛЯЕТСЯ зеркальным BST"""
    t = Tree()
    # Строим на диапазоне 0..size-1
    t.root = build_perfect_reverse_bst(0, size - 1)
    return t

def generate_random_tree(size):
    """Создает случайное дерево (скорее всего НЕ будет зеркальным BST)"""
    t = Tree()
    if size == 0: return t
    t.root = Node(random.randint(0, 10000))
    nodes = [t.root]
    for _ in range(size - 1):
        parent = random.choice(nodes)
        child = Node(random.randint(0, 10000))
        if parent.left is None:
            parent.left = child
            nodes.append(child)
        elif parent.right is None:
            parent.right = child
            nodes.append(child)
    return t

# --- Бенчмарки ---

def benchmark():
    sizes = array('i', range(100, 10100, 500))
    times = array('d')
    
    for n in sizes:
        # Генерируем ВАЛИДНОЕ дерево, чтобы алгоритм прошел все N узлов
        tree = generate_valid_tree(n)
        
        start_time = time.perf_counter()
        is_mirrored_bst(tree.root)
        end_time = time.perf_counter()
        
        times.append(end_time - start_time)
        
    return sizes, times

# --- Демонстрация ---

def print_example():
    print("--- Демонстрация работы check_mirrored_bst ---")
    
    # Случай 1: Валидное Зеркальное Дерево (Root=10, Left=15, Right=5)
    #       10
    #      /  \
    #     15   5
    t1 = Tree()
    t1.root = Node(10)
    t1.root.left = Node(15)
    t1.root.right = Node(5)
    print(f"Test 1 (Valid Mirror BST): {is_mirrored_bst(t1.root)}") # Ожидаем True

    # Случай 2: Обычное BST (Root=10, Left=5, Right=15) - НЕ зеркальное
    #       10
    #      /  \
    #     5    15
    t2 = Tree()
    t2.root = Node(10)
    t2.root.left = Node(5)
    t2.root.right = Node(15)
    print(f"Test 2 (Standard BST):     {is_mirrored_bst(t2.root)}") # Ожидаем False
    
    # Случай 3: Ошибка в глубине
    #       10
    #      /
    #     15
    #    /
    #   12  <-- Ошибка! Слева от 15 должны быть числа > 15 (например 20)
    t3 = Tree()
    t3.root = Node(10)
    t3.root.left = Node(15)
    t3.root.left.left = Node(12) 
    print(f"Test 3 (Invalid Deep):     {is_mirrored_bst(t3.root)}") # Ожидаем False

if __name__ == "__main__":
    print_example()
    
    print("\n--- Запуск тестов производительности (O(N)) ---")
    sizes, measured_times = benchmark()
    
    plt.figure(figsize=(10, 6))
    
    # Практическое время
    plt.plot(sizes, measured_times, label='Practical Time', marker='o')
    
    # Теоретическое время O(N)
    # Рассчитываем коэффициент k по последней точке
    if sizes[-1] > 0:
        k = measured_times[-1] / sizes[-1]
    else:
        k = 0
    theoretical_times = array('d', (k * x for x in sizes))
    
    plt.plot(sizes, theoretical_times, label='Theoretical O(N)', linestyle='--')
    
    plt.xlabel('Количество узлов (N)')
    plt.ylabel('Время (секунды)')
    plt.title('Сложность проверки Зеркального BST')
    plt.legend()
    plt.grid(True)
    
    plt.savefig('mirrored_bst_benchmark.png')
    print("Graph saved to mirrored_bst_benchmark.png")
