#Реализуй класс бинарного дерева Tree с использованием класса узла Node и функцию для нахождения путей от корня до листа, сумма значений узлов которых в диапазоне [a, b], за один обход дерева. Проверьте работу функции на различных конфигурациях деревьев.

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Tree:
    def __init__(self, root=None):
        self.root = root

def build_tree_from_list(values):
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

    if root is None:
        return []

    result = []
    current_path = []
    current_sum = 0

    def dfs(node):
        nonlocal current_sum
        current_path.append(node.value)
        current_sum += node.value

        if node.left is None and node.right is None:
            if a <= current_sum <= b:
                result.append(current_path.copy())
        else:
            if node.left:
                dfs(node.left)
            if node.right:
                dfs(node.right)

        current_path.pop()
        current_sum -= node.value

    dfs(root)
    return result


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


#дерево с одним узлом
tree1 = Tree(Node(5))
test_tree("Дерево с одним узлом (значение 5)", tree1.root, 5, 5)
test_tree("Дерево с одним узлом (значение 5)", tree1.root, 1, 4)

#обычное дерево
tree2 = build_tree_from_list([10, 5, 12, 3, 7, None, 15])
test_tree("обычное дерево, диапазон [15, 25]", tree2.root, 15, 25)
test_tree("обычное дерево, диапазон [20, 30]", tree2.root, 20, 30)

#пустое дерево
tree3 = Tree()
test_tree("Пустое дерево", tree3.root, 0, 100)

#дерево с отрицательными значениями
tree4 = build_tree_from_list([-2, -5, 3, -8, None, None, 1])
test_tree("Дерево с отрицательными числами, диапазон [-10, -5]", tree4.root, -10, -5)
test_tree("Дерево с отрицательными числами, диапазон [0, 5]", tree4.root, 0, 5)
