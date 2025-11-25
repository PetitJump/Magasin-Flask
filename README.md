# Magasin **Dave Shop** de chausson avec les données en SQL.

## Techniques utiliser :

### Pour l'interface :
- HTML : (Avec Jinja)
- Python : (Avec Flask)
- CSS : (Générer par l'IA)

### Pour SQL :
- databse.db : (La base de donnée)
- setup.sql : (Pour initialisé ou rénitialiser la base de donnée)

## Bug actuels :
- Nous pouvons ajouter autant de fois un modèle et une taille dans le panier. Lorsque on achète le panier, le stock dans la base de donnée devient négatif. Il faudrait modifier la base de donné lorsque on met les articles dans le panier