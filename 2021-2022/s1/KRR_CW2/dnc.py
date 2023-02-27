
n = 5
A = [4, 2, 1, 3, 5]


def main():
    global count
    count = 0
    print(wai(A))
    print("count", count)
    print(A)


def wai(A):
    return waih(A, 0, n-1)


def waih(A, l, r):
    global count
    count += 1
    print("no", count,";", A,l,r)

    if l < r:
        s = int((l + r) / 2)
        p = A[s]

        s = partition(A, l, r, s)
        print(s,l,r,A)

        if s == int(n / 2):
            return p
        if s < int(n / 2):
            return waih(A, s+1, r)
        return waih(A, l, s-1)
    return A[l]


def partition(A, l, r, s):
    i = l
    j = r - 1
    p = A[s]
    while i < j:
        while A[i] <= p and i<r:
            i += 1
        while j > i and A[j]>p:
            j -= 1
        print(i,j)
        if i<j:
            t = A[j]
            A[j] = A[i]
            A[i] = t
    # print(t,r)
    # t = A[r]
    # A[r] = A[i]
    # A[i] = t
    return i

# def partition_1(arr, low, high):
#     i = (low - 1)  # index of smaller element
#     pivot = arr[high]  # pivot
#
#     for j in range(low, high):
#
#         # If current element is smaller than or
#         # equal to pivot
#         if arr[j] <= pivot:
#             # increment index of smaller element
#             i = i + 1
#             arr[i], arr[j] = arr[j], arr[i]
#
#     arr[i + 1], arr[high] = arr[high], arr[i + 1]
#     print(arr)
#     return (i + 1)


def test():
    l = 0
    r = 4
    s = 4
    A = [4, 2, 1, 3, 5]
    s = partition(A, l, r, s)
    print(s, A)



if __name__ == "__main__":
    main()
    # test()
