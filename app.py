from flask import Flask, render_template, request, session
import sqlite3


app = Flask(__name__)
app.secret_key = "dave"

def str_to_list(texte: str):
    """S'occupe de passer le panier en une liste visible"""
    separer = texte.split(';')
    a = [] #Exemple : [['SCALA', '38'], ['GRIMP', '44']]
    rendu = [] #Exemple : ["Marque : SCALA, taille : 38", "Marque : GRIMP, taille : 44"]
    for i in range(len(separer)):
        a.append(separer[i].split(','))
    for k in a:
        if k != ['']: #Si k n'est pas une list vide
            rendu.append(f"Marque : {k[0]}, taille : {k[1]}") #k[0] sera toujour la marque et k[1] sera toujour un int (la taille)
    return rendu


def achat(panier: str, nom_panier: str, type: str):
    """Met a jour la base de donnée"""
    DATABASE = 'database.db' #On connecte la base de donnée
    db = sqlite3.connect("database.db")
    cur = db.cursor()

    separer = panier.split(';') #Sépare la chaine de caractère avec ';'
    rendu = []

    for i in range(len(separer)):
        rendu.append(separer[i].split(',')) #Sépare la chaine de caractère avec ','
    for k in rendu:
        if k != ['']: #Si k n'est pas une list vide
            marque = k[0]
            taille = int(k[1])
            cur.execute("""
                SELECT stock
                FROM Chaussons
                WHERE marque = ? AND taille = ?
            """, (str(marque), int(taille))) #On prend le stock actuel
            stock = cur.fetchall()
            if type == "achat": #Si il veut supprimer 1 au stock
                nouveau = (stock[0][0]) - 1 #Le nouveau stock
            elif type == "vendre": #Si il veut ajouter 1 au stock
                session["argent"] = int(session["argent"]) + 10
                nouveau = (stock[0][0]) + 1 #Le nouveau stock

            cur.execute(""" 
                UPDATE Chaussons
                SET stock = ?
                WHERE marque = ? AND taille = ?
            """, (nouveau, str(marque), int(taille))) #Modification du stock

    db.commit()
    db.close()
    print("Achat finis")
    session.pop(nom_panier, None)


################################################################################################


@app.route('/', methods=['GET', 'POST'])
def index():
    
    if not session.get("argent"): #Si il n'y a pas 'argent' dans session
        session["argent"] = 100
    
    msg = "Bienvenue dans Dave Shop" #Message du début

    if request.method == 'POST':
        euro = session["argent"]
        session.clear() #Rénisialise la session (supprime "panier" et "panier2")
        session["argent"] = euro
        msg = "Commande achetée !" #Nouveau message dans le menus
        
    return render_template('index.html', msg=msg, argent=session["argent"])

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
    return render_template('marque.html', marque=resultat, argent=session["argent"]) #On envoie la liste 'resultat' pour pouvoir faire un menus déroulant

@app.route('/taille', methods=['GET', 'POST'])
def taille():
    DATABASE = 'database.db'
    db = sqlite3.connect("database.db")
    cur = db.cursor()

    marque = request.form['marque'] #On prend la marque que l'utilisateur à choisit
    session["marque"] = marque

    cur.execute("""
            SELECT taille
            FROM Chaussons
            WHERE marque = ? AND stock > 0
        """, (str(marque),)) #On prend toute les tailles où la marque = 'marque'
    res = [x[0] for x in cur.fetchall()]
    db.commit()
    db.close()
    return render_template('taille.html', tailles=res, argent=session["argent"]) #On renvoie la taille choisit et la marque pour que la mise à jour se fasse dans la route 'index'

@app.route('/panier', methods=['GET', 'POST'])
def panier():
    if request.method == 'POST':
        taille = request.form['taille'] #On récupère la taille
        marque = session["marque"] #Et la marque
        msg = "" #Aucun message pour le moment (sauf si le user n'a plus d'argent)
        if int(session["argent"]) >= 10:
            session["argent"] = int(session["argent"]) - 10

            if not session.get("panier"): #Si le panier est vide
                session["panier"] = f"{marque},{taille}" #Commence la string sans ';'
            else:
                session["panier"] += f";{marque},{taille}" #Commence la string avec un ';'
            
            if not session.get("panier2"): #Si le panier2 est vide
                session["panier2"] = f"{marque},{taille}" #Commence la string sans ';'
            else:
                session["panier2"] += f";{marque},{taille}" #Commence la string avec un ';'
            
            print(session["panier"]) #Test pour débugage
            print(session["panier2"]) #Test pour débugage
            achat(session["panier"], "panier", "achat") #Modifie la base de donnée
        
        else:
            print("Vous n'avez pas asser d'argent")
            msg = "Pas assez d'argent"

    return render_template('panier.html', total=str_to_list(session["panier2"]), msg=msg, argent=session["argent"]) 

@app.route('/retour', methods=['GET', 'POST'])
def retour():

    achat(session["panier2"], "panier2", "vendre") #Remet le stock
    euro = session["argent"]
    session.clear() #Rénisialise la session (supprime "panier" et "panier2")
    session["argent"] = euro
    
    return render_template('index.html', msg="Commende annuler", argent=session["argent"])

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    session["argent"] = int(session["argent"]) + 20
    return render_template('index.html', msg="20€ on été ajouté à votre compte", argent=session["argent"])

if __name__ == '__main__':
    app.run(debug=True)