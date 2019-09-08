#!/usr/bin/env python
# -*- coding: utf-8 -*-
# programme développé par SALONE Jonathan dans le cadre d'un projet d'école et ne peut etre réutilisé pour une commercialisation ou autre objectif pour obtenir un profit quelconque
# serveur pour un jeux de gestion
from flask import Flask, request, make_response ,abort
from flask import render_template
from db import Db # voyez db.py
from flask_cors import CORS, cross_origin
from flask import render_template
import json
import random
import os
import psycopg2
import urlparse
import threading
import time
app = Flask(__name__)
app.debug = True
CORS(app)
invite=0
debutpartie=0
your_dict={}

newplay=0

ametiste=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.10]
balsate=[0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0]
topaze=[1,2,3,4,5,6,7,8,9,10]
quartz=[2,4,6,8,10,12,14,16,18,20]
ore=[0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10]


error=json.dumps(your_dict), 200, {'Content-Type': 'application/json'}
@app.route('/reset')
def route_dbinit():
  """Cette route sert à initialiser (ou nettoyer) la base de données."""
  db = Db()
  db.executeFile("database_reset.sql")

  db.close()
  return "Done."



@app.before_first_request
def activate_job():

	def G_ametiste():
		route_dbinit()
		db = Db()
		global newplay
		
		idame=db.select("SELECT * FROM Matiere WHERE matiere_nom = %(idmat)s",{"idmat" : 'ametiste'})
		listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
		db.close()
		print ("G_ametiste OK ")
		print (idame)
		while True:
			
			if len(listematame)!=0:
				
				for maliste in range(0,len(listematame)):
					print("1")
					listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
					print("2")
					nivmine=listematame[maliste]['niveau_mat']
					print("3")
					ancien=listematame[maliste]['montant_mat']
					print("4")
					ancien+=ametiste[nivmine]
					print("5")
					db.execute("UPDATE fourni SET montant_mat='"+ str(ancien) +"' WHERE id_matiere= "+ str(listematame[maliste]['id_matiere']) +" AND id_village="+ str(listematame[maliste]['id_village']) +"")
					print("6")
				time.sleep(1)
			else:
				db = Db()
				listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
				time.sleep(1)
				
		db.close()
	def G_balsate():
		
		global newplay
		time.sleep(4)
		db = Db()
		idame=db.select("SELECT * FROM Matiere WHERE matiere_nom = %(idmat)s",{"idmat" : 'balsate'})
		listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
		print ("G_balsate OK")
		print (idame)
		while True:
			if len(listematame)!=0:
				for maliste in range(0,len(listematame)):
					listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
					nivmine=listematame[maliste]['niveau_mat']
					ancien=listematame[maliste]['montant_mat']
					ancien+=balsate[nivmine]
					db.execute("UPDATE fourni SET montant_mat='"+ str(ancien) +"' WHERE id_matiere= "+ str(listematame[maliste]['id_matiere']) +" AND id_village="+ str(listematame[maliste]['id_village']) +"")
				time.sleep(1)
			else:
				listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
				time.sleep(1)
		db.close()

	def G_topaze():
		global newplay
		time.sleep(8)
		db = Db()
		idame=db.select("SELECT * FROM Matiere WHERE matiere_nom = %(idmat)s",{"idmat" : 'topaze'})
		listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
		print ("G_topaze OK")
		print (idame)
		while True:
			if len(listematame)!=0:
				for maliste in range(0,len(listematame)):
					listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
					nivmine=listematame[maliste]['niveau_mat']
					ancien=listematame[maliste]['montant_mat']
					ancien+=topaze[nivmine]
					db.execute("UPDATE fourni SET montant_mat='"+ str(ancien) +"' WHERE id_matiere= "+ str(listematame[maliste]['id_matiere']) +" AND id_village="+ str(listematame[maliste]['id_village']) +"")
				time.sleep(1)
			else:
				listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
				time.sleep(1)
		db.close()
	def G_quartz():
		global newplay
		time.sleep(12)
		db = Db()
		idame=db.select("SELECT * FROM Matiere WHERE matiere_nom = %(idmat)s",{"idmat" : 'quartz'})
		listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
		print ("G_quartz OK")
		print (idame)
		while True:
			if len(listematame)!=0:
				for maliste in range(0,len(listematame)):
					listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
					nivmine=listematame[maliste]['niveau_mat']
					ancien=listematame[maliste]['montant_mat']
					ancien+=quartz[nivmine]
					db.execute("UPDATE fourni SET montant_mat='"+ str(ancien) +"' WHERE id_matiere= "+ str(listematame[maliste]['id_matiere']) +" AND id_village="+ str(listematame[maliste]['id_village']) +"")
				time.sleep(1)
			else:
				listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
				time.sleep(1)
		db.close()
	def G_ore():
		global newplay
		time.sleep(8)
		db = Db()
		idame=db.select("SELECT * FROM Matiere WHERE matiere_nom = %(idmat)s",{"idmat" : 'ore'})
		listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
		print ("G_ore OK")
		print (idame)
		while True:
			if len(listematame)!=0:
				for maliste in range(0,len(listematame)):
					listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
					nivmine=listematame[maliste]['niveau_mat']
					ancien=listematame[maliste]['montant_mat']
					ancien+=ore[nivmine]
					db.execute("UPDATE fourni SET montant_mat='"+ str(ancien) +"' WHERE id_matiere= "+ str(listematame[maliste]['id_matiere']) +" AND id_village="+ str(listematame[maliste]['id_village']) +"")
				time.sleep(1)
			else:
				listematame = db.select("SELECT * FROM fourni WHERE id_matiere = %(idmat)s",{"idmat" : idame[0]['id_matiere']})
				time.sleep(1)
		db.close()	
	thread = threading.Thread(target=G_ametiste)
	thread.start()
	thread = threading.Thread(target=G_balsate)
	thread.start()
	thread = threading.Thread(target=G_topaze)
	thread.start()
	thread = threading.Thread(target=G_quartz)
	thread.start()
	thread = threading.Thread(target=G_ore)
	thread.start()









