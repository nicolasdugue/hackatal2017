import gensim.models

model = gensim.models.Word2Vec.load('patentsword2vec.gensim')

n = len(model.wv.vocab)

with open('embeddingsdist.dat', 'w') as out:
    for i, word in enumerate(model.wv.vocab):
        out.write('{word}\t{nlst}\n'.format(
            word=word,
            nlst=','.join('{n}={d}'.format(n=n, d=d) for n, d in model.wv.most_similar(word))
        ))
        if not i % 100:
            print('{i} ({perc:.2f}%) words done'.format(i=i, perc=100*i/n))
