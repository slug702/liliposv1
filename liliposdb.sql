-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: lilipos
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(45) DEFAULT NULL,
  `category_type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'All','All'),(2,'Appetizers','appetizers'),(3,'Sides','sides'),(4,'Ice Cream','dessert'),(5,'Cookies','baked goods'),(6,'Chicken','meat'),(7,'Pork','meat'),(8,'Beef','meat'),(9,'Vegetables','vegan'),(10,'Puppies','pupcups'),(11,'Mains','Main');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoices`
--

DROP TABLE IF EXISTS `invoices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoices` (
  `iid` int NOT NULL AUTO_INCREMENT,
  `idate` date DEFAULT NULL,
  `iproducts` varchar(45) DEFAULT NULL,
  `mop` varchar(45) DEFAULT NULL,
  `tprce` float DEFAULT NULL,
  `pricebeforedscnt` float DEFAULT NULL,
  `idscnt` float DEFAULT NULL,
  `vat` float DEFAULT NULL,
  `paid` float DEFAULT NULL,
  `change` float DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `cashier` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`iid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoices`
--

LOCK TABLES `invoices` WRITE;
/*!40000 ALTER TABLE `invoices` DISABLE KEYS */;
/*!40000 ALTER TABLE `invoices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `pid` int NOT NULL AUTO_INCREMENT,
  `product_desc` varchar(45) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `category_name` varchar(45) DEFAULT NULL,
  `sub_category` varchar(45) DEFAULT NULL,
  `product_picture` longblob,
  `size` varchar(45) DEFAULT NULL,
  `size_group` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'chickenjoy',200,'Mains','Chicken',NULL,'No Size','No Size'),(3,'cheeseburger',120,'Mains','Beef',NULL,'No Size','No Size'),(4,'chickenskin',100,'Sides','Chicken',NULL,'No Size','No Size'),(5,'humba',300,'Mains','Pork',NULL,'No Size','No Size'),(6,'noodles',3200,'Appetizers','noodles',NULL,'No Size','No Size'),(7,'cheesy fries',400,'Sides','A',NULL,'Small','No Size'),(9,'Biscuit',100,'Sides','A',NULL,'No Size','No Size'),(12,'Banana Cake',200,'Appetizers','Yes',NULL,'No Size','No Size'),(13,'shawarma fries',150,'Mains','Sides',NULL,'No Size','No Size'),(17,'Birria Quesedilla',250,'Mains','Mexican',NULL,'No Size','No Size'),(18,'crossiant',260,'Sides','Sides',NULL,'No Size','No Size'),(21,'L coffee',250,'Drinks','Main',NULL,'L','coffee'),(24,'Jolli Hotdog',250.2,'Hotdog','Franchies',NULL,'No Size','No Size'),(27,'Frites',250,'French','Potatoes',NULL,'No Size','No Size');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `tid` int NOT NULL AUTO_INCREMENT,
  `trpid` int DEFAULT NULL,
  `trdesc` varchar(45) DEFAULT NULL,
  `trprce` float DEFAULT NULL,
  `dscnt` float DEFAULT NULL,
  `invid` int DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `idusers` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `position` varchar(45) DEFAULT NULL,
  `rank` varchar(45) DEFAULT NULL,
  `branch` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idusers`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'geeo','0','Founder','0','Cebu');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-18 21:31:01
