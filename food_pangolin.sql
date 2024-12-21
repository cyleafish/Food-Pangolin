-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-21 10:17:22
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `food_pangolin`
--

-- --------------------------------------------------------

--
-- 資料表結構 `comment`
--

CREATE TABLE `comment` (
  `comment_id` int(11) NOT NULL,
  `rest_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `star` decimal(5,0) DEFAULT NULL,
  `comment` text DEFAULT NULL,
  `data` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `comment`
--

INSERT INTO `comment` (`comment_id`, `rest_id`, `customer_id`, `star`, `comment`, `data`) VALUES
(1, 1, 1, 5, '好粗', '2024-12-15');

-- --------------------------------------------------------

--
-- 資料表結構 `customer`
--

CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `addr` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `customer`
--

INSERT INTO `customer` (`customer_id`, `name`, `phone`, `addr`) VALUES
(1, 'kuo', '0912345678', '南投縣埔里鎮大學路1號');

-- --------------------------------------------------------

--
-- 資料表結構 `customer_star`
--

CREATE TABLE `customer_star` (
  `start_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `deliver_id` int(11) NOT NULL,
  `star` int(5) NOT NULL,
  `order_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `customer_star`
--

INSERT INTO `customer_star` (`start_id`, `customer_id`, `deliver_id`, `star`, `order_id`) VALUES
(16, 1, 1, 1, 5),
(18, 1, 1, 5, 2),
(19, 1, 1, 5, 4);

-- --------------------------------------------------------

--
-- 資料表結構 `deliver`
--

CREATE TABLE `deliver` (
  `deliver_id` int(11) NOT NULL,
  `deliver_name` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `car_num` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `deliver`
--

INSERT INTO `deliver` (`deliver_id`, `deliver_name`, `phone`, `car_num`) VALUES
(1, 'fish', '0909123321', 'NTM-2074');

-- --------------------------------------------------------

--
-- 資料表結構 `deliver_star`
--

CREATE TABLE `deliver_star` (
  `start_id` int(11) NOT NULL,
  `deliver_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `star` int(5) NOT NULL,
  `data` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `deliver_star`
--

INSERT INTO `deliver_star` (`start_id`, `deliver_id`, `customer_id`, `star`, `data`) VALUES
(1, 1, 1, 5, '2024-12-15');

-- --------------------------------------------------------

--
-- 資料表結構 `menu`
--

CREATE TABLE `menu` (
  `menu_id` int(11) NOT NULL,
  `rest_id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `price` decimal(10,0) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `menu`
--

INSERT INTO `menu` (`menu_id`, `rest_id`, `name`, `price`, `description`) VALUES
(1, 1, '大麥克', 80, '牛肉'),
(2, 1, '薯條', 40, '有鹽');

-- --------------------------------------------------------

--
-- 資料表結構 `order`
--

CREATE TABLE `order` (
  `order_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `rest_id` int(11) DEFAULT NULL,
  `total_price` decimal(10,0) DEFAULT NULL,
  `date` datetime DEFAULT current_timestamp(),
  `deliver_id` int(11) DEFAULT NULL,
  `addr` varchar(255) DEFAULT NULL,
  `status` enum('pending','accepted','preparing','on_delivery','arrived','completed','cancelled') NOT NULL DEFAULT 'pending',
  `completed_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `order`
--

INSERT INTO `order` (`order_id`, `customer_id`, `rest_id`, `total_price`, `date`, `deliver_id`, `addr`, `status`, `completed_time`) VALUES
(1, 1, 1, 80, '2024-12-16 00:00:00', NULL, '南投縣埔里鎮大學路1號', 'pending', NULL),
(2, 1, 1, 160, '2024-12-17 00:00:00', 1, '我家', 'completed', '2024-12-21 17:15:40'),
(3, 1, 1, 80, '2024-12-17 22:53:37', NULL, '這裡', 'pending', NULL),
(4, 1, 1, 120, '2024-12-17 23:42:21', 1, '那裡', 'completed', '2024-12-21 17:16:43'),
(5, 1, 1, 160, '2024-12-18 11:30:22', 1, '管院', 'completed', '2024-12-21 17:13:29');

-- --------------------------------------------------------

--
-- 資料表結構 `order_item`
--

CREATE TABLE `order_item` (
  `item_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `menu_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(10,0) DEFAULT NULL,
  `note` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `order_item`
--

INSERT INTO `order_item` (`item_id`, `order_id`, `menu_id`, `quantity`, `price`, `note`) VALUES
(1, 1, 1, 1, 80, ''),
(2, 2, 1, 2, 80, ''),
(3, 3, 1, 1, 80, '不要生菜'),
(4, 4, 1, 1, 80, '不要番茄'),
(5, 4, 2, 1, 40, ''),
(6, 5, 1, 2, 80, '不要番茄');

-- --------------------------------------------------------

--
-- 資料表結構 `restaurant`
--

CREATE TABLE `restaurant` (
  `rest_id` int(11) NOT NULL,
  `restname` varchar(100) NOT NULL,
  `addr` varchar(255) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `time` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `restaurant`
--

INSERT INTO `restaurant` (`rest_id`, `restname`, `addr`, `phone`, `time`) VALUES
(1, 'McDonald', '南投縣埔里鎮信義路1037號', '0492918438', '2024-12-16');

-- --------------------------------------------------------

--
-- 資料表結構 `user_account`
--

CREATE TABLE `user_account` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('customer','restaurant','platform_admin','deliver') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `user_account`
--

INSERT INTO `user_account` (`user_id`, `username`, `password`, `role`, `created_at`) VALUES
(1, 'mcdonalds', 'mcdonalds', 'restaurant', '2024-12-15 13:51:41'),
(2, 'fish', 'fish', 'deliver', '2024-12-15 13:52:17'),
(3, 'kuo', 'kuo', 'customer', '2024-12-15 13:52:45');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`comment_id`),
  ADD KEY `fk_customer` (`customer_id`),
  ADD KEY `rest_id` (`rest_id`);

--
-- 資料表索引 `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`customer_id`);

--
-- 資料表索引 `customer_star`
--
ALTER TABLE `customer_star`
  ADD PRIMARY KEY (`start_id`),
  ADD UNIQUE KEY `unique_rating` (`customer_id`,`deliver_id`,`order_id`);

--
-- 資料表索引 `deliver`
--
ALTER TABLE `deliver`
  ADD PRIMARY KEY (`deliver_id`);

--
-- 資料表索引 `deliver_star`
--
ALTER TABLE `deliver_star`
  ADD PRIMARY KEY (`start_id`),
  ADD KEY `deliver_id` (`deliver_id`,`customer_id`);

--
-- 資料表索引 `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`menu_id`),
  ADD KEY `rest_id` (`rest_id`);

--
-- 資料表索引 `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `fk_customer_order` (`customer_id`),
  ADD KEY `fk_restaurant_order` (`rest_id`),
  ADD KEY `fk_deliver_order` (`deliver_id`);

--
-- 資料表索引 `order_item`
--
ALTER TABLE `order_item`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `menu_id` (`menu_id`);

--
-- 資料表索引 `restaurant`
--
ALTER TABLE `restaurant`
  ADD PRIMARY KEY (`rest_id`);

--
-- 資料表索引 `user_account`
--
ALTER TABLE `user_account`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `comment`
--
ALTER TABLE `comment`
  MODIFY `comment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer_star`
--
ALTER TABLE `customer_star`
  MODIFY `start_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `deliver`
--
ALTER TABLE `deliver`
  MODIFY `deliver_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `menu`
--
ALTER TABLE `menu`
  MODIFY `menu_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `order`
--
ALTER TABLE `order`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `order_item`
--
ALTER TABLE `order_item`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `rest_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `user_account`
--
ALTER TABLE `user_account`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `comment`
--
ALTER TABLE `comment`
  ADD CONSTRAINT `fk_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`);

--
-- 資料表的限制式 `order`
--
ALTER TABLE `order`
  ADD CONSTRAINT `fk_customer_order` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  ADD CONSTRAINT `fk_deliver_order` FOREIGN KEY (`deliver_id`) REFERENCES `deliver` (`deliver_id`),
  ADD CONSTRAINT `fk_restaurant_order` FOREIGN KEY (`rest_id`) REFERENCES `restaurant` (`rest_id`);

--
-- 資料表的限制式 `order_item`
--
ALTER TABLE `order_item`
  ADD CONSTRAINT `order_item_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`order_id`),
  ADD CONSTRAINT `order_item_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`menu_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
