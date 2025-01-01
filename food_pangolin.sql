-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2025-01-01 16:17:00
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
  `order_id` int(11) NOT NULL,
  `star` decimal(5,0) DEFAULT NULL,
  `comment` text DEFAULT NULL,
  `data` date NOT NULL DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `comment`
--

INSERT INTO `comment` (`comment_id`, `rest_id`, `customer_id`, `order_id`, `star`, `comment`, `data`) VALUES
(8, 1, 2, 11, 5, '123', '2025-01-01');

-- --------------------------------------------------------

--
-- 資料表結構 `customer`
--

CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `addr` varchar(255) DEFAULT NULL,
  `email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `customer`
--

INSERT INTO `customer` (`customer_id`, `name`, `phone`, `addr`, `email`) VALUES
(1, 'kuo', '0912345678', '南投縣埔里鎮大學路1號', 'kuo@gmail.com'),
(2, 'a', '0565481254', '南投縣埔里鎮光明巷6號', '123@gmail.com'),
(4, 'me', '0254636587', '清新里 南投縣埔里鎮', '1234@gmail.com');

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
(19, 1, 1, 5, 4),
(20, 1, 1, 4, 3),
(21, 1, 1, 5, 9),
(24, 2, 1, 5, 14),
(25, 2, 1, 5, 11),
(26, 2, 1, 4, 12),
(27, 2, 1, 1, 13),
(28, 2, 1, 3, 21),
(29, 2, 1, 5, 15),
(30, 2, 1, 5, 16),
(31, 2, 1, 5, 17),
(32, 2, 1, 5, 18),
(33, 2, 1, 5, 19),
(34, 2, 1, 5, 20);

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
(1, 'fish', '0909123321', 'NTM-2074'),
(2, 'leafish', '0565481254', 'LMK-2514'),
(3, 'aaa', 'aaa', 'aaa'),
(4, 'ccc', 'ccc', 'ccc'),
(5, 'q', '0915212547', 'qqq-5584'),
(6, 'go', '0954123698', 'LMK-2514');

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
  `description` text DEFAULT NULL,
  `filename` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `menu`
--

INSERT INTO `menu` (`menu_id`, `rest_id`, `name`, `price`, `description`, `filename`) VALUES
(1, 1, '大麥克', 80, '牛肉', '大麥克.jpg'),
(2, 1, '薯條', 40, '有鹽', '薯條.jpg');

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
  `status` enum('order','pending','accepted','prepared','on_delivery','arrived','taked','completed','cancelled') NOT NULL DEFAULT 'order',
  `completed_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `order`
--

INSERT INTO `order` (`order_id`, `customer_id`, `rest_id`, `total_price`, `date`, `deliver_id`, `addr`, `status`, `completed_time`) VALUES
(1, 1, 1, 80, '2024-12-16 00:00:00', 1, '南投縣埔里鎮大學路1號', 'completed', '2024-12-30 21:19:25'),
(2, 1, 1, 160, '2024-12-17 00:00:00', 1, '我家', 'completed', '2024-12-21 17:15:40'),
(3, 1, 1, 80, '2024-12-17 22:53:37', 1, '這裡', 'completed', '2024-12-21 17:29:35'),
(4, 1, 1, 120, '2024-12-17 23:42:21', 1, '那裡', 'completed', '2024-12-21 17:16:43'),
(5, 1, 1, 160, '2024-12-18 11:30:22', 1, '管院', 'completed', '2024-12-21 17:13:29'),
(11, 2, 1, 80, '2024-12-30 15:56:43', 1, '南投縣埔里鎮光明巷6號', 'completed', '2024-12-30 21:29:34'),
(12, 2, 1, 80, '2024-12-30 15:58:13', 1, '南投縣埔里鎮光明巷6號', 'completed', '2024-12-30 21:29:41'),
(13, 2, 1, 40, '2024-12-30 16:29:23', 1, '南投縣埔里鎮光明巷6號', 'completed', '2024-12-30 21:29:42'),
(14, 2, 1, 80, '2024-12-30 16:56:09', 1, '南投縣埔里鎮光明巷6號', 'completed', '2024-12-30 21:24:58'),
(15, 2, 1, 80, '2024-12-30 21:31:36', 1, '南投縣埔里鎮光明巷6號', 'completed', '2024-12-30 22:16:33'),
(16, 2, 1, 40, '2024-12-30 21:48:43', 1, '南投縣埔里鎮光明巷6號', 'completed', '2024-12-30 22:16:37'),
(17, 2, 1, 80, '2024-12-30 21:49:49', 1, '南投縣埔里鎮光明巷6號', 'completed', '2024-12-30 22:16:40'),
(18, 2, 1, 80, '2024-12-30 21:51:53', 1, '南投縣埔里鎮光明巷6號', 'completed', '2024-12-30 22:16:43'),
(19, 2, 1, 80, '2024-12-30 22:05:21', 1, '南投縣埔里鎮光明巷6號', 'completed', '2024-12-30 22:16:46'),
(20, 2, 1, 40, '2024-12-30 22:05:31', 1, '南投縣埔里鎮光明巷6號', 'completed', '2025-01-01 23:16:19'),
(21, 2, 1, 120, '2024-12-30 22:13:01', 1, '南投縣埔里鎮光明巷6號', 'completed', '2024-12-30 22:14:11'),
(22, 2, 1, 40, '2024-12-30 23:21:02', NULL, '南投縣埔里鎮光明巷6號', 'order', NULL),
(23, 2, 1, 40, '2024-12-30 23:32:49', NULL, '南投縣埔里鎮光明巷6號', 'order', NULL),
(24, 2, 1, 80, '2024-12-31 00:24:01', NULL, '南投縣埔里鎮光明巷6號', 'order', NULL);

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
(6, 5, 1, 2, 80, '不要番茄'),
(7, 11, 1, 1, 80, ''),
(8, 12, 1, 1, 80, ''),
(9, 13, 2, 1, 40, '無鹽'),
(10, 14, 1, 1, 80, ''),
(11, 15, 1, 1, 80, ''),
(12, 16, 2, 1, 40, ''),
(13, 17, 2, 2, 40, ''),
(14, 18, 1, 1, 80, ''),
(15, 19, 1, 1, 80, ''),
(16, 20, 2, 1, 40, ''),
(17, 21, 1, 1, 80, '嗨'),
(18, 21, 2, 1, 40, ''),
(19, 22, 2, 1, 40, ''),
(20, 23, 2, 1, 40, ''),
(21, 24, 1, 1, 80, '');

