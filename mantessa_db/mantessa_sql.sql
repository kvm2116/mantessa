-- MySQL Script generated by MySQL Workbench
-- Tue Feb 21 16:59:48 2017
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mantessa_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mantessa_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mantessa_db` DEFAULT CHARACTER SET utf8 ;
USE `mantessa_db` ;

-- -----------------------------------------------------
-- Table `mantessa_db`.`mantessa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mantessa_db`.`mantessa` (
  `ip` INT UNSIGNED NOT NULL,
  `latitude` DECIMAL(10,4) NOT NULL DEFAULT 0,
  `longitude` DECIMAL(10,4) NOT NULL DEFAULT 0,
  `date` DATETIME NULL,
  `day1` TINYINT(1) NULL,
  `day2` TINYINT(1) NULL,
  PRIMARY KEY (`ip`, `latitude`, `longitude`))
ENGINE = InnoDB;

USE `mantessa_db` ;

-- -----------------------------------------------------
-- procedure update_mantessa
-- -----------------------------------------------------

DELIMITER $$
USE `mantessa_db`$$
CREATE PROCEDURE `update_mantessa` (IN col_name VARCHAR(30), IN ip_add VARCHAR(24), IN lat FLOAT , IN longit FLOAT)
BEGIN
Declare foundcount INT;
SET @col = col_name;
SET @a_ip = ip_add;
SET @lati = lat;
SET @longitu = longit;
SET @sql_text = concat('UPDATE mantessa SET ',@col,'=',1,' WHERE ip=',INET_ATON(@a_ip),' and latitude=',@lati,' and longitude=',@longitu);
PREPARE stmt FROM @sql_text;
EXECUTE stmt;
Select ROW_COUNT() INTO foundcount;
DEALLOCATE PREPARE stmt;

IF foundcount <> 1 THEN

SET @sql_text2 = concat('INSERT IGNORE INTO mantessa (ip,latitude,longitude,date,',@col,') VALUES (',INET_ATON(@a_ip),',', @lati,',',  @longitu,',\'',CURRENT_TIMESTAMP(),'\',1)');
PREPARE stmt2 FROM @sql_text2;
EXECUTE stmt2;
DEALLOCATE PREPARE stmt2;
END IF;
END$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
