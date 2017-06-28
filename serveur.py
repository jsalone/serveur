#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
from flask import render_template
from db import Db # voyez db.py
from flask_cors import CORS, cross_origin

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

dfn=0

weathertoday='SUNNY'
weathertomor='RAINNY'
timestamp=0

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
# Requête R4 - Rejoindre une partie //fini
@app.route("/players", methods=["POST"])
def addPlayer():
    print("--------------------------------------rejoindre partie---------------------------------------------------")
    global invite
    db = Db()
    get_json = request.get_json()
    table={}
    if 'name' in get_json:
        table['name'] = get_json['name']
        result = db.select("SELECT * FROM joueur WHERE JoueurNom = %(name)s",{
		"name" : table["name"]
		})
	partiExist = db.select("SELECT idPartie FROM partie")
	taille = len(partiExist)
	#verif parti existant
	if taille == 0:
		partiExist=db.select ("INSERT INTO partie(PartieNom,PartiMetrologitoday,PartiMetrologitomor,Partidfn) VALUES (%(name)s,%(today)s,%(tomor)s,0) RETURNING idPartie",{"name" : table["name"],"today" : "sunny","tomor" : "rainny"})
	taille = len(result)
	if taille!= 0:
		
		
		while taille !=0:
			invite+=1
			table['name'] = "invite%d"% invite
			result = db.select("SELECT * FROM joueur WHERE JoueurNom = %(name)s",{"name" : table["name"]})
			taille = len(result)
					
	#ajout joueur
	idjoueur=db.select ("INSERT INTO joueur(JoueurNom, JoueurBudget,IdPartie) VALUES (%(name)s, 50,%(parti)s) RETURNING idJoueur", {"name" : table["name"],"parti":partiExist[0]['idpartie']})
	result = db.select("SELECT idJoueur FROM joueur WHERE JoueurNom = %(name)s",{
		"name" : table["name"]
		})
	db.select ("INSERT INTO magasin(MagasinPosX, MagasinPosY,idJoueur,MagasinInfluence) VALUES (%(posX)s,%(posY)s,%(idJoueur)s,50) RETURNING idMagasin as magasin", {"posX" : random.randrange(600),"posY" : random.randrange(600),"idJoueur": result[0]['idjoueur']})
	
	limonda = db.select("SELECT * FROM recette WHERE RecetteNom=%(nom)s ",{"nom": 'limonade'})
	racord =db.select ("INSERT INTO avoir(idRecette,idJoueur,vendre,RecettePrix) VALUES (%(rec)s,%(idjou)s,%(vd)s,%(Recpr)s) RETURNING idRecette", {"rec" : limonda[0]['idrecette'],"idjou" : result[0]['idjoueur'],"vd": 0,"Recpr":0.0 })

	result = db.select("SELECT * FROM magasin WHERE idJoueur = %(name)s",{
		"name" : result[0]['idjoueur']
		})
    db.close()
    table['location'] = {}
    table['location']['latitude'] = result[0]['magasinposy']
    table['location']['longitude'] = result[0]['magasinposx']
    table['info'] = {}
    table['info']['cash'] = 50
    table['info']['sales'] = 0
    table['info']['profit'] = 0.0

    return jsonResponse(table)

##########################################################################################################################################
# Requête R4 - Quitter une partie//fini
@app.route("/players/<playerName>", methods=["DELETE"])
def deletePlayer(playerName):
    print("-----------------------------------------delete----------------------------------------------------------")
    db = Db()
    result = db.select("SELECT idJoueur FROM joueur WHERE JoueurNom = %(name)s",{"name" : playerName})
    magasin=db.select("SELECT * FROM magasin WHERE idJoueur = %(name)s",{"name" : result[0]['idjoueur']})
    panneau=db.select("SELECT * FROM panneau WHERE idJoueur = %(name)s",{"name" : result[0]['idjoueur']})

    recette=db.select("SELECT * FROM recette WHERE idJoueur = %(name)s",{"name" : result[0]['idjoueur']})
    
    taille = len(recette)
    if taille !=0:
	db.execute("DELETE FROM recette WHERE idJoueur = %s",result[0]['idjoueur']) 
    	contenir=db.select("SELECT * FROM contenir WHERE idRecette = %(name)s",{"name" : recette[0]['idRecette']})
	taille = len(contenir)
	if taille !=0: 
		db.execute("DELETE FROM contenir WHERE idJoueur = %s",recette[0]['idrecette'])  

    db.execute("DELETE FROM magasin WHERE idJoueur = "+ str(result[0]['idjoueur'])) 
    db.execute("DELETE FROM joueur WHERE idJoueur = "+ str(result[0]['idjoueur'])) 
    db.close()
    #if (playerName == ""):
    return "OK:DELETE " + playerName


