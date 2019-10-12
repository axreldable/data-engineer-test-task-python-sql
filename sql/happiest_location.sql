select l.name, sum(t.sentiment) as total_sentiment
from tweets t
         inner join locations l on t.location_id = l.id
group by l.name
order by total_sentiment desc
limit 1;

-- result:
-- Polska|9
