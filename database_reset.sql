DROP TABLE IF EXISTS ingredient CASCADE;
DROP TABLE IF EXISTS recette CASCADE; 
DROP TABLE IF EXISTS joueur CASCADE;
DROP TABLE IF EXISTS panneauPub CASCADE; 
DROP TABLE IF EXISTS taxe CASCADE;
DROP TABLE IF EXISTS meteo CASCADE;
DROP TABLE IF EXISTS carte CASCADE;

/*Table déduite à partir des relations du modèle jmerise*/
DROP TABLE IF EXISTS contenir CASCADE;
DROP TABLE IF EXISTS vendre CASCADE;
DROP TABLE IF EXISTS faireAction CASCADE;


/*Création des tables avec les données par défaut*/
CREATE TABLE ingredient (
	id_ingredient	SERIAL PRIMARY KEY,
	nom_ingredient	Varchar(25),
	prix_ingredient	Float
);

CREATE TABLE recette (
	id_recette		SERIAL PRIMARY KEY,
	recette_nom		Varchar(25),
	recette_prix_achat	Varchar(25)
);

CREATE TABLE joueur (
	id_joueur		SERIAL PRIMARY KEY,
	pseudo_joueur		Varchar(25),
	isConnected_joueur	Boolean,
	positionX_joueur	Float,
	positionY_joueur	Float,
	latitude_joueur		Float,
	longitude_joueur	Float
);

CREATE TABLE panneauPub (
	id_panneauPub		SERIAL PRIMARY KEY,
	prix_panneauPub		Float,
	positionX_panneauPub	Float,
	positionY_panneauPub	Float,
	latitude_panneauPub	Float,
	longitude_panneauPub	Float,
/*Ici, il y a une foreign key a mettre maisplus tard*/
	id_panneauPub_joueur	Int
);

CREATE TABLE taxe (
	id_taxe			SERIAL PRIMARY KEY,
	tva_taxe		Float,
	montant_fixe_taxe	Float,
	jour_taxe		Float,
/*Ici, il y a une foreign key a mettre maisplus tard*/
	id_taxe_joueur		Int
);

CREATE TABLE meteo (
	id_meteo 		SERIAL PRIMARY KEY,
	actuelle_meteo		Varchar(25),
	previsionnelle_meteo	Varchar(25),
	jour_meteo		Int
);

CREATE TABLE carte (
	id_carte	SERIAL PRIMARY KEY,
	longueur_carte	Float,
	largeur_carte	Float
);

/*Contient deux clés étrangères des tables : recette et ingredient*/
CREATE TABLE contenir (
	id_contenir_recette	Int,
	id_contenir_ingredient	Int
);

/*Contient deux clés étrangères des tables: recette et joueur*/
CREATE TABLE vendre (
	prix_vendre		Float,
	id_vendre_recette	Int,
	id_vendre_joueur	Int

);

/*contient deux clés étrangères des tables: recette et joueur*/
CREATE TABLE faireAction (
	id_action_recette	Int,
	id_action_joueur	Int
);

/*Cette partie est a faire verifier et valider*/
/*Introduction des relations et des clés dans chaque table*/
/*Pour la table faireAction*/
ALTER TABLE faireAction ADD CONSTRAINT FK_id_action_recette FOREIGN KEY (id_action_recette) REFERENCES recette(id_recette);
ALTER TABLE faireAction ADD CONSTRAINT FK_id_action_joueur FOREIGN KEY (id_action_joueur) REFERENCES joueur(id_joueur);

/*Pour la table vendre*/
ALTER TABLE vendre ADD CONSTRAINT FK_id_vendre_recette FOREIGN KEY (id_vendre_recette) REFERENCES recette(id_recette);
ALTER TABLE vendre ADD CONSTRAINT FK_id_vendre_joueur FOREIGN KEY (id_vendre_joueur) REFERENCES joueur(id_joueur);

/*Pour la table contenir*/
ALTER TABLE contenir ADD CONSTRAINT FK_id_contenir_recette FOREIGN KEY (id_contenir_recette) REFERENCES recette(id_recette);
ALTER TABLE contenir ADD CONSTRAINT FK_id_contenir_ingredient FOREIGN KEY (id_contenir_ingredient) REFERENCES ingredient(id_ingredient);

/*Pour la table panneauPub*/
ALTER TABLE panneauPub ADD CONSTRAINT FK_id_panneauPub_joueur FOREIGN KEY (id_panneauPub_joueur) REFERENCES joueur(id_joueur);

/*Pour la table taxe*/
ALTER TABLE taxe ADD CONSTRAINT FK_id_taxe_joueur FOREIGN KEY (id_taxe_joueur) REFERENCES joueur(id_joueur);



/*
Ce message sert à voir les requete alter table
https://www.postgresql.org/message-id/CALnrrJTfs=asHXkiGEX0GecG5HEX5rz5TEhpykerftniurVqfw@mail.gmail.com*/
