from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    msg = "Bienvenue dans Dave Shop" #Message du début
    DATABASE = 'database.db' #On connecte la base de donnée
    db = sqlite3.connect("database.db")
    cur = db.cursor()

    if request.method == 'POST':
        taille = request.form['taille'] #On récupère la taille
        marque = request.form['marque'] #Et la marque
        
        cur.execute("""
            SELECT stock
            FROM Chaussons
            WHERE marque = ? AND taille = ?
        """, (str(marque), int(taille))) #On prend le stock actuel
        stock = cur.fetchall()

        nouveau = (stock[0][0]) - 1 #Le nouveau stock
        cur.execute(""" 
            UPDATE Chaussons
            SET stock = ?
            WHERE marque = ? AND taille = ?
        """, (nouveau, str(marque), int(taille))) #Modification du stock

        msg = "Commande achetée !" #Nouveau message dans le menus
    db.commit()
    db.close()
    return render_template('index.html', msg=msg)

@app.route('/marque', methods=['GET', 'POST'])
def marque():
    DATABASE = 'database.db'
    db = sqlite3.connect("database.db")
    cur = db.cursor()
    cur.execute("""
                SELECT DISTINCT marque
                FROM Chaussons
            """) #On prend toutes les marques qui existent
    resultat = [x[0] for x in cur.fetchall()] #Liste des marques
    db.commit()
    db.close()
    return render_template('marque.html', marque=resultat) #On envoie la liste 'resultat' pour pouvoir faire un menus déroulant

@app.route('/taille', methods=['GET', 'POST'])
def taille():
    DATABASE = 'database.db'
    db = sqlite3.connect("database.db")
    cur = db.cursor()

    marque = request.form['marque'] #On prend la marque que l'utilisateur à choisit

    cur.execute("""
            SELECT taille
            FROM Chaussons
            WHERE marque = ? AND stock > 0
        """, (str(marque),)) #On prend toute les tailles où la marque = 'marque'
    res = [x[0] for x in cur.fetchall()]
    db.commit()
    db.close()
    return render_template('taille.html', tailles=res, marque=marque) #On renvoie la taille choisit et la marque pour que la mise à jour se fasse dans la route 'index'

if __name__ == '__main__':
    app.run(debug=True)