--FIle per creare database
create table users (
    id integer primary key autoincrement,
    username text not null, --questo campo non può essere vuoto
    password text not null,
    expert boolean not null,
    admin boolean not null
);

create table questions (
    id integer primary key autoincrement,
    question_text text not null,
    answer_text text ,
    asked_by_id integer not null, --id di chi fa la domanda
    expert_id integer not null --id dell'esperto che risponde
);
--sqlite3 questions.db < schema.sql