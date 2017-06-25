# hackatal2017 team karaoké

## Installation

To run the code, one needs:

numpy, matplotlib, sklearn, gensim


## Exploring the INPI database

### Pré-traitements 

#### Les années 

Nous supprimons les dossiers 2000, 2016 et 2017 qui contiennent beaucoup moins de brevets afin d'éviter tout biais.

#### Le vocabulaire

Nous avons procédé à une lemmatisation avec **\*\*\*\*Lefff\*\*\*\*** et nous obtenons ainsi le fichier **\*\*\*\*FICHIER.CSV\*\*\*\***
qui décrit levocabulaire que nous considérons lors de nos traitements.

Nous avons la possibilité de filtrer ce vocabulaire en utilisant **filtre.py** sur trois critères :
- un filtre sur les fréquences basses dans le corpus, cette fréquence est paramétrable ;
- un filtre sur le nombre de documents dans lequel le mot doit apparaitre au maximum (de façon à éviter le vocabulaire trop générique) ;
- le nombre de classe dans lequel le mot doit apparaitre au maximum (même raison).

Par ailleurs, nous opérons des filtres sur les mots qui apparaissent une seule année, qui sont des digit(), etc...


### Les fonctionnalités

#### Les distances

Pour être capables de discerner des tendances, des patterns d'évolution dans le corpus, nous nous intéressons en particulier aux **co-évolutions** entre les mots du vocabulaire. Pour les détecter, nous créons d'abord une représentation de notre vocabulaire dans le corpus en nous basant principalement sur deux axes : l'axe **temporel** des années, et l'axe des **catégories** que nous appellerons parfois **clusters** ou **groupes**. Nous considérons ici les grandes catégories (A, B, C, ..., H) pour nous simplifier la tâche. Par ailleurs, les résultats obtenus semblent pertinents empiriquement.

Un mot de notre vocabulaire est ainsi représenté par deux histogrammes :
- le nombre de documents dans lequel le mot apparait chaque année ;
- le nombre de documents dans lequel le mot apparait pour chaque cluster.

A partir de cela, il devient possible de comparer les évolutions de deux mots : selon leur présence dans les classes et dans les années.
Pour cela, nous optons pour des distances sur les histogrammes : euclidiennes ou la divergence de Kullback-Leibler que nous rendons symétrique en l'utilisant dans les deux sens.
Lorsque nous nous intéressons à un mot, il est donc possible de calculer la distance de ce mot aux autres mots du vocabulaire sur ces deux axes. Pour obtenir un chiffre unique de distance, nous prenons le max des deux distances (sur l'axe temporel et sur l'axe catégoriel). Prendre le max permet de pénaliser les termes proches en terme de distribution sur les années mais pas dans les classes et inversement.

Ce résultat est implémenté dans **plotDistance.py** : 
> python plotDistance.py informatique

