def fibonacci(n):
    """Calculate the first n Fibonacci numbers."""
    fib_sequence = []
    a, b = 0, 1
    for _ in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence

# Calculate and print the first 10 Fibonacci numbers
result = fibonacci(10)
print("The first 10 Fibonacci numbers are:")
print(result)
