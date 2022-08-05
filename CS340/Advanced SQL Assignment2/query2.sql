-- We want to find out how many of each category of film MAE HOFFMAN has starred in.

-- So return a table with category_name and the count of the number_of_films that MAE was in that category.

-- Your query should return every category even if MAE has been in no films in that category

-- Order by the category name in descending order.


SELECT cat.name AS category_name, COUNT(film_act.film_id) AS number_of_films FROM category cat

LEFT JOIN film_category film_cat ON cat.category_id = film_cat.category_id

LEFT JOIN film film ON film.film_id = film_cat.film_id

LEFT JOIN film_actor film_act ON film_act.film_id = film.film_id AND film_act.actor_id = (SELECT actor_id FROM actor WHERE first_name = 'MAE' AND last_name = 'HOFFMAN')

GROUP BY category_name ORDER BY category_name DESC;