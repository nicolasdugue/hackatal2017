'''Given a lemma in the patents vocabulary, return the data we have on its lem2vec neighbours.'''

import sys
import numpy as np

import logging
logging.basicConfig(level=logging.INFO)

# Try to select a better matplotlib backend
import matplotlib
gui_env = ['QT5Agg', 'Qt4Agg', 'GTKAgg', 'TKAgg', 'WXAgg']
for gui in gui_env:
    try:
        matplotlib.use(gui, warn=False, force=True)
        from matplotlib import pyplot as plt
        break
    except ImportError:
        continue

logging.info("Using matplotlib backend %s", matplotlib.get_backend())


import gensim.models
model = gensim.models.Word2Vec.load('embeddings/patentslem2vec.gensim')


def kl(p, q):
    """Kullback-Leibler divergence D(P || Q) for discrete distributions

    Parameters
    ----------
    p, q : array-like, dtype=float, shape=n
        Discrete probability distributions.
    """
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)
    return np.sum(np.where(p != 0, p * np.log((p+1) / (q+1)), 0))


def read_voc():
    res = {}
    with open('vocLemma.tsv') as voc_file:
        for line in (l for l in voc_file if not l.isspace()):
            try:
                lem, years, _, classes, _ = line.split('\t')
            except ValueError:
                print(line)
                continue
            years = np.fromiter(map(int, years.strip('[]').split(', ')), dtype=int)
            classes = np.fromiter(map(int, classes.strip('[]').split(', ')), dtype=int)
            res[lem] = (years, classes)
    return res


def neighbourhood(word, n=10):
    neighbs = (w for w, d in model.wv.most_similar(word, topn=n))
    return [(w, voc.get(w, None)) for w in neighbs]


def plot_neighbourhood(word, topn=10):
    n = neighbourhood(word, topn)
    n.append((word, voc[word]))
    for w, d in n:
        if d is None:
            print('Ignoring {w} : filtered out of vocabulary'.format(w=w))

    n = [(w, d) for  w, d in n if d is not None]

    years_plot = plt.subplot(121)
    years = np.arange(2001, 2016)

    classes = 'ABCDEFGH'
    bar_width = 5
    classes_x = bar_width*(len(n)+1)*np.arange(len(classes))
    classes_plot = plt.subplot(122)
    classes_plot.set_xticks(classes_x, minor=False)
    classes_plot.set_xticklabels(classes, minor=False)

    for i, (w, dat) in enumerate(n):
        y, c = map(np.asarray, dat)
        # y = y/np.linalg.norm(y, ord=1)
        years_plot.plot(years, y, label=w)

        c = c/np.linalg.norm(c, ord=1)
        classes_plot.bar(classes_x+i*bar_width,  c, width=bar_width, label=w)

    classes_plot.legend()
    years_plot.legend()
    plt.gcf().canvas.set_window_title('Neighbourhood of {word!r}'.format(word=word))
    plt.show()


def neighbourhood_similarity(word, topn=10):
    n = neighbourhood(word, topn)
    n.append((word, voc[word]))
    n = [(w, d) for w, d in n if d is not None]
    year_oc = [y/np.linalg.norm(y, ord=2) for w, (y, c) in n]
    dists_years = np.asarray([[np.linalg.norm(y1-y2, ord=2) for y2 in year_oc] for y1 in year_oc])
    return dists_years.mean()


voc = read_voc()


if __name__ == '__main__':
    plot_neighbourhood(sys.argv[1])
    # print(neighbourhood_similarity(sys.argv[1]))
