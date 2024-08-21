import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read data from CSV file
df = pd.read_csv('data.csv')  # Ensure 'data.csv' is in the correct path

# Display the first few rows of the dataframe
print("First few rows of the data:")
print(df.head())

# 1. Descriptive Statistics
print("\nDescriptive Statistics:")
print(df.describe(include='all'))

# 2. Counts of each betting type
print("\nCounts of Each Betting Type:")
print(df['Betted On'].value_counts())

# 3. Loss and Win Analysis
loss_win_summary = df.groupby('Betted On').agg({
    'Losscount': 'sum',
    'Wincount': 'sum',
    'CurrentValue': 'mean'
}).reset_index()
print("\nLoss and Win Summary:")
print(loss_win_summary)

# 4. Visualizations

# 4.1. Distribution of Current Values
plt.figure(figsize=(12, 6))
sns.histplot(df['CurrentValue'], kde=True, bins=10)
plt.title('Distribution of Current Values')
plt.xlabel('Current Value')
plt.ylabel('Frequency')
plt.grid(True)

# Add description text to the plot
plt.text(x=0.95, y=0.95, s='Histogram showing the distribution of Current Value.\n'
                            'X-axis: Current Value\n'
                            'Y-axis: Frequency\n'
                            'KDE line indicates the smooth distribution.',
         ha='right', va='top', transform=plt.gca().transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.7))

plt.show()

# 4.2. Boxplot of Current Values by Betting Type
plt.figure(figsize=(12, 6))
sns.boxplot(x='Betted On', y='CurrentValue', data=df)
plt.title('Boxplot of Current Values by Betting Type')
plt.xlabel('Betted On')
plt.ylabel('Current Value')
plt.grid(True)

# Add description text to the plot
plt.text(x=0.95, y=0.95, s='Boxplot comparing Current Value for each Betting Type.\n'
                            'X-axis: Betting Type\n'
                            'Y-axis: Current Value\n'
                            'Box shows the range (IQR) and median value.\n'
                            'Whiskers extend to the range excluding outliers.',
         ha='right', va='top', transform=plt.gca().transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.7))

plt.show()

# 4.3. Scatter Plot of Losscount vs. Wincount
plt.figure(figsize=(12, 6))
scatter_plot = sns.scatterplot(x='Losscount', y='Wincount', hue='Betted On', data=df, palette='viridis')
plt.title('Scatter Plot of Losscount vs. Wincount')
plt.xlabel('Losscount')
plt.ylabel('Wincount')

# Adding annotations for better understanding
for i in range(len(df)):
    scatter_plot.text(df['Losscount'][i], df['Wincount'][i], f'{df["CurrentValue"][i]:,.0f}', 
                      color='black', fontsize=9, ha='right')

# Add description text to the plot
plt.text(x=0.95, y=0.95, s='Scatter plot showing the relationship between Losscount and Wincount.\n'
                            'X-axis: Losscount\n'
                            'Y-axis: Wincount\n'
                            'Color represents Betting Type.\n'
                            'Annotations show the Current Value for each point.',
         ha='right', va='top', transform=plt.gca().transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.7))

plt.grid(True)
plt.legend(title='Betted On')
plt.show()

# 4.4. Heatmap of Correlations
plt.figure(figsize=(10, 8))
correlation_matrix = df[['CurrentValue', 'Losscount', 'Wincount']].corr()
heatmap = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, fmt='.2f')
plt.title('Correlation Heatmap')

# Add description text to the plot
plt.text(x=0.95, y=0.95, s='Heatmap showing correlations between variables.\n'
                            'Color indicates the strength and direction of correlation.\n'
                            'Values range from -1 (perfect negative) to 1 (perfect positive).',
         ha='right', va='top', transform=plt.gca().transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.7))

plt.show()
