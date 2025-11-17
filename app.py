from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    DATABASE = 'database.db'
    db = sqlite3.connect("database.db")
    cur = db.cursor()

    if request.method == 'POST':
        marque = request.form['marque']
        taille = request.form['taille']
        print("marque : ", marque)
        print("taille : ", taille)

        cur.execute("""
            SELECT stock
            FROM Chaussons
            WHERE marque = ? AND taille = ?
        """, (str(marque), int(taille)))
        stock = cur.fetchall()
        print("stock : ", stock)

        nouveau = (stock[0][0]) - 1
        cur.execute(""" 
            UPDATE Chaussons
            SET stock = ?
            WHERE marque = ? AND taille = ?
        """, (nouveau, str(marque), int(taille)))

        db.commit()
        db.close()
        return render_template('index.html', marque="Fait !")
    
    cur.execute("""
                SELECT DISTINCT marque
                FROM Chaussons
            """)
    resultat = [x[0] for x in cur.fetchall()]
    return render_template('index.html', marque=resultat)

if __name__ == '__main__':
    app.run(debug=True)
