'''Simple wrapper around gensim word2vec model for patents.

Usage: singleword2vec [--lemma | --model <modelfile>] <word>

Options:
  -m, --model <modelfile>  Use another gensim model file  [default: patentsword2vec.gensim]
  -l, --lemma  Use lemma2vec instead of word2vec
  -h, --help  Print this help message'''

import sys

from docopt import docopt

import gensim.models


def main_entry_point(argv=sys.argv[1:]):
    arguments = docopt(__doc__, version='0.0.0', argv=argv)

    if arguments['--lemma']:
        model = gensim.models.Word2Vec.load('patentslem2vec.gensim')
    else:
        model = gensim.models.Word2Vec.load(arguments['--model'])

    word = arguments['<word>']

    try:
        print(model.wv.most_similar(word))
    except KeyError:
        print('{word!r} is not in the model'.format(word=word))


if __name__ == '__main__':
    main_entry_point()
