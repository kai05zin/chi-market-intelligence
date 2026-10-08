-- 1. Highest-potential markets
SELECT
    market_rank,
    community_area_name,
    market_segment,
    ROUND(market_score, 2) AS market_score,
    ROUND(population) AS population,
    ROUND(median_income, 0) AS median_income,
    ROUND(restaurant_density, 2) AS restaurant_density
FROM market_opportunity
WHERE population >= 50000
  AND median_income >= 70000
  AND restaurant_density <= 25
ORDER BY market_score DESC;


-- 2. Markets with the largest population-to-restaurant gap
SELECT
    community_area_name,
    ROUND(population) AS population,
    restaurant_businesses,
    ROUND(restaurant_density, 2) AS restaurant_density,
    ROUND(population_per_restaurant, 0) AS people_per_restaurant
FROM market_analysis
WHERE population >= 30000
  AND median_income >= 60000
ORDER BY people_per_restaurant DESC
LIMIT 10;


-- 3. Compare qualified markets
SELECT
    mo.community_area_name,
    ROUND(mo.market_score, 2) AS market_score,
    ROUND(mo.population) AS population,
    ROUND(mo.median_income, 0) AS median_income,
    mo.restaurant_businesses,
    ROUND(mo.restaurant_density, 2) AS restaurant_density,
    ROUND(ma.population_per_restaurant, 0) AS people_per_restaurant,
    mo.market_segment
FROM market_opportunity mo
JOIN market_analysis ma
    ON mo.community_area = ma.community_area
WHERE mo.population >= 30000
  AND mo.median_income >= 70000
ORDER BY mo.market_score DESC;