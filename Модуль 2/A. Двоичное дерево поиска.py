from sys import stdin


class Node:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent

        self.left = None
        self.right = None

    def __eq__(self, other):
        return self.key == other.key


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def add(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
            return True
        parent = self.root
        while parent is not None:
            if key > parent.key:
                if parent.right is not None:
                    parent = parent.right
                else:
                    parent.right = Node(key, value, parent)
                    break
            elif key < parent.key:
                if parent.left is not None:
                    parent = parent.left
                else:
                    parent.left = Node(key, value, parent)
                    break
            else:
                print("error")
                return False
        return True

    def set(self, key, value):
        if self.root is None:
            print("error")
            return False
        parent = self.root
        while parent is not None:
            if key > parent.key:
                if parent.right is not None:
                    parent = parent.right
                else:
                    print("error")
                    return False
            elif key < parent.key:
                if parent.left is not None:
                    parent = parent.left
                else:
                    print("error")
                    return False
            else:
                parent.value = value
                break
        return True

    def next(self, key):
        current = self.root
        successor = None
        while current is not None:
            if current.key > key:
                successor = current
                current = current.left
            else:
                current = current.right
        return successor

    def prev(self, key):
        current = self.root
        predecessor = None
        while current is not None:
            if current.key < key:
                predecessor = current
                current = current.right
            else:
                current = current.left
        return predecessor

    def delete_left(self, key):
        if self.root is None:
            print("error")
            return False
        deleted_node = self.root
        while deleted_node is not None:
            if key > deleted_node.key:
                if deleted_node.right is not None:
                    deleted_node = deleted_node.right
                else:
                    print("error")
                    return False
            elif key < deleted_node.key:
                if deleted_node.left is not None:
                    deleted_node = deleted_node.left
                else:
                    print("error")
                    return False
            else:
                break

        parent = deleted_node.parent
        if deleted_node.left is None and deleted_node.right is None:  # первый случай: удаляемый элемент - лист
            if parent is None:
                self.root = None
            else:
                if parent.left is deleted_node:
                    parent.left = None
                if parent.right is deleted_node:
                    parent.right = None
        elif deleted_node.left is None or deleted_node.right is None:  # второй случай: удаляемый элемент имеет одного потомка
            if deleted_node.left is None:
                if parent is None:
                    self.root = deleted_node.right
                elif parent.left is deleted_node:
                    parent.left = deleted_node.right
                else:
                    parent.right = deleted_node.right
                deleted_node.right.parent = parent
            else:
                if parent is None:
                    self.root = deleted_node.left
                elif parent.left is deleted_node:
                    parent.left = deleted_node.left
                else:
                    parent.right = deleted_node.left
                deleted_node.left.parent = parent
        else:  # третий случай: удаляемый элемент имеет двух потомков
            predecessor = self.prev(deleted_node.key)
            deleted_node.key = predecessor.key
            deleted_node.value = predecessor.value
            if predecessor.parent.left is predecessor:
                predecessor.parent.left = predecessor.left
                if predecessor.left is not None:
                    predecessor.left.parent = predecessor.parent
            else:
                predecessor.parent.right = predecessor.left
                if predecessor.left is not None:
                    predecessor.left.parent = predecessor.parent
        return True

    def delete_right(self, key):
        if self.root is None:
            print("error")
            return False
        deleted_node = self.root
        while deleted_node is not None:
            if key > deleted_node.key:
                if deleted_node.right is not None:
                    deleted_node = deleted_node.right
                else:
                    print("error")
                    return False
            elif key < deleted_node.key:
                if deleted_node.left is not None:
                    deleted_node = deleted_node.left
                else:
                    print("error")
                    return False
            else:
                break

        parent = deleted_node.parent
        if deleted_node.left is None and deleted_node.right is None:  # первый случай: удаляемый элемент - лист
            if parent is None:
                self.root = None
            else:
                if parent.left is deleted_node:
                    parent.left = None
                if parent.right is deleted_node:
                    parent.right = None
        elif deleted_node.left is None or deleted_node.right is None:  # второй случай: удаляемый элемент имеет одного потомка
            if deleted_node.left is None:
                if parent is None:
                    self.root = deleted_node.right
                elif parent.left is deleted_node:
                    parent.left = deleted_node.right
                else:
                    parent.right = deleted_node.right
                deleted_node.right.parent = parent
            else:
                if parent is None:
                    self.root = deleted_node.left
                elif parent.left is deleted_node:
                    parent.left = deleted_node.left
                else:
                    parent.right = deleted_node.left
                deleted_node.left.parent = parent
        else:  # третий случай: удаляемый элемент имеет двух потомков
            successor = self.next(deleted_node.key)
            deleted_node.key = successor.key
            deleted_node.value = successor.value
            if successor.parent.left is successor:
                successor.parent.left = successor.right
                if successor.right is not None:
                    successor.right.parent = successor.parent
            else:
                successor.parent.right = successor.right
                if successor.right is not None:
                    successor.right.parent = successor.parent
        return True

    def search(self, key):
        if self.root is None:
            return "0"
        parent = self.root
        while parent is not None:
            if key > parent.key:
                if parent.right is not None:
                    parent = parent.right
                else:
                    return "0"
            elif key < parent.key:
                if parent.left is not None:
                    parent = parent.left
                else:
                    return "0"
            else:
                return f"1 {parent.value}"

    def min(self):
        if self.root is None:
            return "error"
        parent = self.root
        while parent is not None:
            if parent.left is None:
                return f"{parent.key} {parent.value}"
            parent = parent.left

    def max(self):
        if self.root is None:
            return "error"
        parent = self.root
        while parent is not None:
            if parent.right is None:
                return f"{parent.key} {parent.value}"
            parent = parent.right

    def print(self):
        if self.root is None:
            print("_")
            return True

        queue = [self.root]
        levels = []

        while queue:
            level_nodes = []
            level_size = len(queue)
            has_next_level = False

            for i in range(level_size):
                node = queue.pop(0)
                if node is None:
                    level_nodes.append("_")
                    queue.extend([None, None])
                else:
                    if node == self.root:
                        level_nodes.append(f"[{node.key} {node.value}]")
                    else:
                        level_nodes.append(f"[{node.key} {node.value} {node.parent.key}]")

                    left_child = node.left if node.left else None
                    right_child = node.right if node.right else None
                    queue.extend([left_child, right_child])

                    if left_child is not None or right_child is not None:
                        has_next_level = True

            levels.append(" ".join(level_nodes))

            if not has_next_level:
                break

        for level in levels:
            print(level)
        return True


if __name__ == "__main__":
    newBTS = BinarySearchTree()
    for line in stdin.readlines():
        try:
            command = line.split()
            if command[0] == "add" and len(command) == 3:
                newBTS.add(int(command[1]), command[2])
            elif command[0] == "set" and len(command) == 3:
                newBTS.set(int(command[1]), command[2])
            elif command[0] == "delete" and len(command) == 2:
                newBTS.delete_left(int(command[1]))
            elif command[0] == "search" and len(command) == 2:
                print(newBTS.search(int(command[1])))
            elif command[0] == "min" and len(command) == 1:
                print(newBTS.min())
            elif command[0] == "max" and len(command) == 1:
                print(newBTS.max())
            elif command[0] == "print" and len(command) == 1:
                newBTS.print()
            else:
                raise Exception
        except Exception as ex:
            print("error")
