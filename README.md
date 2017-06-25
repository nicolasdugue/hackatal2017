# hackatal2017 team karaoké

## Installation

To run the code, one needs:

numpy, matplotlib, sklearn, gensim


## Exploring the INPI database

### Pré-traitements 

#### Les années 

Nous supprimons les dossiers 2000, 2016 et 2017 qui contiennent beaucoup moins de brevets afin d'éviter tout biais.

#### Le vocabulaire

Nous avons procédé à une lemmatisation avec **\*\*\*\*TOFILL\*\*\*\*** et nous obtenons ainsi le fichier **\*\*\*\*FICHIER.CSV\*\*\*\***
qui décrit levocabulaire que nous considérons lors de nos traitements.

Nous avons la possibilité de filtrer ce vocabulaire en utilisant **filtre.py** sur trois critères :
- un filtre sur les fréquences basses dans le corpus, cette fréquence est paramétrable ;
- un filtre sur le nombre de documents dans lequel le mot doit apparaitre au maximum (de façon à éviter le vocabulaire trop générique) ;
- le nombre de classe dans lequel le mot doit apparaitre au maximum (même raison).

Par ailleurs, nous opérons des filtres sur les mots qui apparaissent une seule année, qui sont des digit(), etc...
