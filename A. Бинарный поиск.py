from sys import stdin


def binsearch(left, right, k, array):
    if left > right:
        return -1
    middle = (left + right) // 2
    if array[middle] == k:
        if middle == 0 or array[middle - 1] < k:
            return middle
        else:
            return binsearch(left, middle - 1, k, array)
    elif array[middle] < k:
        return binsearch(middle + 1, right, k, array)
    else:
        return binsearch(left, middle - 1, k, array)


arr = list(map(int, stdin.readline().split()))
for command in stdin.readlines():
    action, k = command.split()
    if action == 'search':
        print(binsearch(0, len(arr) - 1, int(k), arr))
