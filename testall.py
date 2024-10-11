def is_alternating(arr):
    # Check if the length of the array is less than 4
    if len(arr) < 4:
        return False
    
    # Get the last 4 characters of the array
    last_four = arr[-4:]
    
    # Check if the last four characters alternate
    if (last_four[0] != last_four[1] and
        last_four[1] != last_four[2] and
        last_four[2] != last_four[3] and
        last_four[0] == last_four[2] and
        last_four[1] == last_four[3]):
        return True
    return False

# Example usage
arr = ['D', 'T', 'D', 'T', 'D', 'T']
print(is_alternating(arr))  # Output: True

arr = ['D', 'D', 'T', 'D', 'T', 'D']
print(is_alternating(arr))  # Output: False
