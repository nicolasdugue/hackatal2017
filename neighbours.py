import sys

import numpy as np
import matplotlib.pyplot as plt

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


def plot_neighbours(word):
    n = neighbours(word)

    years_plot = plt.subplot(121)
    years = np.arange(2000, 2015)

    classes = 'ABCDEFGH'
    bar_width = 5
    classes_x = bar_width*len(n)*np.arange(len(classes))
    classes_plot = plt.subplot(122)
    classes_plot.set_xticks(classes_x, minor=False)
    classes_plot.set_xticklabels(classes, minor=False)

    for i, (w, dat) in enumerate(n):
        if dat is None:
            continue
        y, c = dat
        years_plot.plot(years, y, label=w)
        classes_plot.bar(classes_x+i*bar_width,  c, width=bar_width, label=w)

    classes_plot.legend()
    years_plot.legend()
    plt.show()

voc = read_voc()

if __name__ == '__main__':
    plot_neighbours(sys.argv[1])
