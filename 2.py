import sys

sys.setrecursionlimit(20000)

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None

    def add_node(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._add(self.root, value)

    def _add(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._add(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._add(node.right, value)

    def check_is_linear_in_range(self, c, d):
        return self._check_linear_recursive(self.root, c, d)

    def _check_linear_recursive(self, node, c, d):
        if node is None:
            return True
        
        if not (c <= node.value <= d):
            return False
        
        if node.left is not None and node.right is not None:
            return False
            
        return self._check_linear_recursive(node.left, c, d) and \
               self._check_linear_recursive(node.right, c, d)

    def check_is_avl_in_height_range(self, A, B):
        height = self._get_height_if_avl(self.root)
        if height == -1:
            return False
        return A < height < B

    def _get_height_if_avl(self, node):
        if node is None:
            return 0
        
        left_h = self._get_height_if_avl(node.left)
        if left_h == -1:
            return -1
            
        right_h = self._get_height_if_avl(node.right)
        if right_h == -1:
            return -1
            
        if abs(left_h - right_h) > 1:
            return -1
            
        return max(left_h, right_h) + 1

if __name__ == "__main__":
    t = Tree()
    values = [10, 5, 12, 3] 
    for v in values:
        t.add_node(v)

    print(t.check_is_linear_in_range(0, 20))
    print(t.check_is_avl_in_height_range(2, 5))