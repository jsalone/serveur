DROP TABLE IF EXISTS possede;
DROP TABLE IF EXISTS avoir;
DROP TABLE IF EXISTS fourni;
DROP TABLE IF EXISTS construit;
DROP TABLE IF EXISTS developpe;
DROP TABLE IF EXISTS constituer;
DROP TABLE IF EXISTS creer;
DROP TABLE IF EXISTS prets;
DROP TABLE IF EXISTS Monde;
DROP TABLE IF EXISTS Joueur;
DROP TABLE IF EXISTS Village;
DROP TABLE IF EXISTS Matiere;
DROP TABLE IF EXISTS Batiment;
DROP TABLE IF EXISTS Recherche;
DROP TABLE IF EXISTS Soldat;
DROP TABLE IF EXISTS Armee;

--CREATE TABLE prets (id SERIAL primary key,quoi varchar,qui varchar,status varchar);

CREATE TABLE Monde(
        idmonde   SERIAL primary key ,
        monde_nom Varchar 
);



CREATE TABLE Joueur(
        id_joueur     SERIAL primary key ,
        joueur_mail   Varchar (255) ,
        joueur_mtp    Varchar (25) ,
        joueur_pseudo Varchar (25) 
);


CREATE TABLE Village(
        id_village  SERIAL primary key ,
        village_nom Varchar (25) 
);


CREATE TABLE Matiere(
        id_matiere          SERIAL primary key ,
        matiere_nom         Varchar (25) ,
        matiere_description Varchar (255) ,
        matiere_montant     double precision ,
        matiere_valeur      double precision 
);

CREATE TABLE Batiment(
        id_batiment          SERIAL primary key ,
        batiment_nom         Varchar (25) ,
        batiment_niv         double precision ,
        batiment_description Varchar (255) ,
        batiment_mis_a_jour  Time 
);


CREATE TABLE Recherche(
        id_recherche          SERIAL primary key ,
        recherche_nom         Varchar (255) ,
        recherche_description Varchar (255) 
);


CREATE TABLE Soldat(
        id_soldat          SERIAL primary key ,
        soldat_nom         Varchar (255) ,
        soldat_description Varchar (255) ,
        soldat_nombre      double precision ,
        soldat_attack      double precision ,
        soldat_defense     double precision ,
        soldat_vitesse     double precision ,
        soldat_effet       Bool 
);


CREATE TABLE Armee(
        id_armee SERIAL primary key 
);


CREATE TABLE possede(
        idmonde   Int NOT NULL ,
        id_joueur Int NOT NULL ,
        PRIMARY KEY (idmonde ,id_joueur )
);


CREATE TABLE avoir(
        id_joueur  Int NOT NULL ,
        id_village Int NOT NULL ,
        PRIMARY KEY (id_joueur ,id_village )
);


CREATE TABLE fourni(
        id_village Int NOT NULL ,
        id_matiere Int NOT NULL ,
        PRIMARY KEY (id_village ,id_matiere )
);


CREATE TABLE construit(
        id_village  Int NOT NULL ,
        id_batiment Int NOT NULL ,
        PRIMARY KEY (id_village ,id_batiment )
);


CREATE TABLE developpe(
        id_recherche Int NOT NULL ,
        id_village   Int NOT NULL ,
        PRIMARY KEY (id_recherche ,id_village )
);


CREATE TABLE constituer(
        id_soldat Int NOT NULL ,
        id_armee  Int NOT NULL ,
        PRIMARY KEY (id_soldat ,id_armee )
);


CREATE TABLE creer(
        id_armee   Int NOT NULL ,
        id_village Int NOT NULL ,
        PRIMARY KEY (id_armee ,id_village )
);



ALTER TABLE possede ADD CONSTRAINT FK_possede_idmonde FOREIGN KEY (idmonde) REFERENCES Monde(idmonde);
ALTER TABLE possede ADD CONSTRAINT FK_possede_id_joueur FOREIGN KEY (id_joueur) REFERENCES Joueur(id_joueur);
ALTER TABLE avoir ADD CONSTRAINT FK_avoir_id_joueur FOREIGN KEY (id_joueur) REFERENCES Joueur(id_joueur);
ALTER TABLE avoir ADD CONSTRAINT FK_avoir_id_village FOREIGN KEY (id_village) REFERENCES Village(id_village);
ALTER TABLE fourni ADD CONSTRAINT FK_fourni_id_village FOREIGN KEY (id_village) REFERENCES Village(id_village);
ALTER TABLE fourni ADD CONSTRAINT FK_fourni_id_matiere FOREIGN KEY (id_matiere) REFERENCES Matiere(id_matiere);
ALTER TABLE construit ADD CONSTRAINT FK_construit_id_village FOREIGN KEY (id_village) REFERENCES Village(id_village);
ALTER TABLE construit ADD CONSTRAINT FK_construit_id_batiment FOREIGN KEY (id_batiment) REFERENCES Batiment(id_batiment);
ALTER TABLE developpe ADD CONSTRAINT FK_developpe_id_recherche FOREIGN KEY (id_recherche) REFERENCES Recherche(id_recherche);
ALTER TABLE developpe ADD CONSTRAINT FK_developpe_id_village FOREIGN KEY (id_village) REFERENCES Village(id_village);
ALTER TABLE constituer ADD CONSTRAINT FK_constituer_id_soldat FOREIGN KEY (id_soldat) REFERENCES Soldat(id_soldat);
ALTER TABLE constituer ADD CONSTRAINT FK_constituer_id_armee FOREIGN KEY (id_armee) REFERENCES Armee(id_armee);
ALTER TABLE creer ADD CONSTRAINT FK_creer_id_armee FOREIGN KEY (id_armee) REFERENCES Armee(id_armee);
ALTER TABLE creer ADD CONSTRAINT FK_creer_id_village FOREIGN KEY (id_village) REFERENCES Village(id_village);

--INSERT INTO prets (quoi,qui,status) VALUES ('test','moi','encours');
--INSERT INTO prets (quoi,qui,status) VALUES ('plus','toi','finis');

INSERT INTO Monde (monde_nom) VALUES ('monde1');
