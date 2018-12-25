DROP DATABASE IF EXISTS `bearing_project`;
CREATE DATABASE `bearing_project` /*!40100 DEFAULT CHARACTER SET utf8 */;


use bearing_project;


DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(20) BINARY NOT NULL DEFAULT '' COMMENT '姓名',
  `salutation` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '称呼',
  `mobile` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '手机',
  `tel` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '电话',
  `fax` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '传真',
  `email` VARCHAR(60) NOT NULL DEFAULT '' COMMENT '邮箱',
  `role_id` TINYINT NOT NULL DEFAULT 0 COMMENT '角色（0:默认,1:系统,2:销售,3:经理,4:库管,5:财务）',
  `parent_id` INT NOT NULL DEFAULT 0 COMMENT '上级用户ID',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户全局注册表';


DROP TABLE IF EXISTS `user_auth`;
CREATE TABLE `user_auth` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL DEFAULT 0 COMMENT '用户ID',
  `type_auth` TINYINT NOT NULL DEFAULT 0 COMMENT '认证类型（0:账号,1:邮箱,2:手机,3:QQ,4:微信,5:微博）',
  `auth_key` VARCHAR(60) BINARY NOT NULL DEFAULT '' COMMENT '授权账号（账号;邮箱;手机;第三方登陆，这里是openid）',
  `auth_secret` VARCHAR(60) BINARY NOT NULL DEFAULT '' COMMENT '密码凭证（密码;token）',
  `status_verified` TINYINT NOT NULL DEFAULT 0 COMMENT '认证状态（0:未认证,1:已认证）',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`user_id`),
  UNIQUE (`type_auth`, `auth_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户认证表';


DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '角色名称（0:默认,1:系统,2:销售,3:经理,4:库管,5:财务）',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '角色备注',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='角色权限表';


DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `company_address` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司地址',
  `company_site` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司官网',
  `company_tel` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司电话',
  `company_fax` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司传真',
  `company_email` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司邮箱',
  `company_type` TINYINT NOT NULL DEFAULT 0 COMMENT '公司类型（0:未知,1:中间商2:终端）',
  `owner_uid` INT NOT NULL DEFAULT 0 COMMENT '所属用户ID（未分配为0）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户表';


DROP TABLE IF EXISTS `customer_invoice`;
CREATE TABLE `customer_invoice` (
  `cid` INT NOT NULL,
  `company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `company_tax_id` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '单位税号',
  `company_address` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '单位地址',
  `company_tel` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司电话',
  `company_bank_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '开户银行',
  `company_bank_account` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '银行账号',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户开票资料';


DROP TABLE IF EXISTS `customer_contact`;
CREATE TABLE `customer_contact` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `cid` INT NOT NULL DEFAULT 0 COMMENT '客户ID',
  `name` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '姓名',
  `salutation` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '称呼',
  `mobile` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '手机',
  `tel` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '座机（包含分机）',
  `fax` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '传真（包含分机）',
  `email` VARCHAR(60) NOT NULL DEFAULT '' COMMENT '邮箱',
  `department` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '部门（采购、技术、销售、仓库、经理）',
  `address` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '地址（办公地点、仓库地址）',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '备注',
  `status_default` TINYINT NOT NULL DEFAULT 0 COMMENT '默认状态（0:未默认,1:已默认）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户联系方式';


DROP TABLE IF EXISTS `supplier`;
CREATE TABLE `supplier` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `company_address` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司地址',
  `company_site` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司官网',
  `company_tel` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司电话',
  `company_fax` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司传真',
  `company_email` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司邮箱',
  `company_type` TINYINT NOT NULL DEFAULT 0 COMMENT '公司类型（0:未知,1:中间商2:终端）',
  `owner_uid` INT NOT NULL DEFAULT 0 COMMENT '所属用户ID（未分配为0）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='供应厂商';


DROP TABLE IF EXISTS `supplier_invoice`;
CREATE TABLE `supplier_invoice` (
  `cid` INT NOT NULL,
  `company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `company_tax_id` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '单位税号',
  `company_address` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '单位地址',
  `company_tel` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司电话',
  `company_bank_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '开户银行',
  `company_bank_account` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '银行账号',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='供应厂商开票资料';


DROP TABLE IF EXISTS `supplier_contact`;
CREATE TABLE `supplier_contact` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `cid` INT NOT NULL DEFAULT 0 COMMENT '客户ID',
  `name` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '姓名',
  `salutation` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '称呼',
  `mobile` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '手机',
  `tel` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '座机（包含分机）',
  `fax` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '传真（包含分机）',
  `email` VARCHAR(60) NOT NULL DEFAULT '' COMMENT '邮箱',
  `department` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '部门（采购、技术、销售、仓库、经理）',
  `address` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '地址（办公地点、仓库地址）',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '备注',
  `status_default` TINYINT NOT NULL DEFAULT 0 COMMENT '默认状态（0:未默认,1:已默认）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='供应厂商联系方式';


DROP TABLE IF EXISTS `production`;
CREATE TABLE `production` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category_id` INT NOT NULL DEFAULT 0 COMMENT '类别编号',
  `production_brand` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品品牌',
  `production_model` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品型号',
  `production_sku` VARCHAR(16) NOT NULL DEFAULT 'Pcs' COMMENT '单位（Pcs:个,Pair:对,Set:组）',
  `production_class` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品类型',
  `ind` DECIMAL(4, 0) NOT NULL DEFAULT '0' COMMENT '内径（mm）',
  `oud` DECIMAL(4, 0) NOT NULL DEFAULT '0' COMMENT '外径（mm）',
  `wid` DECIMAL(4, 0) NOT NULL DEFAULT '0' COMMENT '宽度（mm）',
  `speed_g` DECIMAL(6, 0) NOT NULL DEFAULT '0' COMMENT '油脂转速（r/min）',
  `speed_o` DECIMAL(6, 0) NOT NULL DEFAULT '0' COMMENT '油气转速（r/min）',
  `weight` DECIMAL(8, 3) NOT NULL DEFAULT '0.000' COMMENT '重量（kg）',
  `serie` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品系列',
  `accuracy` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '精度等级',
  `preload` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '预紧等级',
  `seal` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '密封形式',
  `angle` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '角度',
  `r_size` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '滚动体大小（大、中、小）',
  `r_matel` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '滚动体材料（轴承钢、陶瓷）',
  `assembly_no` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '配组列数',
  `assembly_type` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '配组形式',
  `note` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品备注',
  `tag` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '产品标签（精密轴承 主轴轴承 高速主轴 高速电机）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`production_model`),
  UNIQUE (`production_brand`, `production_model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='产品明细';


DROP TABLE IF EXISTS `catalogue`;
CREATE TABLE `catalogue` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `production_brand` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品品牌',
  `production_model` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品型号',
  `production_label` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品称号',
  `production_brand_old` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '历史品牌',
  `production_model_old` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '历史型号',
  `production_class` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品类型',
  `ind` DECIMAL(4, 0) NOT NULL DEFAULT '0' COMMENT '内径（mm）',
  `oud` DECIMAL(4, 0) NOT NULL DEFAULT '0' COMMENT '外径（mm）',
  `wid` DECIMAL(4, 0) NOT NULL DEFAULT '0' COMMENT '宽度（mm）',
  `speed_g` DECIMAL(6, 0) NOT NULL DEFAULT '0' COMMENT '油脂转速（r/min）',
  `speed_o` DECIMAL(6, 0) NOT NULL DEFAULT '0' COMMENT '油气转速（r/min）',
  `weight` DECIMAL(8, 3) NOT NULL DEFAULT '0.000' COMMENT '重量（kg）',
  `serie` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品系列',
  `accuracy` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '精度等级',
  `preload` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '预紧等级',
  `seal` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '密封形式',
  `angle` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '角度',
  `r_size` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '滚动体大小（大、中、小）',
  `r_matel` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '滚动体材料（轴承钢、陶瓷）',
  `assembly_no` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '配组列数',
  `assembly_type` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '配组形式',
  `note` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品备注',
  `tag` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '产品标签（精密轴承 主轴轴承 高速主轴 高速电机）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`production_model`),
  KEY (`production_model_old`),
  UNIQUE (`production_brand`, `production_model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='产品型录';


DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '类别名称',
  `main_id` INT NOT NULL DEFAULT 0 COMMENT '顶级编号',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`main_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='产品类别';


DROP TABLE IF EXISTS `warehouse`;
CREATE TABLE `warehouse` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '仓库名称',
  `address` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '仓库地址',
  `linkman` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '联系人',
  `tel` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '座机（包含分机）',
  `fax` VARCHAR(20) NOT NULL DEFAULT '' COMMENT '传真（包含分机）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='仓库';


DROP TABLE IF EXISTS `rack`;
CREATE TABLE `rack` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `warehouse_id` INT NOT NULL COMMENT '仓库编号',
  `name` VARCHAR(16) NOT NULL DEFAULT '' COMMENT '货架名称（区-排列层, 例如:A-010201）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='货架';


DROP TABLE IF EXISTS `inventory`;
CREATE TABLE `inventory` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `production_id` INT NOT NULL COMMENT '产品编号',
  `warehouse_id` INT NOT NULL COMMENT '仓库编号',
  `rack_id` INT NOT NULL COMMENT '货架编号',
  `stock_qty` INT NOT NULL COMMENT '库存数量',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '库存备注',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`production_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='库存明细';


DROP TABLE IF EXISTS `quotation`;
CREATE TABLE `quotation` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uid` INT NOT NULL DEFAULT 0 COMMENT '用户ID',
  `customer_cid` INT NOT NULL DEFAULT 0 COMMENT '公司ID',
  `customer_contact_id` INT NOT NULL DEFAULT 0 COMMENT '联系方式ID',
  `amount_production` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '产品金额',
  `amount_shipping` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '运费金额',
  `amount_adjustment` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '调整金额',
  `amount_quotation` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '报价总额',
  `delivery_way` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '发货方式',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '报价备注',
  `type_tax` TINYINT NOT NULL DEFAULT 1 COMMENT '含税类型（0:不含税,1:已含税）',
  `audit_uid` INT NOT NULL DEFAULT 0 COMMENT '审核用户ID',
  `status_audit` TINYINT NOT NULL DEFAULT 0 COMMENT '审核状态（0:待审核,1:审核通过,2:审核失败）',
  `status_order` TINYINT NOT NULL DEFAULT 0 COMMENT '订单状态（0:待下单,1:下单成功,2:下单失败）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `expiry_date` DATE NOT NULL COMMENT '有效日期（中间商:可设置默认7天;终端用户:可根据情况延长）',
  `audit_time` TIMESTAMP NULL COMMENT '审核时间（通过、失败）',
  `order_time` TIMESTAMP NULL COMMENT '下单时间（成功、失败）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`uid`),
  KEY (`customer_cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='报价总表';


DROP TABLE IF EXISTS `quotation_items`;
CREATE TABLE `quotation_items` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `quotation_id` INT NOT NULL COMMENT '报价总表ID',
  `uid` INT NOT NULL COMMENT '报价人ID',
  `customer_cid` INT NOT NULL DEFAULT 0 COMMENT '公司ID',
  `customer_company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `enquiry_production_model` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '客户询价-产品型号',
  `enquiry_quantity` INT NOT NULL DEFAULT 0 COMMENT '客户询价-产品数量',
  `production_id` INT NOT NULL COMMENT '产品ID',
  `production_brand` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品品牌',
  `production_model` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品型号',
  `production_sku` VARCHAR(16) NOT NULL DEFAULT 'Pcs' COMMENT '单位（Pcs:个,Pair:对,Set:组）',
  `delivery_time` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '货期',
  `quantity` INT NOT NULL DEFAULT 0 COMMENT '报价数量',
  `unit_price` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '单价',
  `note` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品备注',
  `type_tax` TINYINT NOT NULL DEFAULT 1 COMMENT '含税类型（0:不含税,1:已含税）',
  `status_ordered` TINYINT NOT NULL DEFAULT 0 COMMENT '下单状态（0:未下单,1:已下单）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`quotation_id`),
  KEY (`uid`),
  KEY (`customer_cid`),
  KEY (`production_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='报价明细';


DROP TABLE IF EXISTS `enquiry`;
CREATE TABLE `enquiry` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uid` INT NOT NULL DEFAULT 0 COMMENT '用户ID',
  `supplier_cid` INT NOT NULL DEFAULT 0 COMMENT '公司ID',
  `supplier_contact_id` INT NOT NULL DEFAULT 0 COMMENT '联系方式ID',
  `amount_production` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '产品金额',
  `amount_shipping` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '运费金额',
  `amount_adjustment` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '调整金额',
  `amount_enquiry` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '询价总额',
  `delivery_way` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '发货方式',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '询价备注',
  `type_tax` TINYINT NOT NULL DEFAULT 1 COMMENT '含税类型（0:不含税,1:已含税）',
  `audit_uid` INT NOT NULL DEFAULT 0 COMMENT '审核用户ID',
  `status_audit` TINYINT NOT NULL DEFAULT 0 COMMENT '审核状态（0:待审核,1:审核通过,2:审核失败）',
  `status_order` TINYINT NOT NULL DEFAULT 0 COMMENT '订单状态（0:待下单,1:下单成功,2:下单失败）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `expiry_date` DATE NOT NULL COMMENT '有效日期（中间商:可设置默认7天;终端用户:可根据情况延长）',
  `audit_time` TIMESTAMP NULL COMMENT '审核时间（通过、失败）',
  `order_time` TIMESTAMP NULL COMMENT '下单时间（成功、失败）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`uid`),
  KEY (`supplier_cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='询价总表';


DROP TABLE IF EXISTS `enquiry_items`;
CREATE TABLE `enquiry_items` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `enquiry_id` INT NOT NULL COMMENT '询价总表ID',
  `uid` INT NOT NULL COMMENT '询价人ID',
  `supplier_cid` INT NOT NULL DEFAULT 0 COMMENT '公司ID',
  `supplier_company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `enquiry_production_model` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '公司询价-产品型号',
  `enquiry_quantity` INT NOT NULL DEFAULT 0 COMMENT '公司询价-产品数量',
  `production_id` INT NOT NULL COMMENT '产品ID',
  `production_brand` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品品牌',
  `production_model` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品型号',
  `production_sku` VARCHAR(16) NOT NULL DEFAULT 'Pcs' COMMENT '单位（Pcs:个,Pair:对,Set:组）',
  `delivery_time` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '货期',
  `quantity` INT NOT NULL DEFAULT 0 COMMENT '报价数量',
  `unit_price` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '单价',
  `note` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品备注',
  `type_tax` TINYINT NOT NULL DEFAULT 1 COMMENT '含税类型（0:不含税,1:已含税）',
  `status_ordered` TINYINT NOT NULL DEFAULT 0 COMMENT '下单状态（0:未下单,1:已下单）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`enquiry_id`),
  KEY (`uid`),
  KEY (`supplier_cid`),
  KEY (`production_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='询价明细';


DROP TABLE IF EXISTS `sales_order`;
CREATE TABLE `sales_order` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uid` INT NOT NULL DEFAULT 0 COMMENT '用户ID',
  `customer_cid` INT NOT NULL DEFAULT 0 COMMENT '公司ID',
  `customer_contact_id` INT NOT NULL DEFAULT 0 COMMENT '联系方式ID',
  `amount_production` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '产品金额',
  `amount_shipping` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '运费金额',
  `amount_adjustment` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '调整金额',
  `amount_order` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '订单总额',
  `delivery_way` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '发货方式',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '订单备注',
  `type_tax` TINYINT NOT NULL DEFAULT 1 COMMENT '含税类型（0:不含税,1:已含税）',
  `audit_uid` INT NOT NULL DEFAULT 0 COMMENT '审核用户ID',
  `status_audit` TINYINT NOT NULL DEFAULT 0 COMMENT '审核状态（0:待审核,1:审核通过,2:审核失败）',
  `status_effect` TINYINT NOT NULL DEFAULT 0 COMMENT '生效状态（0:待生效,1:已生效,2:未生效）',
  `status_completion` TINYINT NOT NULL DEFAULT 0 COMMENT '完成状态（0:待完成,1:已完成,2:已中止）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `audit_time` TIMESTAMP NULL COMMENT '审核时间（通过、失败）',
  `effect_time` TIMESTAMP NULL COMMENT '生效时间（通过、失败）',
  `completion_time` TIMESTAMP NULL COMMENT '完成时间（完成、中止）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`uid`),
  KEY (`customer_cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='销售订单';


DROP TABLE IF EXISTS `sales_order_items`;
CREATE TABLE `sales_order_items` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `sales_order_id` INT NOT NULL COMMENT '销售订单ID',
  `uid` INT NOT NULL DEFAULT 0 COMMENT '用户ID',
  `customer_cid` INT NOT NULL DEFAULT 0 COMMENT '公司ID',
  `customer_company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `custom_production_brand` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '定制品牌（订单优先显示）',
  `custom_production_model` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '定制型号（订单优先显示）',
  `production_id` INT NOT NULL COMMENT '产品ID',
  `production_brand` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品品牌',
  `production_model` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品型号',
  `production_sku` VARCHAR(16) NOT NULL DEFAULT 'Pcs' COMMENT '单位（Pcs:个,Pair:对,Set:组）',
  `delivery_time` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '货期',
  `quantity` INT NOT NULL DEFAULT 0 COMMENT '数量',
  `unit_price` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '单价',
  `note` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品备注',
  `type_tax` TINYINT NOT NULL DEFAULT 1 COMMENT '含税类型（0:不含税,1:已含税）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`sales_order_id`),
  KEY (`uid`),
  KEY (`customer_cid`),
  KEY (`production_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='销售订单明细';


DROP TABLE IF EXISTS `buyer_order`;
CREATE TABLE `buyer_order` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uid` INT NOT NULL DEFAULT 0 COMMENT '用户ID',
  `supplier_cid` INT NOT NULL DEFAULT 0 COMMENT '公司ID',
  `supplier_contact_id` INT NOT NULL DEFAULT 0 COMMENT '联系方式ID',
  `amount_production` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '产品金额',
  `amount_shipping` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '运费金额',
  `amount_adjustment` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '调整金额',
  `amount_order` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '订单总额',
  `delivery_way` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '发货方式',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '订单备注',
  `type_tax` TINYINT NOT NULL DEFAULT 1 COMMENT '含税类型（0:不含税,1:已含税）',
  `audit_uid` INT NOT NULL DEFAULT 0 COMMENT '审核用户ID',
  `status_audit` TINYINT NOT NULL DEFAULT 0 COMMENT '审核状态（0:待审核,1:审核通过,2:审核失败）',
  `status_effect` TINYINT NOT NULL DEFAULT 0 COMMENT '生效状态（0:待生效,1:已生效,2:未生效）',
  `status_completion` TINYINT NOT NULL DEFAULT 0 COMMENT '完成状态（0:待完成,1:已完成,2:已中止）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `audit_time` TIMESTAMP NULL COMMENT '审核时间（通过、失败）',
  `effect_time` TIMESTAMP NULL COMMENT '生效时间（通过、失败）',
  `completion_time` TIMESTAMP NULL COMMENT '完成时间（完成、中止）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`uid`),
  KEY (`supplier_cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='采购订单';


DROP TABLE IF EXISTS `buyer_order_items`;
CREATE TABLE `buyer_order_items` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `buyer_order_id` INT NOT NULL COMMENT '采购订单ID',
  `uid` INT NOT NULL DEFAULT 0 COMMENT '用户ID',
  `supplier_cid` INT NOT NULL DEFAULT 0 COMMENT '公司ID',
  `supplier_company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `production_id` INT NOT NULL COMMENT '产品ID',
  `production_brand` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品品牌',
  `production_model` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品型号',
  `production_sku` VARCHAR(16) NOT NULL DEFAULT 'Pcs' COMMENT '单位（Pcs:个,Pair:对,Set:组）',
  `delivery_time` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '货期',
  `quantity` INT NOT NULL DEFAULT 0 COMMENT '数量',
  `unit_price` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '单价',
  `note` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品备注',
  `type_tax` TINYINT NOT NULL DEFAULT 1 COMMENT '含税类型（0:不含税,1:已含税）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`buyer_order_id`),
  KEY (`uid`),
  KEY (`supplier_cid`),
  KEY (`production_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='采购订单明细';


DROP TABLE IF EXISTS `delivery`;
CREATE TABLE `delivery` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uid` INT NOT NULL DEFAULT 0 COMMENT '用户ID',
  `sales_order_id` INT DEFAULT 0 COMMENT '销售订单ID',
  `customer_cid` INT NOT NULL DEFAULT 0 COMMENT '公司ID',
  `customer_company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `customer_contact_id` INT NOT NULL DEFAULT 0 COMMENT '联系方式ID',
  `type_delivery` TINYINT NOT NULL DEFAULT 0 COMMENT '出货类型（0:正常销售,1:赠送样品,2:盘亏,3:拆卸,4:损耗报废）',
  `amount_production` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '产品金额',
  `amount_shipping` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '运费金额',
  `amount_adjustment` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '调整金额',
  `amount_delivery` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '出货总额',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '清单备注',
  `type_tax` TINYINT NOT NULL DEFAULT 1 COMMENT '含税类型（0:不含税,1:已含税）',
  `audit_uid` INT NOT NULL DEFAULT 0 COMMENT '审核用户ID',
  `status_audit` TINYINT NOT NULL DEFAULT 0 COMMENT '审核状态（0:待审核,1:审核通过,2:审核失败）',
  `status_confirm` TINYINT NOT NULL DEFAULT 0 COMMENT '确认状态（0:待确认,1:确认成功,2:确认失败）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `audit_time` TIMESTAMP NULL COMMENT '审核时间（通过、失败）',
  `confirm_time` TIMESTAMP NULL COMMENT '确认时间（成功、失败）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`uid`),
  KEY (`sales_order_id`),
  KEY (`customer_cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='出货清单';


DROP TABLE IF EXISTS `delivery_items`;
CREATE TABLE `delivery_items` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `delivery_id` INT NOT NULL COMMENT '出货清单ID',
  `uid` INT NOT NULL DEFAULT 0 COMMENT '用户ID',
  `sales_order_id` INT DEFAULT 0 COMMENT '销售订单ID',
  `customer_cid` INT NOT NULL DEFAULT 0 COMMENT '公司ID',
  `customer_company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `custom_production_brand` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '定制品牌（清单优先显示）',
  `custom_production_model` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '定制型号（清单优先显示）',
  `production_id` INT NOT NULL COMMENT '产品ID',
  `production_brand` VARCHAR(16) NOT NULL DEFAULT '' COMMENT '产品品牌',
  `production_model` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品型号',
  `production_sku` VARCHAR(16) NOT NULL DEFAULT 'Pcs' COMMENT '单位（Pcs:个,Pair:对,Set:组）',
  `note` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品备注',
  `type_tax` TINYINT NOT NULL DEFAULT 1 COMMENT '含税类型（0:不含税,1:已含税）',
  `quantity` INT NOT NULL DEFAULT 0 COMMENT '数量',
  `unit_price` DECIMAL(8, 2) NOT NULL DEFAULT '0.00' COMMENT '单价',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`delivery_id`),
  KEY (`uid`),
  KEY (`sales_order_id`),
  KEY (`customer_cid`),
  KEY (`production_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='出货清单明细';


DROP TABLE IF EXISTS `purchase`;
CREATE TABLE `purchase` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uid` INT NOT NULL DEFAULT 0 COMMENT '用户ID',
  `buyer_order_id` INT DEFAULT 0 COMMENT '采购订单ID',
  `supplier_cid` INT NOT NULL DEFAULT 0 COMMENT '公司ID',
  `supplier_company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `supplier_contact_id` INT NOT NULL DEFAULT 0 COMMENT '联系方式ID',
  `type_purchase` TINYINT NOT NULL DEFAULT 0 COMMENT '进货类型（0:正常采购,1:获赠样品,2:盘盈,3:组装）',
  `amount_production` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '产品金额',
  `amount_shipping` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '运费金额',
  `amount_adjustment` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '调整金额',
  `amount_delivery` DECIMAL(10, 2) NOT NULL DEFAULT '0.00' COMMENT '出货总额',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '清单备注',
  `type_tax` TINYINT NOT NULL DEFAULT 1 COMMENT '含税类型（0:不含税,1:已含税）',
  `audit_uid` INT NOT NULL DEFAULT 0 COMMENT '审核用户ID',
  `status_audit` TINYINT NOT NULL DEFAULT 0 COMMENT '审核状态（0:待审核,1:审核通过,2:审核失败）',
  `status_confirm` TINYINT NOT NULL DEFAULT 0 COMMENT '确认状态（0:待确认,1:确认成功,2:确认失败）',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `audit_time` TIMESTAMP NULL COMMENT '审核时间（通过、失败）',
  `confirm_time` TIMESTAMP NULL COMMENT '确认时间（成功、失败）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`uid`),
  KEY (`buyer_order_id`),
  KEY (`supplier_cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='进货清单';


DROP TABLE IF EXISTS `purchase_items`;
CREATE TABLE `purchase_items` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `purchase_id` INT NOT NULL COMMENT '进货清单ID',
  `uid` INT NOT NULL DEFAULT 0 COMMENT '用户ID',
  `buyer_order_id` INT DEFAULT 0 COMMENT '采购订单ID',
  `supplier_cid` INT NOT NULL DEFAULT 0 COMMENT '公司ID',
  `supplier_company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '公司名称',
  `production_id` INT NOT NULL COMMENT '产品ID',
  `production_brand` VARCHAR(16) NOT NULL DEFAULT '' COMMENT '产品品牌',
  `production_model` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品型号',
  `production_sku` VARCHAR(16) NOT NULL DEFAULT 'Pcs' COMMENT '单位（Pcs:个,Pair:对,Set:组）',
  `note` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品备注',
  `type_tax` TINYINT NOT NULL DEFAULT 1 COMMENT '含税类型（0:不含税,1:已含税）',
  `quantity` INT NOT NULL DEFAULT 0 COMMENT '数量',
  `unit_price` DECIMAL(8, 2) NOT NULL DEFAULT '0.00' COMMENT '单价',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`purchase_id`),
  KEY (`uid`),
  KEY (`buyer_order_id`),
  KEY (`supplier_cid`),
  KEY (`production_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='进货清单明细';


DROP TABLE IF EXISTS `production_sensitive`;
CREATE TABLE `production_sensitive` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `customer_cid` INT NOT NULL DEFAULT 0 COMMENT '敏感型号-客户公司ID',
  `customer_company_name` VARCHAR(100) NOT NULL DEFAULT '' COMMENT '敏感型号-客户公司名称',
  `production_id` INT NOT NULL COMMENT '产品ID',
  `production_brand` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '产品品牌',
  `production_model` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '产品型号',
  `production_sku` VARCHAR(16) NOT NULL DEFAULT 'Pcs' COMMENT '单位（Pcs:个,Pair:对,Set:组）',
  `note` VARCHAR(256) NOT NULL DEFAULT '' COMMENT '型号备注',
  `status_delete` TINYINT NOT NULL DEFAULT 0 COMMENT '删除状态（0:未删除,1:已删除）',
  `delete_time` TIMESTAMP NULL COMMENT '删除时间',
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY (`customer_cid`),
  KEY (`production_id`),
  UNIQUE (`customer_cid`, `production_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='敏感型号';


# catalog_contrast



# 客户询价
#
#     日期 客户名称 询价原型号 询价数量
#
# 公司成本
#
#     SKF型号 SKF最新成本 涨跌趋势
#
# 公司库存
#
#     现存数量 在途数量
#
# 公司报价
#
#     报价时间 报价金额 是否含税
#
# 历史报价
#
#     历史报价-时间 历史报价-金额 历史报价-是否含税
#
# 采购询价
#
#     日系
#         型号 市场价-最高 市场价-最低 报价单位 报价时间
#
#     欧系
#         型号 市场价-最高 市场价-最低 报价单位 报价时间
#
#     SKF同行
#         型号 市场价-最高 市场价-最低 报价单位 报价时间

