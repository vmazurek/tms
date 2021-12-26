drop table if exists task;

create table task (
    id integer primary key autoincrement,
    added_date text not null default (datetime('now', 'utc')),
    defer_until_date text null,
    title text not null default '',
    description text not null default '',
    status integer not null default 0
);