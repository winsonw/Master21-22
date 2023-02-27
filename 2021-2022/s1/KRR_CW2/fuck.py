def xyx( s ):
    return len(s) < 2 or ( s[0] == s[-1] and xyx( s[1: -1] ) )

def xyx_key(n):
    s = str(n)
    l = len(s)
    if xyx(s) and l%2==0:
        return int( s[:int(l/2)] )
    return False


def sum_of_things(n):
    i = 2
    total = 0
    count = 0
    while count < n:
        for j in range(2, i//2 + 1):
            if i%j == 0:
                break
        else:
            total += i
            count += 1
        i += 1
    return total

def b_force_2():
    index = 0
    key = sum_of_things(index)
    while key != 3682913:
        index +=1
        key = sum_of_things(index)
    return index


def b_force_1():
    index = 12458910000000
    key = xyx_key(index)
    while not key or key != 1245891:
        index +=1
        key = xyx_key(index)
    return index

import random
def again():
    # Set temp to random value in range 1-100.
    temp = random.randint(1, 100)

    # Check whether temp is in tolerable range.
    if (temp > 16 or temp < 27):
        print("Temperature tolerable. :)")
    else:
        print("Temperature intolerable. :(")


if __name__ == "__main__":
    again()



