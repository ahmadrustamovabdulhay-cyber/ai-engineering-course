# After Session 03 — Campus event registration

[Week 02](README.md) · [Session 03](session-03.md) · [SQL reference](notes.md)

Your university club runs events. It needs to keep a list of events, a list of students, and a record of who signed up for each event. Build a small database for the club on your computer using the SQL you learned in Session 03.

## Set up PostgreSQL

Use a current installer or package for your operating system. If PostgreSQL is already running on your computer, use your existing installation. [Official PostgreSQL downloads](https://www.postgresql.org/download/)

| System | Watch or follow | Open `psql` |
|---|---|---|
| Windows | [YouTube installation walkthrough](https://www.youtube.com/watch?v=IcJvVUln-KY) · [Windows installer](https://www.postgresql.org/download/windows/) | After the video’s installation steps, open **SQL Shell (psql)** from the Start menu. For a default installation, use `localhost`, database `postgres`, port `5432`, username `postgres`, and the password you chose. |
| macOS | [Prisma’s YouTube walkthrough](https://www.youtube.com/watch?v=wTqosS71Dc4) · [Postgres.app instructions](https://postgresapp.com/) | Initialize the server in Postgres.app and double-click a database to open `psql`. |
| Linux | [PostgreSQL packages by distribution](https://www.postgresql.org/download/linux/) | Start the server and use your distribution’s instructions to connect with `psql`. |

The Windows video demonstrates pgAdmin. For this practice, use SQL Shell and follow the commands below. `psql` is a client that sends your SQL to the PostgreSQL server. [Accessing a database with psql](https://www.postgresql.org/docs/current/tutorial-accessdb.html)

1. At the `psql` prompt, create a database for this exercise.

   ```sql
   CREATE DATABASE campus_practice;
   ```

2. Connect to it with the `psql` command `\connect campus_practice`. Then run the SQL below. The result should be `campus_practice`.

   ```sql
   SELECT current_database();
   ```

If setup blocks you, finish the exercises in a fresh database on [postgres.new](https://postgres.new/) and bring the connection or installation error to the next class.

## Exercise 1 — Create the tables and add data

### A. Create the tables

Write a `CREATE TABLE` statement for each table below. Create `events` and `students` first, then create `registrations`. PostgreSQL needs the referenced tables to exist before it can add the foreign keys.

| Table | Columns |
|---|---|
| `events` | `id` as an integer primary key, `title` as required text, `event_on` as a required date |
| `students` | `id` as an integer primary key, `name` as required text |
| `registrations` | `id` as an integer primary key, `event_id` as a required integer referencing `events.id`, `student_id` as a required integer referencing `students.id`, `registered_on` as a required date, and `cancelled_on` as a date that can be `NULL` |

**Syntax hints:** Write the column name, then its type (`integer`, `text`, or `date`), then any rule. Use `NOT NULL` for required values, `PRIMARY KEY` for the row ID, and `REFERENCES table_name (column_name)` for a foreign key. Separate column definitions with commas and end each statement with a semicolon. Use the [Session 03 table examples](session-03.md) if you get stuck.

### B. Insert the starter rows

1. Insert these two rows into `events`.

   | `id` | `title` | `event_on` |
   |---:|---|---|
   | 1 | Robotics Demo | 2026-11-26 |
   | 2 | AI Study Jam | 2026-11-27 |

2. Insert student `11` with the name `Jin` into `students`.
3. Insert registration `101` into `registrations`. Use event `1`, student `11`, registration date `2026-11-19`, and `NULL` for `cancelled_on`.

**Syntax hint:** Use `INSERT INTO table_name (column_list) VALUES (value_list)`. List the columns in the same order as their values. Put text in single quotes, write a date as `DATE '2026-11-19'`, and write `NULL` without quotes.

**Check your work:** Run a separate `SELECT` on each table. You should see two events, one student, and one registration. In the registration row, check that `event_id` is `1` and `student_id` is `11`. A SQL client may display the `NULL` cancellation date as a blank cell.

## Exercise 2 — Find records

Write and run three queries. Use one table per query. Each result gives you information for the next step or a way to check your work.

1. **List the events.** From `events`, return `id`, `title`, and `event_on`. Use `ORDER BY` to sort by `title` in ascending order. You should see *AI Study Jam* first and *Robotics Demo* second.
2. **Find the registrations that are still active.** From `registrations`, return `id`, `event_id`, `student_id`, and `registered_on` for rows whose `cancelled_on` is missing. Use `WHERE` with `IS NULL`. You should get one row with registration `101`, event `1`, student `11`, and date `2026-11-19`.
3. **Look up the student.** Take the `student_id` from the previous result and use it to filter the `id` column in `students`. Return `id` and `name`. You should get `11` and `Jin`.

Keep the query from step 2. You’ll run it again after changing the data.

## Exercise 3 — Update, delete, and check a constraint

### A. Cancel an existing registration

1. Use `SELECT` with `WHERE id = 101` to check the row you’re about to change. Its cancellation date should be `NULL`.
2. Write an `UPDATE` on `registrations`. Use `SET` to change `cancelled_on` to `2026-11-20` and use the same `WHERE` condition to target registration `101`.
3. Run the same `SELECT` again. It should show `2026-11-20`. Then rerun your active-registration query from Exercise 2. It should return zero rows.

### B. See a foreign key reject a row

1. Try inserting registration `199` for event `99` and student `11`, with registration date `2026-11-22` and no cancellation date. Run this attempt by itself.
2. Read the error. Which ID exists, and which ID is missing? Use `SELECT` to check each referenced table. Record the error and explain which foreign key rejected the row.
3. Query `registrations` for ID `199` to confirm the insert left no row behind.

### C. Delete a practice row

1. Insert registration `102` for event `2` and student `11`, with registration date `2026-11-22` and no cancellation date.
2. Preview the row with `SELECT` and `WHERE id = 102`. Check that the result contains exactly one row and its ID is `102`.
3. Write a `DELETE FROM` statement for `registrations` using that same `WHERE` condition. Rerun the preview query. It should return zero rows.
4. List all registrations. Registration `101` should still be there with its cancellation date of `2026-11-20`.

## What to submit

Save your successful SQL statements in `student-work/YOUR-USERNAME/week-02/session-03-practice.sql`. Add the rejected statement as a SQL comment with the error and your explanation. Include the output of `SELECT current_database();` as a comment if you ran locally. If you used the browser, include a short note about what blocked local setup.

Submit through the [course pull request workflow](../../student-work/README.md).
