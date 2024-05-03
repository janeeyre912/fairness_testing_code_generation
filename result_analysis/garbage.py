import matplotlib.pyplot as plt

# Example data (modify with your actual data)
x_axis = [1, 1, 1.1, 1.1, 2, 2, 2.1, 2.1, 3, 3, 4, 4, 5, 5]  # Adjusted with close points
y_axis = [0.2, 0.4, 0.3, 0.5, 0.1, 0.3, 0.2, 0.4, 0.7, 0.5, 0.8, 0.6, 0.9, 0.1]

# Category data (dictionary with colors)
categories = {'religion': 'red', 'gender': 'blue', 'age': 'green', 'race': 'yellow',
               'education': 'purple', 'employment_status': 'orange', 'marital_status': 'black'}

# Point sizes (adjusted for different categories)
point_sizes = {'religion': 150, 'gender': 120, 'age': 100, 'race': 80,
               'education': 130, 'employment_status': 110, 'marital_status': 90}

# Create the scatter plot
plt.figure(figsize=(12, 10))  # Adjust figure size for better visibility

# Scatter plot with loop to handle categories and colors
for category, color in categories.items():
    # Filter data points for each category
    category_x = [x for x, c in zip(x_axis, categories.values()) if c == color]
    category_y = [y for y, c in zip(y_axis, categories.values()) if c == color]

    # Plot data for each category with adjusted size
    plt.scatter(category_x, category_y, marker='o', alpha=0.7, color=color, label=category, s=point_sizes[category])

# Customize plot elements
plt.xlabel('Models')  # Rename x-axis label
plt.ylabel('Temperature')  # Rename y-axis label
plt.title('Scatter Plot with Multiple Categories (Example)')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.legend(title='Categories')
plt.tight_layout()
plt.show()
