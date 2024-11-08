"""
mcu
"""
length = 10
# numbers = random.sample(range(1, 11), length)
numbers = [2, 1, 2, 2, 0, 1, 2, 2, 2, 0]
print(numbers)
N = 3

sum_max = 0
for i in range(length - N + 1):
    window_left = i
    window_right = i + N
    # if window_right > length:
    #     break
    sum_ = sum(numbers[window_left:window_right])
    sum_max = max(sum_, sum_max)

print(sum_max)

# for right, num_right in enumerate(numbers, N):
#     print(right, num_right)
