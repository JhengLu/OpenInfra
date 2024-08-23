import time
import multiprocessing


def is_prime(n):
    """Returns True if n is a prime number, else False."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def calculate_primes(limit):
    """Calculate all prime numbers up to a given limit."""
    primes = []
    for num in range(2, limit):
        if is_prime(num):
            primes.append(num)
    return primes


def run_high_cpu_job():
    """Run a CPU intensive task across multiple CPU cores."""
    num_cores = multiprocessing.cpu_count()
    limit = 500000  # Adjust this number to increase/decrease CPU load

    print(f"Running high CPU utilization job on {num_cores} cores...")

    # Create a process pool and distribute the work across CPU cores
    with multiprocessing.Pool(processes=num_cores) as pool:
        start_time = time.time()
        pool.map(calculate_primes, [limit] * num_cores)
        end_time = time.time()

    print(f"Job completed in {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    while True:
        run_high_cpu_job()
