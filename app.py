from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    msg = "Bienvenue dans Dave Shop"
    DATABASE = 'database.db'
    db = sqlite3.connect("database.db")
    cur = db.cursor()

    if request.method == 'POST':
        taille = request.form['taille']
        marque = request.form['marque']
        #print("taille :", taille)
        #print("marque : ", marque)
        
        cur.execute("""
            SELECT stock
            FROM Chaussons
            WHERE marque = ? AND taille = ?
        """, (str(marque), int(taille)))
        stock = cur.fetchall()

        #print("stock : ", stock)
        nouveau = (stock[0][0]) - 1
        #print("nouveaux stock : ", nouveau)
        cur.execute(""" 
            UPDATE Chaussons
            SET stock = ?
            WHERE marque = ? AND taille = ?
        """, (nouveau, str(marque), int(taille)))

        msg = "Commande achetée !"
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
            """)
    resultat = [x[0] for x in cur.fetchall()]
    db.commit()
    db.close()
    return render_template('marque.html', marque=resultat)

@app.route('/taille', methods=['GET', 'POST'])
def taille():
    DATABASE = 'database.db'
    db = sqlite3.connect("database.db")
    cur = db.cursor()

    marque = request.form['marque']

    cur.execute("""
            SELECT taille
            FROM Chaussons
            WHERE marque = ? AND stock > 0
        """, (str(marque),))
    res = [x[0] for x in cur.fetchall()]
    db.commit()
    db.close()
    return render_template('taille.html', tailles=res, marque=marque)
    

if __name__ == '__main__':
    app.run(debug=True)
