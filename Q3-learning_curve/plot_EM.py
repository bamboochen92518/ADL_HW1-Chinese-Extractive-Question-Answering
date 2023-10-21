import matplotlib.pyplot as plt

# Step 3: Create Data
x = [0, 1, 2, 3, 4]
y = [0.788634, 0.809904, 0.797939, 0.791625, 0.79661]

plt.xlabel('epoch')
plt.ylabel('exact match')

# Step 4: Plot the Data
plt.plot(x, y)
plt.xticks(x)
plt.scatter(x, y, color='red', marker='o', label='Data Points')

# Step 5: Show the Chart
plt.show()

