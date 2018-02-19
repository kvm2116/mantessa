-- MySQL Script generated by MySQL Workbench
-- Sat Apr  8 13:10:06 2017
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mantessa_db9
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mantessa_db9
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mantessa_db9` DEFAULT CHARACTER SET utf8 ;
USE `mantessa_db9` ;

-- -----------------------------------------------------
-- Table `mantessa_db9`.`mantessa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mantessa_db9`.`mantessa` (
  `ip` INT UNSIGNED NOT NULL,
  `latitude` DECIMAL(10,7) NOT NULL DEFAULT 0,
  `longitude` DECIMAL(10,7) NOT NULL DEFAULT 0,
  `zipCode` VARCHAR(20) NOT NULL,
  `stateCode` VARCHAR(20) NOT NULL,
  `cityName` VARCHAR(30) NOT NULL,
  `counter` INT UNSIGNED NULL DEFAULT 1,
  PRIMARY KEY (`ip`, `latitude`, `longitude`, `zipCode`,`stateCode`,`cityName`))
ENGINE = InnoDB;

USE `mantessa_db9` ;

-- -----------------------------------------------------
-- procedure update_mantessa
-- -----------------------------------------------------

DELIMITER $$
USE `mantessa_db9`$$
DROP PROCEDURE IF EXISTS `update_mantessa`;
CREATE PROCEDURE `update_mantessa` (IN col_name VARCHAR(30), IN ip_add VARCHAR(24), IN lat DECIMAL(10,4) , IN longit DECIMAL(10,4), IN zip VARCHAR(20), IN state VARCHAR(20), IN city VARCHAR(30))
BEGIN

Declare foundcount INT;
SET @col = col_name;
SET @a_ip = ip_add;
SET @lati = lat;
SET @longitu = longit;
SET @zipC = zip;
SET @stateN = state;
SET @cityN = city;

SET @sql_text = concat('UPDATE mantessa SET ',@col,'=',1,',counter=counter+1 WHERE ip=',INET_ATON(@a_ip),' and latitude=',@lati,' and longitude=',@longitu,' and zipCode=',@zipC,' and stateCode=',@stateN,' and cityName=',@cityN);
PREPARE stmt FROM @sql_text;
EXECUTE stmt;
Select ROW_COUNT() INTO foundcount;
DEALLOCATE PREPARE stmt;

IF foundcount <> 1 THEN

SET @sql_text2 = concat('INSERT IGNORE INTO mantessa (ip,latitude,longitude,zipCode,stateCode,cityName',@col,') VALUES (',INET_ATON(@a_ip),',', @lati,',',  @longitu,',',  @zipC,',',  @stateN,',',  @cityN,', 1)');
PREPARE stmt2 FROM @sql_text2;
EXECUTE stmt2;
DEALLOCATE PREPARE stmt2;
END IF;
END$$