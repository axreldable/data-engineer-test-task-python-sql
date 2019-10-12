select c.name, sum(t.sentiment) as total_sentiment
from tweets t
         inner join locations l on t.location_id = l.id
         inner join countries c on l.country_id = c.id
group by c.name
order by total_sentiment desc
limit 1;

-- result:
-- United States|23
