-- .read duckdb/go.sql

/*
drop table if exists xx;

create table xx as
select m_id
, created_at_str
, created_at, ('EPOCH'::TIMESTAMP + INTERVAL (created_at::INT) seconds)::TIMESTAMPTZ  as created_tz
, app
, url
, regexp_replace(regexp_replace(url, '^http[s]://', ''), '/.*$', '') as new_url
, base_url
, language
, favourites
, username
, bot
, tags
, characters
, mastodon_text
FROM read_parquet('s3://mastodon/topics/mastodon-topic/partition=0/*');
*/

select date_part('day', created_tz) as created_day
, date_part('hour', created_tz) as created_hour
, count(*)
from yy
group by 1,2 
order by 1,2
;

-- select username, bot, count(*) from xx group by 1,2 order by 3 desc;

 as select * 



-- old backup
create table toots
as
select  m_id          
, created_at    
, created_at_str
, app           
, url           
, base_url      
, language      
, favourites    
, username      
, bot           
, tags          
, characters    
, mastodon_text 
FROM read_parquet('../xx.parquet');

insert into toots
select
  m_id          
, created_at    
, created_at_str
, app           
, url           
, base_url      
, language      
, favourites    
, username      
, bot           
, tags          
, characters    
, mastodon_text
from read_parquet('*.parquet');

insert into toots
select
  m_id          
, created_at    
, created_at_str
, app           
, url           
, base_url      
, language      
, favourites    
, username      
, bot           
, tags          
, characters    
, mastodon_text
from read_parquet('20230213/mastodon-topic/partition=0/*.parquet');



create table all_toots
as
select
  m_id          
, created_at    
, app           
, url           
, base_url      
, language      
, favourites    
, username      
, bot           
, tags          
, characters    
, mastodon_text
from toots
group by
  m_id          
, created_at    
, app           
, url           
, base_url      
, language      
, favourites    
, username      
, bot           
, tags          
, characters    
, mastodon_text;

COPY all_toots TO 'all_toots.parquet' (FORMAT PARQUET);