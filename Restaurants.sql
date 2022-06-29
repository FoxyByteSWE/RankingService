-- MariaDB dump 10.19  Distrib 10.5.12-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: Restaurants
-- ------------------------------------------------------
-- Server version	10.5.12-MariaDB-1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Restaurants`
--

DROP TABLE IF EXISTS `Restaurants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Restaurants` (
  `Codice_pk` varchar(20) NOT NULL,
  `Nome` varchar(50) NOT NULL,
  `Categoria` varchar(20) DEFAULT NULL,
  `Indirizzo` varchar(100) DEFAULT NULL,
  `Sito` varchar(70) DEFAULT NULL,
  `Telefono` varchar(16) DEFAULT NULL,
  `Longitudine` float DEFAULT NULL,
  `Latitudine` float DEFAULT NULL,
  `Ranking` float DEFAULT NULL,
  PRIMARY KEY (`Codice_pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Restaurants`
--

LOCK TABLES `Restaurants` WRITE;
/*!40000 ALTER TABLE `Restaurants` DISABLE KEYS */;
INSERT INTO `Restaurants` VALUES ('1788391034730029','Farina del mio sacco','Deli','28, Via Saraceno, Centro cittadino, Giardino, Ferrara, Emilia-Romagna, 44121, Italia','https://www.farinadelmiosaccoferrara.it','0532474303',11.6229,44.8329,7),('237766690','Pasticceria Chiurato','Bar','Pasticceria Chiurato, 50, Corso Mazzini, Marostica, Colceresa, Vicenza, Veneto, 36063, Italia','https://www.pasticceriachiurato.it/','042472134',11.656,45.7467,5),('4706333','Al Saiso','Pub','2, Via Crestano Menarola, Angarano, Bassano del Grappa, Colceresa, Vicenza, Veneto, 31061, Italia','http://www.alsaiso.it','0424220819',11.7321,45.7675,5),('742243027','Pizzeria L\'Angelo e il Diavolo','Pizza place','San Mango Piemonte, Salerno, Campania, 84132, Italia','https://www.pizzerialangeloeildiavolo.it','+39089281793',14.8297,40.6995,5);
/*!40000 ALTER TABLE `Restaurants` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-29 18:49:10
