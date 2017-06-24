--------------------------------------------------------------
--        Script MySQL.
--------------------------------------------------------------
DROP TABLE IF EXISTS panneau CASCADE;
DROP TABLE IF EXISTS magasin CASCADE;
DROP TABLE IF EXISTS partie CASCADE;
DROP TABLE IF EXISTS joueur CASCADE;
DROP TABLE IF EXISTS recette CASCADE;
DROP TABLE IF EXISTS ingredient CASCADE;
DROP TABLE IF EXISTS contenir CASCADE;
DROP TABLE IF EXISTS compatible CASCADE;
DROP TABLE IF EXISTS avoir CASCADE;

--------------------------------------------------------------
-- Table: panneau
--------------------------------------------------------------




--CREATE SEQUENCE panneau_seq;

CREATE TABLE panneau(
        idPanneau        int  Default nextval ('panneau_seq')  NOT NULL ,
        PanneauPosX      Int ,
        PanneauPosY      Int ,
        PanneauInfluence Double precision ,
        idJoueur         Int ,
        PRIMARY KEY (idPanneau )
);


--------------------------------------------------------------
-- Table: magasin
--------------------------------------------------------------

--CREATE SEQUENCE magasin_seq;

CREATE TABLE magasin(
        idMagasin   int  Default nextval ('magasin_seq')  NOT NULL ,
        MagasinPosX Int ,
        MagasinPosY Int ,
        idJoueur    Int ,
        PRIMARY KEY (idMagasin )
);


--------------------------------------------------------------
-- Table: partie
--------------------------------------------------------------

--CREATE SEQUENCE partie_seq;

CREATE TABLE partie(
        IdPartie  int  Default nextval ('partie_seq')  NOT NULL ,
        PartieNom Char (25) ,
        PRIMARY KEY (IdPartie )
);


--------------------------------------------------------------
-- Table: joueur
--------------------------------------------------------------

--CREATE SEQUENCE joueur_seq;

CREATE TABLE joueur(
        idJoueur     int  Default nextval ('joueur_seq')  NOT NULL ,
        JoueurNom    Char (25) ,
        JoueurBudget Double precision ,
        IdPartie     Int ,
        PRIMARY KEY (idJoueur )
);


--------------------------------------------------------------
-- Table: recette
--------------------------------------------------------------

--CREATE SEQUENCE recette_seq;

CREATE TABLE recette(
        idRecette  int  Default nextval ('recette_seq')  NOT NULL ,
        RecetteNom Char (25) ,
        PRIMARY KEY (idRecette )
);


--------------------------------------------------------------
-- Table: ingredient
--------------------------------------------------------------

--CREATE SEQUENCE ingredient_seq;

CREATE TABLE ingredient(
        idIngredient          int  Default nextval ('ingredient_seq')  NOT NULL ,
        IngredientNom         Char (25) ,
        IngredientPrix        Double precision ,
        IngredientTemperature Bool ,
        IngredientAlcool      Bool ,
        PRIMARY KEY (idIngredient )
);

--------------------------------------------------------------
-- Table: avoir
--------------------------------------------------------------
CREATE TABLE avoir(
        idJoueur    Int NOT NULL ,
        idRecette Int NOT NULL ,
        PRIMARY KEY (idJoueur ,idRecette )
);

--------------------------------------------------------------
-- Table: contenir
--------------------------------------------------------------

CREATE TABLE contenir(
        idRecette    Int NOT NULL ,
        idIngredient Int NOT NULL ,
        PRIMARY KEY (idRecette ,idIngredient )
);


--------------------------------------------------------------
-- Table: compatible
--------------------------------------------------------------

CREATE TABLE compatible(
        idIngredient            Int NOT NULL ,
        idIngredient_ingredient Int NOT NULL ,
        PRIMARY KEY (idIngredient ,idIngredient_ingredient )
);

ALTER TABLE panneau ADD CONSTRAINT FK_panneau_idJoueur FOREIGN KEY (idJoueur) REFERENCES joueur(idJoueur);
ALTER TABLE magasin ADD CONSTRAINT FK_magasin_idJoueur FOREIGN KEY (idJoueur) REFERENCES joueur(idJoueur);
ALTER TABLE joueur ADD CONSTRAINT FK_joueur_IdPartie FOREIGN KEY (IdPartie) REFERENCES partie(IdPartie);

ALTER TABLE avoir ADD CONSTRAINT FK_avoir_idJoueur FOREIGN KEY (idJoueur) REFERENCES joueur(idJoueur);
ALTER TABLE avoir ADD CONSTRAINT FK_avoir_idRecette FOREIGN KEY (idRecette) REFERENCES recette(idRecette);

ALTER TABLE contenir ADD CONSTRAINT FK_contenir_idRecette FOREIGN KEY (idRecette) REFERENCES recette(idRecette);
ALTER TABLE contenir ADD CONSTRAINT FK_contenir_idIngredient FOREIGN KEY (idIngredient) REFERENCES ingredient(idIngredient);
ALTER TABLE compatible ADD CONSTRAINT FK_compatible_idIngredient FOREIGN KEY (idIngredient) REFERENCES ingredient(idIngredient);
ALTER TABLE compatible ADD CONSTRAINT FK_compatible_idIngredient_ingredient FOREIGN KEY (idIngredient_ingredient) REFERENCES ingredient(idIngredient);


--------------------------------------------------------------
-- Insert
--------------------------------------------------------------

INSERT INTO ingredient (IngredientNom,IngredientPrix,IngredientTemperature,IngredientAlcool) VALUES 
   ('Eau', '0.5', '0', '0'),('orange', '1', '0', '0'),('graine de cafe', '2', '0', '0'),('légume', '4', '0', '0');
INSERT INTO recette (RecetteNom) VALUES 
   ('Eau'),('limonade'),('cafe'),('soupe');
INSERT INTO contenir (idRecette,idIngredient) VALUES 
   (SELECT idRecette from recette where RecetteNom=Eau);
