CREATE OR REPLACE VIEW public.market_dashboard AS
SELECT
    mo.market_rank,
    mo.community_area,
    mo.community_area_name,
    mo.market_segment,
    mo.market_score,
    mo.population,
    mo.median_income,
    mo.restaurant_businesses,
    mo.restaurant_density,
    ma.population_per_restaurant,
    mo.transit_share,
    ma.per_capita_income,
    ma.unemployment,
    ma.crime_count,
    ma.latitude,
    ma.longitude
FROM public.market_opportunity mo
JOIN public.market_analysis ma
    ON mo.community_area = ma.community_area;