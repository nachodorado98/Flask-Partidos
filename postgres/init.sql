CREATE DATABASE bbdd_partidos;

\c bbdd_partidos;

CREATE TABLE partidos (id SERIAL PRIMARY KEY,
    					competicion VARCHAR(255),
						ronda VARCHAR(255),
						fecha DATE,
						hora VARCHAR(255),
						local VARCHAR(255),
						marcador VARCHAR(255),
						visitante VARCHAR(255),
						publico INT,
						sede VARCHAR(255));