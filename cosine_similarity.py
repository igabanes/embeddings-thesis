'''
Calculate average cosine similarity for the wordpairs in benchmarks
'''

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# Get the vector for every word in the given column
# When words are not in corpus, add empty vectors instead
def read_column(column_name, benchmark, words_to_vectors):
    vectors = []
    empty_vector = [0] * 50
    for word in benchmark[column_name]:
        try:
            vectors.append(words_to_vectors[word])
        except KeyError:
            # print(f"The word {word1} is not in the corpus")
            vectors.append(empty_vector)
    return vectors


# Calculate the average cosine of every wordpair
def calculate_similarity(benchmark):
    pred_sim = []
    for i in range(len(benchmark)):
        pred_sim.append(
            cosine_similarity([benchmark.iloc[i]["vector1"]], [benchmark.iloc[i]["vector2"]])
        )
    return pred_sim


# Read a target file and for every word that exists in the word pairs, get its vector
def extract_word_vectors(current_target, word_pairs):
    model = open(f"vectors_{current_target}.txt",'r')
    lines = model.readlines()
    
    # Create dictionary with the words and their vectors
    words_to_vectors = {}
    
    for line in lines:
        words = line.split()
        word = words[0]
        vector = [float(i) for i in words[1:]]
            
        if (word_pairs == word).any():
           words_to_vectors[word] = vector    
    return words_to_vectors


def write_results(benchmark, benchmark_name, current_target, window_size):
    # Drop rows with empty values
    if (benchmark_name == "wordsim353"):
        benchmark = benchmark.drop([22, 37, 38, 41, 46, 47, 48, 121, 158, 159, 161, 162, 169, 178, 209, 219, 259, 321])
    
    if (window_size == 1): 
        columns_to_write = ["word1","word2","human_sim",f"pred_sim_{current_target}"]
    else:
        columns_to_write = [f"pred_sim_{current_target}"]
        
    benchmark.to_csv(f"results_{benchmark_name}_{current_target}.csv", index=False, columns = columns_to_write)


# Symmetry should be 1 for symmetric or 0 for asymmetric
def generate_all_similarities_for_benchmark(benchmark_name, symmetry, window_size):
    current_target = f"{symmetry}_{window_size}"
    benchmark = pd.read_csv(f"{benchmark_name}.csv")
    
    columns = [benchmark['word1'], benchmark['word2']]
    word_pairs = pd.concat(columns)
    
    words_to_vectors = extract_word_vectors(current_target, word_pairs)
    
    # Add two columns with the vectors for each word to the dataframe
    benchmark['vector1'] = read_column('word1', benchmark, words_to_vectors)
    benchmark['vector2'] = read_column('word2', benchmark, words_to_vectors)
    
    # Calculate similarity between the vectors of word1 and word2
    benchmark[f"pred_sim_{current_target}"] = calculate_similarity(benchmark)
    
    write_results(benchmark, benchmark_name, current_target, window_size)


# benchmark_name = wordsim353 or simlex999
for symmetry in range(0, 2):
    for window_size in [*range(1,10), *range(10, 51, 5)]:
        generate_all_similarities_for_benchmark("simlex999", symmetry, window_size)
       