#Реализуй класс бинарного дерева Tree с использованием класса узла Node и функцию для нахождения путей от корня до листа, сумма значений узлов которых в диапазоне [a, b], за один обход дерева. Проверьте работу функции на различных конфигурациях деревьев.

class Node:
    """Узел бинарного дерева."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Tree:
    """Бинарное дерево с корнем."""
    def __init__(self, root=None):
        self.root = root

    @staticmethod
    def from_list(values):
        """
        Простой способ построить дерево из списка (уровневое добавление).
        Используется для удобства тестирования.
        """
        if not values:
            return Tree()
        root = Node(values[0])
        queue = [root]
        i = 1
        while i < len(values):
            node = queue.pop(0)
            if i < len(values) and values[i] is not None:
                node.left = Node(values[i])
                queue.append(node.left)
            i += 1
            if i < len(values) and values[i] is not None:
                node.right = Node(values[i])
                queue.append(node.right)
            i += 1
        return Tree(root)


def find_paths_in_sum_range(root, a, b):
    """
    Находит все пути от корня до листа, сумма значений которых в [a, b].
    Возвращает список путей (каждый путь — список значений узлов).
    """
    if root is None:
        return []

    result = []
    current_path = []
    current_sum = 0

    def dfs(node):
        nonlocal current_sum
        # добавляем текущий узел
        current_path.append(node.value)
        current_sum += node.value

        # если лист, проверяем сумму
        if node.left is None and node.right is None:
            if a <= current_sum <= b:
                result.append(current_path.copy())  # сохраняем копию
        else:
            # рекурсивно обходим детей
            if node.left:
                dfs(node.left)
            if node.right:
                dfs(node.right)

        # возврат (backtracking)
        current_path.pop()
        current_sum -= node.value

    dfs(root)
    return result


# ========== Тестирование ==========

def print_paths(paths):
    for path in paths:
        print(" -> ".join(map(str, path)))

def test_tree(description, tree_root, a, b):
    print(f"\n{description}")
    paths = find_paths_in_sum_range(tree_root, a, b)
    if paths:
        print(f"Найдено путей с суммой в [{a}, {b}]:")
        print_paths(paths)
    else:
        print(f"Нет путей с суммой в [{a}, {b}]")


# Конфигурация 1: дерево с одним узлом
tree1 = Tree(Node(5))
test_tree("Дерево с одним узлом (значение 5)", tree1.root, 5, 5)
test_tree("Дерево с одним узлом (значение 5)", tree1.root, 1, 4)

# Конфигурация 2: дерево из примера
#        10
#       /  \
#      5    12
#     / \     \
#    3   7     15
tree2 = Tree()
tree2.root = Node(10)
tree2.root.left = Node(5)
tree2.root.right = Node(12)
tree2.root.left.left = Node(3)
tree2.root.left.right = Node(7)
tree2.root.right.right = Node(15)
test_tree("Дерево из примера, диапазон [15, 25]", tree2.root, 15, 25)
test_tree("Дерево из примера, диапазон [20, 30]", tree2.root, 20, 30)

# Конфигурация 3: пустое дерево
tree3 = Tree()
test_tree("Пустое дерево", tree3.root, 0, 100)

# Конфигурация 4: дерево с отрицательными значениями
#        -2
#       /  \
#     -5    3
#     /      \
#   -8        1
tree4 = Tree()
tree4.root = Node(-2)
tree4.root.left = Node(-5)
tree4.root.right = Node(3)
tree4.root.left.left = Node(-8)
tree4.root.right.right = Node(1)
test_tree("Дерево с отрицательными числами, диапазон [-10, -5]", tree4.root, -10, -5)
test_tree("Дерево с отрицательными числами, диапазон [0, 5]", tree4.root, 0, 5)

# Конфигурация 5: несбалансированное дерево (одна ветвь)
#     1
#      \
#       2
#        \
#         3
#          \
#           4
tree5 = Tree()
tree5.root = Node(1)
tree5.root.right = Node(2)
tree5.root.right.right = Node(3)
tree5.root.right.right.right = Node(4)
test_tree("Вырожденное дерево (справа), диапазон [6, 10]", tree5.root, 6, 10)
test_tree("Вырожденное дерево (справа), диапазон [10, 15]", tree5.root, 10, 15)
