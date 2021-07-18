create schema vejice;

create table vejice.reports (
  id serial primary key,
  sentence_id text
);

create table vejice.users (
  id varchar(256) primary key,
  user_profile text
);