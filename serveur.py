#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
from flask import render_template
from db import Db # voyez db.py


import json
import random
import os
import psycopg2
import urlparse

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/reset')
def route_dbinit():
  """Cette route sert à initialiser (ou nettoyer) la base de données."""
  db = Db()
  db.executeFile("database_reset.sql")
  db.close()
  return "Done."

##########################################################################################################################################
# Fonction de réponse
def jsonResponse(data, status=200):
  return json.dumps(data), status, {'Content-Type': 'application/json'}


##########################################################################################################################################
# Requête R8 - Reset
#@app.route("/reset", methods=["GET"])
#def reset():
#    #return json.dumps(json_table[len(json_table)-1])
#    return "OK:RESET"


##########################################################################################################################################
# Requête R4 - Rejoindre une partie
@app.route("/players", methods=["POST"])
def addPlayer():
    db = Db()
    get_json = request.get_json()
    table={}
    if 'name' in get_json:
        table['name'] = get_json['name']
        result = db.select("SELECT * FROM joueur WHERE JoueurNom = %(name)s",{
		"name" : table["name"]
		})
	taille = len(result)
	if taille!= 0:
		table['name'] = random.randrange(100)
	
	idjoueur=db.select ("INSERT INTO joueur(JoueurNom, JoueurBudget) VALUES (%(name)s, 50) RETURNING idJoueur", {"name" : table["name"]})

	db.select ("INSERT INTO magasin(MagasinPosX, MagasinPosY,idJoueur) VALUES (%(posX)d,%(posY)d,%(idJoueur)d) RETURNING idMagasin as magasin", {"posX" : random.randrange(10),"posY" : random.randrange(10),"idJoueur": idjoueur[0].get('idJoueur')})
	
    else:
        table['name'] = "Jacky"

    table['location'] = {}
    table['location']['latitude'] = random.randrange(10)
    table['location']['longitude'] = random.randrange(10)
    table['info'] = {}
    table['info']['cash'] = 50
    table['info']['sales'] = 0
    table['info']['profit'] = 0.0

    return jsonResponse(table)

##########################################################################################################################################
# Requête R4 - Quitter une partie
@app.route("/players/<playerName>", methods=["DELETE"])
def deletePlayer(playerName):
    #if (playerName == ""):
    return "OK:DELETE " + playerName


##########################################################################################################################################
# Requête R1/R7 - Metrology
@app.route("/metrology", methods=["GET", "POST"])
def metrology():
    global json_table
    if request.method == "GET":
        return "OK:GET_METROLOGY"
    elif request.method == "POST":
        return "OK:POST_METROLOGY"

    #return json.dumps(json_table), 200, {'Content-Type': 'application/json'}


##########################################################################################################################################
# Requête R3 - Sales
@app.route("/sales", methods=["POST"])
def sales():
    global json_table
    get_json = request.get_json()
    #json_table[value].update(get_json)
    print (get_json)

    return "OK:POST_SALES"


##########################################################################################################################################
# Requête R6 - Instructions du joueur
@app.route("/actions/<playerName>", methods=["POST"])
def actionsPlayer(playerName):
    #global json_table
    #return json.dumps(json_table[value])
    return "OK:POST_" + playerName


##########################################################################################################################################
# Requête R2 -  Map
@app.route("/map", methods=["GET"])
def map():
    #return json.dumps(json_table)
    return "OK:GET_MAP"


##########################################################################################################################################
# Requête R5 - Détails d'une partie
@app.route("/map/<playerName>", methods=["GET"])
def mapPlayer(playerName):
    return "GET:OK_MAP_PLAYER" + playerName


##########################################################################################################################################
# Requête R9 - Liste ingrédients
@app.route("/ingredients", methods=["GET"])
def ingredients():
    return "GET:OK_INGREDIENTS"




if __name__ == "__main__":
    app.run()
