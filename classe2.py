# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 18:08:55 2021

@author: lpeti
"""


class Liste_com:
        # Initialisation des variables de la classe
    def __init__(self, nom_page):
        self.nom_dep = nom_page
        self.nom_dep=self.nom_dep.replace('Communes of the ',"")
        self.nom_dep=self.nom_dep.replace(' department',"")
        self.liste_com = {}
        self.n_com = 0
        
    def __str__(self):
        return self.nom_dep
    
    def add (self,liste_com):
        self.liste_com=liste_com
        self.n_com = liste_com.__len__()


class Communes:
            # Initialisation des variables de la classe
    def __init__(self, nom_page, dep):
        self.nom_com = nom_page
        self.nom_dep=dep
        self.liens = []
        self.n_liens=0
    
    def __str__(self):
        return self.nom_dep
        
    def add (self,liens):
        self.liens=liens
        self.n_liens = liens.__len__()
