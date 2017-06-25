import sys

import gensim.models
model = gensim.models.Word2Vec.load('embeddings/patentslem2vec.gensim')


def read_voc():
    res = {}
    with open('vocLemma.tsv') as voc_file:
        for line in (l for l in voc_file if not l.isspace()):
            try:
                lem, years, _, classes, _ = line.split('\t')
            except ValueError:
                print(line)
                continue
            years = list(map(int, years.strip('[]').split(', ')))
            classes = list(map(int, classes.strip('[]').split(', ')))
            res[lem] = (years, classes)
    return res


def neighbours(word):
    neighbs = (w for w, d in model.wv.most_similar(word))
    return [(w, voc.get(w, None)) for w in neighbs]


voc = read_voc()

if __name__ == '__main__':
    print(len(voc))
    print(neighbours(sys.argv[1]))
