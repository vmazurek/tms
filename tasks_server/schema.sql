drop table if exists task;

create table task (
    id integer primary key autoincrement,
    title text not null
);