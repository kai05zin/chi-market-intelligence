# CHI Market Intelligence

## Business Expansion Analytics Platform

CHI Market Intelligence is an end-to-end analytics project designed to identify Chicago neighborhoods with strong potential for restaurant business expansion.

The project combines public business license data with demographic and socioeconomic data to evaluate market size, competition, income, and accessibility across Chicago community areas.

## Business Problem

A restaurant company considering expansion into Chicago needs to identify neighborhoods with attractive market conditions.

This project answers:

> Which Chicago neighborhoods offer the strongest market opportunities for a new restaurant?

The analysis does not attempt to predict restaurant success. Instead, it provides a data-driven screening framework for comparing neighborhood market conditions.

## Project Architecture

Chicago Data Portal  
↓  
Python / pandas ETL  
↓  
PostgreSQL  
↓  
SQL Analysis  
↓  
Market Opportunity Scoring  
↓  
Power BI Dashboard

## Data Sources

- Chicago Business Licenses — Current Active
- Chicago crime data
- Chicago community demographic and socioeconomic data

The business license dataset contains more than 54,000 active license records.

## Methodology

The analysis evaluates Chicago community areas using several indicators:

- Population
- Median household income
- Restaurant-related business density
- Population per restaurant-related business
- Public transit share

Restaurant-related businesses were identified using business license descriptions and business activity fields. Because license records do not represent a perfect count of physical restaurants, the restaurant measure should be interpreted as an analytical proxy.

## Market Opportunity Score

Qualified markets were defined as community areas with:

- Population of at least 30,000
- Median income of at least $60,000

The market score combines:

- Population — 30%
- Median income — 30%
- Competition — 40%

Competition is evaluated using restaurant-related business density, with lower density receiving a higher competition score.

The resulting score is intended as a market-screening tool rather than a prediction of actual restaurant performance.

## Market Segments

Markets are categorized into four segments:

- **High Opportunity** — higher income and lower competition
- **Large Market** — larger population and lower competition
- **Competitive Market** — higher income but higher competition
- **Emerging Market** — other qualified markets

## Key Findings

The analysis identified several neighborhoods with attractive combinations of population, income, and relatively low restaurant-related business density.

Examples include:

- Norwood Park
- West Ridge
- Portage Park
- Ashburn
- Dunning
- Garfield Ridge

The results help compare neighborhoods and identify areas that may deserve further business research.

## Dashboard

The project includes an interactive Power BI dashboard with:

- Market opportunity KPIs
- Top neighborhood rankings
- Market opportunity scatter analysis
- Market segment filtering
- Neighborhood-level market metrics

## Tech Stack

- Python
- pandas
- SQL
- PostgreSQL
- Power BI
- Git / GitHub

## Project Structure

```text
chi-market-intelligence/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── python/
├── sql/
├── docs/
│
├── README.md
├── requirements.txt
└── .gitignore