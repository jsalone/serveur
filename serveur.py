#!/usr/bin/env python
# -*- coding: utf-8 -*-
# programme développé par SALONE Jonathan dans le cadre d'un projet d'école et ne peut etre réutilisé pour une commercialisation ou autre objectif pour obtenir un profit quelconque
# serveur pour un jeux de gestion
from flask import Flask, request, make_response
from flask import render_template
from db import Db # voyez db.py
from flask_cors import CORS, cross_origin
from flask import render_template
import json
import random
import os
import psycopg2
import urlparse

app = Flask(__name__)
app.debug = True
CORS(app)
invite=0
debutpartie=0
your_dict={}
error=json.dumps(your_dict), 404, {'Content-Type': 'application/json'}
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
@app.route("/connexion", methods=["GET"])
def connexionget():
	return "connexion.html"

##########################################################################################################################################
@app.route("/connexion/<idmonde>", methods=["POST"])
def connexionpost(idmonde):

	db = Db()
	get_json = request.get_json()
	table={}
	tablemtp={}
	Temps={}
	if 'mail' in get_json:
		if 'password' in get_json:
			table['mail'] = get_json['mail']
			tablemtp['mtp'] = get_json['password']
			bonmtp = db.select("SELECT * FROM Joueur WHERE joueur_mail = %(mail)s",{"mail" : table["mail"]})
			if len(bonmtp)!=0:
				db.close()
				return jsonResponse(var jason = {"village":"village.html"};)
#			else:
#				db.close()
#				return error
#		else:
#			db.close()
#			return error
#	db.close()
#	return error
##########################################################################################################################################
@app.route("/inscription", methods=["GET"])
def inscriptionget():
	return render_template("inscription.html")

##########################################################################################################################################
@app.route("/village/<idjoueur>", methods=["GET"])
def monvillage(idjoueur):
	return "village.html"



##########################################################################################################################################
#$('#pseudo').val();
#var mail=  $('#mail').val();
#var pw=  $('#password').val();
@app.route("/inscription/<idmonde>", methods=["POST"])
def inscriptionpost(idmonde):


	db = Db()
	get_json = request.get_json()
	table={}
	tablemtp={}
	tablepseudo={}

	if 'mail' in get_json:
		if 'pseudo' in get_json:
			if 'password' in get_json:

				table['mail'] = get_json['mail']
				tablemtp['mtp'] = get_json['password']
				tablepseudo['pseudo']= get_json['pseudo']
				#on verifie que le joueur n'a pas de compte deja cree
				verifexit = db.select("SELECT * FROM Joueur WHERE joueur_mtp = %(mtp)s AND joueur_mail = %(mail)s",{"mtp" : tablemtp["mtp"],"mail" : table["mail"]})
				
				if len(verifexit)==0:	
					
					id_monde=db.select("SELECT idmonde FROM Monde WHERE monde_nom = %(idmonde)s ",{"idmonde" : idmonde})
					
					idjoueur=db.select("INSERT INTO Joueur (joueur_mail,joueur_pseudo, joueur_mtp) VALUES (%(joueur_mail)s, %(joueur_pseudo)s, %(joueur_mtp)s) RETURNING id_joueur", {
						'joueur_mail': table["mail"],
						'joueur_mtp': tablemtp["mtp"],
						'joueur_pseudo': tablepseudo['pseudo']
					})
					
					idjoueur=idjoueur[0]['id_joueur']
					idjoueur=db.select("INSERT INTO possede ( id_joueur,idmonde) VALUES (%(id_joueur)s,%(idmonde)s)RETURNING id_joueur", {
						'id_joueur': idjoueur,
						'idmonde': id_monde[0]['idmonde']
					})

					
					
					db.close()
					return "connexion.html"
				else:
					db.close()
					return error
			else:
				db.close()
				return error
		else:
			db.close()
			return error

	else:
		db.close()
		return error


#-----------------------------------------------------------------
@app.route('/admin', methods=['GET'])
def affichejoueur():
	db = Db()
	joueur=db.select("SELECT * FROM Joueur")
	db.close()
	resp = make_response(json.dumps(joueur))
	resp.mimetype = 'application/json'
	return resp




if __name__ == "__main__":
  app.run()