##########################################################################################################################################
# Requête R1/R7 - Metrology
@app.route("/metrology", methods=["GET", "POST"])
def metrology():
    print"-----------------------------------------METRO-----------------------------------------------------------"
    db = Db()
    meteoparti = db.select("SELECT * FROM partie")
    if request.method == "GET" and len(meteoparti)!=0 :
	print"-----------------------------------------GET METRO-----------------------------------------------------------"
	
	weather={}
	forcast={}
	Temps={}
	
	forcast['dfn']={}
	forcast['weather']={}

	forcast['dfn'][0]=meteoparti[0]['partidfn']
	forcast['weather'][0]=meteoparti[0]['partimetrologitoday']
	forcast['dfn'][1]=1
	forcast['weather'][1]=meteoparti[0]['partimetrologitomor']
	Temps['timestamp']=meteoparti[0]['partitimestamp']
	Temps['weather']=forcast
	db.close()
        return jsonResponse(Temps)
    if request.method == "POST" :
	get_json = request.get_json()
	day=get_json['weather'][0]['dfn']
	if day==0:
		db.execute("UPDATE partie SET PartiMetrologitoday=(%(today)s),PartiMetrologitomor=(%(tomor)s),Partidfn=(%(dfn)s),PartiTimestamp=(%(stamp)s)", {"today": get_json['weather'][0]['weather'],"tomor" : get_json['weather'][1]['weather'],"dfn" : get_json['weather'][0]['dfn'],"stamp": get_json['timestamp']})

	else :
		db.execute("UPDATE partie SET PartiMetrologitoday=(%(today)s),PartiMetrologitomor=(%(tomor)s),Partidfn=(%(dfn)s), PartiTimestamp=(%(stamp)s)", {"today": get_json['weather'][1]['weather'],"tomor" : get_json['weather'][0]['weather'],"dfn" : get_json['weather'][0]['dfn'],"stamp": get_json[0]['timestamp']})
		weathertoday=get_json['weather'][1]['weather']
		weathertomor=get_json['weather'][0]['weather']		
	db.close()
        return "OK:POST_METROLOGY"
#timestamp: int nb d'heure joue 0 aujourd'hui 1 demain
#weather:
#	forcast: // 2 forcast pour aujourd'hui et demain
#		dfn : int day from now - 0 aujourd'hui 1 demain
#		weather



##########################################################################################################################################
# Requête R3 - Sales
@app.route("/sales", methods=["POST"])
def sales():
    
    global json_table
    table={}
    #player: string
    #item : string
    #quantity
    db = Db()
    get_json = request.get_json()
    print"-----------------------------------------sales----------------------------------------------------------"
    for dep in range(len(get_json['sales'])):
	idrecette = db.select("SELECT idRecette FROM recette WHERE RecetteNom = %(nom)s",{"nom" : get_json['sales'][dep]['item']})
	monjoueur = db.select("SELECT * FROM joueur WHERE JoueurNom = %(name)s",{"name" : get_json['sales'][dep]['player']})
	db.execute("UPDATE avoir SET vendre=(%(vd)s) WHERE idRecette =%(idrect)s AND idJoueur=%(name)s", {"vd": 0 ,"idrect":idrecette[0]['idrecette'],"name" : monjoueur[0]['idjoueur']})
	db.execute("UPDATE avoir SET vendre=(%(vd)s) WHERE idRecette =%(idrect)s AND idJoueur=%(name)s", {"vd": get_json['sales'][dep]['quantity'],"idrect":idrecette[0]['idrecette'],"name" : monjoueur[0]['idjoueur']})

	avoir= db.select("SELECT * FROM avoir WHERE idRecette = %(rec)s AND idJoueur = %(nom)s",{"nom" : monjoueur[0]['idjoueur'],"rec" : idrecette[0]['idrecette']})

	newbudget=avoir[0]['recetteprix']*get_json['sales'][dep]['quantity']
	newbudget+=monjoueur[0]['joueurbudget']	
	db.execute("UPDATE joueur SET JoueurBudget=(%(vd)s) WHERE idJoueur=%(name)s", {"vd": newbudget,"name" : monjoueur[0]['idjoueur']})

    #json_table[value].update(get_json)
    db.close()

    return "OK"