-- --------------------------------------------------------

--
-- 資料表結構 `restaurant`
--

CREATE TABLE `restaurant` (
  `rest_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `restname` varchar(100) NOT NULL,
  `addr` varchar(255) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `time` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `restaurant`
--

INSERT INTO `restaurant` (`rest_id`, `user_id`, `restname`, `addr`, `phone`, `time`) VALUES
(1, 1, 'McDonald', '南投縣埔里鎮信義路1037號', '0492918438', '2024-12-16'),
(2, 10, 'kfc', '東門里 南投縣埔里鎮', '0492997651', '2024-12-23'),
(3, 12, 'feeling18', '南投縣埔里鎮慈恩街20號', '0492984863', '2024-12-23');

-- --------------------------------------------------------

--
-- 資料表結構 `user_account`
--

CREATE TABLE `user_account` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('customer','restaurant','platform','deliver') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `user_account`
--

INSERT INTO `user_account` (`user_id`, `username`, `password`, `role`, `created_at`) VALUES
(1, 'mcdonalds', 'mcdonalds', 'restaurant', '2024-12-15 13:51:41'),
(2, 'fish', 'fish', 'deliver', '2024-12-15 13:52:17'),
(3, 'kuo', 'kuo', 'customer', '2024-12-15 13:52:45'),
(4, 'leafish', 'leafish', 'deliver', '2024-12-21 13:17:37'),
(5, 'aaa', 'aaa', 'deliver', '2024-12-21 14:11:03'),
(6, 'ccc', 'ccc', 'deliver', '2024-12-21 14:13:26'),
(7, 'king', 'king', 'platform', '2024-12-21 15:49:42'),
(8, 'q', 'q', 'deliver', '2024-12-23 04:26:58'),
(9, 'a', 'a', 'customer', '2024-12-23 04:32:40'),
(10, 'kfc', 'kfc', 'restaurant', '2024-12-23 04:39:37'),
(12, 'feeling18', 'feeling18', 'restaurant', '2024-12-23 05:19:35'),
(13, 'me', 'me', 'customer', '2024-12-23 05:30:14'),
(14, 'go', 'go', 'deliver', '2024-12-23 05:30:58');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`comment_id`),
  ADD UNIQUE KEY `order_id` (`order_id`),
  ADD KEY `fk_customer` (`customer_id`),
  ADD KEY `rest_id` (`rest_id`);

--
-- 資料表索引 `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `email` (`email`);

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
  ADD PRIMARY KEY (`rest_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

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
  MODIFY `comment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer_star`
--
ALTER TABLE `customer_star`
  MODIFY `start_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `deliver`
--
ALTER TABLE `deliver`
  MODIFY `deliver_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `menu`
--
ALTER TABLE `menu`
  MODIFY `menu_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `order`
--
ALTER TABLE `order`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `order_item`
--
ALTER TABLE `order_item`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `rest_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `user_account`
--
ALTER TABLE `user_account`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

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
