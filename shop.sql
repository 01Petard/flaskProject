/*
 Navicat Premium Data Transfer

 Source Server         : 华为云mysql
 Source Server Type    : MySQL
 Source Server Version : 80403
 Source Host           : 1.94.147.176:3306
 Source Schema         : shop

 Target Server Type    : MySQL
 Target Server Version : 80403
 File Encoding         : 65001

 Date: 09/11/2024 21:59:13
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tbl_order
-- ----------------------------
DROP TABLE IF EXISTS `tbl_order`;
CREATE TABLE `tbl_order`  (
  `order_id` bigint(0) NOT NULL AUTO_INCREMENT COMMENT '一个订单的id',
  `item_id` int(0) NOT NULL COMMENT '订单中每个商品的详情id',
  `create_time` datetime(0) NOT NULL,
  `modify_time` datetime(0) NOT NULL,
  `create_id` bigint(0) NOT NULL,
  `modify_id` bigint(0) NOT NULL,
  `order_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '配送地址',
  PRIMARY KEY (`order_id`) USING BTREE,
  UNIQUE INDEX `order_id`(`order_id`) USING BTREE,
  INDEX `tbl_order_index_item_id`(`item_id`) USING BTREE,
  INDEX `tbl_order_index_create_time`(`create_time`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '商品表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_order
-- ----------------------------

-- ----------------------------
-- Table structure for tbl_order_item
-- ----------------------------
DROP TABLE IF EXISTS `tbl_order_item`;
CREATE TABLE `tbl_order_item`  (
  `item_id` int(0) NOT NULL AUTO_INCREMENT,
  `item_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '商品名称',
  `item_count` int(0) NOT NULL COMMENT '商品数量',
  `item_price` int(0) NOT NULL COMMENT '商品价格',
  `item_amount` int(0) NOT NULL COMMENT '商品总结',
  `item_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '商品的配送地址',
  `create_time` datetime(0) NOT NULL,
  `modify_time` datetime(0) NOT NULL,
  `create_id` bigint(0) NOT NULL,
  `modify_id` bigint(0) NOT NULL,
  PRIMARY KEY (`item_id`) USING BTREE,
  UNIQUE INDEX `item_id`(`item_id`) USING BTREE,
  INDEX `tbl_order_item_index_create_time`(`create_time`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '商品详情表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_order_item
-- ----------------------------

-- ----------------------------
-- Table structure for tbl_user
-- ----------------------------
DROP TABLE IF EXISTS `tbl_user`;
CREATE TABLE `tbl_user`  (
  `user_id` bigint(0) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_age` int(0) NOT NULL,
  `user_gender` smallint(0) NOT NULL COMMENT '0：女，1：男',
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `tbl_user_index_user_name`(`user_name`) USING BTREE,
  INDEX `tbl_user_index_user_age`(`user_age`) USING BTREE,
  INDEX `tbl_user_index_user_gender`(`user_gender`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tbl_user
-- ----------------------------
INSERT INTO `tbl_user` VALUES (2, 'hzx11', 19, 0);
INSERT INTO `tbl_user` VALUES (3, 'hzx22', 19, 1);
INSERT INTO `tbl_user` VALUES (4, 'hzx222', 20, 0);
INSERT INTO `tbl_user` VALUES (5, 'hahaha', 21, 1);
INSERT INTO `tbl_user` VALUES (6, 'wadw', 22, 0);
INSERT INTO `tbl_user` VALUES (7, 'hhhh', 23, 1);

SET FOREIGN_KEY_CHECKS = 1;
