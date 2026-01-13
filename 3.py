import random
import time
import matplotlib.pyplot as plt
import sys

class SimpleNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class SimpleSinglyLinkedList:
    def __init__(self):
        self.head = None

    def push(self, value):
        new_node = SimpleNode(value)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.head:
            self.head = self.head.next

    def get_min(self):
        if not self.head: return None
        current = self.head
        min_val = current.value
        while current:
            if current.value < min_val:
                min_val = current.value
            current = current.next
        return min_val

    def get_max(self):
        if not self.head: return None
        current = self.head
        max_val = current.value
        while current:
            if current.value > max_val:
                max_val = current.value
            current = current.next
        return max_val

class ModNode:
    def __init__(self, value, cur_min, cur_max):
        self.value = value
        self.cur_min = cur_min
        self.cur_max = cur_max
        self.next = None

class ModifiedSinglyLinkedList:
    def __init__(self):
        self.head = None

    def push(self, value):
        if self.head is None:
            new_node = ModNode(value, value, value)
        else:
            new_min = min(value, self.head.cur_min)
            new_max = max(value, self.head.cur_max)
            new_node = ModNode(value, new_min, new_max)
        
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.head:
            self.head = self.head.next

    def get_min(self):
        if not self.head: return None
        return self.head.cur_min

    def get_max(self):
        if not self.head: return None
        return self.head.cur_max

class ModDoublyNode:
    def __init__(self, value, cur_min, cur_max):
        self.value = value
        self.cur_min = cur_min
        self.cur_max = cur_max
        self.next = None
        self.prev = None

class ModifiedDoublyLinkedList:
    def __init__(self):
        self.head = None

    def push(self, value):
        if self.head is None:
            new_node = ModDoublyNode(value, value, value)
        else:
            new_min = min(value, self.head.cur_min)
            new_max = max(value, self.head.cur_max)
            new_node = ModDoublyNode(value, new_min, new_max)
        
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        self.head = new_node

    def pop(self):
        if self.head:
            self.head = self.head.next
            if self.head:
                self.head.prev = None

    def get_min(self):
        if not self.head: return None
        return self.head.cur_min

    def get_max(self):
        if not self.head: return None
        return self.head.cur_max

def measure_performance():
    ns = []
    simple_times = []
    mod_times = []

    step = 1000
    max_n = 10000

    for n in range(step, max_n + step, step):
        simple_list = SimpleSinglyLinkedList()
        mod_list = ModifiedSinglyLinkedList()
        
        vals = [random.randint(0, 100000) for _ in range(n)]
        
        for v in vals:
            simple_list.push(v)
            mod_list.push(v)
        
        start = time.perf_counter()
        simple_list.get_min()
        end = time.perf_counter()
        simple_times.append(end - start)

        start = time.perf_counter()
        mod_list.get_min()
        end = time.perf_counter()
        mod_times.append(end - start)
        
        ns.append(n)
        print(f"N={n} обработан")

    plt.figure(figsize=(10, 6))
    plt.plot(ns, simple_times, 'r-o', label='Простой список O(N)')
    plt.plot(ns, mod_times, 'g-o', label='Модифицированный список O(1)')
    
    plt.xlabel('Количество элементов')
    plt.ylabel('Время поиска минимума (сек)')
    plt.title('Сравнение времени поиска Min')
    plt.legend()
    plt.grid(True)
    plt.savefig('list_comparison.png')
    print("График сохранен в list_comparison.png")

if __name__ == "__main__":
    msll = ModifiedSinglyLinkedList()
    mdll = ModifiedDoublyLinkedList()
    
    test_vals = [10, 20, 5, 8, 30]
    for v in test_vals:
        msll.push(v)
        mdll.push(v)
        
    print(f"Мин. модиф. односвязный: {msll.get_min()} (Ожидается 5)")
    print(f"Макс. модиф. односвязный: {msll.get_max()} (Ожидается 30)")
    
    msll.pop() 
    print(f"Мин. после удаления (pop): {msll.get_min()} (Ожидается 5)")
    
    print(f"Мин. модиф. двусвязный: {mdll.get_min()} (Ожидается 5)")

    measure_performance()