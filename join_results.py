'''
Join all results into a csv file
'''

import pandas as pd

# benchmark_name = wordsim353 or simlex999
benchmark_name = "wordsim353"
all_results = []

# symmetric = 1, asymmetric = 0
for symmetry in [0]:
    for window_size in [*range(1, 10), *range(10, 51, 5)]:
        all_results.append(pd.read_csv(f"results_{benchmark_name}_{symmetry}_{window_size}.csv"))

results = pd.concat(all_results, axis=1)

# Remove the vector brackets 
for col in results:
    if results[col].dtype == 'object':
        results[col] = results[col].str.replace('[', '')
for col in results:
    if results[col].dtype == 'object':
        results[col] = results[col].str.replace(']', '')

results.to_csv(f"all_results_{benchmark_name}_{symmetry}.csv", index=False)