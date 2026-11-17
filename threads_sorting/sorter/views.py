import threading
import time
import random
from django.shortcuts import render
from django.http import JsonResponse
from .sorters import TBubbleSorter, TInsertionSorter, TQuickSorter

# Глобальное хранилище состояний (в реальном проекте используйте кэш или БД)
thread_states = {
    'bubble':    {'status': 'idle', 'iter_count': 0, 'progress': 0, 'result': None, 'spent_time': 0},
    'insertion': {'status': 'idle', 'iter_count': 0, 'progress': 0, 'result': None, 'spent_time': 0},
    'quick':     {'status': 'idle', 'iter_count': 0, 'progress': 0, 'result': None, 'spent_time': 0},
    'monitor':   {'status': 'idle', 'iter_count': 0, 'progress': 0, 'result': None, 'spent_time': 0},
}
state_lock = threading.Lock()

def _run_sort(algo_name, arr, sorter_class):
    """Обертка для запуска сортировки в отдельном потоке."""
    with state_lock:
        thread_states[algo_name]['status'] = 'running'
        thread_states[algo_name]['progress'] = 0
        thread_states[algo_name]['result'] = None
        thread_states[algo_name]['iter_count'] = 0
        thread_states[algo_name]['spent_time'] = 0
    try:
        sorter = sorter_class(arr, thread_states[algo_name])
        sorter.run()
    except Exception as e:
        with state_lock:
            thread_states[algo_name]['status'] = 'error'
            thread_states[algo_name]['error'] = str(e)

def _monitor_worker():
    """Четвёртый поток: имитация фонового мониторинга."""
    with state_lock:
        thread_states['monitor']['status'] = 'running'
    for i in range(100):
        time.sleep(0.05)
        with state_lock:
            thread_states['monitor']['progress'] = i + 1
            thread_states['monitor']['result'] = f'Мониторинг: {i+1}%'
    with state_lock:
        thread_states['monitor']['status'] = 'completed'
        thread_states['monitor']['result'] = 'Мониторинг завершён'

def about(request):
    """Страница «О проекте»."""
    return render(request, 'sorter/about.html')


def index(request):
    """Главная страница: сброс состояний и запуск четырёх потоков."""
    with state_lock:
        for key in thread_states:
            thread_states[key] = {'status': 'idle', 'iter_count': 0, 'progress': 0, 'result': None, 'spent_time': 0}

    # Генерируем случайный список для сортировки
    original = [random.randint(1, 100) for _ in range(30)]

    threads = [
        threading.Thread(target=_run_sort, args=('bubble', original.copy(), TBubbleSorter)),
        threading.Thread(target=_run_sort, args=('insertion', original.copy(), TInsertionSorter)),
        threading.Thread(target=_run_sort, args=('quick', original.copy(), TQuickSorter)),
        threading.Thread(target=_monitor_worker),
    ]
    for t in threads:
        t.daemon = True
        t.start()

    context = {
        'original': original,
        'algorithms': ['bubble', 'insertion', 'quick', 'monitor'],
    }
    return render(request, 'sorter/dashboard.html', context)

def status_api(request):
    """Возвращает текущие состояния всех потоков в формате JSON."""
    with state_lock:
        # Делаем копию, чтобы не отдавать ссылку на изменяемый объект
        tasks = {k: v.copy() for k, v in thread_states.items()}
        refresh = not all(v["status"] == "completed" for v in tasks.values())
        refresh = "on" if refresh else "off"
        data = {"refresh": refresh, "tasks": tasks}
    return JsonResponse(data)
