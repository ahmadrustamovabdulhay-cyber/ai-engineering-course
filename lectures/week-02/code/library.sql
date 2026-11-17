CREATE TABLE books (
    id integer PRIMARY KEY,
    title text NOT NULL
);

CREATE TABLE members (
    id integer PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE loans (
    id integer PRIMARY KEY,
    book_id integer NOT NULL REFERENCES books (id),
    member_id integer NOT NULL REFERENCES members (id),
    borrowed_on date NOT NULL,
    returned_on date
);

INSERT INTO books (id, title)
VALUES
    (1, 'The Hobbit'),
    (2, 'A Wizard of Earthsea'),
    (3, 'The Little Prince');

INSERT INTO members (id, name)
VALUES (11, 'Mina'), (12, 'Ali'), (13, 'Sara');

INSERT INTO loans (id, book_id, member_id, borrowed_on, returned_on)
VALUES
    (101, 1, 11, DATE '2026-01-05', DATE '2026-01-10'),
    (102, 1, 12, DATE '2026-01-12', NULL),
    (103, 2, 13, DATE '2026-01-06', DATE '2026-01-09');
