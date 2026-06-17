import time
import requests

def run_benchmark(url, iterations=500):
    start_time = time.time()
    for _ in range(iterations):
        response = requests.get(url)
        assert response.status_code == 200
    end_time = time.time()

    total_time = end_time - start_time
    print(f"Total time for {iterations} requests: {total_time:.4f} seconds")
    print(f"Average time per request: {total_time/iterations:.4f} seconds")

if __name__ == "__main__":
    run_benchmark("http://127.0.0.1:5000/receitas/cocktails", 500)
