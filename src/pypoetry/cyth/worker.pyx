# src/pypoetry/cyth/worker.pyx

def worker_func():
    print("Worker")
    for i in range(5):
        print(f"i = {i}")
    print("Worker finished")
