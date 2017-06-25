from tkinter import *
import numpy as np

#from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

#Not functional yet : wordcloud, entry (input user), action buttons

def make_a_cloud_of_words(mots_proches):
    """
    :param : mots_proches : liste de mots proches sémantiquement du terme rentré par l'user
    :return: affiche nuage des 5 mots les plus proches
    """
    wordcloud = WordCloud(font_path='/Users/kunal/Library/Fonts/sans-serif.ttf',
                          #stopwords=STOPWORDS,
                          background_color='white',
                          width=1200,
                          height=1000
                          ).generate(mots_proches)

    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()


def plot(liste_mots_proches, y_domaines, x_annees):
    """

    :param liste_mots_proches: liste des 5 mots les plus proches sémantiquement du mot rentré par l'user
    :param y_domaines: liste des classes où le mot apparait ++
    :param x_annees: 2001 à 2015
    :return:graphe de freq du mot sur 15 ans et par classe dans les revendications
    """

    print('Building plots')

    y_domaines= [1,2,3] #todo : add classes -> dans fetch, then erase this line

    plt.plot(x_annees, y_domaines)
    plt.ylabel('classes')

    plt.xlabel('années')
    plt.show()

#plot([1,2,3,4],["A", "G", "C"], [2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015])

def fetch(entree, fichier_distance):
    """

    :param fichier_distance
    :param entree:string from the user
    :return: affiche un graphe de freq pour l'entree pour domaines/annees, et nuage de mots proches
    """

    print('Mot recherché : {}'.format(ent.get()))# % ent.get())

    entree = ent.get() #min

    #lance rapprochement_distance_embedding TODO : utiliser le script rapprochement_distance_embedding.py
    #pour obtenir les points de la ligne du graphe -> besoin d'une liste de vecteurs
    list_dist = [5,8,4,2,6,...]#todo : get the list of vectors for the word, distance_embedding.py -- entree, replace value in this line
    list_classes_max = ["A","B","C","D","E",...][:15] #float that
    x_years = [2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015]

    #todo : utiliser voc_lemma dans rapprochement_distance_embedding

    #fetch les 5 mots les plus proches du mot entré
    mots_proches = [line.strip('\r').split()[0] for line in fichier_distance.read_csv('r', sep='\t')][:5]

    #affiche graphe et nuage pour le mot recherché
    nuage = make_a_cloud_of_words(mots_proches)
    graphe = plot(list_dist, list_classes_max, x_years)



def affiche_brevets():#TODO - in the best of worlds
    print('Start affiche brevets...')
    # fetch list of brevets (hyperlinks) in which the word appears

#******************************************************************************
#
#        INTERFACE
#
#*******************************************************************************
fenetre = Tk() # Création de la fenêtre racine
fenetre.title('My little token')
fenetre.geometry("500x200-10+50") #dimensions de la fenêtre
fenetre['bg']='light blue' # couleur de fond

ent = Entry(fenetre) #todo : debug
ent.insert(0,"Your word")
ent.pack(side=TOP, fill=X)
ent.bind('<Return>', (lambda event:fetch())) #input de l'utilisateur


button_search = Button(fenetre, text='rechercher', command='fetch')
button_search.pack(side = LEFT)

button_test = Button(fenetre, text='plot_test_tactile', command='plot')
button_test.pack(side = LEFT)

button_affiche_brevet = Button(fenetre, text='brevets', command='affiche_brevets')
button_affiche_brevet.pack(side = LEFT)

BoutonQuitter = Button(fenetre, text ='Quitter', command = fenetre.destroy)
BoutonQuitter.pack(side = LEFT)


fenetre.mainloop()
