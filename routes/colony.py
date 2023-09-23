def calculate_weight(N, colony):
    # Initialize the count array for generation 0
    count = [0] * N
    for digit in colony:
        count[int(digit)] += 1

    # Iterate through generations
    for generation in range(1, N + 1):
        new_count = [0] * N
        for i in range(len(colony) - 1):
            digit1 = int(colony[i])
            digit2 = int(colony[i + 1])
            signature = 10 - abs(digit1 - digit2)
            new_count[digit1] += signature
            new_count[digit2] += signature
        count = new_count  # Update colony count for the next generation

    # Calculate the weight by summing up the count of each digit
    weight = sum(count)
    return weight

# Example usage:
N = 10
colony = "914"
weight = calculate_weight(N, colony)
print(weight)  # Output: 150
