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
        PanneauPosX      Double precision ,
        PanneauPosY      Double precision ,
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
        MagasinPosX Double precision ,
        MagasinPosY Double precision ,
	MagasinInfluence Double precision ,
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
	PartiMetrologitoday Char (25) ,
	PartiMetrologitomor Char (25) ,
	Partidfn int ,
	PartiTimestamp int ,
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
        RecetteTemperature Bool ,
        RecetteAlcohol      Bool ,
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
        IngredientAlcohol      Bool ,
        PRIMARY KEY (idIngredient )
);

--------------------------------------------------------------
-- Table: avoir
--------------------------------------------------------------
CREATE TABLE avoir(
	vendre    Int ,
        idJoueur    Int NOT NULL ,
        idRecette Int NOT NULL ,
	RecettePrix Double precision,
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
INSERT INTO partie(PartieNom,PartiMetrologitoday,PartiMetrologitomor) VALUES
   ('maparti','sunny','sunny');
INSERT INTO joueur(JoueurNom,JoueurBudget,IdPartie) VALUES
   ('moi','50',(select idPartie from partie)),('toi','50',(select idPartie from partie));
INSERT INTO ingredient (IngredientNom,IngredientPrix,IngredientTemperature,IngredientAlcohol) VALUES 
   ('eg', '0.5', '0', '0'),('sirop', '1', '0', '0'),('glace', '2', '0', '0'),('sucre', '4', '0', '0'),('chocolat', '4', '0', '0'),('legume', '4', '0', '0'),('lait', '4', '0', '0'),('alcohol', '4', '0', '1'),('cafe', '4', '1', '0'),('the', '4', '1', '0');
INSERT INTO recette (RecetteNom) VALUES 
   ('eg'),('limonade'),('cafe'),('soupe');
INSERT INTO contenir (idRecette,idIngredient) VALUES
   ((select idRecette from recette where RecetteNom='eg'),(select idIngredient from ingredient where IngredientNom='eg'));
INSERT INTO contenir (idRecette,idIngredient) VALUES
   ((select idRecette from recette where RecetteNom='cafe'),(select idIngredient from ingredient where IngredientNom='cafe'));


INSERT INTO contenir (idRecette,idIngredient) VALUES
   ((select idRecette from recette where RecetteNom='soupe'),(select idIngredient from ingredient where IngredientNom='eg'));
INSERT INTO contenir (idRecette,idIngredient) VALUES
   ((select idRecette from recette where RecetteNom='soupe'),(select idIngredient from ingredient where IngredientNom='legume'));


INSERT INTO avoir (idRecette,idJoueur,vendre,RecettePrix) VALUES
   ((select idRecette from recette where RecetteNom='soupe'),(select idJoueur from joueur where JoueurNom='toi'),'4','6.0'),((select idRecette from recette where RecetteNom='soupe'),(select idJoueur from joueur where JoueurNom='moi'),'10','8.0');





