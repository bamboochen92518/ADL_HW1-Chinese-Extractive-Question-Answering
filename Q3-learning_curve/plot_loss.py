import matplotlib.pyplot as plt

# Step 3: Create Data
x = [0, 1, 2, 3, 4]
y = [1.0062, 0.5632, 0.4177, 0.3313, 0.2799]

plt.xlabel('epoch')
plt.ylabel('loss')

# Step 4: Plot the Data
plt.plot(x, y)
plt.xticks(x)
plt.scatter(x, y, color='red', marker='o', label='Data Points')

# Step 5: Show the Chart
plt.show()

