import random
from time import time


def create_random_array(length, min_value, max_value):
    """
    Crea un array di lunghezza specificata, riempito con numeri casuali nell'intervallo specificato.
    :param length: la lunghezza dell'array
    :param min_value: il valore minimo (incluso) per i numeri casuali
    :param max_value: il valore massimo (escluso) per i numeri casuali
    :return: l'array di numeri casuali
    """
    return [random.randint(min_value, max_value) for _ in range(length)]


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


start_time = time()
a = create_random_array(10000, 2, 200)
b = bubble_sort(a)
print(b)
end_time = time()
elapsed_time = end_time - start_time

# Aggiungi il tempo di esecuzione all'output
print(f"Elapsed time: {elapsed_time:.2f} seconds")
