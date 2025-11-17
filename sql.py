#Fichier qui me sert d'exemple pour coder. Ce fichier a été coder par moi même
#Voici son github : https://github.com/PetitJump/Magasin-chaussons-SQL-Terminal

import sqlite3
DATABASE = 'database.db'

db = sqlite3.connect("database.db")
cur = db.cursor()

cur.execute("""
            SELECT DISTINCT marque
            FROM Chaussons
        """)

resultat = [x[0] for x in cur.fetchall()]
for k in resultat:
    print(resultat.index(k) , k)

print("")
marque = int(input("Quel marque voulez vous acheter ? "))
print("")

cur.execute("""
            SELECT taille
            FROM Chaussons
            WHERE marque = ? AND stock > 0
        """, (resultat[marque],))

res = [x[0] for x in cur.fetchall()]
print("Voici les tailles dispo :")
print(res)

print("")
taille = int(input("Quel taille voulez vous acheter ? "))

cur.execute("""
            SELECT stock
            FROM Chaussons
            WHERE marque = ? AND taille = ?
        """, (resultat[marque], taille))

res = cur.fetchall()

cur.execute("""
            UPDATE Chaussons
            SET stock = ?
            WHERE marque = ? AND taille = ?
        """, (res[0][0] - 1, resultat[marque], taille))

print("Le stock a été mis a jour !")
db.close()