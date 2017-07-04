
CREATE TABLE `tujia`(
`id` INT(11) UNSIGNED auto_increment,
`city_en_name` VARCHAR(128) not NULL COMMENT '城市英文名',
`city_cn_name` VARCHAR(128) not NULL COMMENT '城市中文名',
`query_start_time` date NOT NULL COMMENT '查询起始时间',
`query_end_time` date NOT NULL COMMENT '查询结束时间',
`house_serial_number` VARCHAR(64) NOT NULL COMMENT '房屋编号',
`house_title` VARCHAR(128) NOT NULL COMMENT '房屋名称',
`merchant_manage` VARCHAR(32) NOT NULL COMMENT '是否商户经营,T:是,F:否',
`best_choice` VARCHAR(32) NOT NULL COMMENT '是否优选,T:是,F:否',
`real_shot` VARCHAR(32) NOT NULL COMMENT '是否实拍,T:是,F:否',
`score` decimal(5,2) UNSIGNED DEFAULT NULL COMMENT '评分',
`score_times` INT(8) UNSIGNED DEFAULT NULL COMMENT '评分次数',
`location` VARCHAR(255) DEFAULT NULL COMMENT '地理位置',
`price` DECIMAL(11,2) DEFAULT NULL COMMENT '价格',
`estate_type` VARCHAR(128) DEFAULT NULL COMMENT '物业类型',
`house_square` VARCHAR(128) DEFAULT NULL COMMENT '房源户型',
`bed_count` INT(3) UNSIGNED DEFAULT NULL COMMENT '床铺数',
`prefered_guests_count` INT(3) UNSIGNED DEFAULT NULL COMMENT '宜住人数',
`can_cooking` VARCHAR(32) NOT NULL COMMENT '允许做饭,T:是,F:否',
`have_wifi` VARCHAR(32) NOT NULL COMMENT '支持wifi,T:是,F:否',
`allow_pets` VARCHAR(32) NOT NULL COMMENT '携带宠物,T:是,F:否',
`allow_smoke` VARCHAR(32) NOT NULL COMMENT '允许吸烟,T:是,F:否',
`allow_party` VARCHAR(32) NOT NULL COMMENT '允许派对,T:是,F:否',
`checkin_time` VARCHAR(32) DEFAULT NULL COMMENT '入住时间',
`checkout_time` VARCHAR(32) DEFAULT NULL COMMENT '退房时间',
`receive_foreign_guest` VARCHAR(32) NOT NULL COMMENT '接待外宾,T:是,F:否',
`facility_list` VARCHAR(516) DEFAULT NULL COMMENT '设施项',
`service_list` VARCHAR(516) DEFAULT NULL COMMENT '服务项',
`house_desc` text DEFAULT NULL COMMENT '房源描述',
`link`  VARCHAR(255) DEFAULT NULL COMMENT '详情链接',
`created_at` datetime DEFAULT CURRENT_TIMESTAMP,
`updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY(`id`),
UNIQUE KEY `city_en_name`(`city_en_name`, `query_start_time`, `query_end_time`, `house_serial_number`),
KEY city_cn_name(`city_cn_name`),
KEY merchant_manage(`merchant_manage`, `best_choice`, `real_shot`),
KEY score(`score`, `score_times`),
KEY price(`price`),
KEY estate_type(`estate_type`),
KEY prefered_guests_count(`prefered_guests_count`),
key `option`(`can_cooking`, `have_wifi`, `allow_pets`, `allow_smoke`, `allow_party`, `receive_foreign_guest`),
KEY `checkin_time`(`checkin_time`),
KEY checkout_time(`checkout_time`)
)ENGINE=INNODB DEFAULT CHARSET=utf8




CREATE TABLE `airbnb`(
`id` INT(11) UNSIGNED auto_increment,
`city_en_name` VARCHAR(128) not NULL COMMENT '城市英文名',
`city_cn_name` VARCHAR(128) not NULL COMMENT '城市中文名',
`query_start_time` date NOT NULL COMMENT '查询起始时间',
`query_end_time` date NOT NULL COMMENT '查询结束时间',
`primary_host_id` VARCHAR(64) NOT NULL COMMENT '房东id',
`house_title` VARCHAR(128) NOT NULL COMMENT '房屋名称',
`listing_id` VARCHAR(128) NOT NULL COMMENT '房源id',
`price` DECIMAL(11,2) DEFAULT NULL COMMENT '价格',
`deposit_fee` DECIMAL(11,2) DEFAULT NULL COMMENT '押金',
`clean_fee` DECIMAL(11,2) DEFAULT NULL COMMENT '清洁费',
`airbnb_guest_fee` DECIMAL(11,2) DEFAULT NULL COMMENT '服务费',
`extra_guest_fee` VARCHAR(64) DEFAULT NULL COMMENT '额外住客费用',
`weekend_price` DECIMAL(11,2) DEFAULT NULL COMMENT '周末价格',
`monthly_discount` DECIMAL(5,2) DEFAULT NULL COMMENT '月折扣率',
`weekly_discount` DECIMAL(5,2) DEFAULT NULL COMMENT '周折扣率',
`reserve_situation` VARCHAR(255) NOT NULL COMMENT '未来预定情况',
`house_type` VARCHAR(128) NOT NULL COMMENT '房源类型',
`reviews_count` INT(8) UNSIGNED DEFAULT NULL COMMENT '评价数量',
`score` decimal(5,2) UNSIGNED DEFAULT NULL COMMENT '评分',
`wishlist_saved_count` INT(8) UNSIGNED DEFAULT NULL COMMENT '保存次数',
`bedrooms` INT(5) UNSIGNED DEFAULT NULL COMMENT '房间数',
`bathrooms` INT(5) UNSIGNED DEFAULT NULL COMMENT '卫生间数',
`beds` INT(6) UNSIGNED DEFAULT NULL COMMENT '床铺数',
`person_capacity` INT(6) UNSIGNED DEFAULT NULL COMMENT '可住人数',
`checkin_time` VARCHAR(32) DEFAULT NULL COMMENT '入住时间',
`checkout_time` VARCHAR(32) DEFAULT NULL COMMENT '退房时间',
`self_checkin` VARCHAR(64) DEFAULT NULL COMMENT '自助入住',
`is_superhost` VARCHAR(32) NOT NULL COMMENT '是否超赞房东,T:是,F:否',
`instant_bookable` VARCHAR(32) NOT NULL COMMENT '是否闪订,T:是,F:否',
`allows_pets` VARCHAR(32) NOT NULL COMMENT '携带宠物,T:是,F:否',
`allows_children` VARCHAR(32) NOT NULL COMMENT '适合儿童,T:是,F:否',
`allows_infants` VARCHAR(32) NOT NULL COMMENT '适合婴儿,T:是,F:否',
`allows_smoking` VARCHAR(32) NOT NULL COMMENT '允许吸烟,T:是,F:否',
`allows_events` VARCHAR(32) NOT NULL COMMENT '允许派对,T:是,F:否',
`minimum_nights` INT(6) UNSIGNED DEFAULT NULL COMMENT '最晚起订天数',
`cancellation_policy` VARCHAR(64) DEFAULT NULL COMMENT '取消预订政策',
`facility_list` VARCHAR(516) DEFAULT NULL COMMENT '硬件配置清单',
`house_desc` text DEFAULT NULL COMMENT '房源描述',
`location` VARCHAR(255) DEFAULT NULL COMMENT '地理位置',
`created_at` datetime DEFAULT CURRENT_TIMESTAMP,
`updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY(`id`),
UNIQUE KEY `city_en_name`(`city_en_name`, `query_start_time`, `query_end_time`, `listing_id`),
KEY city_cn_name(`city_cn_name`),
KEY score(`score`, `reviews_count`),
KEY price(`price`),
KEY house_type(`house_type`),
key `option`(`is_superhost`, `instant_bookable`, `allows_pets`, `allows_children`, `allows_smoking`, `allows_events`),
KEY `checkin_time`(`checkin_time`),
KEY checkout_time(`checkout_time`)
)ENGINE=INNODB DEFAULT CHARSET=utf8