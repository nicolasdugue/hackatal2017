'''Given a lemma in the patents vocabulary, return the data we have on its lem2vec neighbours.

Usage:
  neighbours [--forms | --model <modelfile>] [--number <n>] <word>
  neighbours plot [options] <word>

Commands:
  plot (default)  Display a graphical representation

Options:
  -f, --forms  Use word2vec instead of lem2vec
  -m, --model <modelfile>  Use another gensim model file
                           [default: embeddings/patentslem2vec.gensim]
  -n, --number <n>  Size of the neighbourhood  [default: 10]
  -h, --help  Print this help message'''

import typing as ty

import sys

try:
    import logbook
    logger = logbook.Logger('neighbours', level=logbook.DEBUG)
    logbook.StderrHandler(level=logbook.DEBUG).push_application()
except ImportError:  # Fall back to stdlib logging
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

import gensim.models
import numpy as np

import scipy.interpolate

from docopt import docopt

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

logger.info("Using matplotlib backend %s", matplotlib.get_backend())


# Only load the model and vocabulary on-demand
CACHED_MODEL = None
CACHED_VOCABULARY = None


def get_model(
    model_path: str = 'embeddings/patentslem2vec.gensim',
    force_reload: bool = False
    ) -> gensim.models.keyedvectors.KeyedVectors:

    global CACHED_MODEL
    if CACHED_MODEL is None or force_reload:
        CACHED_MODEL = gensim.models.Word2Vec.load('embeddings/patentslem2vec.gensim')
    return CACHED_MODEL



def get_voc(
    voc_path: str = 'vocLemma.tsv',
    force_reload: bool = False
    ) -> ty.Dict[str, ty.Tuple[np.ndarray, np.ndarray]]:
    '''Extract the temporal and class repartition of `word` in from a vocabulary file.'''
    global CACHED_VOCABULARY
    if CACHED_VOCABULARY is not None and not force_reload:
        return CACHED_VOCABULARY

    res = {}  # type: ty.Dict[str, ty.Tuple[np.ndarray, np.ndarray]]
    with open('vocLemma.tsv') as voc_file:
        for line in (l for l in voc_file if not l.isspace()):
            try:
                lem, years, _, classes, _ = line.split('\t')
            except ValueError:
                logger.warn('Incorrect line in lexicon : {line!r}'.format(line=line))
                continue
            years = np.fromiter(map(int, years.strip('[]').split(', ')), dtype=int)
            classes = np.fromiter(map(int, classes.strip('[]').split(', ')), dtype=int)
            res[lem] = (years, classes)
    CACHED_VOCABULARY = res
    return res


def neighbourhood(
    word: str, n: int = 10,
    model: gensim.models.keyedvectors.KeyedVectors = None,
    voc: ty.Dict[str, ty.Tuple[np.ndarray, np.ndarray]] = None
    ) -> ty.List[ty.Tuple[str, ty.Union[ty.Tuple[np.ndarray, np.ndarray], None]]]:
    '''Return the `n` closest neighbours of `word` in `model`.'''
    if model is None:
        model = get_model()
    if voc is None:
        voc = get_voc()

    neighbs = (w for w, d in model.wv.most_similar(word, topn=n))
    return [(w, voc.get(w, None)) for w in (word, *neighbs)]


def plot_neighbourhood(
    word: str, topn: int = 10,
    model: gensim.models.keyedvectors.KeyedVectors = None,
    voc: ty.Dict[str, ty.Tuple[np.ndarray, np.ndarray]] = None):
    '''Display a graphical representation of the temporal and class distribution of the
       `topn` closest neighbours of `word`.'''
    n = neighbourhood(word, topn, model, voc)
    for w, d in n:
        if d is None:
            logger.warn('Ignoring {w!r} : filtered out of vocabulary'.format(w=w))

    n = [(w, d) for w, d in n if d is not None]

    years_plot = plt.subplot(121)
    years = np.arange(2001, 2016)

    classes = 'ABCDEFGH'
    bar_width = 5
    classes_x = bar_width*(len(n)+1)*np.arange(len(classes))
    classes_plot = plt.subplot(122)
    classes_plot.set_xticks(classes_x, minor=False)
    classes_plot.set_xticklabels(classes, minor=False)

    for i, (w, dat) in enumerate(n):
        y, c = dat
        # y = y/np.linalg.norm(y, ord=1)
        years_plot.plot(years, y, label=repr(w))

        c = c/np.linalg.norm(c, ord=1)
        classes_plot.bar(classes_x+i*bar_width, c, width=bar_width, label=repr(w))

    # Average temporal curve
    average_plot = years_plot.twinx()
    average_plot.set_ylim([0, 1])
    average_curve = np.mean(np.stack(y/np.linalg.norm(y, ord=2) for w, (y, c) in n), axis=0)
    # average_curve = np.mean(np.stack(y for w, (y, c) in n), axis=0)
    average_regression = scipy.interpolate.UnivariateSpline(years, average_curve, s=20)
    average_plot.plot(years, average_regression(years), linestyle='dotted', label='Average')

    classes_plot.legend(loc='best')
    years_plot.legend(loc='best')
    average_plot.legend(loc='best')
    plt.gcf().canvas.set_window_title('Neighbourhood of {word!r}'.format(word=word))
    plt.show()


def neighbourhood_similarity(word, topn=10):
    n = neighbourhood(word, topn)
    n.append((word, voc[word]))
    n = [(w, d) for w, d in n if d is not None]
    year_oc = [y/np.linalg.norm(y, ord=2) for w, (y, c) in n]
    dists_years = np.asarray([[np.linalg.norm(y1-y2, ord=2) for y2 in year_oc] for y1 in year_oc])
    return dists_years.mean()


def main_entry_point(argv=sys.argv[1:]):
    arguments = docopt(__doc__, version='0.0.0', argv=argv)

    if arguments['--forms']:
        model_path = 'embeddings/patentsword2vec.gensim'
    else:
        model_path = arguments['--model']

    model = get_model(model_path)

    word = arguments['<word>']

    if word not in model.wv.vocab:
        logger.error('{word!r} is not in the model'.format(word=word))
        sys.exit(1)

    plot_neighbourhood(word,
                       topn=int(arguments['--number']),
                       model=model)


if __name__ == '__main__':
    main_entry_point()
