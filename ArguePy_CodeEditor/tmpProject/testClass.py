
import random

class algo:
    
    def __init__(self):
        pass
        
    def create_random_array(self, length, min_value, max_value):
        """    
        Crea un array di lunghezza specificata, riempito con numeri casuali nell'intervallo specificato.
        :param length: la lunghezza dell'array
        :param min_value: il valore minimo (incluso) per i numeri casuali
        :param max_value: il valore massimo (escluso) per i numeri casuali
        :return: l'array di numeri casuali
        """
        return [random.randint(min_value, max_value) for _ in range(length)]

    
    def bubble_sort(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

                   