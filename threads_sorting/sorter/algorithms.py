import time
import random

def bubble_sort(arr, state):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
            state['progress'] = (i * n + j) / (n * n) * 100
            time.sleep(0.01)
        if not swapped:
            break
    state['status'] = 'completed'
    state['result'] = arr.copy()

def insertion_sort(arr, state):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            state['progress'] = (i * len(arr) + j) / (len(arr) ** 2) * 100
            time.sleep(0.01)
        arr[j + 1] = key
    state['status'] = 'completed'
    state['result'] = arr.copy()

def quick_sort(arr, state, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = partition(arr, low, high, state)
        quick_sort(arr, state, low, pi - 1)
        quick_sort(arr, state, pi + 1, high)
    if low == 0 and high == len(arr) - 1:
        state['status'] = 'completed'
        state['result'] = arr.copy()

def partition(arr, low, high, state):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
        state['progress'] = (j - low + 1) / (high - low + 1) * 100
        time.sleep(0.01)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