##########################################################################################################################################
# Fonction de réponse
def jsonResponse(data, status=200):
  return json.dumps(data), status, {'Content-Type': 'application/json'}

def jsonResponseerror(data, status=404):
  return json.dumps({'village':"NULL"}), status, {'Content-Type': 'application/json'}

##########################################################################################################################################
@app.route("/connexion", methods=["GET"])
@app.route("/static/connexion", methods=["GET"])
@app.route("/", methods=["GET"])
@app.route("/static/", methods=["GET"])
def connexionget():
	return render_template("connexion.html")

##########################################################################################################################################
@app.route("/connexion/<idmonde>", methods=["POST"])
@app.route("/static/connexion/<idmonde>", methods=["POST"])
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
			bonmtp = db.select("SELECT id_joueur FROM Joueur WHERE joueur_mail = %(mail)s AND joueur_mtp = %(mtp)s",{"mail" : table["mail"],"mtp" : tablemtp['mtp']})
			
			if len(bonmtp)!=0:
				db.close()
				return jsonResponse({'idjoueur':bonmtp[0]['id_joueur']})
			else:
				db.close()
				abort(404)
		else:
			db.close()
			abort(404)
	db.close()
	abort(404)
##########################################################################################################################################
@app.route("/inscription", methods=["GET"])
@app.route("/static/inscription", methods=["GET"])
def inscriptionget():
	return render_template("inscription.html")

##########################################################################################################################################
@app.route("/village/<idjoueur>", methods=["GET"])
@app.route("/static/village/<idjoueur>", methods=["GET"])
def monvillage(idjoueur):
	return render_template("village.html")



##########################################################################################################################################
#$('#pseudo').val();
#var mail=  $('#mail').val();
#var pw=  $('#password').val();
@app.route("/inscription/<idmonde>", methods=["POST"])
@app.route("/static/inscription/<idmonde>", methods=["POST"])
def inscriptionpost(idmonde):


	db = Db()
	get_json = request.get_json()
	table={}
	tablemtp={}
	tablepseudo={}
	global newplay
	if 'mail' in get_json:
		if 'pseudo' in get_json:
			if 'password' in get_json:

				table['mail'] = get_json['mail']
				tablemtp['mtp'] = get_json['password']
				tablepseudo['pseudo']= get_json['pseudo']
				#on verifie que le joueur n'a pas de compte deja cree
				verifexit = db.select("SELECT * FROM Joueur WHERE joueur_mail = %(mail)s",{"mail" : table["mail"]})
				
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
					idvillage=db.select("INSERT INTO village ( village_nom) VALUES (%(village_nom)s)RETURNING id_village", {
						'village_nom': 'NouveauVillage'
					})
					idavoir=db.select("INSERT INTO avoir (id_joueur,id_village) VALUES (%(id_joueur)s,%(id_village)s)RETURNING id_village", {
						'id_joueur': idjoueur[0]['id_joueur'],'id_village': idvillage[0]['id_village']
					})
					tpierre=db.select("SELECT * FROM Matiere ")
					pierre=db.select("SELECT * FROM Matiere WHERE matiere_nom = %(idmat)s",{"idmat" : 'ametiste'})

					
					idfourni=db.select("INSERT INTO fourni (id_matiere,id_village,montant_mat,niveau_mat) VALUES (%(id_matiere)s,%(id_village)s,%(montant_mat)s,%(niveau_mat)s)RETURNING id_village", {'id_matiere': pierre[0]['id_matiere'],'id_village': idvillage[0]['id_village'],'montant_mat':50,'niveau_mat':0
					})
					pierre=db.select("SELECT id_matiere FROM Matiere WHERE matiere_nom='balsate'")
					idfourni=db.select("INSERT INTO fourni (id_matiere,id_village,montant_mat,niveau_mat) VALUES (%(id_matiere)s,%(id_village)s,%(montant_mat)s,%(niveau_mat)s)RETURNING id_village", {
						'id_matiere': pierre[0]['id_matiere'],'id_village': idvillage[0]['id_village'],'montant_mat':100,'niveau_mat':0
					})
					pierre=db.select("SELECT id_matiere FROM Matiere WHERE matiere_nom='topaze'")
					idfourni=db.select("INSERT INTO fourni (id_matiere,id_village,montant_mat,niveau_mat) VALUES (%(id_matiere)s,%(id_village)s,%(montant_mat)s,%(niveau_mat)s)RETURNING id_village", {
						'id_matiere': pierre[0]['id_matiere'],'id_village': idvillage[0]['id_village'],'montant_mat':150,'niveau_mat':0
					})
					pierre=db.select("SELECT id_matiere FROM Matiere WHERE matiere_nom='quartz'")
					idfourni=db.select("INSERT INTO fourni (id_matiere,id_village,montant_mat,niveau_mat) VALUES (%(id_matiere)s,%(id_village)s,%(montant_mat)s,%(niveau_mat)s)RETURNING id_village", {
						'id_matiere': pierre[0]['id_matiere'],'id_village': idvillage[0]['id_village'],'montant_mat':200,'niveau_mat':0
					})
					pierre=db.select("SELECT id_matiere FROM Matiere WHERE matiere_nom='ore'")
					idfourni=db.select("INSERT INTO fourni (id_matiere,id_village,montant_mat,niveau_mat) VALUES (%(id_matiere)s,%(id_village)s,%(montant_mat)s,%(niveau_mat)s)RETURNING id_village", {
						'id_matiere': pierre[0]['id_matiere'],'id_village': idvillage[0]['id_village'],'montant_mat':20,'niveau_mat':0
					})
					newplay=1
					db.close()
					return render_template("connexion.html")
				else:
					db.close()
					abort(404)
			else:
				db.close()
				abort(404)
		else:
			db.close()
			abort(404)

	else:
		db.close()
		abort(404)