##########################################################################################################################################
# Requête R6 - Instructions du joueur
@app.route("/actions/<playerName>", methods=["POST"])
def actionsPlayer(playerName):
    
#action:

    db = Db()
    get_json = request.get_json()
    print "----------------------------------action -----------------------------------------"
    monjoueur = db.select("SELECT * FROM joueur WHERE JoueurNom = %(name)s",{"name" : playerName})
    action=get_json['actions']
    #ajout recette
    if action['kind']=='recipe':

	idrecette = db.select ("INSERT INTO recette(RecetteNom) VALUES (%(nom)s) RETURNING idRecette", {"nom" : get_json['actions']['recipe']['name'] })
	racord =db.select ("INSERT INTO avoir(idRecette,idJoueur,vendre,RecettePrix) VALUES (%(rec)s,%(idjou)s,%(vd)s,%(Recpr)s) RETURNING idRecette", {"rec" : idrecette[0]['idrecette'],"idjou" : monjoueur[0]['idjoueur'],"vd": 0,"Recpr":0.0 })
	idingr={}
	for matable in range(len(get_json['actions']['recipe']['ingredients'])):
		idingr= db.select("SELECT idIngredient FROM ingredient WHERE IngredientNom=%(nom)s ",{"nom":get_json['actions']['recipe']['ingredients'][matable]['name']})

		if not idingr:
			print"vide"
		else:
			contenir = db.select ("INSERT INTO contenir(idRecette,idIngredient) VALUES (%(idrec)s,%(iding)s) RETURNING idRecette", {"idrec" : idrecette[0]['idrecette'],"iding" : idingr[0]['idingredient'] })
    #ajout panneau
    if action['kind']=='ad':

	act=action['radius'][0]
	act=int(act)*10

	if act>monjoueur[0]['joueurbudget']:

		fund={}
		fund['sufficientFunds']= False
		fund['totalCost']=action['radius']
		return jsonResponse(fund)
	newbud=monjoueur[0]['joueurbudget']-act

	db.execute("UPDATE joueur SET JoueurBudget=(%(new)s) WHERE JoueurNom = %(name)s", {"new" : newbud,"name" : playerName})
	contenir = db.select ("INSERT INTO panneau(PanneauPosX,PanneauPosY,PanneauInfluence,idJoueur) VALUES (%(x)s,%(y)s,%(inf)s,%(joueur)s) RETURNING idPanneau", {"x" : random.randrange(10),"y" : random.randrange(10),"inf" : action['radius'],"joueur" :monjoueur[0]['idjoueur'] })
	
    #vente drink
    if action['kind']=='drinks':
	print"------------------------------------",action['prepare'].keys()
	keyboisson=action['prepare'].keys()
	print"------------------------------------",action['prepare'][keyboisson[0]]
	idrecette=recette=db.select("SELECT * FROM recette WHERE RecetteNom=%(idrec)s ",{"idrec" : keyboisson[0]})
	db.execute("UPDATE avoir SET vendre=(%(vd)s),recetteprix=(%(recpri)s) WHERE idRecette =%(idrect)s AND idJoueur=%(name)s", {"recpri": action['price'][keyboisson[0]],"vd": action['prepare'][keyboisson[0]],"idrect":idrecette[0]['idrecette'],"name" : monjoueur[0]['idjoueur']})
    #global json_table
    #return json.dumps(json_table[value])
    return "OK:POST_" + playerName


##########################################################################################################################################
# Requête R2 -  Map
@app.route("/map", methods=["GET"])
def map():
    db = Db()
    mamap={}
    availableIngredients={}
    mamap['map']={}
    idrecette=recette=db.select("SELECT * FROM recette")
    print "----------------------------------map -----------------------------------------"

    ranking={}
    mamap['map']['ranking']=[]
    
    table={}
    table=db.select("SELECT JoueurNom FROM joueur ORDER BY JoueurBudget")
    
    for dep in range(len(table)):
	mamap['map']['ranking'].append(table[dep]['joueurnom'])
    #pour chaque joueur
    itemsByPlayer={}
    itemsByPlayer['location']={}


    mapItem={}
    nomjoueur="joueur"
    mamap['map']['itemsByPlayer']={}


    mamap['map']['playerInfo']={}



    mamap['map']['region']={}
    mamap['map']['region']['center']={}
    mamap['map']['region']['center']['latitude']=300.0
    mamap['map']['region']['center']['longitude']=300.0
    mamap['map']['region']['span']={}
    mamap['map']['region']['span']['latitudeSpan']=600.0
    mamap['map']['region']['span']['longitudeSpan']=600.0

    mamap['map']['playerInfo']={}

    mamap['map']['drinksByPlayer']={}    
