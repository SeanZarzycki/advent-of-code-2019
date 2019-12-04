hi = 643281
lo = 128392

def num_good(num):
    last = 10
    adj = False
    digits = []
    last_last = 10
    while num > 0:
        check = num % 10
        digits.append(check)
        if last < check:
            return False
        last = check
        num = int(num / 10)
    adj = False
    trip = False
    trip_digits = []
    adj_digits = []
    for i in range(len(digits)-2):
        if digits[i] == digits[i+1] and digits[i] == digits[i+2]:
            trip_digits.append(digits[i])
        if digits[i] == digits[i+1]:
            adj_digits.append(digits[i])
    if digits[4] == digits[5]:
        adj_digits.append(digits[4])
    
    only_dubs = [x for x in adj_digits if x not in trip_digits]
    return len(only_dubs) > 0

count = 0
for i in range(lo, hi):
    if num_good(i):
        count = count + 1

print(count)