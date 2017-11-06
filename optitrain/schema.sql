DROP TABLE IF EXISTS trip;
CREATE TABLE trip(
  id integer primary key autoincrement,
  email text not null,
  origin text not null,
  dest text not null,
  trip_date integer not null
);
