USE `bearing_project`;

-- 插入用户信息
TRUNCATE TABLE `user`;
INSERT INTO `user` VALUES (1, 'demo', '先生', '13800001111', '021-12345678-8006', '021-12345678', 'yuhuangdadi@tianting.com', 2, 3, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user` VALUES (2, 'test', '先生', '13800001111', '021-12345678-8006', '021-12345678', '', 1, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user` VALUES (3, 'cto', '经理', '13800001111', '021-12345678-8006', '021-12345678', '', 3, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user` VALUES (4, 'ceo', '经理', '13800001111', '021-12345678-8006', '021-12345678', '', 3, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user` VALUES (5, 'cat', '小姐', '13800001111', '021-12345678-8006', '021-12345678', '', 2, 3, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user` VALUES (6, 'dog', '先生', '13800001111', '021-12345678-8006', '021-12345678', '', 2, 4, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入用户认证信息
TRUNCATE TABLE `user_auth`;
INSERT INTO `user_auth` VALUES (1, 1, 0, 'demo', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user_auth` VALUES (2, 2, 0, 'test', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user_auth` VALUES (3, 3, 0, 'cto', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user_auth` VALUES (4, 4, 0, 'ceo', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user_auth` VALUES (5, 5, 0, 'cat', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user_auth` VALUES (6, 6, 0, 'dog', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入角色信息（0:默认,1:系统,2:销售,3:经理,4:库管,5:财务）
TRUNCATE TABLE `role`;
INSERT INTO `role` VALUES (1, '系统', '', '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `role` VALUES (2, '销售', '', '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `role` VALUES (3, '经理', '', '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入客户信息
TRUNCATE TABLE `customer`;
INSERT INTO `customer` VALUES (1, '上海测试科技有限公司', '上海市虹口区曲阳路898号1202室', 'http://www.baidu.com', '021-12345678', '021-12345678', 'youyiku@example.com', 1, 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `customer` VALUES (2, '测试公司2', '公司地址2', 'http://www.baidu.com', '021-12345678', '021-12345678', 'youyiku@example.com', 1, 6, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `customer` VALUES (3, '测试公司3', '公司地址3', 'http://www.baidu.com', '021-12345678', '021-12345678', 'youyiku@example.com', 1, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `customer` VALUES (4, '测试公司4', '公司地址4', 'http://www.baidu.com', '021-12345678', '021-12345678', 'youyiku@example.com', 1, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入客户联系方式信息
TRUNCATE TABLE `customer_contact`;
INSERT INTO `customer_contact` VALUES (1, 1, '小马', '先生', '13800000000', '021-12345678', '021-12345678', 'wangchuanjun@example.com', '采购', '上海市虹口区曲阳路898号1202室', '', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `customer_contact` VALUES (2, 1, '小兰', '小姐', '13811111111', '021-12345678', '021-12345678', 'youyiku@example.com', '采购', '上海市虹口区曲阳路898号1202室', '', 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入产品类别
TRUNCATE TABLE `category`;
INSERT INTO `category` VALUES (1, '轴承', 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (2, '调心球轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (3, '调心滚子轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (4, '圆锥滚子轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (5, '推力球轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (6, '深沟球轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (7, '角接触球轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (8, '圆柱滚子轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (9, '滚针轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (10, '双向推力角接触球轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (11, '转台轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (12, '滚珠丝杠轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (13, '精密锁紧螺母', 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入产品信息
TRUNCATE TABLE `production`;
INSERT INTO `production` VALUES (1, 0, 'SKF', '7008CEGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (2, 0, 'SKF', '7012CEGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (3, 0, 'SKF', '7008CEGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (4, 0, 'SKF', '7012CEGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (5, 0, 'SKF', '7008CDGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (6, 0, 'SKF', '7012CDGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (7, 0, 'SKF', '7008CDGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (8, 0, 'SKF', '7012CDGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (9, 0, 'SKF', '7008ACEGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (10, 0, 'SKF', '7012ACEGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (11, 0, 'SKF', '7008ACEGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (12, 0, 'SKF', '7012ACEGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (13, 0, 'SKF', '7008ACDGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (14, 0, 'SKF', '7012ACDGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (15, 0, 'SKF', '7008ACDGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (16, 0, 'SKF', '7012ACDGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (17, 0, 'SKF', '7008CBGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (18, 0, 'SKF', '7012CBGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (19, 0, 'SKF', '7008CBGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (20, 0, 'SKF', '7012CBGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (21, 0, 'SKF', '7008ACBGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (22, 0, 'SKF', '7012ACBGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (23, 0, 'SKF', '7008ACBGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (24, 0, 'SKF', '7012ACBGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (25, 0, 'SKF', '7008FBGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (26, 0, 'SKF', '7012FBGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (27, 0, 'SKF', '7008FBGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (28, 0, 'SKF', '7012FBGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');

-- 插入报价汇总信息
TRUNCATE TABLE `quotation`;
INSERT INTO `quotation` VALUES (1, 1, 1, 1, '11000.00', '10.00', '0.00', '11000.00', '', '', 1, 0, 0, 0, 0, '2018-03-21', NULL, NULL, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation` VALUES (2, 1, 1, 1, '11000.00', '10.00', '0.00', '11000.00', '', '', 1, 0, 0, 0, 0, '2018-03-21', NULL, NULL, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入报价明细信息
TRUNCATE TABLE `quotation_items`;
INSERT INTO `quotation_items` VALUES (1, 1, 1, 1, '测试公司1', '7008CE', 0, 1, 'SKF', '7008CEGA/P4A', 'Pcs', '', 10, '20.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (2, 1, 1, 1, '测试公司1', '7012CE', 0, 2, 'SKF', '7012CEGA/P4A', 'Pcs', '', 10, '80.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (3, 1, 1, 1, '测试公司1', '7008CE/HC', 0, 3, 'SKF', '7008CEGA/HCP4A', 'Pcs', '', 10, '20.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (4, 1, 1, 1, '测试公司1', '7012CE/HC', 0, 4, 'SKF', '7012CEGA/HCP4A', 'Pcs', '', 10, '80.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (5, 2, 1, 1, '测试公司1', '7008CE', 0, 1, 'SKF', '7008CEGA/P4A', 'Pcs', '', 10, '20.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (6, 2, 1, 1, '测试公司1', '7012CE', 0, 2, 'SKF', '7012CEGA/P4A', 'Pcs', '', 10, '80.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (7, 2, 1, 1, '测试公司1', '7008CE/HC', 0, 3, 'SKF', '7008CEGA/HCP4A', 'Pcs', '', 10, '20.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (8, 2, 1, 1, '测试公司1', '7012CE/HC', 0, 4, 'SKF', '7012CEGA/HCP4A', 'Pcs', '', 10, '80.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');

USE bearing_project;

-- 插入用户信息
TRUNCATE TABLE `user`;
INSERT INTO `user` VALUES (1, 'demo', '先生', '13800001111', '021-12345678-8006', '021-12345678', 'yuhuangdadi@tianting.com', 2, 3, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user` VALUES (2, 'test', '先生', '13800001111', '021-12345678-8006', '021-12345678', '', 1, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user` VALUES (3, 'cto', '经理', '13800001111', '021-12345678-8006', '021-12345678', '', 3, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user` VALUES (4, 'ceo', '经理', '13800001111', '021-12345678-8006', '021-12345678', '', 3, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user` VALUES (5, 'cat', '小姐', '13800001111', '021-12345678-8006', '021-12345678', '', 2, 3, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user` VALUES (6, 'dog', '先生', '13800001111', '021-12345678-8006', '021-12345678', '', 2, 4, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入用户认证信息
TRUNCATE TABLE `user_auth`;
INSERT INTO `user_auth` VALUES (1, 1, 0, 'demo', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user_auth` VALUES (2, 2, 0, 'test', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user_auth` VALUES (3, 3, 0, 'cto', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user_auth` VALUES (4, 4, 0, 'ceo', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user_auth` VALUES (5, 5, 0, 'cat', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `user_auth` VALUES (6, 6, 0, 'dog', '123456', 1, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入角色信息（0:默认,1:系统,2:销售,3:经理,4:库管,5:财务）
TRUNCATE TABLE `role`;
INSERT INTO `role` VALUES (1, '系统', '', '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `role` VALUES (2, '销售', '', '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `role` VALUES (3, '经理', '', '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入客户信息
TRUNCATE TABLE `customer`;
INSERT INTO `customer` VALUES (1, '上海测试客户有限公司', '上海市虹口区曲阳路898号1202室', 'http://www.baidu.com', '021-12345678', '021-12345678', 'youyiku@example.com', 1, 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `customer` VALUES (2, '测试公司2', '公司地址2', 'http://www.baidu.com', '021-12345678', '021-12345678', 'youyiku@example.com', 1, 6, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `customer` VALUES (3, '测试公司3', '公司地址3', 'http://www.baidu.com', '021-12345678', '021-12345678', 'youyiku@example.com', 1, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `customer` VALUES (4, '测试公司4', '公司地址4', 'http://www.baidu.com', '021-12345678', '021-12345678', 'youyiku@example.com', 1, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入客户联系方式信息
TRUNCATE TABLE `customer_contact`;
INSERT INTO `customer_contact` VALUES (1, 1, '小马', '先生', '13800000000', '021-12345678', '021-12345678', 'wangchuanjun@example.com', '采购', '上海市虹口区曲阳路898号1202室', '', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `customer_contact` VALUES (2, 1, '小兰', '小姐', '13811111111', '021-12345678', '021-12345678', 'youyiku@example.com', '采购', '上海市虹口区曲阳路898号1202室', '', 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入友商信息
TRUNCATE TABLE `supplier`;
INSERT INTO `supplier` VALUES (1, '上海测试友商有限公司', '上海市虹口区曲阳路898号1202室', 'http://www.baidu.com', '021-12345678', '021-12345678', 'youyiku@example.com', 1, 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `supplier` VALUES (2, '测试公司2', '公司地址2', 'http://www.baidu.com', '021-12345678', '021-12345678', 'youyiku@example.com', 1, 6, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `supplier` VALUES (3, '测试公司3', '公司地址3', 'http://www.baidu.com', '021-12345678', '021-12345678', 'youyiku@example.com', 1, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `supplier` VALUES (4, '测试公司4', '公司地址4', 'http://www.baidu.com', '021-12345678', '021-12345678', 'youyiku@example.com', 1, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入友商联系方式信息
TRUNCATE TABLE `supplier_contact`;
INSERT INTO `supplier_contact` VALUES (1, 1, '小马', '先生', '13800000000', '021-12345678', '021-12345678', 'wangchuanjun@example.com', '采购', '上海市虹口区曲阳路898号1202室', '', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `supplier_contact` VALUES (2, 1, '小兰', '小姐', '13811111111', '021-12345678', '021-12345678', 'youyiku@example.com', '采购', '上海市虹口区曲阳路898号1202室', '', 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入产品类别
TRUNCATE TABLE `category`;
INSERT INTO `category` VALUES (1, '轴承', 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (2, '调心球轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (3, '调心滚子轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (4, '圆锥滚子轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (5, '推力球轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (6, '深沟球轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (7, '角接触球轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (8, '圆柱滚子轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (9, '滚针轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (10, '双向推力角接触球轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (11, '转台轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (12, '滚珠丝杠轴承', 1, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `category` VALUES (13, '精密锁紧螺母', 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入产品信息
TRUNCATE TABLE `production`;
INSERT INTO `production` VALUES (1, 0, 'SKF', '7008CEGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (2, 0, 'SKF', '7012CEGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (3, 0, 'SKF', '7008CEGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (4, 0, 'SKF', '7012CEGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (5, 0, 'SKF', '7008CDGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (6, 0, 'SKF', '7012CDGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (7, 0, 'SKF', '7008CDGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (8, 0, 'SKF', '7012CDGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (9, 0, 'SKF', '7008ACEGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (10, 0, 'SKF', '7012ACEGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (11, 0, 'SKF', '7008ACEGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (12, 0, 'SKF', '7012ACEGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (13, 0, 'SKF', '7008ACDGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (14, 0, 'SKF', '7012ACDGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (15, 0, 'SKF', '7008ACDGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (16, 0, 'SKF', '7012ACDGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (17, 0, 'SKF', '7008CBGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (18, 0, 'SKF', '7012CBGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (19, 0, 'SKF', '7008CBGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (20, 0, 'SKF', '7012CBGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (21, 0, 'SKF', '7008ACBGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (22, 0, 'SKF', '7012ACBGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (23, 0, 'SKF', '7008ACBGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (24, 0, 'SKF', '7012ACBGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (25, 0, 'SKF', '7008FBGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (26, 0, 'SKF', '7012FBGA/P4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (27, 0, 'SKF', '7008FBGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `production` VALUES (28, 0, 'SKF', '7012FBGA/HCP4A', 'Pcs', '', '0', '0', '0', '0', '0', '0.000', '', '', '', '', '', '', '', '', '', '', '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入敏感型号
TRUNCATE TABLE `production_sensitive`;
INSERT INTO `production_sensitive` VALUES (1, 1, '上海测试科技有限公司', 25, 'SKF', '7008FBGA/P4A', 'Pcs', '批量订单', 0, null, '2019-03-18 09:44:17', '2019-03-18 09:44:17');


-- 插入报价汇总信息
TRUNCATE TABLE `quotation`;
INSERT INTO `quotation` VALUES (1, 1, 1, 1, '11000.00', '10.00', '0.00', '11000.00', '', '', 1, 0, 0, 0, 0, '2018-03-21', NULL, NULL, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation` VALUES (2, 1, 1, 1, '11000.00', '10.00', '0.00', '11000.00', '', '', 1, 0, 0, 0, 0, '2018-03-21', NULL, NULL, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入报价明细信息
TRUNCATE TABLE `quotation_items`;
INSERT INTO `quotation_items` VALUES (1, 1, 1, 1, '测试公司1', '7008CE', 0, 1, 'SKF', '7008CEGA/P4A', 'Pcs', '', 10, '20.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (2, 1, 1, 1, '测试公司1', '7012CE', 0, 2, 'SKF', '7012CEGA/P4A', 'Pcs', '', 10, '80.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (3, 1, 1, 1, '测试公司1', '7008CE/HC', 0, 3, 'SKF', '7008CEGA/HCP4A', 'Pcs', '', 10, '20.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (4, 1, 1, 1, '测试公司1', '7012CE/HC', 0, 4, 'SKF', '7012CEGA/HCP4A', 'Pcs', '', 10, '80.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (5, 2, 1, 1, '测试公司1', '7008CE', 0, 1, 'SKF', '7008CEGA/P4A', 'Pcs', '', 10, '20.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (6, 2, 1, 1, '测试公司1', '7012CE', 0, 2, 'SKF', '7012CEGA/P4A', 'Pcs', '', 10, '80.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (7, 2, 1, 1, '测试公司1', '7008CE/HC', 0, 3, 'SKF', '7008CEGA/HCP4A', 'Pcs', '', 10, '20.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `quotation_items` VALUES (8, 2, 1, 1, '测试公司1', '7012CE/HC', 0, 4, 'SKF', '7012CEGA/HCP4A', 'Pcs', '', 10, '80.00', '', 0, 0, 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入询价汇总信息
TRUNCATE TABLE `enquiry`;
INSERT INTO `enquiry` VALUES (1, 1, 1, 1, 10.00, 0.00, 0.00, 10.00, '', '', 1, 0, 0, 0, 0, '2019-04-03', null, null, null, '2019-03-27 07:22:10', '2019-03-27 07:22:10');


-- 插入询价明细信息
TRUNCATE TABLE `enquiry_items`;
INSERT INTO `enquiry_items` VALUES (1, 1, 1, 1, '上海测试友商有限公司', '', 1, 27, 'SKF', '7008FBGA/HCP4A', 'Pcs', '', 1, 10.00, '', 1, 0, 0, null, '2019-03-27 07:22:10', '2019-03-27 07:22:10');


-- 插入仓库信息
TRUNCATE TABLE `warehouse`;
INSERT INTO `warehouse` VALUES (1, '保税仓储中心', '保税区', '小马', '021-66662222', '021-66668888', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `warehouse` VALUES (2, '无人分拣中心', '郊区', '老马', '021-22226666', '021-88886666', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入货架信息
TRUNCATE TABLE `rack`;
INSERT INTO `rack` VALUES (1, 1, 'A-010201', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `rack` VALUES (2, 1, 'B-020101', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `rack` VALUES (3, 2, 'C-010201', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `rack` VALUES (4, 2, 'D-020101', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入库存信息
TRUNCATE TABLE `inventory`;
INSERT INTO `inventory` VALUES (1, 1, 'SKF', '7008CEGA/P4A', 'Pcs', 1, '保税仓储中心', 1, 'A-010201', 100, 100, 'SNFA', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `inventory` VALUES (2, 1, 'SKF', '7008CEGA/P4A', 'Pcs', 1, '保税仓储中心', 2, 'B-020101', 20, 20, '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `inventory` VALUES (3, 2, 'SKF', '7012CEGA/P4A', 'Pcs', 1, '保税仓储中心', 1, 'A-010201', 20, 20, 'SNFA', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');
INSERT INTO `inventory` VALUES (4, 2, 'SKF', '7012CEGA/P4A', 'Pcs', 1, '保税仓储中心', 2, 'B-020101', 80, 80, '', 0, NULL, '2018-03-14 10:00:00', '2018-03-14 10:00:00');


-- 插入销售订单
TRUNCATE TABLE `sales_order`;
INSERT INTO `sales_order` VALUES (1, 1, 1, 1, 14000.00, 0.00, 0.00, 14000.00, '', '', 1, 0, 0, 0, 0, 0, null, null, null, null, '2019-03-27 08:00:37', '2019-03-27 08:00:37');

-- 插入销售订单明细
TRUNCATE TABLE `sales_order_items`;
INSERT INTO `sales_order_items` VALUES (1, 1, 1, 1, '上海测试客户有限公司', '', '', 23, 'SKF', '7008ACBGA/HCP4A', 'Pcs', '', 2, 3000.00, '', 1, 0, null, '2019-03-27 08:00:37', '2019-03-27 08:00:37');
INSERT INTO `sales_order_items` VALUES (2, 1, 1, 1, '上海测试客户有限公司', '', '', 22, 'SKF', '7012ACBGA/P4A', 'Pcs', '', 2, 4000.00, '', 1, 0, null, '2019-03-27 08:00:37', '2019-03-27 08:00:37');


-- 插入采购订单
TRUNCATE TABLE `buyer_order`;
INSERT INTO `buyer_order` VALUES (1, 1, 1, 1, 10000.00, 0.00, 0.00, 10000.00, '', '', 1, 0, 0, 0, 0, 0, null, null, null, null, '2019-03-27 08:03:05', '2019-03-27 08:03:05');

-- 插入采购订单明细
TRUNCATE TABLE `buyer_order_items`;
INSERT INTO `buyer_order_items` VALUES (1, 1, 1, 1, '上海测试友商有限公司', '', '', 23, 'SKF', '7008ACBGA/HCP4A', 'Pcs', '', 2, 2000.00, '', 1, 0, null, '2019-03-27 08:03:05', '2019-03-27 08:03:05');
INSERT INTO `buyer_order_items` VALUES (2, 1, 1, 1, '上海测试友商有限公司', '', '', 22, 'SKF', '7012ACBGA/P4A', 'Pcs', '', 2, 3000.00, '', 1, 0, null, '2019-03-27 08:03:05', '2019-03-27 08:03:05');


-- 插入销售出货
TRUNCATE TABLE `delivery`;
INSERT INTO `delivery` VALUES (1, 1, 0, 1, '', 1, 0, 21000.00, 0.00, 0.00, 21000.00, 1, '', 1, 0, 0, 0, 0, null, null, null, '2019-03-19 11:18:57', '2019-03-19 11:24:57');


-- 插入销售出货明细
TRUNCATE TABLE `delivery_items`;
INSERT INTO `delivery_items` VALUES (1, 1, 1, 0, 1, '上海测试客户有限公司', '', '', 17, 'SKF', '7008CBGA/P4A', 'Pcs', 1, 1, '', 1, 4, 3200.00, 0, null, '2019-03-19 11:18:57', '2019-03-19 11:18:57');
INSERT INTO `delivery_items` VALUES (2, 1, 1, 0, 1, '上海测试客户有限公司', '', '', 22, 'SKF', '7012ACBGA/P4A', 'Pcs', 1, 2, '', 1, 2, 4100.00, 0, null, '2019-03-19 11:18:57', '2019-03-19 11:18:57');


-- 插入采购进货
INSERT INTO `purchase` VALUES (1, 1, 0, 1, '', 1, 0, 10200.00, 0.00, 0.00, 10200.00, 1, '', 1, 0, 0, 0, 0, null, null, null, '2019-03-19 10:32:14', '2019-03-19 10:45:54');

-- 插入采购进货明细
INSERT INTO `purchase_items` VALUES (1, 1, 1, 0, 1, '上海测试友商有限公司', 23, 'SKF', '7008ACBGA/HCP4A', 'Pcs', 1, 1, '', 1, 2, 3100.00, 0, null, '2019-03-19 10:32:14', '2019-03-19 10:45:54');
INSERT INTO `purchase_items` VALUES (2, 1, 1, 0, 1, '上海测试友商有限公司', 28, 'SKF', '7012FBGA/HCP4A', 'Pcs', 1, 2, '', 1, 1, 4000.00, 0, null, '2019-03-19 10:32:14', '2019-03-19 10:32:14');

-- 插入仓库出库


-- 插入仓库入库

