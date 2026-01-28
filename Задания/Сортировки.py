#Реализуйте два алгоритма сортировки: слиянием и вставками. Сравните их производительность, а также производительность встроенной сортировки, на случайных, почти отсортированных и обратно отсортированных массивах

import sys
import time
import random
import matplotlib.pyplot as plt

# Увеличиваем лимит рекурсии для Merge Sort
sys.setrecursionlimit(20000)

# --- 1. Алгоритм сортировки вставками (Insertion Sort) ---
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# --- 2. Алгоритм сортировки слиянием (Merge Sort) ---
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

# --- 3. Генерация данных ---
def generate_array(size, kind):
    if kind == 'random':
        return [random.randint(0, 10000) for _ in range(size)]
    elif kind == 'sorted':
        # Берем отсортированный и немного "портим" (5% перестановок)
        arr = list(range(size))
        swaps = int(size * 0.05)
        for _ in range(swaps):
            idx1 = random.randint(0, size - 1)
            idx2 = random.randint(0, size - 1)
            arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
        return arr
    elif kind == 'reverse':
        return list(range(size, 0, -1))
    return []

# --- 4. Бенчмарк ---
def run_benchmark():
    # Размеры массивов (небольшие, так как Insertion Sort медленный)
    sizes = range(100, 1600, 200)
    scenarios = ['random', 'sorted', 'reverse']
    
    # Структура для хранения результатов: results['random']['insertion'] = [time1, time2...]
    results = {
        kind: {'insertion': [], 'merge': [], 'builtin': []} 
        for kind in scenarios
    }
    
    for kind in scenarios:
        for n in sizes:
            base_data = generate_array(n, kind)
            
            # Тест Insertion Sort
            arr = list(base_data)
            t0 = time.perf_counter()
            insertion_sort(arr)
            results[kind]['insertion'].append(time.perf_counter() - t0)
            
            # Тест Merge Sort
            arr = list(base_data)
            t0 = time.perf_counter()
            merge_sort(arr)
            results[kind]['merge'].append(time.perf_counter() - t0)
            
            # Тест Built-in (Timsort)
            arr = list(base_data)
            t0 = time.perf_counter()
            arr.sort()
            results[kind]['builtin'].append(time.perf_counter() - t0)
            
    return sizes, results

# --- 5. Построение графиков ---
if __name__ == "__main__":
    print("Running benchmark (may take a few seconds)...")
    sizes, results = run_benchmark()
    
    # Создаем 3 графика в ряд
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
    scenario_titles = {
        'random': 'Random Array', 
        'sorted': 'Nearly Sorted', 
        'reverse': 'Reverse Sorted'
    }
    
    for i, kind in enumerate(['random', 'sorted', 'reverse']):
        ax = axs[i]
        
        # Получаем данные
        y_ins = results[kind]['insertion']
        y_mrg = results[kind]['merge']
        y_blt = results[kind]['builtin']
        
        # Рисуем линии
        ax.plot(sizes, y_ins, label='Insertion', marker='o')
        ax.plot(sizes, y_mrg, label='Merge', marker='s')
        ax.plot(sizes, y_blt, label='Built-in', marker='^', linestyle='--')
        
        ax.set_title(scenario_titles[kind])
        ax.set_xlabel('Elements (N)')
        ax.set_ylabel('Time (sec)')
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    plt.savefig('sorting_comparison.png')
    print("Graphs saved to 'sorting_comparison.png'")
