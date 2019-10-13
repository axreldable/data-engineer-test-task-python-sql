select u.name, t.text
from tweets t
         inner join users u on t.user_id = u.id
where u.name = (select name
                from (select u.name, sum(t.sentiment) as total_sentiment
                      from tweets t
                               inner join users u on t.user_id = u.id
                      group by u.name
                      order by total_sentiment desc
                      limit 1));

-- result:

-- BIRTHDAY GIRL ✨|Hi @ShawnMendes 😘
-- Today is my birthday🎈
-- Can you follow me? This would be the best a birthday gift ever. 🎁
-- I love you soo much! 💕
-- x12,098

-- BIRTHDAY GIRL ✨|Hi @ShawnMendes 😘
-- Today is my birthday🎈
-- Can you follow me? This would be the best a birthday gift ever. 🎁
-- I love you soo much! 💕
-- x12,134