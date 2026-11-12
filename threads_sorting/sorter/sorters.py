import time


class TBaseSorter(object):
    def __init__(self, target: list, state: dict):
        self.target = target  # target array for sorting
        self.state = state

    def run(self):
        ...

    def get_sample(self):
        """Get a sample evenly across the entire target list. Used for visualisation in UI"""
        rarefaction = 1000
        res = []
        for i in range(0, len(self.target), rarefaction):
            res.append(self.target[i])
        return res


class TBubbleSorter(TBaseSorter):
    def run(self):
        self.state["status"] = "running"
        arr = self.target
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                self.state["progress"] = (i * n + j) / (n * n) * 100
                time.sleep(0.01)
            if not swapped:
                break
        self.state["status"] = 'completed'
        self.state['result'] = arr


class TInsertionSorter(TBaseSorter):
    def run(self):
        self.state["status"] = "running"
        arr = self.target

        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
                self.state["progress"] = (i * len(arr) + j) / (len(arr) ** 2) * 100
                time.sleep(0.01)
            arr[j + 1] = key
        self.state["status"] = 'completed'
        self.state['result'] = arr


class TQuickSorter(TBaseSorter):
    def run(self):
        def quick_sort(arr, low=0, high=None):
            if high is None:
                high = len(arr) - 1
            if low < high:
                pi = partition(arr, low, high)
                quick_sort(arr, low, pi - 1)
                quick_sort(arr, pi + 1, high)
            #if low == 0 and high == len(arr) - 1:
            #    state['status'] = 'completed'
            #    state['result'] = arr.copy()

        def partition(arr, low, high):
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                self.state["progress"] = (j - low + 1) / (high - low + 1) * 100
                time.sleep(0.01)
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        self.state["status"] = "running"
        quick_sort(self.target)
        self.state["status"] = 'completed'
        self.state['result'] = self.target
