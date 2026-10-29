class MaxHeap:
    """Max-heap of (priority, name) tasks, stored in a list."""

    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def insert(self, priority, name):
        self.heap.append((priority, name))
        self._sift_up(len(self.heap) - 1)

    def extract_max(self):
        if self.is_empty():
            raise IndexError("extract_max from empty scheduler")
        top = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return top

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i][0] > self.heap[parent][0]:
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self.heap)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            largest = i
            if left < n and self.heap[left][0] > self.heap[largest][0]:
                largest = left
            if right < n and self.heap[right][0] > self.heap[largest][0]:
                largest = right
            if largest == i:
                break
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            i = largest


def main():
    scheduler = MaxHeap()

    tasks = [
        (3, "Write log"),
        (10, "Handle interrupt"),
        (5, "Update UI"),
        (8, "Disk I/O"),
        (1, "Idle task"),
    ]

    for priority, name in tasks:
        scheduler.insert(priority, name)
        print(f"INSERT      -> priority={priority:<3} {name}")

    print()
    while not scheduler.is_empty():
        priority, name = scheduler.extract_max()
        print(f"EXTRACT-MAX -> priority={priority:<3} running: {name}")


if __name__ == "__main__":
    main()