-- phpMyAdmin SQL Dump
-- version 4.9.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 25, 2022 at 01:02 AM
-- Server version: 5.7.24
-- PHP Version: 7.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kamera`
--

-- --------------------------------------------------------

--
-- Table structure for table `cctv`
--

CREATE TABLE `cctv` (
  `no` int(11) NOT NULL,
  `lokasi_kamera` varchar(30) NOT NULL,
  `ip_address` varchar(15) NOT NULL,
  `username` varchar(16) NOT NULL,
  `password` varchar(16) NOT NULL,
  `port` varchar(16) NOT NULL,
  `is_webcame` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cctv`
--

INSERT INTO `cctv` (`no`, `lokasi_kamera`, `ip_address`, `username`, `password`, `port`, `is_webcame`) VALUES
(1, 'Ruang Belajar 01 Lantai 1', '192.168.100.119', 'admin', 'admin', '554', 1),
(2, 'Ruang Belajar 02 Lantai 1', '192.168.100.4', 'admin', 'admin', '554', 0),
(3, 'Ruang Belajar 03 Lantai 3', '192.168.100.29', 'admin', 'admin', '554', 0),
(4, 'Ruang Belajar 04 Lantai 3', '192.168.100.29', 'admin', 'admin', '554', 0),
(5, 'Ruang Belajar 05 Lantai 3', '192.168.100.29', 'admin', 'admin', '554', 0),
(6, 'Ruang Belajar 06 Lantai 3', '192.168.100.29', 'admin', 'admin', '554', 0),
(7, 'Ruang Belajar 07 Lantai 3', '192.168.100.29', 'admin', 'admin', '554', 0),
(8, 'Ruang Belajar 08 Lantai 3', '192.168.100.29', 'admin', 'admin', '554', 0),
(9, 'Ruang Belajar 09 Lantai 3', '192.168.100.29', 'admin', 'admin', '554', 0),
(10, 'Ruang Belajar 10 Lantai 3', '192.168.100.29', 'admin', 'admin', '554', 0),
(11, 'Ruang Belajar 11 Lantai 3', '192.168.100.29', 'admin', 'admin', '554', 0),
(12, 'Ruang Belajar 12 Lantai 3', '192.168.100.29', 'admin', 'admin', '554', 0);

-- --------------------------------------------------------

--
-- Table structure for table `tabel_login`
--

CREATE TABLE `tabel_login` (
  `user` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tabel_login`
--

INSERT INTO `tabel_login` (`user`, `password`) VALUES
('admin', '1234567');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `level` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `level`) VALUES
(1, 'admin', '$2y$12$IqbsEIXXj3x1v/gxJqnlIubarIhIdSnpQqd5EQd6LVxNEenggMRX6', 1),
(2, 'alfi', '$2b$12$c47Kk6FSGtgZrWWPKegF9Op25GY4f2kSiQVe/oXR8lLoCfVtqlBbS', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cctv`
--
ALTER TABLE `cctv`
  ADD PRIMARY KEY (`no`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cctv`
--
ALTER TABLE `cctv`
  MODIFY `no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
