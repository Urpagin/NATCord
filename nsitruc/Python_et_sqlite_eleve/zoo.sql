DROP TABLE IF EXISTS LesMaladies;
DROP TABLE IF EXISTS LesAnimaux;
DROP TABLE IF EXISTS LesResponsables;
DROP TABLE IF EXISTS LesGardiens;
DROP TABLE IF EXISTS LesEmployes;
DROP TABLE IF EXISTS LesCages;

CREATE TABLE LesCages(
     noCage int, 
     fonction varchar(100), 
     noAllee int,
     CONSTRAINT PK_Cages PRIMARY KEY(noCage)
);
    
INSERT INTO LesCages VALUES (11,'fauve', 10);
INSERT INTO LesCages VALUES (1,'fosse', 1);
INSERT INTO LesCages VALUES (2,'aquarium', 1);
INSERT INTO LesCages VALUES (3,'petits oiseaux', 2);
INSERT INTO LesCages VALUES (4,'grand aquarium', 1);
INSERT INTO LesCages VALUES (12,'fauve', 10);
insert into LesCages VALUES (5,'fauve',10);

CREATE TABLE LesAnimaux (
     nomA varchar(100), 
     sexe varchar(12), 
     type varchar(100), 
     pays varchar(100), 
     anNais int, 
     noCage int,
     CONSTRAINT PK_Animaux PRIMARY KEY (nomA),
     CONSTRAINT FK_Animaux_Cages FOREIGN KEY (noCage) REFERENCES LesCages(noCage)
);
     
INSERT INTO LesAnimaux VALUES ('Charly', 'male', 'lion', 'Kenya', 1999, 12);
INSERT INTO LesAnimaux VALUES ('Arthur', 'male', 'ours', 'France', 2000, 1);
INSERT INTO LesAnimaux VALUES ('Chloe', 'femelle', 'pie', 'France', 2001, 3);
INSERT INTO LesAnimaux VALUES ('Milou', 'male', 'leopard', 'France', 2013, 11);
INSERT INTO LesAnimaux VALUES ('Tintin', 'male', 'leopard', 'France', 2013, 11);
INSERT INTO LesAnimaux VALUES ('Charlotte', 'femelle', 'lion', 'Kenya', 2012, 12);
INSERT INTO LesAnimaux VALUES ('Huan','femelle','panda','Chine',2005,1);
INSERT INTO LesAnimaux VALUES ('Lola','femelle','lion','Kenya',1999,5);
INSERT INTO LesAnimaux VALUES ('Tola','femelle','ours','Espagne', 2003,1);
INSERT INTO LesAnimaux VALUES ('Tai Lung','femelle','leopard','Chine',2006,5);


CREATE TABLE LesMaladies(
  nomA varchar(100), 
  nomM varchar(100), 
  CONSTRAINT PK_Maladies PRIMARY KEY(nomA, nomM), 
  CONSTRAINT FK_Maladies_Animaux FOREIGN KEY (nomA) REFERENCES LesAnimaux(nomA)
);

INSERT INTO LesMaladies VALUES ('Charlotte', 'grippe');
INSERT INTO LesMaladies VALUES ('Charly', 'rage de dents');
INSERT INTO LesMaladies VALUES ('Charly', 'grippe');
INSERT INTO LesMaladies VALUES ('Milou', 'angine');
INSERT INTO LesMaladies VALUES ('Chloe', 'grippe');
INSERT INTO LesMaladies VALUES ('Huan','angine');
INSERT INTO LesMaladies VALUES ('Huan','grippe');
INSERT INTO LesMaladies VALUES ('Huan','rage de dents');

CREATE TABLE LesEmployes(
  nomE varchar(100), 
  adresse varchar(200), 
  CONSTRAINT PK_Employes PRIMARY KEY (nomE)
);

INSERT INTO LesEmployes VALUES ('Peyrin', 'Noumea');
INSERT INTO LesEmployes VALUES ('Berrut', 'Sartene');
INSERT INTO LesEmployes VALUES ('Maraninchi', 'Calvi');
INSERT INTO LesEmployes VALUES ('Cartade', 'Pointe a Pitre');
INSERT INTO LesEmployes VALUES ('Scholl', 'Ushuaia');
INSERT INTO LesEmployes VALUES ('Adiba', 'Papeete');


CREATE TABLE LesResponsables(
  noAllee int, 
  nomE varchar(100), 
  CONSTRAINT PK_Responsables PRIMARY KEY (noAllee), 
  CONSTRAINT FK_Responsables_Employes FOREIGN KEY (nomE) REFERENCES LesEmployes(nomE)
);

INSERT INTO LesResponsables VALUES (10, 'Peyrin');
INSERT INTO LesResponsables VALUES (1, 'Adiba');
INSERT INTO LesResponsables VALUES (2, 'Cartade');


CREATE TABLE LesGardiens(
  noCage int, nomE varchar(100), 
  CONSTRAINT PK_Gardiens PRIMARY KEY (noCage, nomE), 
  CONSTRAINT FK_Gardiens_Employes FOREIGN KEY (nomE) REFERENCES LesEmployes(nomE), 
  CONSTRAINT FK_Gardians_Cages FOREIGN KEY (noCage) REFERENCES LesCages(noCage)
);

INSERT INTO LesGardiens VALUES (12, 'Berrut');
INSERT INTO LesGardiens VALUES (12, 'Maraninchi');
INSERT INTO LesGardiens VALUES (11, 'Berrut');
INSERT INTO LesGardiens VALUES (11, 'Maraninchi');
INSERT INTO LesGardiens VALUES (1, 'Scholl');
INSERT INTO LesGardiens VALUES (3, 'Scholl');
INSERT INTO LesGardiens VALUES (12, 'Scholl');
INSERT INTO LesGardiens VALUES (11, 'Scholl');
INSERT INTO LesGardiens VALUES (5, 'Scholl');