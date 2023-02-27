
def removeDuplicates(nums):
    l = len(nums) - 1
    index = 1
    count = True
    num = nums[0]
    while (index <= l):
        if nums[index] == num:
            if count:
                count = False
                index += 1
            else:
                nums.pop(index)
                l -=1
        else:
            num = nums[index]
            count = True
            index +=1

nums = [0,0,1,1,1,1,2,3,3]
removeDuplicates(nums)
