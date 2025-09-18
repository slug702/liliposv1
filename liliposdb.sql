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
-- Table structure for table `invoices`
--

DROP TABLE IF EXISTS `invoices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoices` (
  `inv_id` int NOT NULL AUTO_INCREMENT,
  `table_num` int DEFAULT NULL,
  `cashier` varchar(45) DEFAULT NULL,
  `order_type` varchar(45) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `total_vat` decimal(10,2) DEFAULT NULL,
  `order_date` date DEFAULT NULL,
  PRIMARY KEY (`inv_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoices`
--

LOCK TABLES `invoices` WRITE;
/*!40000 ALTER TABLE `invoices` DISABLE KEYS */;
INSERT INTO `invoices` VALUES (1,NULL,'Me','Takeaway','UNPAID',12.00,NULL),(2,NULL,NULL,NULL,'UNPAID',NULL,NULL),(3,NULL,NULL,NULL,'UNPAID',NULL,NULL),(4,NULL,NULL,NULL,'UNPAID',NULL,NULL),(5,NULL,NULL,NULL,'NEW',NULL,'2025-09-18'),(6,NULL,NULL,NULL,'NEW',NULL,'2025-09-18'),(7,NULL,NULL,NULL,'NEW',NULL,'2025-09-18'),(8,NULL,NULL,NULL,'NEW',NULL,'2025-09-19'),(9,NULL,NULL,NULL,'NEW',NULL,'2025-09-19'),(10,NULL,NULL,NULL,'NEW',NULL,'2025-09-19'),(11,NULL,NULL,NULL,'NEW',NULL,'2025-09-19'),(12,NULL,NULL,NULL,'NEW',NULL,'2025-09-19');
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
  `price` decimal(10,2) DEFAULT NULL,
  `category_name` varchar(45) DEFAULT NULL,
  `sub_category` varchar(45) DEFAULT NULL,
  `product_picture` longblob,
  `size` varchar(45) DEFAULT NULL,
  `size_group` varchar(45) DEFAULT NULL,
  `vat` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (32,'Fries',150.00,'Potatoes','Fried',NULL,'No Size','No Size','yes'),(33,'Iced Tea',50.00,'Drinks','Tea',NULL,'No Size','No Size','yes'),(34,'Coke',35.50,'Drinks','Soda',NULL,'No Size','No Size','yes'),(35,'Cheeseburger',225.50,'Sandwich','Beef',NULL,'No Size','No Size','yes'),(36,'Beef Shawarma',250.00,'Wrap','Beef',NULL,'No Size','No Size','yes'),(37,'Burger-Steak',200.00,'Meal','Rice',NULL,'No Size','No Size','no');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile`
--

DROP TABLE IF EXISTS `profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile` (
  `profile_id` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `vat_rate` decimal(10,2) DEFAULT NULL,
  `vat_enabled` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile`
--

LOCK TABLES `profile` WRITE;
/*!40000 ALTER TABLE `profile` DISABLE KEYS */;
INSERT INTO `profile` VALUES (1,'Sunburst',12.00,'yes');
/*!40000 ALTER TABLE `profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `tr_id` int NOT NULL AUTO_INCREMENT,
  `inv_id` int DEFAULT NULL,
  `p_id` int DEFAULT NULL,
  `tr_type` varchar(45) DEFAULT NULL,
  `tr_desc` varchar(45) DEFAULT NULL,
  `vat` varchar(45) DEFAULT NULL,
  `gross_price` decimal(10,2) DEFAULT NULL,
  `net` decimal(10,2) DEFAULT NULL,
  `vat_total` decimal(10,2) DEFAULT NULL,
  `total_discount` decimal(10,2) DEFAULT NULL,
  `rounding` decimal(10,2) DEFAULT NULL,
  `discount_rate` decimal(10,2) DEFAULT NULL,
  `mop` varchar(45) DEFAULT NULL,
  `tr_date` date DEFAULT NULL,
  PRIMARY KEY (`tr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (20,1,32,'product','Fries','yes',150.00,150.00,NULL,NULL,0.00,NULL,NULL,'2025-09-19'),(21,1,33,'product','Iced Tea','yes',50.00,50.00,NULL,NULL,0.00,NULL,NULL,'2025-09-19'),(22,1,34,'product','Coke','yes',30.00,30.00,NULL,NULL,0.00,NULL,NULL,'2025-09-19'),(27,11,32,'product','Fries','yes',150.00,NULL,NULL,NULL,NULL,NULL,NULL,'2025-09-19'),(28,11,33,'product','Iced Tea','yes',50.00,NULL,NULL,NULL,NULL,NULL,NULL,'2025-09-19'),(29,11,34,'product','Coke','yes',30.00,NULL,NULL,NULL,NULL,NULL,NULL,'2025-09-19'),(32,12,32,'product','Fries','yes',150.00,NULL,NULL,NULL,NULL,NULL,NULL,'2025-09-19'),(33,12,33,'product','Iced Tea','yes',50.00,NULL,NULL,NULL,NULL,NULL,NULL,'2025-09-19'),(34,12,34,'product','Coke','yes',36.00,NULL,NULL,NULL,NULL,NULL,NULL,'2025-09-19');
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

-- Dump completed on 2025-09-19  2:26:46
