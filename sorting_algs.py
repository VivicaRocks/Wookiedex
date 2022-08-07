import time
from random import randint


def merge_sort(array):
    arr0 = array
    if len(arr0) > 1:
        halflength = int(len(array)/2)
        arr1 = arr0[:halflength]
        arr2 = arr0[halflength:]
        arr1 = merge_sort(arr1)
        arr2 = merge_sort(arr2)

        arr0 = []

        while len(arr1) > 0 and len(arr2) > 0:
            if arr1[0] < arr2[0]:
                arr0.append(arr1[0])
                arr1.pop(0)
            else:
                arr0.append(arr2[0])
                arr2.pop(0)
        while len(arr1) > 0:
            arr0.append(arr1[0])
            arr1.pop(0)
        while len(arr2) > 0:
            arr0.append(arr2[0])
            arr2.pop(0)
    return arr0


def bubble_sort(array):
    arr = array
    swap = False
    for i in range(len(arr)-1):
        if arr[i] > arr[i+1]:
            value = arr.pop(i)
            arr.insert(i+1, value)
            swap = True
    if swap:
        return bubble_sort(arr)
    else:
        return arr

def insertion_sort(array):
    arr = array
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -=1
        arr[j+1] = key
    return arr

def compare_sorts(num):
    array = randomarray(num)

    time1merge = time.time()
    merged = merge_sort(array)
    time2merge = time.time()
    mergetime = time2merge - time1merge

    time1bubble = time.time()
    bubbled = merge_sort(array)
    time2bubble = time.time()
    bubbletime = time2bubble - time1bubble

    time1insert = time.time()
    inserted = insertion_sort(array)
    time2insert = time.time()
    inserttime = time2insert - time1insert

    time1sortmethod = time.time()
    sortmethod = sorted(array)
    time2sortmethod = time.time()
    sortmethodtime = time2sortmethod - time1sortmethod

    print(f'Merge sort completed in:{mergetime}')
    print(f'Bubble sort completed in:{bubbletime}')
    print(f'Insertion sort completed in:{inserttime}')
    print(f'Sort built-in finished in:{sortmethodtime}')

def randomarray(array_length):
    array = [randint(1, 1000) for i in range(array_length)]
    return array








