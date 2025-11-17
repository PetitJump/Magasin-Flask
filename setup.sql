DROP TABLE IF EXISTS Chaussons;

CREATE TABLE Chaussons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    marque TEXT NOT NULL,
    taille INTEGER NOT NULL,
    prix REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    UNIQUE(marque, taille) --Pour qu'il n'y ai pas deux taille par marque
);

INSERT INTO Chaussons (marque, taille, prix, stock) VALUES
('Scala', 35, 95.00, 5),
('Scala', 36, 95.00, 5),
('Scala', 37, 95.00, 5),
('Scala', 38, 95.00, 5),
('Scala', 39, 95.00, 5),
('Scala', 40, 95.00, 5),
('Scala', 41, 95.00, 5),
('Scala', 42, 95.00, 5),
('Scala', 43, 95.00, 5),
('Scala', 44, 95.00, 5),
('Scala', 45, 95.00, 5);

INSERT INTO Chaussons (marque, taille, prix, stock) VALUES
('Grip', 35, 110.50, 3),
('Grip', 36, 110.50, 3),
('Grip', 37, 110.50, 2),
('Grip', 38, 110.50, 1),
('Grip', 39, 110.50, 2),
('Grip', 40, 110.50, 3),
('Grip', 41, 110.50, 3),
('Grip', 42, 110.50, 1),
('Grip', 43, 110.50, 0),
('Grip', 44, 110.50, 2),
('Grip', 45, 110.50, 3);

INSERT INTO Chaussons (marque, taille, prix, stock) VALUES
('Varap', 35, 130.00, 1),
('Varap', 36, 130.00, 1),
('Varap', 37, 130.00, 0),
('Varap', 38, 130.00, 1),
('Varap', 39, 130.00, 1),
('Varap', 40, 130.00, 2),
('Varap', 41, 130.00, 2),
('Varap', 42, 130.00, 0),
('Varap', 43, 130.00, 1),
('Varap', 44, 130.00, 1),
('Varap', 45, 130.00, 0);