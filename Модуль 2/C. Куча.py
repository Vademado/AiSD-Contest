from sys import stdin
from copy import deepcopy


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class MinBinaryHeap:
    def __init__(self):
        self.binary_heap_array = list()
        self.hash_table = dict()  # key - index (позиция в массиве binary_heap_array)

    def heapify_recursive(self, i):
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i
        if left <= self.size() and self.binary_heap_array[left].key < self.binary_heap_array[largest].key:
            largest = left
        if right <= self.size() and self.binary_heap_array[right].key < self.binary_heap_array[largest].key:
            largest = right
        if largest != i:
            self.swap(i, largest)
            self.heapify(largest)

    def heapify(self, i):
        while 2 * i < self.size():
            left = 2 * i + 1
            right = 2 * i + 2
            largest = left
            if right < self.size() and self.binary_heap_array[right].key < self.binary_heap_array[largest].key:
                largest = right
            if self.binary_heap_array[i].key > self.binary_heap_array[largest].key:
                return
            self.swap(i, largest)
            i = largest

    def swap(self, i, j):
        self.binary_heap_array[i], self.binary_heap_array[j] = self.binary_heap_array[j], self.binary_heap_array[i]
        self.hash_table[self.binary_heap_array[i].key] = i
        self.hash_table[self.binary_heap_array[j].key] = j

    def shift_up(self, i):
        parent = (i - 1) // 2
        while i > 0 and self.binary_heap_array[parent].key > self.binary_heap_array[i].key:
            self.swap(i, parent)
            i = parent
            parent = (i - 1) // 2

    def shift_down(self, i):
        n = self.size()
        while 2 * i + 1 < n:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = left
            if right < n and self.binary_heap_array[right].key < self.binary_heap_array[left].key:
                smallest = right
            if self.binary_heap_array[i].key <= self.binary_heap_array[smallest].key:
                break
            self.swap(i, smallest)
            i = smallest

    def add(self, key, value):
        if key in self.hash_table:
            return False
        self.binary_heap_array.append(Node(key, value))
        if self.size() == 0:
            self.hash_table[key] = 0
        else:
            index = self.size() - 1
            self.hash_table[key] = index
            self.shift_up(index)
        return True

    def set(self, key, value):
        if key not in self.hash_table:
            return False
        self.binary_heap_array[self.hash_table[key]].value = value
        return True

    def delete(self, key):
        if key not in self.hash_table:
            return False
        if self.size() == 1:
            self.binary_heap_array.clear()
            self.hash_table.clear()
        else:
            index = self.hash_table[key]
            new_key = self.binary_heap_array[0].key - 1
            self.hash_table.pop(key)
            self.hash_table[new_key] = index
            self.binary_heap_array[index].key = new_key
            self.shift_up(index)
            self.extract_root()
        return True

    def search(self, key):
        if key not in self.hash_table:
            return None
        return self.hash_table[key], self.binary_heap_array[self.hash_table[key]].value

    def extract_root(self):
        if self.size() == 0:
            return None
        out = deepcopy(self.binary_heap_array[0])
        self.binary_heap_array[0] = self.binary_heap_array.pop(self.size() - 1)
        self.hash_table[self.binary_heap_array[0].key] = 0
        self.hash_table.pop(out.key)
        self.shift_down(0)
        return out

    def min(self):
        if self.size() == 0:
            raise None
        return self.binary_heap_array[0].key, 0, self.binary_heap_array[0].value

    def max(self):
        if self.size() == 0:
            raise None
        current_index = self.size() - 1
        index_max = self.size() - 1
        while current_index >= self.size() // 2:
            if self.binary_heap_array[current_index].key > self.binary_heap_array[index_max].key:
                index_max = current_index
            current_index -= 1
        return self.binary_heap_array[index_max].key, index_max, self.binary_heap_array[index_max].value

    def size(self):
        return len(self.binary_heap_array)

    def print(self, stream=None):
        if self.size() == 0:
            print('_')
            return
        print(f'[{self.binary_heap_array[0].key} {self.binary_heap_array[0].value}]')
        level = 1
        i = 1
        while i < self.size():
            level_size = 1 << level
            level_end = min(i + level_size, self.size())
            line_parts = []
            for pos in range(i, level_end):
                parent_index = (pos - 1) // 2
                line_parts.append(
                    f'[{self.binary_heap_array[pos].key} {self.binary_heap_array[pos].value} {self.binary_heap_array[parent_index].key}]')
            while len(line_parts) < level_size:
                line_parts.append('_')
            print(' '.join(line_parts))
            i = level_end
            level += 1


if __name__ == "__main__":
    binaryHeap = MinBinaryHeap()
    for line in stdin.readlines():
        try:
            command = line.split()
            if command[0] == "add":
                if len(command) == 3:
                    if not binaryHeap.add(int(command[1]), command[2]): print("error")
                elif len(command) == 2:
                    if not binaryHeap.add(int(command[1]), ''): print("error")
                else:
                    print("error")
            elif command[0] == "set":
                if len(command) == 3:
                    if not binaryHeap.set(int(command[1]), command[2]): print("error")
                elif len(command) == 2:
                    if not binaryHeap.set(int(command[1]), ''): print("error")
                else:
                    print("error")
            elif command[0] == "delete" and len(command) == 2:
                if not binaryHeap.delete(int(command[1])): print("error")
            elif command[0] == "search" and len(command) == 2:
                result = binaryHeap.search(int(command[1]))
                if result is not None:
                    print(f"1 {result[0]} {result[1]}")
                else:
                    print("0")
            elif command[0] == "extract" and len(command) == 1:
                root = binaryHeap.extract_root()
                if root is not None:
                    print(f"{root.key} {root.value}")
                else:
                    print("error")
            elif command[0] == "min" and len(command) == 1:
                min_node = binaryHeap.min()
                if min_node is not None:
                    print(f"{min_node[0]} {min_node[1]} {min_node[2]}")
                else:
                    print("error")
            elif command[0] == "max" and len(command) == 1:
                max_node = binaryHeap.max()
                if max_node is not None:
                    print(f"{max_node[0]} {max_node[1]} {max_node[2]}")
                else:
                    print("error")
            elif command[0] == "print" and len(command) == 1:
                binaryHeap.print()
            else:
                raise Exception
        except Exception as ex:
            print("error")
