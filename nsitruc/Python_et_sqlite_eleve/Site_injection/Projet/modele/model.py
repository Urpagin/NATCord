import sqlite3

def ouvrir_connexion():
	cnx = None
	try:
		cnx = sqlite3.connect('Projet/db/authentification.db')
		print('connexion ouverte')
	except BaseException as e:
		print('passe par exception')
		print(e)
	return cnx

def db_identification(resultat):	
	cnx = ouvrir_connexion()
	cur = cnx.cursor()
	chaine = "SELECT * FROM Utilisateurs WHERE Login = '"+resultat['login']+"' AND Password = '"+resultat['password']+"'"
	cur.execute(chaine)
	rows = cur.fetchall()
	cnx.close()
	return rows