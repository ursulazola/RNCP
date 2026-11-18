-- Requêtes utilisées dans pipeline.py

-- Canaux d'achat 
SELECT channel_code, channel_name, acquisition_cost_gbp FROM channels WHERE is_active=1;
-- Pays
SELECT * FROM countries;
-- Catégories de livres actifs
SELECT category_name, margin_rate, strategic_flag FROM category_rules WHERE is_active=1;


-- Requêtes utilisées dans api.py

-- Aperçu ventes par pays 
SELECT * FROM sales_by_country;

-- Aperçu ventes par genre 
SELECT * FROM sales_by_category;


