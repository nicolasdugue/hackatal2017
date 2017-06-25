'''Simple wrapper around gensim word2vec model for patents.'''

import sys

import gensim.models

model = gensim.models.Word2Vec.load('patentsword2vec.gensim')

positive = [a for a in sys.argv[1:] if not a.startswith('-')]
negative = [a[1:] for a in sys.argv[1:] if a.startswith('-')]

positive_filtered = [w for w in positive if w in model.wv.vocab]
negative_filtered = [w for w in negative if w in model.wv.vocab]

# print('Not in vocabulary : {}'.format(list()))

print(model.wv.most_similar(positive=positive, negative=negative))
