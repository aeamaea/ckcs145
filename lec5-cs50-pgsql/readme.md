** What is this? ** 
** Oct 22, 2023 ** 

aeam :: Oct212023

This is the PGSQL version of the Lecture 5 mongoapp but instead of the ORM, here I will try to use straight up SQL statements.

You may need to import psycopg along with CS50 (so you need to pip install it first in the venv or conda env or what have you before yougo about using it. mmmmkay?

Pre-reqs (that I can think of rn)
1. You must have a postgresql database called Inventory with a table called "customer" This is my createdb statement:

    CREATE TABLE IF NOT EXISTS public.customer
(
    customer_id integer NOT NULL,
    name character varying(128) COLLATE pg_catalog."default" NOT NULL,
    quantity integer DEFAULT 0,
    price integer DEFAULT 0,
    CONSTRAINT customer_pkey PRIMARY KEY (customer_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.customer
    OWNER to whateverpostgresuseryoucreated;

2. pip installed CS50, psycopg2 (use the binary version if you're on m1/m2 macs).
3. more here ...
