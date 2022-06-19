'''
Training GloVe models with different window-size and symmetry

This code has been adapted for python3 from the original in C
by Pennington et al. (2014): https://github.com/stanfordnlp/GloVe.git
'''

import subprocess


CORPUS= "enwik9_clean.txt"
VOCAB_FILE= "vocab.txt"
COOCCURRENCE_FILE= "cooccurrence.bin"
COOCCURRENCE_SHUF_FILE= "cooccurrence.shuf.bin"
BUILDDIR= "build"
VERBOSE=2
MEMORY=4.0
VOCAB_MIN_COUNT=5
VECTOR_SIZE=50
MAX_ITER=15
WINDOW_SYMMETRY=0
BINARY=2
NUM_THREADS=8
X_MAX=10


# It constructs unigram counts from a corpus and optionally
# thresholds the resulting vocabulary based on total vocabulary size or minimum frequency count
def vocab_count():
    with open (VOCAB_FILE, 'w') as vocab, open(CORPUS, 'r') as corpus:
        subprocess.run(args = ["build/vocab_count", "-min-count", str(VOCAB_MIN_COUNT), "-verbose", str(VERBOSE)], stdin=corpus, stdout=vocab)

vocab_count()


# Constructs word-word cooccurrence statistics from a corpus
def cooccur(window_size, window_symmetry = 0):
    with open (COOCCURRENCE_FILE, 'w') as cooccurrence, open(CORPUS, 'r') as corpus:
        subprocess.run(args = ["build/cooccur", "-memory",str(MEMORY), "-vocab-file", VOCAB_FILE, "-verbose", str(VERBOSE), "-window-size", str(window_size), "-symmetric", str(window_symmetry)], stdin=corpus, stdout=cooccurrence)


# Shuffles the binary file of cooccurrence statistics produced by `cooccur`
def shuffle():
    with open (COOCCURRENCE_SHUF_FILE, 'w') as cooccurrence_shuf, open(COOCCURRENCE_FILE, 'r') as cooccurrence:
        subprocess.run(args = ["build/shuffle", "-memory", str(MEMORY), "-verbose", str(VERBOSE)], stdin=cooccurrence, stdout=cooccurrence_shuf)


# Train the GloVe model on the specified cooccurrence data
def glove(save_file):
    subprocess.run(args = ["build/glove", "-save-file", save_file, "-threads", str(NUM_THREADS), "-input-file", COOCCURRENCE_SHUF_FILE, "-x-max", str(MAX_ITER), "-vector-size", str(VECTOR_SIZE), "-binary", str(BINARY), "-vocab-file", VOCAB_FILE, "-verbose", str(VERBOSE)])


words = []

def train(window_size, symmetric):
    print('Running model for window size', window_size)
    cooccur(window_size, symmetric)
    shuffle()
    glove('vectors_' + str(symmetric) + '_' + str(window_size))
  
           
# symmetric = 1, asymmetric = 0
for symmetric in range(0, 2):
    for window_size in [*range(1,10), *range(10, 51, 5)]:
        train(window_size, symmetric)
        