#map:
#	region : 
#		center :
#			coordinates :
#				latitude
#				longitude
#		span :
#			coordinatesSpan :
#				latitudeSpan
#				longitudeSpan
	
#	ranking: string id/name all player

    for numjoueur in range(len(mamap['map']['ranking'])):

	monjoueur = db.select("SELECT * FROM joueur WHERE JoueurNom = %(name)s",{"name" : mamap['map']['ranking'][numjoueur]})

	if range(len(monjoueur))!=0 :
		
		pan = db.select("SELECT * FROM panneau WHERE idJoueur = %(idjou)s",{"idjou" : monjoueur[0]['idjoueur']})
		mag = db.select("SELECT * FROM magasin WHERE idJoueur = %(idjou)s",{"idjou" : monjoueur[0]['idjoueur']})
		avoir = db.select("SELECT * FROM avoir WHERE idJoueur = %(idjou)s",{"idjou" : monjoueur[0]['idjoueur']})
		nbpan=len(pan)
	#	itemsByPlayer:{mapItem: repeated pour tous les joueurs		
	#		kind :string stand ou at
	#		owner : string playername
	#		location :
	#			coordinates :
	#				latitude
	#				longitude
	#		influence : float distance
	#		}
		newplayeurname=mamap['map']['ranking'][numjoueur]
		mamap['map']['itemsByPlayer'][newplayeurname]=[]
		drinksbyplayer={}
		drinksbyplayer['kind']={}
		drinksbyplayer['location']={}
		drinksbyplayer['owner']={}
		drinksbyplayer['influence']={}
		drinksbyplayer['location']={}
		drinksbyplayer['location']['latitude']={}
		drinksbyplayer['location']['longitude']={}


		#parti panneau

		if nbpan!= 0:
			for matable in range(len(pan)):
				drinksbyplayer['kind']= 'ad'
				drinksbyplayer['owner']= newplayeurname
				drinksbyplayer['location']['latitude']=pan[matable]['panneauposy']
				drinksbyplayer['location']['longitude']= pan[matable]['panneauposx']
				drinksbyplayer['influence']=pan[matable]['panneauinfluence']
				mamap['map']['itemsByPlayer'][newplayeurname].append(drinksbyplayer)
			
		drinksbyplayer['kind']= 'stand'
		drinksbyplayer['owner']= monjoueur[0]['joueurnom']
		drinksbyplayer['location']['latitude']=mag[0]['magasinposy']
		drinksbyplayer['location']['longitude']= mag[0]['magasinposx']
		drinksbyplayer['influence']=mag[0]['magasininfluence']
		mamap['map']['itemsByPlayer'][newplayeurname].append(drinksbyplayer)
		

	#	playerInfo:{playerInfo: repeated pour tous les joueurs
	#		cash: float
	#		sales: int nombre de vendu par recettes
	#		profit : float -> negatif perdu
	#		drinksOffered:
	#			name
	#			price
	#			hasAlcohol
	#			isCold
	#		}
	
		mamap['map']['playerInfo'][newplayeurname]={}
		mamap['map']['playerInfo'][newplayeurname]['cash']={}#float
		mamap['map']['playerInfo'][newplayeurname]['cash']= monjoueur[0]['joueurbudget']
		mamap['map']['playerInfo'][newplayeurname]['sales']={}#int
		mamap['map']['playerInfo'][newplayeurname]['profit']={}#float
		mamap['map']['playerInfo'][newplayeurname]['drinksOffered']=[]
		drinksOffered={}
		drinksOffered['name']={}
		drinksOffered['price']={}
		drinksOffered['hasAlcohol']={}
		drinksOffered['isCold']={}
	
		totalvend = 0
		
		mamap['map']['drinksByPlayer'][newplayeurname]=[]
		drinksByPlayer={}
		drinksByPlayer['name']={}#string
		drinksByPlayer['price']={}#float
		drinksByPlayer['hasAlcohol']={}#bo
		drinksByPlayer['isCold']={}#bo
		for dep in range(len(avoir)):
			if not avoir[0]['vendre']:
				avoir[0]['vendre']=0		
		
		for dep in range(len(avoir)):
			
			totalvend+=avoir[0]['vendre']
			nomrec = db.select("SELECT RecetteNom FROM recette WHERE idRecette = %(idre)s",{"idre" : avoir[dep]['idrecette']})
			drinksOffered['name'] =	nomrec[0]['recettenom']
			drinksOffered['price']= avoir[0]['recetteprix']
			drinksOffered['hasAlcohol']= False
			drinksOffered['isCold']= True
			drinksByPlayer['name']=nomrec[0]['recettenom']
			
			drinksByPlayer['price']= avoir[0]['recetteprix']
			drinksByPlayer['hasAlcohol']=False
			drinksByPlayer['isCold']=True
			print"--------------------------------------",drinksByPlayer
		
			mamap['map']['playerInfo'][newplayeurname]['drinksOffered'].append(drinksOffered)
			print"--------------------------------------",mamap['map']['playerInfo'][newplayeurname]['drinksOffered']
			mamap['map']['drinksByPlayer'][newplayeurname].append(drinksByPlayer)

		mamap['map']['playerInfo'][newplayeurname]['sales'] = totalvend
		mamap['map']['playerInfo'][newplayeurname]['profit']=0






		

    #return json.dumps(json_table)
    return jsonResponse(mamap)


