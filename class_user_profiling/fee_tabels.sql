DROP TABLE IF EXISTS `dpy_fee_type`;
CREATE TABLE `dpy_fee_type` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `desc` varchar(250) NOT NULL,
  `status` tinyint(4) unsigned NOT NULL,
  `added_by` int(11) unsigned NOT NULL,
  `added_on` datetime NOT NULL,
  `updated_by` int(11) unsigned NOT NULL,
  `updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `dpy_institute_class_fee`;
CREATE TABLE `dpy_institute_class_fee` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `fee_type_id` int(11) unsigned NOT NULL,
  `institute_class_id` int(11) unsigned NOT NULL,
  `amount` tinyint(4) unsigned NOT NULL,
  `cycle` tinyint(4) unsigned NOT NULL,
  `display_name` varchar(250) NOT NULL,
  `bifercations` longtext NOT NULL,
  `status` tinyint(4) unsigned NOT NULL,
  `added_by` int(11) unsigned NOT NULL,
  `added_on` datetime NOT NULL,
  `updated_by` int(11) unsigned NOT NULL,
  `updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `institute_class_id` (`institute_class_id`),
  KEY `fee_type_id` (`fee_type_id`),
  CONSTRAINT `dpy_institute_class_fee_ibfk_1` FOREIGN KEY (`fee_type_id`) REFERENCES `dpy_fee_type` (`id`)
  CONSTRAINT `dpy_institute_class_fee_ibfk_2` FOREIGN KEY (`institute_class_id`) REFERENCES `dpy_institute_classes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `dpy_user_fee_ignore`;
CREATE TABLE `dpy_user_fee_ignore` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `institute_class_fee_id` int(11) unsigned NOT NULL,
  `user_id` int(11) unsigned NOT NULL,
  `percent_discount` float(11) unsigned NOT NULL,
  `status` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '1-ignore,0-not ignore',
  `added_on` datetime NOT NULL,
  `added_by` int(11) unsigned NOT NULL,
  `updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `institute_class_fee_id` (`institute_class_fee_id`),
  CONSTRAINT `dpy_user_fee_ignore_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `dpy_user` (`id`),
  CONSTRAINT `dpy_institute_class_fee_ibfk_2` FOREIGN KEY (`institute_class_fee_id`) REFERENCES `dpy_institute_class_fee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `dpy_payment_receipt`;
CREATE TABLE `dpy_payment_receipt` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `institute_id` int(11) unsigned NOT NULL,
  `token_or_chequeno` longtext DEFAULT NULL COMMENT 'unique code or gateway reference id in case of online payment',
  `response` longtext DEFAULT NULL,
  `mop` int(11) unsigned NOT NULL DEFAULT '4',
  `receipt_amount` float unsigned NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `added_on` datetime NOT NULL,
  `added_by` int(11) unsigned NOT NULL,
  `updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `institute_id` (`institute_id`),
  CONSTRAINT `dpy_institute_receipt_ibfk_1` FOREIGN KEY (`institute_id`) REFERENCES `dpy_institute` (`id`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `dpy_fee_transaction`;
CREATE TABLE `dpy_fee_transaction` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned NOT NULL,
  `institute_class_fee_id` int(11) unsigned NOT NULL,
  `receipt_id` int(11) unsigned NOT NULL,
  `paid_amount` float DEFAULT NULL,
  `cycle` int(11) unsigned NOT NULL,
  `cycle_slot` int(11) unsigned NOT NULL,
  `dsc` longtext NOT NULL,
  `mop` int(11) unsigned NOT NULL DEFAULT 1 COMMENT '1=CASH,2=CHEQUE,3=NEFT/RTGS,4=ONLINE,5=BANK DEPOSITE',
  `status` int(11) unsigned NOT NULL DEFAULT '1' COMMENT '1=Paid,2=Cheque Pending,3=Online Pending,4=Refund',
  `added_on` datetime NOT NULL,
  `added_by` int(11) unsigned NOT NULL,
  `updated_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `receipt_id` (`receipt_id`),
  KEY `institute_class_fee_id` (`institute_class_fee_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `dpy_fee_transaction_ibfk_2` FOREIGN KEY (`receipt_id`) REFERENCES `dpy_payment_receipt` (`id`),
  CONSTRAINT `dpy_fee_transaction_ibfk_3` FOREIGN KEY (`institute_class_fee_id`) REFERENCES `dpy_institute_class_fee` (`id`),
  CONSTRAINT `dpy_fee_transaction_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `dpy_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;