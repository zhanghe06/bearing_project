USE bearing_project;

-- 插入用户信息
TRUNCATE TABLE `user`;
INSERT INTO `user` VALUES (1, 'demo', 1, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user` VALUES (2, 'test', 1, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入用户认证信息
TRUNCATE TABLE `user_auth`;
INSERT INTO `user_auth` VALUES (1, 1, 0, 'demo', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user_auth` VALUES (2, 2, 0, 'test', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入角色信息
TRUNCATE TABLE `role`;
INSERT INTO `role` VALUES (1, '销售', '', '产品,客户,报价,统计', '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `role` VALUES (2, '经理', '', '产品,客户,报价,统计,用户', '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `role` VALUES (3, '系统', '', '产品,客户,报价,统计,用户,角色,系统', '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入客户信息
TRUNCATE TABLE `customer`;
INSERT INTO `customer` VALUES (1, '测试公司', '公司地址', 'http://www.baidu.com', '123456', '123456', 1, 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `customer` VALUES (2, '测试公司', '公司地址', 'http://www.baidu.com', '123456', '123456', 1, 2, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入客户联系方式信息
TRUNCATE TABLE `customer_contact`;
INSERT INTO `customer_contact` VALUES (1, 1, '小马', '先生', '13800000000', '123456-006', '123456-006', '采购', '', '', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `customer_contact` VALUES (2, 1, '小兰', '小姐', '13811111111', '123456-002', '123456-002', '采购', '', '', 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入产品信息
TRUNCATE TABLE `product`;
INSERT INTO `product` VALUES (1, 'SKF', '7008CEGA/P4A', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `product` VALUES (2, 'SKF', '7012CEGA/P4A', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入报价汇总信息
TRUNCATE TABLE `quote`;
INSERT INTO `quote` VALUES (1, 1, 1, 1, '1000.00', '', 0, 0, 0, NULL, NULL, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入报价明细信息
TRUNCATE TABLE `quote_item`;
INSERT INTO `quote_item` VALUES (1, 1, 1, 'SKF', '7008CEGA/P4A', '', 10, '20.00', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quote_item` VALUES (2, 1, 2, 'SKF', '7012CEGA/P4A', '', 10, '80.00', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
