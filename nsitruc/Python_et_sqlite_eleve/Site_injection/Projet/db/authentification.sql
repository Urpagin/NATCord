
DROP TABLE IF EXISTS "Utilisateurs";
CREATE TABLE IF NOT EXISTS "Utilisateurs" (
	"Login"	TEXT,
	"Password"	TEXT,
	"Nom"	TEXT,
	"Prénom"	TEXT,
	"Privilèges"	TEXT,
	PRIMARY KEY("Login")
);

INSERT INTO "Utilisateurs" ("Login","Password","Nom","Prénom","Privilèges") VALUES ('LukeS','Luke5','Skywalker','Luke','user');
INSERT INTO "Utilisateurs" ("Login","Password","Nom","Prénom","Privilèges") VALUES ('LeiaS','Le1a5','Skywalker','Leïa','admin');
INSERT INTO "Utilisateurs" ("Login","Password","Nom","Prénom","Privilèges") VALUES ('Ackbar','Am1ral','Ackbar','Gial','user');
INSERT INTO "Utilisateurs" ("Login","Password","Nom","Prénom","Privilèges") VALUES ('admin','@dmin','Skywalker','Anakin','admin');
INSERT INTO "Utilisateurs" ("Login","Password","Nom","Prénom","Privilèges") VALUES ('AnakS','@n@k1n','Skywalker','Anakin','user');
