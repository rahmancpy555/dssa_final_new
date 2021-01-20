-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jan 20, 2021 at 11:38 AM
-- Server version: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `document_similarity`
--

-- --------------------------------------------------------

--
-- Table structure for table `addfiles`
--

CREATE TABLE IF NOT EXISTS `addfiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `did` int(11) NOT NULL,
  `file` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `addfiles`
--

INSERT INTO `addfiles` (`id`, `did`, `file`) VALUES
(7, 10, 'Cloud_Computing_Notes.pdf'),
(8, 11, 'Big_Data.pdf'),
(10, 14, 'artificial_intelligence.pdf');

-- --------------------------------------------------------

--
-- Table structure for table `addkeyword`
--

CREATE TABLE IF NOT EXISTS `addkeyword` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idf` float NOT NULL,
  `keyword` varchar(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=51 ;

--
-- Dumping data for table `addkeyword`
--

INSERT INTO `addkeyword` (`id`, `idf`, `keyword`) VALUES
(1, -4.04597, 'cloud'),
(2, -3.69304, 'computing'),
(3, -3.16407, 'use'),
(4, -3.82501, 'data'),
(5, -2.83321, 'services'),
(6, -2.73003, 'applications'),
(7, -3.36153, 'systems'),
(8, -2.91777, 'using'),
(9, -2.60269, 'storage'),
(10, -2.63906, 'network'),
(11, -2.79321, 'based'),
(12, -2.65089, 'web'),
(13, -2.91777, 'new'),
(14, -3.39002, 'such'),
(15, -2.87168, 'small'),
(16, -3.54578, 'example'),
(17, -2.93563, 'number'),
(18, -2.75154, 'security'),
(19, -2.82336, 'possible'),
(20, -2.83321, 'following'),
(21, -2.67415, 'resources'),
(22, -2.75154, 'memory'),
(23, -3.46574, 'used'),
(24, -2.74084, 'process'),
(25, -3.08344, 'information'),
(26, -3.54096, 'service'),
(27, -3.99207, 'set'),
(28, -3.00403, 'node'),
(29, -3.32623, 'true'),
(30, -2.70805, 'space'),
(31, -2.84297, 'function'),
(32, -2.62708, 'defined'),
(33, -3.33814, 'state'),
(34, -2.85263, 'language'),
(35, -2.74084, 'way'),
(36, -3.02852, 'logic'),
(37, -2.81341, 'value'),
(38, -2.69688, 'given'),
(39, -3.18497, 'rules'),
(40, -2.61496, 'sets'),
(41, -2.62708, 'values'),
(42, -3.42318, 'knowledge'),
(43, -3.14988, 'search'),
(44, -2.8622, 'problem'),
(45, -2.66259, 'max'),
(46, -3.04452, 'rule'),
(47, -3.88156, 'fuzzy'),
(48, -2.69688, 'expert'),
(49, -2.78295, 'sentence'),
(50, -2.76212, 'membership');

-- --------------------------------------------------------

--
-- Table structure for table `domain`
--

CREATE TABLE IF NOT EXISTS `domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domains` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=15 ;

--
-- Dumping data for table `domain`
--

INSERT INTO `domain` (`id`, `domains`) VALUES
(10, 'cloud computing'),
(11, 'big data'),
(13, 'uploaddocs'),
(14, 'artificial intelligence');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE IF NOT EXISTS `login` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `type` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`id`, `username`, `password`, `type`) VALUES
(1, 'fasalu', 'fas', 'user'),
(3, 'admin', 'password', 'admin'),
(8, 'greeshma', 'greeshma', 'user'),
(9, 'anupama', 'anupama', 'pending'),
(10, 'delji', 'delji', 'pending');

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

CREATE TABLE IF NOT EXISTS `registration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `contact` bigint(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10 ;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`id`, `login_id`, `first_name`, `last_name`, `email`, `contact`) VALUES
(1, 1, 'fasalu', 'fas', 'fasa', 123),
(7, 8, 'greeshma', 'p', 'abcd', 6454547567),
(8, 9, 'anupama', 'a', 'abcd', 5564847),
(9, 10, 'delji', 'p', 'abcd', 44568678);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
