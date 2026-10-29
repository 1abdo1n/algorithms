import random
import time

import matplotlib.pyplot as plt


def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr):
    n = len(arr)
    src, dst = arr[:], [0] * n
    width = 1
    while width < n: 
        for lo in range(0, n, 2 * width):
            mid = min(lo + width, n)
            hi = min(lo + 2 * width, n)
            i, j, k = lo, mid, lo
            while i < mid and j < hi:
                if src[i] <= src[j]:
                    dst[k] = src[i]
                    i += 1
                else:
                    dst[k] = src[j]
                    j += 1
                k += 1
            while i < mid:
                dst[k] = src[i]
                i += 1
                k += 1
            while j < hi:
                dst[k] = src[j]
                j += 1
                k += 1
        src, dst = dst, src
        width *= 2
    return src


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[random.randrange(len(arr))]
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)


def python_sorted(arr):
    return sorted(arr)


ALGORITHMS = {
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
    "sorted()": python_sorted,
}

SIZES = [10**3, 10**4, 10**5]
KINDS = ["sorted", "reversed", "random"]
INSERTION_MAX_N = 10**4


def make_data(kind, n):
    data = list(range(n))
    if kind == "reversed":
        data.reverse()
    elif kind == "random":
        random.shuffle(data)
    return data


def measure(func, data, repeats):
    best = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        result = func(data)
        best = min(best, time.perf_counter() - t0)
    assert result == sorted(data), f"{func.__name__} gave a wrong result"
    return best


def main():
    random.seed(42)
    results = {k: {name: [] for name in ALGORITHMS} for k in KINDS}

    for kind in KINDS:
        for n in SIZES:
            data = make_data(kind, n)
            repeats = 3 if n <= 10**4 else 1
            for name, func in ALGORITHMS.items():
                if name == "insertion" and n > INSERTION_MAX_N:
                    results[kind][name].append(None)
                    continue
                t = measure(func, data, repeats)
                results[kind][name].append(t)
                print(f"{kind:9} n={n:<7} {name:10} {t:.6f}s")

    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)
    for ax, kind in zip(axes, KINDS):
        for name in ALGORITHMS:
            xs = [n for n, t in zip(SIZES, results[kind][name]) if t is not None]
            ys = [t for t in results[kind][name] if t is not None]
            ax.plot(xs, ys, marker="o", label=name)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(f"{kind} data")
        ax.set_xlabel("n")
        ax.grid(True, which="both", alpha=0.3)
    axes[0].set_ylabel("time (seconds)")
    axes[0].legend()
    fig.suptitle("Sorting Benchmark Lab")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
