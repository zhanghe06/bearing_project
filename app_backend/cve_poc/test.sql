--
-- Current Database: `test`
--

-- DROP DATABASE IF EXISTS `test`;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `test`;

DROP TABLE IF EXISTS `sql_test`;
CREATE TABLE `sql_test` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '名称',
  `des` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='sql测试表';


-- 插入用户认证信息
TRUNCATE TABLE `sql_test`;
INSERT INTO `sql_test` VALUES (1, 'a', '001');
INSERT INTO `sql_test` VALUES (2, 'b', '002');
INSERT INTO `sql_test` VALUES (3, 'c', '003');
INSERT INTO `sql_test` VALUES (4, 'd', '004');
INSERT INTO `sql_test` VALUES (5, 'e', '005');
