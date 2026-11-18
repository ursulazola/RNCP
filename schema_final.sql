-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'orders_final'
-- 
-- ---

DROP TABLE IF EXISTS `orders_final`;
		
CREATE TABLE `orders_final` (
  `order_id` VARCHAR(18) NULL DEFAULT NULL,
  `order_date` DATE NULL DEFAULT NULL,
  `book_id` VARCHAR(9) NULL DEFAULT NULL,
  `country_code` VARCHAR(255) NULL DEFAULT NULL,
  `channel_code` VARCHAR(255) NULL DEFAULT NULL,
  `quantity` INTEGER NULL DEFAULT NULL,
  `discount_rate` DECIMAL(5,4) NULL DEFAULT NULL,
  `book_name` VARCHAR(255) NULL DEFAULT NULL,
  `id_client` VARCHAR(255) NULL DEFAULT NULL,
  `price_gbp_HT_with_discount` DECIMAL(10,4) NULL DEFAULT NULL,
  `price_eur_HT_with_discount` DECIMAL(10,4) NULL DEFAULT NULL,
  `total_revenue_gbp` DECIMAL(18,4) NULL DEFAULT NULL,
  `total_revenue_eur` DECIMAL(18,4) NULL DEFAULT NULL,
  `profit_total_gbp` DECIMAL(18,4) NULL DEFAULT NULL,
  `profit_total_eur` DECIMAL(18,4) NULL DEFAULT NULL,
  PRIMARY KEY (`order_id`)
);

-- ---
-- Table 'exchange_rate'
-- 
-- ---

DROP TABLE IF EXISTS `exchange_rate`;
		
CREATE TABLE `exchange_rate` (
  `order_date` DATE NULL DEFAULT NULL,
  `exchange_rate` DECIMAL(18,4) NULL DEFAULT NULL,
  PRIMARY KEY (`order_date`)
);

-- ---
-- Table 'countries'
-- 
-- ---

DROP TABLE IF EXISTS `countries`;
		
CREATE TABLE `countries` (
  `country_code` VARCHAR(255) NULL DEFAULT NULL,
  `country_name` VARCHAR(255) NULL DEFAULT NULL,
  `currency_code` VARCHAR(255) NULL DEFAULT NULL,
  `vat_rate` DECIMAL(6,4) NULL DEFAULT NULL,
  `region` VARCHAR(255) NULL DEFAULT NULL,
  `country_is_active` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`country_code`)
);

-- ---
-- Table 'books_scrap_category'
-- 
-- ---

DROP TABLE IF EXISTS `books_scrap_category`;
		
CREATE TABLE `books_scrap_category` (
  `book_name` VARCHAR(255) NULL DEFAULT NULL,
  `price_gbp` DECIMAL(10,4) NULL DEFAULT NULL,
  `stock` INTEGER NULL DEFAULT NULL,
  `note` INTEGER NULL DEFAULT NULL,
  `category_name` VARCHAR(255) NULL DEFAULT NULL,
  `margin_rate` DECIMAL(5,4) NULL DEFAULT NULL,
  `strategic_flag` BINARY NULL DEFAULT NULL,
  PRIMARY KEY (`book_name`)
);

-- ---
-- Table 'channels'
-- 
-- ---

DROP TABLE IF EXISTS `channels`;
		
CREATE TABLE `channels` (
  `channel_code` VARCHAR(255) NULL DEFAULT NULL,
  `channel_name` VARCHAR(255) NULL DEFAULT NULL,
  `acquisition_cost_gbp` DECIMAL(8,4) NULL DEFAULT NULL,
  PRIMARY KEY (`channel_code`)
);

-- ---
-- Table 'sales_by_category'
-- 
-- ---

DROP TABLE IF EXISTS `sales_by_category`;
		
CREATE TABLE `sales_by_category` (
  `category_name` VARCHAR(255) NULL DEFAULT NULL,
  `total_orders` INTEGER NULL DEFAULT NULL,
  `total_quantity` INTEGER NULL DEFAULT NULL,
  `total_revenue_gbp` DECIMAL(18,4) NULL DEFAULT NULL,
  `profit_total_gbp` DECIMAL(18,4) NULL DEFAULT NULL,
  `total_revenue_eur` DECIMAL(18,4) NULL DEFAULT NULL,
  `profit_total_eur` DECIMAL(18,4) NULL DEFAULT NULL,
  PRIMARY KEY (`category_name`)
);

-- ---
-- Table 'sales_by_country'
-- 
-- ---

DROP TABLE IF EXISTS `sales_by_country`;
		
CREATE TABLE `sales_by_country` (
  `country_code` VARCHAR(255) NULL DEFAULT NULL,
  `country_name` VARCHAR(255) NULL DEFAULT NULL,
  `total_orders` INTEGER NULL DEFAULT NULL,
  `total_quantity` INTEGER NULL DEFAULT NULL,
  `total_revenue_gbp` DECIMAL(18,4) NULL DEFAULT NULL,
  `profit_total_gbp` DECIMAL(18,4) NULL DEFAULT NULL,
  `total_revenue_eur` DECIMAL(18,4) NULL DEFAULT NULL,
  `profit_total_eur` DECIMAL(18,4) NULL DEFAULT NULL,
  PRIMARY KEY (`country_code`)
);

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `orders_final` ADD FOREIGN KEY (order_date) REFERENCES `exchange_rate` (`order_date`);
ALTER TABLE `orders_final` ADD FOREIGN KEY (country_code) REFERENCES `countries` (`country_code`);
ALTER TABLE `orders_final` ADD FOREIGN KEY (channel_code) REFERENCES `channels` (`channel_code`);
ALTER TABLE `orders_final` ADD FOREIGN KEY (book_name) REFERENCES `books_scrap_category` (`book_name`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `orders_final` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `exchange_rate` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `countries` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `books_scrap_category` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `channels` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `sales_by_category` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `sales_by_country` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `orders_final` (`order_id`,`order_date`,`book_id`,`country_code`,`channel_code`,`quantity`,`discount_rate`,`book_name`,`id_client`,`price_gbp_HT_with_discount`,`price_eur_HT_with_discount`,`total_revenue_gbp`,`total_revenue_eur`,`profit_total_gbp`,`profit_total_eur`) VALUES
-- ('','','','','','','','','','','','','','','');
-- INSERT INTO `exchange_rate` (`order_date`,`exchange_rate`) VALUES
-- ('','');
-- INSERT INTO `countries` (`country_code`,`country_name`,`currency_code`,`vat_rate`,`region`,`country_is_active`) VALUES
-- ('','','','','','');
-- INSERT INTO `books_scrap_category` (`book_name`,`price_gbp`,`stock`,`note`,`category_name`,`margin_rate`,`strategic_flag`) VALUES
-- ('','','','','','','');
-- INSERT INTO `channels` (`channel_code`,`channel_name`,`acquisition_cost_gbp`) VALUES
-- ('','','');
-- INSERT INTO `sales_by_category` (`category_name`,`total_orders`,`total_quantity`,`total_revenue_gbp`,`profit_total_gbp`,`total_revenue_eur`,`profit_total_eur`) VALUES
-- ('','','','','','','');
-- INSERT INTO `sales_by_country` (`country_code`,`country_name`,`total_orders`,`total_quantity`,`total_revenue_gbp`,`profit_total_gbp`,`total_revenue_eur`,`profit_total_eur`) VALUES
-- ('','','','','','','','');