#-----------------------------------------------------------------

@app.route("/ressource/<idjoueur>/<nomvillage>", methods=["GET"])
@app.route("/static/ressource/<idjoueur>/<nomvillage>", methods=["GET"])
def myressource(idjoueur,nomvillage):
	db = Db()
	idvillage=db.select("SELECT id_village FROM avoir WHERE id_joueur = %(id_joueur)s",{"id_joueur" : idjoueur})
	pierreame=db.select("SELECT * FROM Matiere WHERE matiere_nom = %(idmat)s",{"idmat" : 'ametiste'})
	listemyressourceame = db.select("SELECT * FROM fourni WHERE id_village = %(id_village)s AND id_matiere= %(id_matiere)s",{"id_village" : idvillage[0]['id_village'],'id_matiere':pierreame[0]['id_matiere']})
	pierrebal=db.select("SELECT * FROM Matiere WHERE matiere_nom = %(idmat)s",{"idmat" : 'balsate'})
	listemyressourcebal = db.select("SELECT * FROM fourni WHERE id_village = %(id_village)s AND id_matiere= %(id_matiere)s",{"id_village" : idvillage[0]['id_village'],'id_matiere':pierrebal[0]['id_matiere']})
	pierretop=db.select("SELECT * FROM Matiere WHERE matiere_nom = %(idmat)s",{"idmat" : 'topaze'})
	listemyressourcetop = db.select("SELECT * FROM fourni WHERE id_village = %(id_village)s AND id_matiere= %(id_matiere)s",{"id_village" : idvillage[0]['id_village'],'id_matiere':pierretop[0]['id_matiere']})
	pierrequa=db.select("SELECT * FROM Matiere WHERE matiere_nom = %(idmat)s",{"idmat" : 'quartz'})
	listemyressourcequa = db.select("SELECT * FROM fourni WHERE id_village = %(id_village)s AND id_matiere= %(id_matiere)s",{"id_village" : idvillage[0]['id_village'],'id_matiere':pierrequa[0]['id_matiere']})
	pierreore=db.select("SELECT * FROM Matiere WHERE matiere_nom = %(idmat)s",{"idmat" : 'ore'})
	listemyressourceore = db.select("SELECT * FROM fourni WHERE id_village = %(id_village)s AND id_matiere= %(id_matiere)s",{"id_village" : idvillage[0]['id_village'],'id_matiere':pierreore[0]['id_matiere']})
	db.close()
	total={'ametiste':listemyressourceame,'balsate':listemyressourcebal,'topaze':listemyressourcetop,'quartz':listemyressourcequa,'ore':listemyressourceore}
	resp = make_response(json.dumps(total))
	resp.mimetype = 'application/json'
	
	return resp

##########################################################################################################################################
@app.route("/pierre", methods=["GET"])
@app.route("/static/pierre", methods=["GET"])
def mypierre():
	db = Db()
	pierre=db.select("SELECT * FROM Matiere")
	db.close()
	return jsonResponse({'liste':pierre})

##########################################################################################################################################
@app.route("/interface", methods=["GET"])
def interface():
	return render_template("/interface")



##########################################################################################################################################
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