##########################################################################################################################################
# Requête R5 - Détails d'une partie
@app.route("/map/<playerName>", methods=["GET"])
def mapPlayer(playerName):
    db = Db()
    mamap={}
    availableIngredients={}
    mamap['map']={}
    idrecette=recette=db.select("SELECT * FROM recette")
    print "----------------------------------map -----------------------------------------"

    ranking={}
    mamap['map']['ranking']=[]
    
    table={}
    table=db.select("SELECT JoueurNom FROM joueur ORDER BY JoueurBudget")
    
    for dep in range(len(table)):
	mamap['map']['ranking'].append(table[dep]['joueurnom'])
    #pour chaque joueur
    itemsByPlayer={}
    itemsByPlayer['location']={}


    mapItem={}
    nomjoueur="joueur"
    mamap['map']['itemsByPlayer']={}


    mamap['map']['playerInfo']={}



    mamap['map']['region']={}
    mamap['map']['region']['center']={}
    mamap['map']['region']['center']['latitude']=300.0
    mamap['map']['region']['center']['longitude']=300.0
    mamap['map']['region']['span']={}
    mamap['map']['region']['span']['latitudeSpan']=600.0
    mamap['map']['region']['span']['longitudeSpan']=600.0

    mamap['map']['playerInfo']={}

    mamap['map']['drinksByPlayer']={}    
#map:
#	region : 
#		center :
#			coordinates :
#				latitude
#				longitude
#		span :
#			coordinatesSpan :
#				latitudeSpan
#				longitudeSpan
	
#	ranking: string id/name all player




    monjoueur = db.select("SELECT * FROM joueur WHERE JoueurNom = %(name)s",{"name" : playerName})
    
    if range(len(monjoueur))!=0 :
	
	pan = db.select("SELECT * FROM panneau WHERE idJoueur = %(idjou)s",{"idjou" : monjoueur[0]['idjoueur']})
	mag = db.select("SELECT * FROM magasin WHERE idJoueur = %(idjou)s",{"idjou" : monjoueur[0]['idjoueur']})
	avoir = db.select("SELECT * FROM avoir WHERE idJoueur = %(idjou)s",{"idjou" : monjoueur[0]['idjoueur']})
	nbpan=len(pan)
#	itemsByPlayer:{mapItem: repeated pour tous les joueurs		
#		kind :string stand ou at
#		owner : string playername
#		location :
#			coordinates :
#				latitude
#				longitude
#		influence : float distance
#		}
	
	mamap['map']['itemsByPlayer'][playerName]=[]
	drinksbyplayer={}
	drinksbyplayer['kind']={}
	drinksbyplayer['location']={}
	drinksbyplayer['owner']={}
	drinksbyplayer['influence']={}
	drinksbyplayer['location']={}
	drinksbyplayer['location']['latitude']={}
	drinksbyplayer['location']['longitude']={}
	if nbpan!= 0:
		#parti panneau
		
		for matable in range(len(pan)):
			drinksbyplayer['kind'][matable]= 'at'
			drinksbyplayer['owner'][matable]= playerName
			drinksbyplayer['location'][matable]['latitude']=pan[matable]['panneauposy']
			drinksbyplayer['location'][matable]['longitude']= pan[matable]['panneauposx']
			drinksbyplayer['influence'][matable]=pan[matable]['panneauinfluence']
		#partie mag
		drinksbyplayer['kind'][nbpan+1]= 'stand'
		drinksbyplayer['owner'][nbpan+1]= playerName	
		drinksbyplayer['location'][nbpan+1]['latitude']=mag[nbpan+1]['magasinposy']
		drinksbyplayer['location'][nbpan+1]['longitude']= mag[nbpan+1]['magasinposx']
		drinksbyplayer['influence'][nbpan+1]=mag[nbpan+1]['magasininfluence']
	else:
		
		drinksbyplayer['kind']= 'stand'
		drinksbyplayer['owner']= monjoueur[0]['joueurnom']
		drinksbyplayer['location']['latitude']=mag[0]['magasinposy']
		drinksbyplayer['location']['longitude']= mag[0]['magasinposx']
		drinksbyplayer['influence']=mag[0]['magasininfluence']
	mamap['map']['itemsByPlayer'][playerName].append(drinksbyplayer)
	
