'''Simple wrapper around gensim word2vec model for patents.'''

import sys

import gensim.models

if sys.argv[1] in ['-h', '--help']:
    print('USAGE: python3 word2vecdist.py écran affichage -cloison -mur')
    sys.exit(0)

model = gensim.models.Word2Vec.load('patentsword2vec.gensim')

positive = [a for a in sys.argv[1:] if not a.startswith('-')]
negative = [a[1:] for a in sys.argv[1:] if a.startswith('-')]

positive_filtered = [w for w in positive if w in model.wv.vocab]
negative_filtered = [w for w in negative if w in model.wv.vocab]

ignored = [w for w in positive+negative if w not in positive_filtered+negative_filtered]
if ignored:
    print('Ignoring {}'.format(ignored))

print(model.wv.most_similar(positive=positive, negative=negative))
