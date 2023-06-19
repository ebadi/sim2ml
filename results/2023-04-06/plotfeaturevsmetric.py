import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read input vectors from CSV file
X = pd.read_csv('2023-04-06-16-51-18X.csv', header=0)

# Read output metrics from CSV file
y = pd.read_csv('2023-04-06-16-51-18Y-summary.csv', header=0)

input_feature_name = 'Hour'  # Change this to the name of the desired input feature column
output_metric_name = 'num_of_detection'  # Change this to the name of the desired output metric column

num_bins = 10  # Number of bins to split x-axis into

# Get min and max values of input feature
xmin = X[input_feature_name].min()
xmax = X[input_feature_name].max()

# Calculate bin edges
bin_edges = np.linspace(xmin, xmax, num_bins + 1)

# Get indices of the bin that each input value belongs to
bin_indices = np.digitize(X[input_feature_name], bin_edges)

# Calculate mean and variance of output metric for each bin
means = []
variances = []
for i in range(1, num_bins + 1):
    bin_mask = bin_indices == i
    bin_values = y.loc[bin_mask, output_metric_name]
    means.append(np.mean(bin_values))
    variances.append(np.var(bin_values))

# Generate bar plot of mean and variance for each bin
fig, ax = plt.subplots()
ax.bar(range(num_bins), means, yerr=variances, align='center')
ax.set_xticks(range(num_bins))
ax.set_xticklabels(bin_edges[:-1], rotation=45)
ax.set_xlabel('Input Feature ' + input_feature_name + ' Bins')
ax.set_ylabel('Evaluation Metric ' + output_metric_name)
ax.set_title('Mean and Variance of "' + output_metric_name + '" for parameter "' + input_feature_name+ '"') 
plt.show()