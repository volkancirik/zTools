-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.5.22 - MySQL Community Server (GPL)
-- Server OS:                    Win32
-- HeidiSQL version:             7.0.0.4053
-- Date/time:                    2012-05-08 17:39:12
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;

-- Dumping structure for table rocket_orders_v03.cross_order_orderattributeset
CREATE TABLE IF NOT EXISTS `cross_order_orderattributeset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `attributeName` varchar(50) NOT NULL,
  `attributeCode` varchar(50) NOT NULL,
  `isInvalid` tinyint(1) NOT NULL,
  `createTime` datetime NOT NULL,
  `order` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- Dumping data for table rocket_orders_v03.cross_order_orderattributeset: ~6 rows (approximately)
/*!40000 ALTER TABLE `cross_order_orderattributeset` DISABLE KEYS */;
INSERT INTO `cross_order_orderattributeset` (`id`, `attributeName`, `attributeCode`, `isInvalid`, `createTime`, `order`) VALUES
	(1, 'Apparel', 'AP', 0, '2012-05-08 14:54:52', 10),
	(2, 'Accessories', 'AC', 0, '2012-05-08 14:54:52', 20),
	(3, 'Shoes', 'SH', 0, '2012-05-08 14:54:52', 30),
	(4, 'Jewellery', 'JE', 0, '2012-05-08 14:54:52', 40),
	(5, 'Beauty', 'BE', 0, '2012-05-08 14:54:52', 50),
	(6, 'Home textiles & Decoration', 'HO', 0, '2012-05-08 14:54:52', 60);
/*!40000 ALTER TABLE `cross_order_orderattributeset` ENABLE KEYS */;
/*!40014 SET FOREIGN_KEY_CHECKS=1 */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
