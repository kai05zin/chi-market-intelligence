CREATE TABLE market_analysis (
    community_area INTEGER PRIMARY KEY,
    community_area_name VARCHAR(100),
    population NUMERIC,
    restaurant_businesses INTEGER,
    restaurant_density NUMERIC,
    population_per_restaurant NUMERIC,
    median_income NUMERIC,
    per_capita_income NUMERIC,
    unemployment NUMERIC,
    transit_commuters NUMERIC,
    total_commuters NUMERIC,
    transit_share NUMERIC,
    crime_count BIGINT,
    latitude NUMERIC(10, 6),
    longitude NUMERIC(10, 6)
);

CREATE TABLE market_opportunity (
    market_rank INTEGER PRIMARY KEY,
    community_area INTEGER,
    community_area_name VARCHAR(100),
    market_segment VARCHAR(50),
    market_score NUMERIC,
    population NUMERIC,
    population_percentile NUMERIC,
    median_income NUMERIC,
    income_percentile NUMERIC,
    restaurant_businesses INTEGER,
    restaurant_density NUMERIC,
    competition_percentile NUMERIC,
    transit_share NUMERIC,

    CONSTRAINT fk_market_area
        FOREIGN KEY (community_area)
        REFERENCES market_analysis(community_area)
);

CREATE TABLE crime_by_community (
    community_area INTEGER PRIMARY KEY,
    crime_count BIGINT
);

CREATE TABLE community_area_coordinates (
    community_area INTEGER PRIMARY KEY,
    latitude NUMERIC(10, 6),
    longitude NUMERIC(10, 6)
);