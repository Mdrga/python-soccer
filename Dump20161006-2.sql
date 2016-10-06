CREATE DATABASE  IF NOT EXISTS `fanfootball` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `fanfootball`;
-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: localhost    Database: fanfootball
-- ------------------------------------------------------
-- Server version	5.7.15-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `league`
--

DROP TABLE IF EXISTS `league`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `league` (
  `leagueID` int(11) NOT NULL,
  `leagueDesc` varchar(45) DEFAULT NULL,
  `leagueURL` varchar(90) DEFAULT NULL,
  `leagueCountry` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`leagueID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `player_statistics`
--

DROP TABLE IF EXISTS `player_statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player_statistics` (
  `seasonID` int(11) NOT NULL,
  `teamID` int(11) NOT NULL,
  `matchID` int(11) NOT NULL,
  `playerID` int(11) NOT NULL,
  `statCategoryID` int(11) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`seasonID`,`teamID`,`matchID`,`playerID`,`statCategoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `players` (
  `pl_seasonID` int(11) NOT NULL,
  `pl_playerID` int(11) NOT NULL,
  `pl_playerTeam` int(11) NOT NULL,
  `pl_jerseyNo` int(11) NOT NULL,
  `pl_playerName` varchar(45) DEFAULT NULL,
  `pl_playerURL` varchar(90) DEFAULT NULL,
  PRIMARY KEY (`pl_seasonID`,`pl_playerID`,`pl_playerTeam`,`pl_jerseyNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `season`
--

DROP TABLE IF EXISTS `season`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `season` (
  `seasonID` int(11) NOT NULL,
  `seasonDesc` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`seasonID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stat_categories`
--

DROP TABLE IF EXISTS `stat_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stat_categories` (
  `statCategoryID` int(11) NOT NULL,
  `statCategoryDescriptions` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`statCategoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stg_match_details`
--

DROP TABLE IF EXISTS `stg_match_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stg_match_details` (
  `matchID` int(11) NOT NULL,
  `seasonID` int(11) NOT NULL,
  `homeSide` int(11) DEFAULT NULL,
  `awaySide` int(11) DEFAULT NULL,
  `homeScore` int(11) DEFAULT NULL,
  `awayScore` int(11) DEFAULT NULL,
  `parseStatus` varchar(45) DEFAULT NULL,
  `stadium` varchar(45) DEFAULT NULL,
  `attendance` int(11) DEFAULT NULL,
  `matchURL` varchar(90) DEFAULT NULL,
  PRIMARY KEY (`matchID`,`seasonID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stg_player_news`
--

DROP TABLE IF EXISTS `stg_player_news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stg_player_news` (
  `seasonID` int(11) DEFAULT NULL,
  `player_news_status` tinyint(4) NOT NULL,
  `player_updateDate` varchar(45) NOT NULL,
  `player_rowadded` varchar(45) NOT NULL,
  `player_returndate` varchar(45) DEFAULT NULL,
  `player_firstName` varchar(45) DEFAULT NULL,
  `player_name` varchar(90) NOT NULL,
  `player_team` varchar(3) DEFAULT NULL,
  `player_status` varchar(45) DEFAULT NULL,
  `player_news` varchar(1000) DEFAULT NULL,
  `player_newsURL` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stg_player_stats`
--

DROP TABLE IF EXISTS `stg_player_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stg_player_stats` (
  `ps_matchdate` varchar(10) NOT NULL,
  `ps_seasonID` int(11) NOT NULL,
  `ps_leagueID` int(11) NOT NULL,
  `ps_team` int(11) NOT NULL,
  `ps_teamSide` varchar(4) NOT NULL,
  `ps_matchID` int(11) NOT NULL,
  `ps_playerID` int(11) NOT NULL,
  `ps_playerPOS` varchar(3) DEFAULT NULL,
  `ps_jerseyNo` varchar(2) DEFAULT NULL,
  `ps_playerName` varchar(60) DEFAULT NULL,
  `ps_playerURL` varchar(60) DEFAULT NULL,
  `ps_Shots` int(11) DEFAULT NULL,
  `ps_ShotsOnGoal` int(11) DEFAULT NULL,
  `ps_Goals` int(11) DEFAULT NULL,
  `ps_Assists` int(11) DEFAULT NULL,
  `ps_Offsides` int(11) DEFAULT NULL,
  `ps_FoulsDrawn` int(11) DEFAULT NULL,
  `ps_FoulsCommitted` int(11) DEFAULT NULL,
  `ps_Saves` int(11) DEFAULT NULL,
  `ps_YellowCards` int(11) DEFAULT NULL,
  `ps_RedCards` int(11) DEFAULT NULL,
  `ps_RosterStatus` varchar(45) DEFAULT NULL,
  `ps_Subbed` varchar(45) DEFAULT NULL,
  `ps_SubbedName` varchar(45) DEFAULT NULL,
  `ps_TimeOn` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`ps_matchdate`,`ps_seasonID`,`ps_leagueID`,`ps_team`,`ps_teamSide`,`ps_matchID`,`ps_playerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teams` (
  `teamID` int(11) NOT NULL,
  `teamShortName` varchar(4) DEFAULT NULL,
  `teamLongName` varchar(45) DEFAULT NULL,
  `teamCity` varchar(45) DEFAULT NULL,
  `teamActiveInd` tinyint(4) DEFAULT NULL,
  `teamLeagueID` int(11) DEFAULT NULL,
  `teamCountry` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`teamID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-06 11:23:10
