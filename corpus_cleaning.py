'''
Corpus cleaning
'''

import re
from num2words import num2words

file = open('corpus.txt','r')

file_contents = file.readlines()
file.close()

corpus = ' '.join(file_contents)


# 1 - remove markup
def remove_markup(corpus):
    corpus_no_markup = corpus.lower()
    corpus_no_markup = re.sub("<(.*?)>", "", corpus_no_markup)
    corpus_no_markup = re.sub("[\[].*?[\)\]]", "", corpus_no_markup)
    corpus_no_markup = re.sub("&lt;br&gt;", "", corpus_no_markup)
    return corpus_no_markup

cleaned_corpus_1 = remove_markup(corpus)


# 2 - remove punctuation
def remove_punctuation(cleaned_corpus_1):
    corpus_no_punctuation = re.sub("\W", " ", cleaned_corpus_1)
    return corpus_no_punctuation

cleaned_corpus_2 = remove_punctuation(cleaned_corpus_1)


# 3 - remove multiple spaces
def remove_multiple_spaces(cleaned_corpus_2):
    corpus_no_multiple_spaces = re.sub("\s+"," ", cleaned_corpus_2)
    return corpus_no_multiple_spaces

cleaned_corpus_3 = remove_multiple_spaces(cleaned_corpus_2)


# 4 - convert numbers to spelled out text
def convert_num_to_words(cleaned_corpus_3, lang='en'):
  corpus_words = cleaned_corpus_3.split()
  for i in range(0, len(corpus_words)): 
      word = corpus_words[i]
      if (i % 100 == 0):
          print(i , '/', len(corpus_words))
      try:
        if word.isnumeric():
          word = num2words(float(word), lang=lang)
          corpus_words[i] = word
      except Exception:
          print('Failed to process', word)
          pass
  return ' '.join(corpus_words)

cleaned_corpus_final = convert_num_to_words(cleaned_corpus_3)


with open('cleaned_corpus.txt', 'w') as cleaned_corpus:
    cleaned_corpus.write(cleaned_corpus_final)
cleaned_corpus.close