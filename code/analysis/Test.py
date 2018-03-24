def binary_search(num, list):
    low = 0
    high = len(list) - 1
    while (low <= high):
        middle = int((low + high) / 2)
        if list[middle] > num:
            high = middle - 1
        elif list[middle] < num:
            low = middle + 1
        else:
            return middle
    return -1


if __name__ == '__main__':
    list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    num = 1
    location = binary_search(num, list1)
    print(location)
