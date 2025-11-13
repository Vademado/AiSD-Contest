from collections import deque
from sys import stdin


class Node:
    def __init__(self, key, value, parent=None, left=None, right=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right


class SplayTree:
    def __init__(self):
        self.root = None

    def right_rotate(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right is not None:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

    def left_rotate(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left is not None:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    def splay(self, node):
        while node.parent is not None:
            if node == node.parent.left:  # node - левый ребенок
                if node.parent.parent is None:
                    self.right_rotate(node.parent)  # Zig (правый)
                elif node.parent.parent.left == node.parent:
                    self.right_rotate(node.parent.parent)  # Zig-zig (правый-правый)
                    self.right_rotate(node.parent)
                else:
                    self.right_rotate(node.parent)  # Zig-zag (правый-левый)
                    self.left_rotate(node.parent)
            else:  # node - правый ребенок
                if node.parent.parent is None:
                    self.left_rotate(node.parent)  # Zig (левый)
                elif node.parent.parent.right == node.parent:
                    self.left_rotate(node.parent.parent)  # Zig-zig (левый-левый)
                    self.left_rotate(node.parent)
                else:
                    self.left_rotate(node.parent)  # Zig-zag (левый-правый)
                    self.right_rotate(node.parent)

    def find(self, key):
        if self.root is None:
            return None
        prev_node, current_node = None, self.root
        while current_node is not None:
            prev_node = current_node
            if key > current_node.key:
                current_node = current_node.right
            elif key < current_node.key:
                current_node = current_node.left
            else:
                return current_node
        return prev_node

    def add(self, key, value):
        find_node = self.find(key)
        if find_node and find_node.key == key:
            self.splay(find_node)
            return False
        new_node = Node(key, value)
        prev_node, current_node = None, self.root
        while current_node is not None:
            prev_node = current_node
            if key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        new_node.parent = prev_node
        if prev_node is None:
            self.root = new_node
        elif new_node.key > prev_node.key:
            prev_node.right = new_node
        else:
            prev_node.left = new_node
        self.splay(new_node)
        return True

    def set(self, key, value):
        find_node = self.find(key)
        if find_node is None or find_node.key != key:
            if find_node is not None:
                self.splay(find_node)
            return False
        find_node.value = value
        self.splay(find_node)
        return True

    def delete(self, key):
        find_node = self.find(key)
        if find_node is None:
            return False
        self.splay(find_node)
        if find_node.key != key:
            return False
        if find_node.left is None:
            self.root = find_node.right
            if self.root is not None:
                self.root.parent = None
            return True
        if find_node.right is None:
            self.root = find_node.left
            find_node.left.parent = None
            return True
        find_node.left.parent = None
        o = find_node.left
        while o.right:
            o = o.right
        self.splay(o)
        if find_node.right:
            o.right = find_node.right
            find_node.right.parent = o
        self.root = o
        return True

    def search(self, key):
        if self.root is None:
            return None
        prev_node, current_node = None, self.root
        while current_node is not None:
            prev_node = current_node
            if key > current_node.key:
                current_node = current_node.right
            elif key < current_node.key:
                current_node = current_node.left
            else:
                self.splay(current_node)
                return current_node
        self.splay(prev_node)
        return None

    def min(self):
        if self.root is None:
            return None
        current_node = self.root
        while current_node.left is not None:
            current_node = current_node.left
        self.splay(current_node)
        return current_node

    def max(self):
        if self.root is None:
            return None
        current_node = self.root
        while current_node.right is not None:
            current_node = current_node.right
        self.splay(current_node)
        return current_node

    def height_tree(self, node):
        if node is None:
            return 0
        return 1 + max(self.height_tree(node.left), self.height_tree(node.right))

    def print(self):
        if self.root is None:
            print('_')
            return
        q = deque()
        pos = deque()
        print(f'[{self.root.key} {self.root.value}]')
        if self.root.left is not None:
            q.append(self.root.left)
            pos.append(0)
        if self.root.right is not None:
            q.append(self.root.right)
            pos.append(1)
        height = self.height_tree(self.root)
        nums_of_nodes = len(pos)
        if nums_of_nodes == 0:
            return
        curr = pos.popleft()
        for level in range(1, height):
            curr_pos = 0
            width_level = 2 ** level
            while nums_of_nodes != 0:
                if curr_pos == curr:
                    nums_of_nodes -= 1
                    node = q.popleft()
                    parent_key = node.parent.key if node.parent is not None else '_'
                    if curr != width_level - 1:
                        print(f'[{node.key} {node.value} {parent_key}] ', end='')
                    else:
                        print(f'[{node.key} {node.value} {parent_key}]', end='')
                    if node.left is not None:
                        q.append(node.left)
                        pos.append(2 * curr)
                    if node.right is not None:
                        q.append(node.right)
                        pos.append(2 * curr + 1)
                    curr_pos = curr + 1
                    if len(pos) != 0:
                        curr = pos.popleft()
                elif curr - curr_pos != 0:
                    print('_ ' * (curr - curr_pos), end='')
                    curr_pos = curr
                if nums_of_nodes == 0:
                    print('_ ' * (width_level - curr_pos - 1), end='')
                    if curr_pos != width_level:
                        print('_', end='')
            nums_of_nodes = len(pos) + 1
            print()


if __name__ == "__main__":
    splayTree = SplayTree()
    for line in stdin.readlines():
        try:
            command = line.split()
            if command[0] == "add":
                if len(command) == 3:
                    if not splayTree.add(int(command[1]), command[2]): print("error")
                elif len(command) == 2:
                    if not splayTree.add(int(command[1]), ''): print("error")
                else: print("error")
            elif command[0] == "set":
                if len(command) == 3:
                    if not splayTree.set(int(command[1]), command[2]): print("error")
                elif len(command) == 2:
                    if not splayTree.set(int(command[1]), ''): print("error")
                else: print("error")
            elif command[0] == "delete" and len(command) == 2:
                if not splayTree.delete(int(command[1])): print("error")
            elif command[0] == "search" and len(command) == 2:
                result = splayTree.search(int(command[1]))
                if result is not None:
                    print(f"1 {result.value}")
                else:
                    print("0")
            elif command[0] == "min" and len(command) == 1:
                min_node = splayTree.min()
                if min_node is not None:
                    print(f"{min_node.key} {min_node.value}")
                else:
                    print("error")
            elif command[0] == "max" and len(command) == 1:
                max_node = splayTree.max()
                if max_node is not None:
                    print(f"{max_node.key} {max_node.value}")
                else:
                    print("error")
            elif command[0] == "print" and len(command) == 1:
                splayTree.print()
            else:
                raise Exception
        except Exception as ex:
            print("error")
