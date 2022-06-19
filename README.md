## Training word embeddings with different context size and symmetry

This code belongs to a Master's thesis titled "Analyzing How Context Size and Symmetry Influence Word Embedding Information" by Ines Gabanes Anuncibay.

The project aimed to analyze the effect of these two parameters (context size and symmetry) and evaluate how well embeddings captured the notions of semantic similarity and relatedness at different scales. The models were trained with [GloVe](https://github.com/stanfordnlp/GloVe) with different context sizes, as well as placing the context window symmetrically and asymmetrically on the left; then, they were quantitatively evaluated through a similarity task, using WordSim-353 (for relatedness) and SimLex-999 (for semantic similarity) as benchmarks.


## Files

The files are expected to be run in the following order:


**1. corpus_cleaning.py**

This file includes: removal of markup, removal of punctuation, removal of multiple spaces, conversion of number digits to spelled-out text, and conversion of all text to lowercase.

**2. train_models.py**

This code to train GloVe models was adapted for python3 from the original in C by Pennington et al. (2014).
Our program executes GloVe and systematically generates embeddings trained on different window sizes using both symmetric and asymmetric context windows. Other parameters can also be modified.

**3. cosine_similarity.py**

This program calculates the average cosine similarity for every word pair from a benchmark.

**4. join_results.py**

This file joins all previous results into a single csv document.

**5. correlations.R**

This R program computes the Spearman correlation coefficient between a list of human scores and the results from the models.
