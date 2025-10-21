from sys import stdin


class MyDeque:
    def __init__(self):
        self.size = 0
        self.start = 0
        self.capacity = None
        self.deque_array = []

    def set_size(self, size):
        self.capacity = size
        self.deque_array = [None] * size

    def pushb(self, x):
        self.deque_array[(self.start + self.size) % self.capacity] = x
        if self.size < self.capacity:
            self.size += 1
        else:
            self.start = (self.start + 1) % self.capacity

    def pushf(self, x):
        self.deque_array[(self.start - 1) % self.capacity] = x
        if self.size < self.capacity: self.size += 1
        self.start = (self.start - 1) % self.capacity

    def popb(self):
        if not self.size: return "underflow"
        self.size -= 1
        return self.deque_array[(self.start + self.size) % self.capacity]

    def popf(self):
        if not self.size: return "underflow"
        self.size -= 1
        self.start = (self.start + 1) % self.capacity
        return self.deque_array[(self.start - 1) % self.capacity]

    def print(self):
        print(" ".join([self.deque_array[i % self.capacity] for i in range(self.start, self.start + self.size) if
                        self.deque_array[i % self.capacity] is not None]) if self.size > 0 else "empty")


myDeque = MyDeque()
if __name__ == '__main__':
    for line in stdin.readlines():
        if line == "\n": continue
        command = line.split(" ")
        if len(command) == 1 and any(
                i == command[0].strip() for i in ["popf", "popb", "print"]) and myDeque.capacity is not None:
            command = command[0].strip()
            if command == "popf":
                print(myDeque.popf())
            elif command == "popb":
                print(myDeque.popb())
            else:
                myDeque.print()
        elif len(command) == 2 and any(i in command for i in ["set_size", "pushf", "pushb"]):
            if command[0] == "set_size":
                if command[1].strip().isdigit() and int(command[1]) >= 0 and not myDeque.capacity:
                    myDeque.set_size(int(command[1].strip()))
                else:
                    print("error")
            elif (command[0] == "pushf" or command[0] == "pushb") and myDeque.capacity is not None:
                if myDeque.size == myDeque.capacity:
                    print("overflow")
                elif command[0] == "pushf":
                    myDeque.pushf(command[1].strip())
                elif command[0] == "pushb":
                    myDeque.pushb(command[1].strip())
            else:
                print("error")
        else:
            print("error")
