/* il database è quello di default di postgres: postgres*/

create schema progetto_cavallari;

set search_path=progetto_cavallari;

create table contratti(
	id_offerta integer,
	id_richiesta integer,
	sum integer,
	perc float,
	FOREIGN KEY (id_offerta) REFERENCES offerte(id),
	FOREIGN KEY (id_richiesta) REFERENCES richieste(id),
	primary key (id_offerta,id_richiesta)
);





POSTGRES
CREATE TABLE offerte (
    id serial NOT NULL primary key,
    perc float,
    processed boolean,
    sum integer
);


CREATE TABLE richieste (
    id serial NOT NULL primary key,
    perc float,
    processed boolean,
    sum integer
);
