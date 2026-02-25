#Реализуйте класс бинарного дерева Tree с использованием класса узла Node и функцию для нахождения путей от корня до листа одинаковой длины за один обход дерева (возвращает длину пути и сами пути). Проверьте работу функции на различных конфигурациях деревьев.

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


def find_paths_grouped_by_length(root):
    if root is None:
        return {}

    result = {}
    current_path = []

    def dfs(node):
        current_path.append(node.value)

        if node.left is None and node.right is None:
            length = len(current_path)
            if length not in result:
                result[length] = []
            result[length].append(current_path.copy())
        else:
            if node.left:
                dfs(node.left)
            if node.right:
                dfs(node.right)

        current_path.pop()

    dfs(root)
    return result


def print_paths_by_length(paths_dict):
    if not paths_dict:
        print("  Нет путей (дерево пусто)")
        return
    for length in sorted(paths_dict.keys()):
        print(f"  Длина {length}:")
        for path in paths_dict[length]:
            print("    " + " -> ".join(map(str, path)))


def test_tree(description, tree_root):
    print(f"\n{description}")
    paths = find_paths_grouped_by_length(tree_root)
    print_paths_by_length(paths)


#дерево с одним узлом
tree1 = Tree(Node(5))
test_tree("Дерево с одним узлом (значение 5)", tree1.root)

#обычное дерево
tree2 = build_tree_from_list([10, 5, 12, 3, 7, None, 15])
test_tree("Дерево из примера", tree2.root)

#пустое дерево
tree3 = Tree()
test_tree("Пустое дерево", tree3.root)

#дерево с отрицательными значениями
tree4 = build_tree_from_list([-2, -5, 3, -8, None, None, 1])
test_tree("Дерево с отрицательными числами", tree4.root)

#вырожденное дерево (одна ветвь)
tree5 = build_tree_from_list([1, None, 2, None, 3, None, 4])
test_tree("Вырожденное дерево (справа)", tree5.root)