#	playerInfo:{playerInfo: repeated pour tous les joueurs
#		cash: float
#		sales: int nombre de vendu par recettes
#		profit : float -> negatif perdu
#		drinksOffered:
#			name
#			price
#			hasAlcohol
#			isCold
#		}
	
	mamap['map']['playerInfo'][playerName]={}
	mamap['map']['playerInfo'][playerName]['cash']={}#float
	mamap['map']['playerInfo'][playerName]['cash']= monjoueur[0]['joueurbudget']
	mamap['map']['playerInfo'][playerName]['sales']={}#int
	mamap['map']['playerInfo'][playerName]['profit']={}#float
	mamap['map']['playerInfo'][playerName]['drinksOffered']=[]
	drinksOffered={}
	drinksOffered['name']={}
	drinksOffered['price']={}
	drinksOffered['hasAlcohol']={}
	drinksOffered['isCold']={}

	totalvend = 0
		
	mamap['map']['drinksByPlayer'][playerName]=[]
	drinksByPlayer={}
	drinksByPlayer['name']={}#string
	drinksByPlayer['price']={}#float
	drinksByPlayer['hasAlcohol']={}#bo
	drinksByPlayer['isCold']={}#bo
	for dep in range(len(avoir)):
		if not avoir[0]['vendre']:
			avoir[0]['vendre']=0		
		
	for dep in range(len(avoir)):
		totalvend+=avoir[0]['vendre']
		nomrec = db.select("SELECT RecetteNom FROM recette WHERE idRecette = %(idre)s",{"idre" : avoir[0]['idrecette']})
		drinksOffered['name'] =	nomrec[0]['recettenom']
		drinksOffered['price']= avoir[0]['recetteprix']
		drinksOffered['hasAlcohol']= False
		drinksOffered['isCold']= True
		drinksByPlayer['name']=nomrec[0]['recettenom']
			
		drinksByPlayer['price']= avoir[0]['recetteprix']
		drinksByPlayer['hasAlcohol']=False
		drinksByPlayer['isCold']=True

	mamap['map']['playerInfo'][playerName]['sales'] = totalvend
	mamap['map']['playerInfo'][playerName]['drinksOffered'].append(drinksOffered)
	mamap['map']['playerInfo'][playerName]['profit']=0






	mamap['map']['drinksByPlayer'][playerName].append(drinksByPlayer)

    #return json.dumps(json_table)
    return jsonResponse(mamap)


#availableIngredients:
#		name string
#		cost float
#		hasAlcohol bool
#		isCold bool	
#map:
#	region:
#		center:
#			latitude : float
#			longitude : flot
#		span:
#			latitudeSpan : float
#			longitudeSpan : float
#
#	ranking: string
#	itemsByPlayer :
#		mapItem :
#			kind: string stand or ad
#			owner: string
#			location :
#				latitude : float
#			influence : float
#playerInfo:
#	cash: float
#	sales: int nombre de vendu
#	profit : float -> negatif perdu
#	drinksOffered:
#		name
#		price
#		has alcohol
#		is cold
#	}

##########################################################################################################################################
# Requête R9 - Liste ingrédients
@app.route("/ingredients", methods=["GET"])
def ingredients():
    print("-----------------------------------------ingredients----------------------------------------------------------")
    db = Db()
    table={}
    result = db.select("SELECT * FROM ingredient")
    #print(result)
    table['ingredients'] = result
    db.close()
    return jsonResponse(table)




if __name__ == "__main__":
    app.run()
