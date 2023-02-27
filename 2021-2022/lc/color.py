
def sortColors(nums):
    l = len(nums)
    count = [0,0,0]
    for i in nums:
        count[i] += 1
    for index in range(l):
        if count[0] > index:
            nums[index] = 0
        elif (l - count[2]) <= index:
            nums[index] = 2
        else:
            nums[index] = 1

sortColors(nums)
