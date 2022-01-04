# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 18:02:00 2021

@author: lpeti
"""

import wikipedia

import classe2

import re

import pickle

import networkx as nx

import matplotlib.pyplot as plt

import math



wikipedia.set_lang ("en")

#Certaines boucles mettant un certain temps à se résoudre, il y a quelques reprises des alertes sonores signifiant la fin d'une section.

# ------------------------ LISTE DES COMMUNES ----------

# Récupération de la liste des départements pour obtenir leur liste de communes respectives

departements = wikipedia.page("Lists of communes of France", auto_suggest=False)

liste_dep = list(departements.links)
liste_dep_cl = []

# Obtenir uniquement les pages "communes of departement"

for dep in liste_dep:
    if  not ('Communes of the' in dep):
        liste_dep_cl.append(dep)
        
for dep in liste_dep_cl:
    liste_dep.remove(dep)
    


# créer une liste des communes par département

liste_com_dep=[]

for dep in liste_dep:
    liste_com = wikipedia.page(dep, auto_suggest=False).links
    
    liste_com_cl=[]
    
    for com in liste_com:
        if  ('Corneilla' in com) or ('commune' in com) or ('Institut' in com) or ('Communes of ' in com) or ('Le Ribéral' in com) or ('Castillon' in com) or ('Navarre' in com) or ('Corsica' in com) or ('Arné' in com) or ('Reignier-Esery' in com) or ('Brittany' in com) or ('Overseas department' in com) or ('archives' in com) or ('Metropolis' in com) or ('Cergy-Pontoise' in com) or ('La Perche' in com) or ('Saint-Nazaire' in com) or ('France' in com) or ('Agglomération' in com) or ('Department' in com) or ('Administrative' in com) or ('Agglomeration' in com) or ('Communauté ' in com) or ('INSEE' in com) or ('Paris' in com) or ('Postal' in com):
                liste_com_cl.append(com)
            
    for com in liste_com_cl:
        liste_com.remove(com)
        
    #on utilise une classe pour mettre chaque département et sa liste de communes
    liste_communes = classe2.Liste_com(dep)
    
    #on retire les nom de département de la liste des communes
    dep_name = liste_communes.__str__()
    
    regex = re.compile('.*'+dep_name+'.*')
    filtered = [i for i in liste_com if not regex.match(i)]
    
    liste_com=filtered
    
    print(dep_name)
    
    #on complète l'objet liste_communes et on l'ajoute a la liste des communes par départements

    liste_communes.add(liste_com)
    
    liste_com_dep.append(liste_communes)

    





#------------------------------ LISTE DES LIENS ENTRE LES COMMUNES VERSION 1-------------------------

# Cette version recouvre toutes les communes, cela représente presque 30 000 itérations: c'est trop long et il reste des erreurs 
# On utilise plutôt la version de démo qui ne concerne que les communes du département rhône
wikipedia.set_lang ("fr")

'''

#construire un set avec chaque commune et chaque département individuelle


communes_all = []
departements_all =[]

for dep in liste_com_dep:
    communes_all=communes_all+dep.liste_com
    departements_all.append(dep.nom_dep)
    
communes_all.append('Paris')
departements_all.append('Paris')
communes_all.append('Lyon')

communes_all=list(set(communes_all))
communes_all.sort()

departements_all=list(set(departements_all))
departements_all.sort()

liste_com_liens=[] #ENLEVER SI IL Y A ERREUR

commune = classe2.Communes('Paris','Paris')
liens= wikipedia.page('Paris', auto_suggest=False).links
liens_cl=[]
            
for i in liens:
    if i in communes_all:
        liens_cl.append(i)
                    
commune.add(liens_cl)
liste_com_liens.append(commune)

commune = classe2.Communes('Lyon','Rhône')
liens= wikipedia.page('Lyon', auto_suggest=False).links
liens_cl=[]
            
for i in liens:
    if i in communes_all:
        liens_cl.append(i)
                    
commune.add(liens_cl)
liste_com_liens.append(commune)


dep_decrease=departements_all

communes_decrease=communes_all
#jusqu'à là


f = open('D:/Documents/Université/M1/algo/projet wiki/store.pckl', 'rb') #METTRE SI IL Y A ERREUR
liste_com_liens = pickle.load(f)
f.close()


 dep_decrease=dep_decrease[86:] #boucle longue NON NECESSAIRE UNE FOIS LE CORPUS CREE



for dep in liste_com_dep:
    if(dep.nom_dep in dep_decrease):
        print(' DEPARTEMENT '+dep.nom_dep)
        for com in dep.liste_com:
                if com in communes_decrease:
                    print(com)
                    search=com + " "+dep.nom_dep
                    print(search)
                    commune=classe2.Communes(com,dep.nom_dep)
                    try:
                        liens = wikipedia.page(search, auto_suggest=True).links
                    except wikipedia.exceptions.PageError:
                        liens = wikipedia.page(com, auto_suggest=False).links
                    except wikipedia.exceptions.DisambiguationError:
                        liens = wikipedia.page(com, auto_suggest=False).links
                    except:
                        print ("communes non trouvé")
                
                    liens_cl=[]
                    
                    for i in liens:
                        if i in communes_all:
                            liens_cl.append(i)
                            
                    commune.add(liens_cl)
                    liste_com_liens.append(commune)
                    communes_decrease.remove(com)
                    
        dep_decrease.remove(dep.nom_dep)     
    
    
print('\a')

#on utilise pickle pour stocker la liste des communes afin de ne pas perdre ce qui a déjà été scrappé


f = open('store.pckl', 'wb')
pickle.dump(liste_com_liens, f)
f.close()'''


#------------------------------ LISTE DES LIENS ENTRE LES COMMUNES VERSION 2-------------------------
#Cette version ne permet de faire le graph des relations inter-régions que sur un département
#Ici on test sur le département Rhône qui a pour numéros dans notre liste 78
#Pour tester sur un autre département, il faut modifier les 78 en le numéros du département dans liste_com_dep
#Il faut égalemment enlever les lignes concernant Lyon. Si l'on veut inclure Paris, reproduire ces 3 lignes en remplaçant Lyon par Paris

#construire un set avec chaque commune et chaque département individuelle


communes_all = []

for dep in liste_com_dep:
    communes_all=communes_all+liste_com_dep[78].liste_com
    

communes_all.append('Lyon')

communes_all=list(set(communes_all))
communes_all.sort()

#construire la liste des communes et leurs liens

liste_com_liens=[] 

#Lyon doit être ajouter séparemment car elle était traité en tant que "métropole" dans la liste des communes

commune = classe2.Communes('Lyon','Rhône')
liens= wikipedia.page('Lyon', auto_suggest=False).links

liens_cl=[]


            
for i in liens:
    if i in communes_all:
        liens_cl.append(i)
                    
commune.add(liens_cl)
liste_com_liens.append(commune)
#fin du code permettant d'ajouter Lyon

communes_decrease=communes_all


dep = liste_com_dep[78]

#pour chaque commune de la liste des communes du département, on va chercher les liens de sa page wikipedia

for com in dep.liste_com:
    if com in communes_decrease:
        print(com)
        search=com + " "+dep.nom_dep
        print(search)
        commune=classe2.Communes(com,dep.nom_dep)
        
        #gestion des erreurs selon la recherche de la page, on tente avec différentes orthographes
        
        try:
            print('1')
            liens = wikipedia.page(search, auto_suggest=True).links
        except Exception:
            try :
                liens = wikipedia.page(com, auto_suggest=True).links
            except Exception:
                try:
                    liens = wikipedia.page(com, auto_suggest=False).links
                except Exception:
                    print('Commune non trouvée')
            
    
        liens_cl=[]
        
        #on fait la liste des liens en ne prenant que ceux faisant partit des communes du départements
        
        for i in liens:
            if i in communes_all:
                liens_cl.append(i)
                
        commune.add(liens_cl)
        liste_com_liens.append(commune)
        communes_decrease.remove(com)
        

    
print('\a')

#on utilise pickle pour stocker la liste des communes afin de ne pas perdre ce qui a déjà été scrappé


f = open('store.pckl', 'wb')
pickle.dump(liste_com_liens, f)
f.close()

        
#---------------------------AFFICHER GRAPH --------------------



G = nx.DiGraph()
node_list=[]

# on rajoute, pour chaque commune, sa node et tous les edges partant d'elle même et allant vers les communes dont elle est liée

for com in liste_com_liens:
    print(com.nom_com)
    G.add_node(com.nom_com)
    
    for target in com.liens:
        if not target in node_list:
            G.add_node(target)
            node_list.append(target)
        G.add_edge(com.nom_com, target)


pos = nx.spring_layout(G)

#on configure le visuel du graph et on l'affiche
#les degrées servent a pondéré les tailles des nodes et du texte afin de mettre en avant les communes ayant le plus de lien

plt.figure(figsize=(50,50))

#on peut choisir entre pondérer le graph en fonction du nombre de liens dans sa page vers d'autres (demi-degré extèrieur) ou du nombre de liens vers sa page venant des autres (demi-degré intèrieur)
d = dict(G.degree) #demi-degré extèrieur
#d = dict(G.in_degree) #demi-degré intèrieur


nx.draw(G, pos=pos, node_color='orange', 
        with_labels=False, 
        node_size=[d[k]*300 for k in d])
for node, (x, y) in pos.items():
    plt.text(x, y, node, fontsize=math.sqrt(d[node])*3, bbox=dict(boxstyle="square,pad=0.3", fc="white"), ha='center', va='center', color='blue')
    
plt.show() #ploting the graph 



print('\a')

