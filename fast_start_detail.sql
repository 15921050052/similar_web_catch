/*
Navicat MySQL Data Transfer

Source Server         : eping
Source Server Version : 50620
Source Host           : 117.29.166.222:4360
Source Database       : trivest_spider

Target Server Type    : MYSQL
Target Server Version : 50620
File Encoding         : 65001

Date: 2017-09-06 16:59:19
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for xueqiu_detail
-- ----------------------------
DROP TABLE IF EXISTS `xueqiu_detail`;
CREATE TABLE `xueqiu_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content_txt` longtext CHARACTER SET utf8mb4,
  `title` varchar(255) DEFAULT NULL,
  `source_url` varchar(255) DEFAULT NULL,
  `post_date` datetime DEFAULT NULL,
  `sub_channel` varchar(255) DEFAULT NULL,
  `post_user` varchar(255) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `styles` longtext,
  `content_html` longtext CHARACTER SET utf8mb4,
  `hash_code` varchar(255) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `info_type` int(1) DEFAULT NULL,
  `src_source_id` int(11) DEFAULT NULL,
  `src_account_id` int(11) DEFAULT NULL,
  `src_channel` varchar(255) DEFAULT NULL,
  `src_ref` varchar(255) DEFAULT NULL,
  `wx_account` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3823 DEFAULT CHARSET=utf8;
