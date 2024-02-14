import numpy as np

# Create a 2D numpy array
arr_2d = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Method 1: Using flatten()
arr_1d_flatten = arr_2d.flatten()

# Method 2: Using ravel()
arr_1d_ravel = arr_2d.ravel()

# Printing the original and flattened arrays
print("Original 2D Array:")
print(arr_2d)
print("\nFlattened Array (using flatten()):")
print(arr_1d_flatten)
print("\nFlattened Array (using ravel()):")
print(arr_1d_ravel)
