-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- 생성 시간: 18-03-12 21:10
-- 서버 버전: 5.7.20
-- PHP 버전: 7.1.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 데이터베이스: `aws`
--

-- --------------------------------------------------------

--
-- 테이블 구조 `aws`
--

CREATE TABLE `aws` (
  `id` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `picture` varchar(100) NOT NULL,
  `number` varchar(40) NOT NULL,
  `attendent` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 테이블의 덤프 데이터 `aws`
--

INSERT INTO `aws` (`id`, `name`, `picture`, `number`, `attendent`) VALUES
(1, '김종수', 'https://s3.us-east-2.amazonaws.com/newhansung1/%EA%B9%80%EC%A2%85%EC%88%98.jpg', '1494052', '.'),
(2, '김희택', 'https://s3.us-east-2.amazonaws.com/newhansung1/%EA%B9%80%ED%9D%AC%ED%83%9D.jpg', '1494053', '.'),
(3, '신현수', 'https://s3.us-east-2.amazonaws.com/newhansung1/%EC%8B%A0%ED%98%84%EC%88%98.jpg', '1494060', '.');

--
-- 덤프된 테이블의 인덱스
--

--
-- 테이블의 인덱스 `aws`
--
ALTER TABLE `aws`
  ADD PRIMARY KEY (`id`);

--
-- 덤프된 테이블의 AUTO_INCREMENT
--

--
-- 테이블의 AUTO_INCREMENT `aws`
--
ALTER TABLE `aws`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
