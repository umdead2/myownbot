N= map(int, input().split())
numbers = list(map(int, input().split()))

largest = -10**18
secondlargest = -10**18

for i in range(len(numbers)):
    if numbers[i]> secondlargest:
        if numbers[i]> largest:
            largest = numbers[i]
        else:
            secondlargest = numbers[i]
print(largest)
print(secondlargest)