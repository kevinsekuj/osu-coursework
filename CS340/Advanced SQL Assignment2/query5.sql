-- Find the film_title of all films which feature both RALPH CRUZ and WILL WILSON
-- Order the results by film_title in ascending order.
--  Warning: this is a tricky one and while the syntax is all things you know, you have to think a bit oustide the box to figure out how to get a table that shows pairs of actors in movies.


-- Put your query for q5 here.

SELECT ralph_cruz.title AS film_title FROM (
    SELECT F.film_id, F.title FROM film F

    JOIN film_actor FA ON FA.film_id = F.film_id

    JOIN actor A ON FA.actor_id = A.actor_id

    WHERE A.actor_id = (SELECT actor_id FROM actor WHERE first_name = 'RALPH' and last_name = 'CRUZ')) as ralph_cruz

JOIN (
    SELECT F.film_id, F.title FROM film F

    JOIN film_actor FA ON FA.film_id = F.film_id

    JOIN actor A ON FA.actor_id = A.actor_id

    WHERE A.actor_id = (SELECT actor_id FROM actor WHERE first_name = 'WILL' and last_name = 'WILSON')) AS will_wilson

    WHERE ralph_cruz.film_id = will_wilson.film_id;