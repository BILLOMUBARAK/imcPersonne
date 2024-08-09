CREATE DATABASE imcpersonne;
\c imcpersonne;
CREATE TABLE imctable (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    taille INTEGER,
    poids INTEGER,
    imc FLOAT,
    interpretation VARCHAR(100)
);

INSERT INTO imctable (nom, prenom, taille, poids, imc, interpretation)
VALUES ('John Doe', 'Example', 180, 75, 23.15, 'Corpulence normale');
