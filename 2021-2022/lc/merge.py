
def merge(nums1, m, nums2, n):
    del nums1[m:]
    del nums2[n:]
    l = m + n
    i1 = 0
    i2 = 0
    if m == 0:
        for i in range(n):
            nums1.insert(i,nums2[i])
        m = n
    elif n != 0:
        while (m < l):
            while i1 <= (m - 1) and nums1[i1] < nums2[i2]:
                i1 += 1
            while (i1 == m or nums1[i1] >= nums2[i2]) and i2 <= (n - 1):
                nums1.insert(i1, nums2[i2])
                print(nums1)
                i2 += 1
                i1 += 1
                m += 1
    print(nums1)

nums1, m, nums2, n = [0,0,0,0,0],0,[1,2,3,4,5],5
merge(nums1, m, nums2, n)
