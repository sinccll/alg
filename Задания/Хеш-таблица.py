#Реализуйте хеш-таблицу с открытой адресацией (два вида пробирования), осуществляющую подсчет коллизий и расширение в случае превышения порога M кол-ва коллизий. Подберите различные конфигурации данных / хещ-функции и сравните скорость работы стандартных операций (вставки/удаления/поиска), операции расширения(отдельно от других операций), а также количество коллизий

import sys
import time
import random
import string
from array import array
import matplotlib.pyplot as plt

class HashTable:
    def __init__(self, method='linear'):
        self.size = 16
        self.count = 0
        self.slots = [None] * self.size
        self.method = method  # 'linear' или 'quadratic'
        
        # Параметры для расширения
        self.collision_threshold = 50  # Порог коллизий (M)
        self.total_collisions = 0
    
    def _hash(self, key):
        return hash(key)

    def _get_index(self, key_hash, i):
        if self.method == 'quadratic':
            return (key_hash + i + i**2) % self.size
        return (key_hash + i) % self.size  # Linear

    def _resize(self):
        old_slots = self.slots
        self.size *= 2
        self.slots = [None] * self.size
        self.count = 0
        self.total_collisions = 0
        
        for item in old_slots:
            if item is not None:
                self.insert(item[0], item[1], resize_mode=True)

    def insert(self, key, value, resize_mode=False):
        # Проверка порога коллизий перед вставкой (если не в режиме ресайза)
        if not resize_mode and self.total_collisions > self.collision_threshold:
            self._resize()

        key_hash = self._hash(key)
        i = 0
        while i < self.size:
            idx = self._get_index(key_hash, i)
            slot = self.slots[idx]

            # Если слот пуст
            if slot is None:
                self.slots[idx] = (key, value)
                self.count += 1
                return True
            
            # Если ключ совпадает (обновление)
            if slot[0] == key:
                self.slots[idx] = (key, value)
                return True
            
            # Коллизия
            if not resize_mode:
                self.total_collisions += 1
            i += 1
            
        # Если таблица заполнилась (редкий случай)
        if not resize_mode:
            self._resize()
            self.insert(key, value)
        return False

    def search(self, key):
        key_hash = self._hash(key)
        i = 0
        while i < self.size:
            idx = self._get_index(key_hash, i)
            slot = self.slots[idx]
            
            if slot is None:
                return None
            if slot[0] == key:
                return slot[1]
            i += 1
        return None

# --- Вспомогательные функции ---

def generate_random_keys(count):
    # Генерируем строки
    return [''.join(random.choices(string.ascii_letters, k=8)) for _ in range(count)]

def benchmark():
    # Размеры: 100, 1100, 2100 ...
    sizes = array('i', range(100, 5000, 200))
    
    times_linear = array('d')
    times_quad = array('d')
    
    for n in sizes:
        keys = generate_random_keys(n)
        
        # 1. Тест Linear Probing
        ht_lin = HashTable(method='linear')
        t0 = time.perf_counter()
        for k in keys:
            ht_lin.insert(k, k) # Вставка N элементов
        times_linear.append(time.perf_counter() - t0)
        
        # 2. Тест Quadratic Probing
        ht_quad = HashTable(method='quadratic')
        t0 = time.perf_counter()
        for k in keys:
            ht_quad.insert(k, k)
        times_quad.append(time.perf_counter() - t0)
        
    return sizes, times_linear, times_quad

# --- Демонстрация ---
def print_example():
    print("--- Демонстрация Хеш-таблицы ---")
    ht = HashTable(method='linear')
    ht.insert("apple", 100)
    ht.insert("banana", 200)
    ht.insert("cherry", 300)
    
    val = ht.search("banana")
    print(f"Search 'banana': {val} (Ожидается 200)")
    print(f"Total Collisions: {ht.total_collisions}")
    print(f"Table Size: {ht.size}")

if __name__ == "__main__":
    print_example()
    
    print("\n--- Запуск тестов производительности ---")
    sizes, times_lin, times_quad = benchmark()
    
    plt.figure(figsize=(10, 6))
    
    # График для Linear
    plt.plot(sizes, times_lin, label='Linear Probing', marker='o', markersize=4)
    
    # График для Quadratic
    plt.plot(sizes, times_quad, label='Quadratic Probing', marker='x', markersize=4)
    
    # Теоретическая сложность O(N) для операции вставки N элементов
    # (так как одна вставка O(1), то N вставок = O(N))
    k = times_lin[-1] / sizes[-1] if sizes[-1] > 0 else 0
    theoretical_times = array('d', (k * x for x in sizes))
    plt.plot(sizes, theoretical_times, label='Theoretical O(N)', linestyle='--')
    
    plt.xlabel('Количество элементов (N)')
    plt.ylabel('Время вставки (секунды)')
    plt.title('Сложность вставки в Хеш-таблицу')
    plt.legend()
    plt.grid(True)
    
    plt.savefig('hashtable_plot.png')
