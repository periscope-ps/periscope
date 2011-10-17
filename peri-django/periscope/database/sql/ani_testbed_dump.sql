-- MySQL dump 10.13  Distrib 5.1.58, for debian-linux-gnu (i486)
--
-- Host: localhost    Database: periscopedb
-- ------------------------------------------------------
-- Server version	5.1.58-1

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
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_403f60f` (`user_id`),
  KEY `django_admin_log_1bb8f392` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'content type','contenttypes','contenttype'),(2,'session','sessions','session'),(3,'site','sites','site'),(4,'lifetime','topology','lifetime'),(5,'location','topology','location'),(6,'contact','topology','contact'),(7,'role','topology','role'),(8,'address','topology','address'),(9,'name','topology','name'),(10,'description','topology','description'),(11,'network object','topology','networkobject'),(12,'network object names','topology','networkobjectnames'),(13,'network object descriptions','topology','networkobjectdescriptions'),(14,'relation','topology','relation'),(15,'relation property','topology','relationproperty'),(16,'topology','topology','topology'),(17,'topology properties','topology','topologyproperties'),(18,'domain','topology','domain'),(19,'domain properties','topology','domainproperties'),(20,'node addresses','topology','nodeaddresses'),(21,'node','topology','node'),(22,'node properties','topology','nodeproperties'),(23,'port addresses','topology','portaddresses'),(24,'port','topology','port'),(25,'port properties','topology','portproperties'),(26,'global name','topology','globalname'),(27,'link','topology','link'),(28,'link properties','topology','linkproperties'),(29,'network','topology','network'),(30,'network properties','topology','networkproperties'),(31,'path','topology','path'),(32,'path properties','topology','pathproperties'),(33,'hop','topology','hop'),(34,'hop properties','topology','hopproperties'),(35,'service','topology','service'),(36,'service properties','topology','serviceproperties'),(37,'end point pair','topology','endpointpair'),(38,'end point pair names','topology','endpointpairnames'),(39,'dcn topology properties','topology','dcntopologyproperties'),(40,'dcn port properties','topology','dcnportproperties'),(41,'dcn link properties','topology','dcnlinkproperties'),(42,'dcn link protection type','topology','dcnlinkprotectiontype'),(43,'dcn link administrative group','topology','dcnlinkadministrativegroup'),(44,'dcn switching capability descriptor','topology','dcnswitchingcapabilitydescriptor'),(45,'dcn switching capability specific info','topology','dcnswitchingcapabilityspecificinfo'),(46,'tps port properties','topology','tpsportproperties'),(47,'time series data','topology','timeseriesdata'),(48,'periscope saved topology','topology','periscopesavedtopology'),(49,'periscope domain properties','topology','periscopedomainproperties'),(50,'periscope node properties','topology','periscopenodeproperties'),(51,'periscope port properties','topology','periscopeportproperties'),(52,'periscope shape','topology','periscopeshape'),(53,'ps hop properties','topology','pshopproperties'),(54,'cloud node properties','topology','cloudnodeproperties'),(55,'l3 port properties','topology','l3portproperties'),(56,'event type','topology','eventtype'),(57,'ps service properties','topology','psserviceproperties'),(58,'ps service properties event types','topology','psservicepropertieseventtypes'),(59,'ps service watch list','topology','psservicewatchlist'),(60,'path data model','monitoring','pathdatamodel'),(61,'grid ftp transfer','monitoring','gridftptransfer'),(62,'network object status','monitoring','networkobjectstatus'),(63,'dns cache','measurements','dnscache'),(64,'units','measurements','units'),(65,'metadata','measurements','metadata'),(66,'data','measurements','data'),(67,'log entry','admin','logentry');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_3da3d3d8` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measurements_data`
--

DROP TABLE IF EXISTS `measurements_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `measurements_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `metadata_id` int(11) NOT NULL,
  `time` datetime NOT NULL,
  `value` double NOT NULL,
  `units` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `measurements_data_ae34f7f` (`metadata_id`),
  CONSTRAINT `metadata_id_refs_id_538f2974` FOREIGN KEY (`metadata_id`) REFERENCES `measurements_metadata` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measurements_data`
--

LOCK TABLES `measurements_data` WRITE;
/*!40000 ALTER TABLE `measurements_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `measurements_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measurements_dnscache`
--

DROP TABLE IF EXISTS `measurements_dnscache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `measurements_dnscache` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(256) DEFAULT NULL,
  `ip` varchar(40) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measurements_dnscache`
--

LOCK TABLES `measurements_dnscache` WRITE;
/*!40000 ALTER TABLE `measurements_dnscache` DISABLE KEYS */;
/*!40000 ALTER TABLE `measurements_dnscache` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measurements_metadata`
--

DROP TABLE IF EXISTS `measurements_metadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `measurements_metadata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_id` int(11) NOT NULL,
  `event_type_id` int(11) NOT NULL,
  `service_id` int(11) DEFAULT NULL,
  `key` varchar(255) DEFAULT NULL,
  `poll` tinyint(1) NOT NULL,
  `last_poll` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `measurements_metadata_638462f1` (`subject_id`),
  KEY `measurements_metadata_349f2f81` (`event_type_id`),
  KEY `measurements_metadata_6f1d73c2` (`service_id`),
  CONSTRAINT `event_type_id_refs_id_2d8f678b` FOREIGN KEY (`event_type_id`) REFERENCES `topology_eventtype` (`id`),
  CONSTRAINT `service_id_refs_networkobject_ptr_id_72bd5866` FOREIGN KEY (`service_id`) REFERENCES `topology_service` (`networkobject_ptr_id`),
  CONSTRAINT `subject_id_refs_id_1ce2cfc2` FOREIGN KEY (`subject_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measurements_metadata`
--

LOCK TABLES `measurements_metadata` WRITE;
/*!40000 ALTER TABLE `measurements_metadata` DISABLE KEYS */;
/*!40000 ALTER TABLE `measurements_metadata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measurements_units`
--

DROP TABLE IF EXISTS `measurements_units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `measurements_units` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measurements_units`
--

LOCK TABLES `measurements_units` WRITE;
/*!40000 ALTER TABLE `measurements_units` DISABLE KEYS */;
/*!40000 ALTER TABLE `measurements_units` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monitoring_gridftptransfer`
--

DROP TABLE IF EXISTS `monitoring_gridftptransfer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monitoring_gridftptransfer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transfer_id` varchar(200) NOT NULL,
  `status` varchar(200) NOT NULL,
  `src` varchar(200) NOT NULL,
  `dst` varchar(200) NOT NULL,
  `src_port` varchar(200) NOT NULL,
  `dst_port` varchar(200) NOT NULL,
  `user` varchar(200) NOT NULL,
  `misc` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monitoring_gridftptransfer`
--

LOCK TABLES `monitoring_gridftptransfer` WRITE;
/*!40000 ALTER TABLE `monitoring_gridftptransfer` DISABLE KEYS */;
/*!40000 ALTER TABLE `monitoring_gridftptransfer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monitoring_networkobjectstatus`
--

DROP TABLE IF EXISTS `monitoring_networkobjectstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monitoring_networkobjectstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `network_object_id` int(11) NOT NULL,
  `status` varchar(200) NOT NULL,
  `last_update` datetime DEFAULT NULL,
  `gri` varchar(255) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `userid` varchar(255) DEFAULT NULL,
  `obj_type` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `monitoring_networkobjectstatus_26093e` (`network_object_id`),
  CONSTRAINT `network_object_id_refs_id_6f5869f6` FOREIGN KEY (`network_object_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monitoring_networkobjectstatus`
--

LOCK TABLES `monitoring_networkobjectstatus` WRITE;
/*!40000 ALTER TABLE `monitoring_networkobjectstatus` DISABLE KEYS */;
/*!40000 ALTER TABLE `monitoring_networkobjectstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monitoring_pathdatamodel`
--

DROP TABLE IF EXISTS `monitoring_pathdatamodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monitoring_pathdatamodel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path_id` varchar(200) NOT NULL,
  `src` varchar(200) NOT NULL,
  `dst` varchar(200) NOT NULL,
  `src_port_range` varchar(200) NOT NULL,
  `dst_port_range` varchar(200) NOT NULL,
  `vlan_id` varchar(200) NOT NULL,
  `direction` varchar(200) NOT NULL,
  `start_time` int(11) NOT NULL,
  `duration` int(11) NOT NULL,
  `bandwidth` int(11) NOT NULL,
  `bw_class` varchar(200) NOT NULL,
  `status` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monitoring_pathdatamodel`
--

LOCK TABLES `monitoring_pathdatamodel` WRITE;
/*!40000 ALTER TABLE `monitoring_pathdatamodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `monitoring_pathdatamodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_address`
--

DROP TABLE IF EXISTS `topology_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) NOT NULL,
  `type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_address`
--

LOCK TABLES `topology_address` WRITE;
/*!40000 ALTER TABLE `topology_address` DISABLE KEYS */;
INSERT INTO `topology_address` VALUES (1,'172.31.255.18','ipv4'),(2,'172.31.255.17','ipv4');
/*!40000 ALTER TABLE `topology_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_cloudnodeproperties`
--

DROP TABLE IF EXISTS `topology_cloudnodeproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_cloudnodeproperties` (
  `nodeproperties_ptr_id` int(11) NOT NULL,
  `CIDR` varchar(19) DEFAULT NULL,
  PRIMARY KEY (`nodeproperties_ptr_id`),
  CONSTRAINT `nodeproperties_ptr_id_refs_id_34b36319` FOREIGN KEY (`nodeproperties_ptr_id`) REFERENCES `topology_nodeproperties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_cloudnodeproperties`
--

LOCK TABLES `topology_cloudnodeproperties` WRITE;
/*!40000 ALTER TABLE `topology_cloudnodeproperties` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_cloudnodeproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_cloudnodeproperties_bwctl`
--

DROP TABLE IF EXISTS `topology_cloudnodeproperties_bwctl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_cloudnodeproperties_bwctl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cloudnodeproperties_id` int(11) NOT NULL,
  `port_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cloudnodeproperties_id` (`cloudnodeproperties_id`,`port_id`),
  KEY `topology_cloudnodeproperties_bwctl_28c62e23` (`cloudnodeproperties_id`),
  KEY `topology_cloudnodeproperties_bwctl_3af60259` (`port_id`),
  CONSTRAINT `cloudnodeproperties_id_refs_nodeproperties_ptr_id_280f6268` FOREIGN KEY (`cloudnodeproperties_id`) REFERENCES `topology_cloudnodeproperties` (`nodeproperties_ptr_id`),
  CONSTRAINT `port_id_refs_networkobject_ptr_id_72d3cf4` FOREIGN KEY (`port_id`) REFERENCES `topology_port` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_cloudnodeproperties_bwctl`
--

LOCK TABLES `topology_cloudnodeproperties_bwctl` WRITE;
/*!40000 ALTER TABLE `topology_cloudnodeproperties_bwctl` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_cloudnodeproperties_bwctl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_cloudnodeproperties_owamp`
--

DROP TABLE IF EXISTS `topology_cloudnodeproperties_owamp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_cloudnodeproperties_owamp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cloudnodeproperties_id` int(11) NOT NULL,
  `port_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cloudnodeproperties_id` (`cloudnodeproperties_id`,`port_id`),
  KEY `topology_cloudnodeproperties_owamp_28c62e23` (`cloudnodeproperties_id`),
  KEY `topology_cloudnodeproperties_owamp_3af60259` (`port_id`),
  CONSTRAINT `cloudnodeproperties_id_refs_nodeproperties_ptr_id_be40ba0` FOREIGN KEY (`cloudnodeproperties_id`) REFERENCES `topology_cloudnodeproperties` (`nodeproperties_ptr_id`),
  CONSTRAINT `port_id_refs_networkobject_ptr_id_349a9cec` FOREIGN KEY (`port_id`) REFERENCES `topology_port` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_cloudnodeproperties_owamp`
--

LOCK TABLES `topology_cloudnodeproperties_owamp` WRITE;
/*!40000 ALTER TABLE `topology_cloudnodeproperties_owamp` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_cloudnodeproperties_owamp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_cloudnodeproperties_pinger`
--

DROP TABLE IF EXISTS `topology_cloudnodeproperties_pinger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_cloudnodeproperties_pinger` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cloudnodeproperties_id` int(11) NOT NULL,
  `port_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cloudnodeproperties_id` (`cloudnodeproperties_id`,`port_id`),
  KEY `topology_cloudnodeproperties_pinger_28c62e23` (`cloudnodeproperties_id`),
  KEY `topology_cloudnodeproperties_pinger_3af60259` (`port_id`),
  CONSTRAINT `cloudnodeproperties_id_refs_nodeproperties_ptr_id_18e905be` FOREIGN KEY (`cloudnodeproperties_id`) REFERENCES `topology_cloudnodeproperties` (`nodeproperties_ptr_id`),
  CONSTRAINT `port_id_refs_networkobject_ptr_id_46c233b6` FOREIGN KEY (`port_id`) REFERENCES `topology_port` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_cloudnodeproperties_pinger`
--

LOCK TABLES `topology_cloudnodeproperties_pinger` WRITE;
/*!40000 ALTER TABLE `topology_cloudnodeproperties_pinger` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_cloudnodeproperties_pinger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_cloudnodeproperties_traceroute`
--

DROP TABLE IF EXISTS `topology_cloudnodeproperties_traceroute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_cloudnodeproperties_traceroute` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cloudnodeproperties_id` int(11) NOT NULL,
  `port_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cloudnodeproperties_id` (`cloudnodeproperties_id`,`port_id`),
  KEY `topology_cloudnodeproperties_traceroute_28c62e23` (`cloudnodeproperties_id`),
  KEY `topology_cloudnodeproperties_traceroute_3af60259` (`port_id`),
  CONSTRAINT `cloudnodeproperties_id_refs_nodeproperties_ptr_id_506311af` FOREIGN KEY (`cloudnodeproperties_id`) REFERENCES `topology_cloudnodeproperties` (`nodeproperties_ptr_id`),
  CONSTRAINT `port_id_refs_networkobject_ptr_id_8cd1f23` FOREIGN KEY (`port_id`) REFERENCES `topology_port` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_cloudnodeproperties_traceroute`
--

LOCK TABLES `topology_cloudnodeproperties_traceroute` WRITE;
/*!40000 ALTER TABLE `topology_cloudnodeproperties_traceroute` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_cloudnodeproperties_traceroute` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_contact`
--

DROP TABLE IF EXISTS `topology_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `priority` int(11) DEFAULT NULL,
  `email` varchar(75) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `administrator` varchar(255) DEFAULT NULL,
  `institution` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_contact_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_networkobject_ptr_id_419de81c` FOREIGN KEY (`parent_id`) REFERENCES `topology_node` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_contact`
--

LOCK TABLES `topology_contact` WRITE;
/*!40000 ALTER TABLE `topology_contact` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_dcnlinkadministrativegroup`
--

DROP TABLE IF EXISTS `topology_dcnlinkadministrativegroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_dcnlinkadministrativegroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `group` int(11) NOT NULL,
  `group_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_dcnlinkadministrativegroup_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_linkproperties_ptr_id_5aacbc80` FOREIGN KEY (`parent_id`) REFERENCES `topology_dcnlinkproperties` (`linkproperties_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_dcnlinkadministrativegroup`
--

LOCK TABLES `topology_dcnlinkadministrativegroup` WRITE;
/*!40000 ALTER TABLE `topology_dcnlinkadministrativegroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_dcnlinkadministrativegroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_dcnlinkproperties`
--

DROP TABLE IF EXISTS `topology_dcnlinkproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_dcnlinkproperties` (
  `linkproperties_ptr_id` int(11) NOT NULL,
  `capacity` varchar(255) DEFAULT NULL,
  `maximum_reservable_capacity` varchar(255) DEFAULT NULL,
  `minimum_reservable_capacity` varchar(255) DEFAULT NULL,
  `granularity` varchar(255) DEFAULT NULL,
  `unreserverd_capacity` varchar(255) DEFAULT NULL,
  `traffic_engineering_metric` varchar(255) NOT NULL,
  PRIMARY KEY (`linkproperties_ptr_id`),
  CONSTRAINT `linkproperties_ptr_id_refs_id_70c12029` FOREIGN KEY (`linkproperties_ptr_id`) REFERENCES `topology_linkproperties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_dcnlinkproperties`
--

LOCK TABLES `topology_dcnlinkproperties` WRITE;
/*!40000 ALTER TABLE `topology_dcnlinkproperties` DISABLE KEYS */;
INSERT INTO `topology_dcnlinkproperties` VALUES (1,NULL,NULL,NULL,NULL,NULL,'100'),(2,NULL,NULL,NULL,NULL,NULL,'100'),(3,NULL,NULL,NULL,NULL,NULL,'100'),(4,NULL,NULL,NULL,NULL,NULL,'100'),(5,NULL,NULL,NULL,NULL,NULL,'100'),(6,NULL,NULL,NULL,NULL,NULL,'100'),(7,NULL,NULL,NULL,NULL,NULL,'100'),(8,NULL,NULL,NULL,NULL,NULL,'100'),(9,NULL,NULL,NULL,NULL,NULL,'100'),(10,NULL,NULL,NULL,NULL,NULL,'100'),(11,NULL,NULL,NULL,NULL,NULL,'100'),(12,NULL,NULL,NULL,NULL,NULL,'100'),(13,NULL,NULL,NULL,NULL,NULL,'100'),(14,NULL,NULL,NULL,NULL,NULL,'100'),(15,NULL,NULL,NULL,NULL,NULL,'100'),(16,NULL,NULL,NULL,NULL,NULL,'100'),(17,NULL,NULL,NULL,NULL,NULL,'100'),(18,NULL,NULL,NULL,NULL,NULL,'100'),(19,NULL,NULL,NULL,NULL,NULL,'100'),(20,NULL,NULL,NULL,NULL,NULL,'100'),(21,NULL,NULL,NULL,NULL,NULL,'100'),(22,NULL,NULL,NULL,NULL,NULL,'100'),(23,NULL,NULL,NULL,NULL,NULL,'100'),(24,NULL,NULL,NULL,NULL,NULL,'100'),(25,NULL,NULL,NULL,NULL,NULL,'100'),(26,NULL,NULL,NULL,NULL,NULL,'100');
/*!40000 ALTER TABLE `topology_dcnlinkproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_dcnlinkprotectiontype`
--

DROP TABLE IF EXISTS `topology_dcnlinkprotectiontype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_dcnlinkprotectiontype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_dcnlinkprotectiontype_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_linkproperties_ptr_id_40feb74b` FOREIGN KEY (`parent_id`) REFERENCES `topology_dcnlinkproperties` (`linkproperties_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_dcnlinkprotectiontype`
--

LOCK TABLES `topology_dcnlinkprotectiontype` WRITE;
/*!40000 ALTER TABLE `topology_dcnlinkprotectiontype` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_dcnlinkprotectiontype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_dcnportproperties`
--

DROP TABLE IF EXISTS `topology_dcnportproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_dcnportproperties` (
  `portproperties_ptr_id` int(11) NOT NULL,
  `capacity` varchar(255) DEFAULT NULL,
  `maximum_reservable_capacity` varchar(255) DEFAULT NULL,
  `minimum_reservable_capacity` varchar(255) DEFAULT NULL,
  `granularity` varchar(255) DEFAULT NULL,
  `unreserverd_capacity` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`portproperties_ptr_id`),
  CONSTRAINT `portproperties_ptr_id_refs_id_c5e1be1` FOREIGN KEY (`portproperties_ptr_id`) REFERENCES `topology_portproperties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_dcnportproperties`
--

LOCK TABLES `topology_dcnportproperties` WRITE;
/*!40000 ALTER TABLE `topology_dcnportproperties` DISABLE KEYS */;
INSERT INTO `topology_dcnportproperties` VALUES (1,'10000000000','10000000000','1000000','1000000',NULL),(2,'10000000000','10000000000','1000000','1000000',NULL),(3,'10000000000','10000000000','1000000','1000000',NULL),(4,'10000000000','10000000000','1000000','1000000',NULL),(5,'10000000000','10000000000','1000000','1000000',NULL),(6,'10000000000','10000000000','1000000','1000000',NULL),(7,'10000000000','10000000000','1000000','1000000',NULL),(8,'10000000000','10000000000','1000000','1000000',NULL),(9,'10000000000','10000000000','1000000','1000000',NULL),(10,'10000000000','10000000000','1000000','1000000',NULL),(11,'10000000000','10000000000','1000000','1000000',NULL),(12,'10000000000','10000000000','1000000','1000000',NULL),(13,'10000000000','10000000000','1000000','1000000',NULL),(14,'10000000000','10000000000','1000000','1000000',NULL),(15,'1000000000','1000000000','1000000','1000000',NULL),(16,'1000000000','1000000000','1000000','1000000',NULL),(17,'1000000000','1000000000','1000000','1000000',NULL),(18,'10000000000','10000000000','1000000','1000000',NULL),(19,'10000000000','10000000000','1000000','1000000',NULL),(20,'10000000000','10000000000','1000000','1000000',NULL),(21,'10000000000','10000000000','1000000','1000000',NULL),(22,'10000000000','10000000000','1000000','1000000',NULL),(23,'10000000000','10000000000','1000000','1000000',NULL),(24,'10000000000','10000000000','1000000','1000000',NULL),(25,'10000000000','10000000000','1000000','1000000',NULL),(26,'10000000000','10000000000','1000000','1000000',NULL),(27,'1000000000','1000000000','1000000','1000000',NULL);
/*!40000 ALTER TABLE `topology_dcnportproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_dcnswitchingcapabilitydescriptor`
--

DROP TABLE IF EXISTS `topology_dcnswitchingcapabilitydescriptor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_dcnswitchingcapabilitydescriptor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `switching_cap_type` varchar(6) NOT NULL,
  `encoding_type` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_dcnswitchingcapabilitydescriptor_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_linkproperties_ptr_id_7cf2a7b0` FOREIGN KEY (`parent_id`) REFERENCES `topology_dcnlinkproperties` (`linkproperties_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_dcnswitchingcapabilitydescriptor`
--

LOCK TABLES `topology_dcnswitchingcapabilitydescriptor` WRITE;
/*!40000 ALTER TABLE `topology_dcnswitchingcapabilitydescriptor` DISABLE KEYS */;
INSERT INTO `topology_dcnswitchingcapabilitydescriptor` VALUES (1,1,'','packet'),(2,2,'','packet'),(3,3,'','packet'),(4,4,'','packet'),(5,5,'','packet'),(6,6,'','packet'),(7,7,'','packet'),(8,8,'','packet'),(9,9,'','packet'),(10,10,'','packet'),(11,11,'','packet'),(12,12,'','packet'),(13,13,'','packet'),(14,14,'','packet'),(15,15,'','packet'),(16,16,'','packet'),(17,17,'','packet'),(18,18,'','packet'),(19,19,'','packet'),(20,20,'','packet'),(21,21,'','packet'),(22,22,'','packet'),(23,23,'','packet'),(24,24,'','packet'),(25,25,'','packet'),(26,26,'','packet');
/*!40000 ALTER TABLE `topology_dcnswitchingcapabilitydescriptor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_dcnswitchingcapabilityspecificinfo`
--

DROP TABLE IF EXISTS `topology_dcnswitchingcapabilityspecificinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_dcnswitchingcapabilityspecificinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `capability` varchar(255) DEFAULT NULL,
  `interface_mtu` int(11) DEFAULT NULL,
  `vlan_range_availability` varchar(255) DEFAULT NULL,
  `suggested_vlan_range` varchar(255) DEFAULT NULL,
  `vlan_translation` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_dcnswitchingcapabilityspecificinfo_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_id_5dd523f0` FOREIGN KEY (`parent_id`) REFERENCES `topology_dcnswitchingcapabilitydescriptor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_dcnswitchingcapabilityspecificinfo`
--

LOCK TABLES `topology_dcnswitchingcapabilityspecificinfo` WRITE;
/*!40000 ALTER TABLE `topology_dcnswitchingcapabilityspecificinfo` DISABLE KEYS */;
INSERT INTO `topology_dcnswitchingcapabilityspecificinfo` VALUES (1,1,NULL,9000,'3000-4000',NULL,NULL),(2,2,NULL,9000,'3000-4000',NULL,NULL),(3,3,NULL,9000,'3000-4000',NULL,NULL),(4,4,NULL,9000,'3000-4000',NULL,NULL),(5,5,NULL,9000,'3000-4000',NULL,NULL),(6,6,NULL,9000,'3000-4000',NULL,NULL),(7,7,NULL,9000,'3000-4000',NULL,NULL),(8,8,NULL,9000,'3000-4000',NULL,NULL),(9,9,NULL,9000,'3000-4000',NULL,NULL),(10,10,NULL,9000,'3000-4000',NULL,NULL),(11,11,NULL,9000,'3000-4000',NULL,NULL),(12,12,NULL,9000,'3000-4000',NULL,NULL),(13,13,NULL,9000,'3000-4000',NULL,NULL),(14,14,NULL,9000,'3000-4000',NULL,NULL),(15,15,NULL,9000,'3000-4000',NULL,NULL),(16,16,NULL,9000,'3000-4000',NULL,NULL),(17,17,NULL,9000,'3000-4000',NULL,NULL),(18,18,NULL,9000,'3000-4000',NULL,NULL),(19,19,NULL,9000,'3000-4000',NULL,NULL),(20,20,NULL,9000,'3000-4000',NULL,NULL),(21,21,NULL,9000,'3000-4000',NULL,NULL),(22,22,NULL,9000,'3000-4000',NULL,NULL),(23,23,NULL,9000,'3000-4000',NULL,NULL),(24,24,NULL,9000,'3000-4000',NULL,NULL),(25,25,NULL,9000,'3000-4000',NULL,NULL),(26,26,NULL,9000,'3000-4000',NULL,NULL);
/*!40000 ALTER TABLE `topology_dcnswitchingcapabilityspecificinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_dcntopologyproperties`
--

DROP TABLE IF EXISTS `topology_dcntopologyproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_dcntopologyproperties` (
  `topologyproperties_ptr_id` int(11) NOT NULL,
  `idc_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`topologyproperties_ptr_id`),
  CONSTRAINT `topologyproperties_ptr_id_refs_id_402ad6ff` FOREIGN KEY (`topologyproperties_ptr_id`) REFERENCES `topology_topologyproperties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_dcntopologyproperties`
--

LOCK TABLES `topology_dcntopologyproperties` WRITE;
/*!40000 ALTER TABLE `topology_dcntopologyproperties` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_dcntopologyproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_description`
--

DROP TABLE IF EXISTS `topology_description`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_description` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) NOT NULL,
  `type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_description`
--

LOCK TABLES `topology_description` WRITE;
/*!40000 ALTER TABLE `topology_description` DISABLE KEYS */;
INSERT INTO `topology_description` VALUES (1,'Port to Diskpt-2 (3 of 3)',NULL),(2,'Port to Diskpt-2 (2 of 3)',NULL),(3,'Port to Diskpt-2 (1 of 3)',NULL),(4,'Port to Open Flow/Diskpt-1',NULL),(5,'os=CentOS 5.5,kernel=2.6.18-194.el5,memory=24GB,cpu=Intel(R) Xeon(R) CPU E5530  @ 2.40GHz,cores=16,blob=BNL diskpt-1',NULL),(6,'Port to Diskpt-1 (3 of 3)',NULL),(7,'Port to Diskpt-1 (2 of 3)',NULL),(8,'Port to Diskpt-1 (1 of 3)',NULL),(9,'Port to Diskpt-2 (I/O tester)',NULL),(10,'os=CentOS 5.5,kernel=2.6.18-194.el5,memory=24GB,cpu=Intel(R) Xeon(R) CPU E5530  @ 2.40GHz,cores=16,blob=BNL diskpt-2',NULL),(11,'Port to Open Flow/Diskpt-1',NULL),(12,'Port to Open Flow/Diskpt-1',NULL),(13,'NEC switch',NULL),(14,'Port to newy-tb-rt-1 (2 of 2)',NULL),(15,'Port to newy-tb-rt-1 (1 of 2)',NULL),(16,'Port to Diskpt-2 (I/O tester)',NULL),(17,'Port to Open Flow/Diskpt-1',NULL),(18,'Port to Mon-2 (Monitoring Host)',NULL),(19,'Port to bnl-app (Application host virtual machines bnl-app-vm-1 to bnl-app-vm-28)',NULL),(20,'Virtual Machines Host',NULL),(21,'Port to newy-app (Application host virtual machines tb-vm-1 to tb-vm-28)',NULL),(22,'os=,kernel=,memory=,cpu=,cores=,blob=NEC IP8800',NULL),(23,'os=CentOS 5.5,kernel=2.6.18-194.el5,memory=24GB,cpu=Intel(R) Xeon(R) CPU E5530  @ 2.40GHz,cores=16,blob=NEWY diskpt-1',NULL),(24,'Port to Diskpt-1 (I/O tester) - 3 of 3',NULL),(25,'Port to Diskpt-1 (I/O tester) - 2 of 3',NULL),(26,'Port to Diskpt-1 (I/O tester) - 1 of 3',NULL),(27,'Port to bnl-tb-rt-2 (2 of 2)',NULL),(28,'Port to bnl-tb-rt-2 (1 of 2)',NULL),(29,'Port to Diskpt-1 (I/O tester) - 3 of 3',NULL),(30,'Port to Diskpt-1 (I/O tester) - 2 of 3',NULL),(31,'Port to Diskpt-1 (I/O tester) - 1 of 3',NULL),(32,'Port to Open Flow',NULL),(33,'Port to newy-app (Application host virtual machines tb-vm-1 to tb-vm-28)',NULL);
/*!40000 ALTER TABLE `topology_description` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_domain`
--

DROP TABLE IF EXISTS `topology_domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_domain` (
  `networkobject_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`networkobject_ptr_id`),
  CONSTRAINT `networkobject_ptr_id_refs_id_4e9b1df9` FOREIGN KEY (`networkobject_ptr_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_domain`
--

LOCK TABLES `topology_domain` WRITE;
/*!40000 ALTER TABLE `topology_domain` DISABLE KEYS */;
INSERT INTO `topology_domain` VALUES (2);
/*!40000 ALTER TABLE `topology_domain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_domainproperties`
--

DROP TABLE IF EXISTS `topology_domainproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_domainproperties` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_domainproperties_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_networkobject_ptr_id_501a99dc` FOREIGN KEY (`parent_id`) REFERENCES `topology_domain` (`networkobject_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_domainproperties`
--

LOCK TABLES `topology_domainproperties` WRITE;
/*!40000 ALTER TABLE `topology_domainproperties` DISABLE KEYS */;
INSERT INTO `topology_domainproperties` VALUES (1,2);
/*!40000 ALTER TABLE `topology_domainproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_endpointpair`
--

DROP TABLE IF EXISTS `topology_endpointpair`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_endpointpair` (
  `networkobject_ptr_id` int(11) NOT NULL,
  `src_id` int(11) DEFAULT NULL,
  `dst_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`networkobject_ptr_id`),
  KEY `topology_endpointpair_36ba328f` (`src_id`),
  KEY `topology_endpointpair_4cf50386` (`dst_id`),
  CONSTRAINT `dst_id_refs_id_45a650b6` FOREIGN KEY (`dst_id`) REFERENCES `topology_networkobject` (`id`),
  CONSTRAINT `networkobject_ptr_id_refs_id_45a650b6` FOREIGN KEY (`networkobject_ptr_id`) REFERENCES `topology_networkobject` (`id`),
  CONSTRAINT `src_id_refs_id_45a650b6` FOREIGN KEY (`src_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_endpointpair`
--

LOCK TABLES `topology_endpointpair` WRITE;
/*!40000 ALTER TABLE `topology_endpointpair` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_endpointpair` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_endpointpairnames`
--

DROP TABLE IF EXISTS `topology_endpointpairnames`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_endpointpairnames` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `endpointpair_id` int(11) NOT NULL,
  `name_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_id` (`name_id`),
  KEY `topology_endpointpairnames_3a5f0685` (`endpointpair_id`),
  CONSTRAINT `endpointpair_id_refs_networkobject_ptr_id_443ea9be` FOREIGN KEY (`endpointpair_id`) REFERENCES `topology_endpointpair` (`networkobject_ptr_id`),
  CONSTRAINT `name_id_refs_id_3cfbd250` FOREIGN KEY (`name_id`) REFERENCES `topology_name` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_endpointpairnames`
--

LOCK TABLES `topology_endpointpairnames` WRITE;
/*!40000 ALTER TABLE `topology_endpointpairnames` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_endpointpairnames` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_eventtype`
--

DROP TABLE IF EXISTS `topology_eventtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_eventtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `value` (`value`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_eventtype`
--

LOCK TABLES `topology_eventtype` WRITE;
/*!40000 ALTER TABLE `topology_eventtype` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_eventtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_globalname`
--

DROP TABLE IF EXISTS `topology_globalname`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_globalname` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) NOT NULL,
  `type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_globalname`
--

LOCK TABLES `topology_globalname` WRITE;
/*!40000 ALTER TABLE `topology_globalname` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_globalname` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_hop`
--

DROP TABLE IF EXISTS `topology_hop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_hop` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `unis_id` varchar(255) NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_hop_63f17a16` (`parent_id`),
  KEY `topology_hop_6ca73769` (`target_id`),
  CONSTRAINT `parent_id_refs_networkobject_ptr_id_3af5bbc2` FOREIGN KEY (`parent_id`) REFERENCES `topology_path` (`networkobject_ptr_id`),
  CONSTRAINT `target_id_refs_id_5fb38999` FOREIGN KEY (`target_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_hop`
--

LOCK TABLES `topology_hop` WRITE;
/*!40000 ALTER TABLE `topology_hop` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_hop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_hopproperties`
--

DROP TABLE IF EXISTS `topology_hopproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_hopproperties` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_hopproperties_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_id_33c45f9c` FOREIGN KEY (`parent_id`) REFERENCES `topology_hop` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_hopproperties`
--

LOCK TABLES `topology_hopproperties` WRITE;
/*!40000 ALTER TABLE `topology_hopproperties` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_hopproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_l3portproperties`
--

DROP TABLE IF EXISTS `topology_l3portproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_l3portproperties` (
  `portproperties_ptr_id` int(11) NOT NULL,
  `netmask` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`portproperties_ptr_id`),
  CONSTRAINT `portproperties_ptr_id_refs_id_20a9e10c` FOREIGN KEY (`portproperties_ptr_id`) REFERENCES `topology_portproperties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_l3portproperties`
--

LOCK TABLES `topology_l3portproperties` WRITE;
/*!40000 ALTER TABLE `topology_l3portproperties` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_l3portproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_lifetime`
--

DROP TABLE IF EXISTS `topology_lifetime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_lifetime` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_lifetime`
--

LOCK TABLES `topology_lifetime` WRITE;
/*!40000 ALTER TABLE `topology_lifetime` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_lifetime` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_link`
--

DROP TABLE IF EXISTS `topology_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_link` (
  `networkobject_ptr_id` int(11) NOT NULL,
  `global_name_id` int(11) DEFAULT NULL,
  `directed` tinyint(1) NOT NULL,
  PRIMARY KEY (`networkobject_ptr_id`),
  UNIQUE KEY `global_name_id` (`global_name_id`),
  CONSTRAINT `networkobject_ptr_id_refs_id_3b1d10e3` FOREIGN KEY (`networkobject_ptr_id`) REFERENCES `topology_networkobject` (`id`),
  CONSTRAINT `global_name_id_refs_id_b46660b` FOREIGN KEY (`global_name_id`) REFERENCES `topology_globalname` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_link`
--

LOCK TABLES `topology_link` WRITE;
/*!40000 ALTER TABLE `topology_link` DISABLE KEYS */;
INSERT INTO `topology_link` VALUES (5,NULL,1),(7,NULL,1),(9,NULL,1),(11,NULL,1),(14,NULL,1),(16,NULL,1),(18,NULL,1),(20,NULL,1),(23,NULL,1),(25,NULL,1),(28,NULL,1),(30,NULL,1),(32,NULL,1),(34,NULL,1),(36,NULL,1),(38,NULL,1),(41,NULL,1),(43,NULL,1),(46,NULL,1),(48,NULL,1),(50,NULL,1),(52,NULL,1),(55,NULL,1),(57,NULL,1),(59,NULL,1),(61,NULL,1),(63,NULL,1),(66,NULL,1),(68,NULL,1),(70,NULL,1),(72,NULL,1),(74,NULL,1),(76,NULL,1),(78,NULL,1),(80,NULL,1),(81,NULL,1),(82,NULL,1),(83,NULL,1);
/*!40000 ALTER TABLE `topology_link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_linkproperties`
--

DROP TABLE IF EXISTS `topology_linkproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_linkproperties` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_linkproperties_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_networkobject_ptr_id_6fc0eb44` FOREIGN KEY (`parent_id`) REFERENCES `topology_link` (`networkobject_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_linkproperties`
--

LOCK TABLES `topology_linkproperties` WRITE;
/*!40000 ALTER TABLE `topology_linkproperties` DISABLE KEYS */;
INSERT INTO `topology_linkproperties` VALUES (1,5),(2,7),(3,9),(4,11),(5,14),(6,16),(7,18),(8,20),(9,23),(10,25),(11,28),(12,30),(13,32),(14,34),(15,36),(16,38),(17,43),(18,52),(19,61),(20,63),(21,66),(22,68),(23,72),(24,74),(25,76),(26,78);
/*!40000 ALTER TABLE `topology_linkproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_location`
--

DROP TABLE IF EXISTS `topology_location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_location` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `continent` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `zipcode` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `institution` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `street_address` varchar(255) DEFAULT NULL,
  `floor` varchar(255) DEFAULT NULL,
  `room` varchar(255) DEFAULT NULL,
  `cage` varchar(255) DEFAULT NULL,
  `rack` varchar(255) DEFAULT NULL,
  `shelf` varchar(255) DEFAULT NULL,
  `latitude` varchar(255) DEFAULT NULL,
  `longitude` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_location`
--

LOCK TABLES `topology_location` WRITE;
/*!40000 ALTER TABLE `topology_location` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_name`
--

DROP TABLE IF EXISTS `topology_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_name` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) NOT NULL,
  `type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_name`
--

LOCK TABLES `topology_name` WRITE;
/*!40000 ALTER TABLE `topology_name` DISABLE KEYS */;
INSERT INTO `topology_name` VALUES (1,'eth10##192.168.100.58',NULL),(2,'eth10','ifName'),(3,'eth8##192.168.100.58',NULL),(4,'eth8','ifName'),(5,'eth4##192.168.100.58',NULL),(6,'eth4','ifName'),(7,'eth5##192.168.100.58',NULL),(8,'eth5','ifName'),(9,'ANI-ANI-bnl-diskpt-1.testbed.es.net',NULL),(10,'bnl-diskpt-1.testbed.es.net','hostname'),(11,'eth9##192.168.100.178',NULL),(12,'eth9','ifName'),(13,'eth8##192.168.100.178',NULL),(14,'eth8','ifName'),(15,'eth7##192.168.100.178',NULL),(16,'eth7','ifName'),(17,'eth4##192.168.100.178',NULL),(18,'eth4','ifName'),(19,'ANI-ANI-bnl-diskpt-2.testbed.es.net',NULL),(20,'bnl-diskpt-2.testbed.es.net','hostname'),(21,'10GBE0/26##192.168.100.182',NULL),(22,'10GBE0/26','ifName'),(23,'10GBE0/25##192.168.100.182',NULL),(24,'10GBE0/25','ifName'),(25,'xe-0/0/1.0##192.168.100.22',NULL),(26,'xe-0/0/1','ifName'),(27,'xe-0/0/0.0##192.168.100.18',NULL),(28,'xe-0/0/0','ifName'),(29,'xe-1/2/0.0##192.168.100.61',NULL),(30,'xe-1/2/0','ifName'),(31,'xe-1/3/0.0##192.168.100.181',NULL),(32,'xe-1/3/0','ifName'),(33,'ge-1/0/0.0##192.168.100.162',NULL),(34,'ge-1/0/0','ifName'),(35,'ge-1/0/1.0##192.168.100.193',NULL),(36,'ge-1/0/1','ifName'),(37,'eth1##192.168.100.100',NULL),(38,'eth1','ifName'),(39,'ge-1/0/1.0##192.168.100.97',NULL),(40,'eth2','ifName'),(41,'Gi0/6##192.168.100.82',NULL),(42,'Gi0/8##192.168.100.82',NULL),(43,'10GBE0/25##192.168.100.82',NULL),(44,'10GBE0/26##192.168.100.82',NULL),(45,'eth1##192.168.100.50',NULL),(46,'eth1','ifName'),(47,'eth5##192.168.100.82',NULL),(48,'eth5','ifName'),(49,'xe-0/0/2.0##192.168.100.93',NULL),(50,'eth9','ifName'),(51,'eth8##192.168.100.90',NULL),(52,'eth8','ifName'),(53,'eth4##192.168.100.86',NULL),(54,'eth4','ifName'),(55,'ANI-ANI-newy-diskpt-1.testbed.es.net',NULL),(56,'newy-diskpt-1.testbed.es.net','hostname'),(57,'xe-1/3/0.0##192.168.100.21',NULL),(58,'xe-1/2/0.0##192.168.100.1',NULL),(59,'xe-0/0/2.0##192.168.100.93',NULL),(60,'xe-0/0/1.0##192.168.100.85',NULL),(61,'xe-0/0/0.0##192.168.100.81',NULL),(62,'xe-0/0/3.0##192.168.100.81',NULL),(63,'ge-1/0/1.0##192.168.100.97',NULL);
/*!40000 ALTER TABLE `topology_name` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_network`
--

DROP TABLE IF EXISTS `topology_network`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_network` (
  `networkobject_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`networkobject_ptr_id`),
  CONSTRAINT `networkobject_ptr_id_refs_id_5706766` FOREIGN KEY (`networkobject_ptr_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_network`
--

LOCK TABLES `topology_network` WRITE;
/*!40000 ALTER TABLE `topology_network` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_network` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_network_links`
--

DROP TABLE IF EXISTS `topology_network_links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_network_links` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `network_id` int(11) NOT NULL,
  `link_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `network_id` (`network_id`,`link_id`),
  KEY `topology_network_links_4d5bad5` (`network_id`),
  KEY `topology_network_links_bb3ce60` (`link_id`),
  CONSTRAINT `link_id_refs_networkobject_ptr_id_e3609e2` FOREIGN KEY (`link_id`) REFERENCES `topology_link` (`networkobject_ptr_id`),
  CONSTRAINT `network_id_refs_networkobject_ptr_id_251e33b1` FOREIGN KEY (`network_id`) REFERENCES `topology_network` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_network_links`
--

LOCK TABLES `topology_network_links` WRITE;
/*!40000 ALTER TABLE `topology_network_links` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_network_links` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_network_nodes`
--

DROP TABLE IF EXISTS `topology_network_nodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_network_nodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `network_id` int(11) NOT NULL,
  `node_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `network_id` (`network_id`,`node_id`),
  KEY `topology_network_nodes_4d5bad5` (`network_id`),
  KEY `topology_network_nodes_474baebc` (`node_id`),
  CONSTRAINT `network_id_refs_networkobject_ptr_id_5bc35bc5` FOREIGN KEY (`network_id`) REFERENCES `topology_network` (`networkobject_ptr_id`),
  CONSTRAINT `node_id_refs_networkobject_ptr_id_6c35dcc6` FOREIGN KEY (`node_id`) REFERENCES `topology_node` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_network_nodes`
--

LOCK TABLES `topology_network_nodes` WRITE;
/*!40000 ALTER TABLE `topology_network_nodes` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_network_nodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_network_ports`
--

DROP TABLE IF EXISTS `topology_network_ports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_network_ports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `network_id` int(11) NOT NULL,
  `port_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `network_id` (`network_id`,`port_id`),
  KEY `topology_network_ports_4d5bad5` (`network_id`),
  KEY `topology_network_ports_3af60259` (`port_id`),
  CONSTRAINT `network_id_refs_networkobject_ptr_id_50173d88` FOREIGN KEY (`network_id`) REFERENCES `topology_network` (`networkobject_ptr_id`),
  CONSTRAINT `port_id_refs_networkobject_ptr_id_62e9a0fa` FOREIGN KEY (`port_id`) REFERENCES `topology_port` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_network_ports`
--

LOCK TABLES `topology_network_ports` WRITE;
/*!40000 ALTER TABLE `topology_network_ports` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_network_ports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_networkobject`
--

DROP TABLE IF EXISTS `topology_networkobject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_networkobject` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `unis_id` varchar(255) DEFAULT NULL,
  `unis_idref` varchar(255) DEFAULT NULL,
  `lifetime_id` int(11) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unis_id` (`unis_id`),
  UNIQUE KEY `lifetime_id` (`lifetime_id`),
  KEY `topology_networkobject_63f17a16` (`parent_id`),
  CONSTRAINT `lifetime_id_refs_id_7b22f6f6` FOREIGN KEY (`lifetime_id`) REFERENCES `topology_lifetime` (`id`),
  CONSTRAINT `parent_id_refs_id_16e825bd` FOREIGN KEY (`parent_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_networkobject`
--

LOCK TABLES `topology_networkobject` WRITE;
/*!40000 ALTER TABLE `topology_networkobject` DISABLE KEYS */;
INSERT INTO `topology_networkobject` VALUES (1,NULL,'ANI testbed topology',NULL,NULL,NULL),(2,1,'urn:ogf:network:domain=testbed.es.net',NULL,NULL,NULL),(3,2,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1',NULL,NULL,NULL),(4,3,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth10',NULL,NULL,NULL),(5,4,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth10:link=eth10##192.168.100.58',NULL,NULL,NULL),(6,3,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth8',NULL,NULL,NULL),(7,6,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth8:link=eth8##192.168.100.58',NULL,NULL,NULL),(8,3,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth4',NULL,NULL,NULL),(9,8,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth4:link=eth4##192.168.100.58',NULL,NULL,NULL),(10,3,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth5',NULL,NULL,NULL),(11,10,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth5:link=eth5##192.168.100.58',NULL,NULL,NULL),(12,2,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2',NULL,NULL,NULL),(13,12,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth9',NULL,NULL,NULL),(14,13,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth9:link=eth9##192.168.100.178',NULL,NULL,NULL),(15,12,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth8',NULL,NULL,NULL),(16,15,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth8:link=eth8##192.168.100.178',NULL,NULL,NULL),(17,12,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth7',NULL,NULL,NULL),(18,17,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth7:link=eth7##192.168.100.178',NULL,NULL,NULL),(19,12,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth4',NULL,NULL,NULL),(20,19,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth4:link=eth4##192.168.100.178',NULL,NULL,NULL),(21,2,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-of-2',NULL,NULL,NULL),(22,21,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-of-2:port=10GBE0/26',NULL,NULL,NULL),(23,22,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-of-2:port=10GBE0/26:link=10GBE0/26##192.168.100.182',NULL,NULL,NULL),(24,21,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-of-2:port=10GBE0/25',NULL,NULL,NULL),(25,24,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-of-2:port=10GBE0/25:link=10GBE0/25##192.168.100.182',NULL,NULL,NULL),(26,2,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2',NULL,NULL,NULL),(27,26,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-0/0/1',NULL,NULL,NULL),(28,27,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-0/0/1:link=xe-0/0/1.0##192.168.100.22',NULL,NULL,NULL),(29,26,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-0/0/0',NULL,NULL,NULL),(30,29,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-0/0/0:link=xe-0/0/0.0##192.168.100.18',NULL,NULL,NULL),(31,26,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-1/2/0',NULL,NULL,NULL),(32,31,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-1/2/0:link=xe-1/2/0.0##192.168.100.61',NULL,NULL,NULL),(33,26,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-1/3/0',NULL,NULL,NULL),(34,33,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-1/3/0:link=xe-1/3/0.0##192.168.100.181',NULL,NULL,NULL),(35,26,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=ge-1/0/0',NULL,NULL,NULL),(36,35,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=ge-1/0/0:link=ge-1/0/0.0##192.168.100.162',NULL,NULL,NULL),(37,26,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=ge-1/0/1',NULL,NULL,NULL),(38,37,'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=ge-1/0/1:link=ge-1/0/1.0##192.168.100.193',NULL,NULL,NULL),(39,2,'urn:ogf:network:domain=testbed.es.net:node=newy-app',NULL,NULL,NULL),(40,39,'urn:ogf:network:domain=testbed.es.net:node=newy-app:port=eth1',NULL,NULL,NULL),(41,40,'urn:ogf:network:domain=testbed.es.net:node=newy-app:port=eth1:link=eth1##192.168.100.100',NULL,NULL,NULL),(42,39,'urn:ogf:network:domain=testbed.es.net:node=newy-app:port=eth2',NULL,NULL,NULL),(43,42,'urn:ogf:network:domain=testbed.es.net:node=newy-app:port=eth2:link=eth2##192.168.100.98',NULL,NULL,NULL),(44,2,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1',NULL,NULL,NULL),(45,44,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=Gi0/6',NULL,NULL,NULL),(46,45,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=Gi0/6:link=Gi0/6##192.168.100.82',NULL,NULL,NULL),(47,44,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=Gi0/8',NULL,NULL,NULL),(48,47,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=Gi0/8:link=Gi0/8##192.168.100.82',NULL,NULL,NULL),(49,44,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=10GBE0/25',NULL,NULL,NULL),(50,49,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=10GBE0/25:link=10GBE0/25##192.168.100.82',NULL,NULL,NULL),(51,44,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=10GBE0/26',NULL,NULL,NULL),(52,51,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=10GBE0/26:link=10GBE0/26##192.168.100.82',NULL,NULL,NULL),(53,2,'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1',NULL,NULL,NULL),(54,53,'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth1',NULL,NULL,NULL),(55,54,'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth1:link=eth1##192.168.100.50',NULL,NULL,NULL),(56,53,'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth5',NULL,NULL,NULL),(57,56,'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth5:link=eth5##192.168.100.82',NULL,NULL,NULL),(58,53,'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth9',NULL,NULL,NULL),(59,58,'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth9:link=eth9##192.168.100.94',NULL,NULL,NULL),(60,53,'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth8',NULL,NULL,NULL),(61,60,'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth8:link=eth8##192.168.100.90',NULL,NULL,NULL),(62,53,'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth4',NULL,NULL,NULL),(63,62,'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth4:link=eth4##192.168.100.86',NULL,NULL,NULL),(64,2,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1',NULL,NULL,NULL),(65,64,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-1/3/0',NULL,NULL,NULL),(66,65,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-1/3/0:link=xe-1/3/0.0##192.168.100.21',NULL,NULL,NULL),(67,64,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-1/2/0',NULL,NULL,NULL),(68,67,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-1/2/0:link=xe-1/2/0.0##192.168.100.1',NULL,NULL,NULL),(69,64,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-0/0/2',NULL,NULL,NULL),(70,69,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-0/0/2:link=xe-0/0/2.0##192.168.100.93',NULL,NULL,NULL),(71,64,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-0/0/1',NULL,NULL,NULL),(72,71,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-0/0/1:link=xe-0/0/1.0##192.168.100.85',NULL,NULL,NULL),(73,64,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-0/0/0',NULL,NULL,NULL),(74,73,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-0/0/0:link=xe-0/0/0.0##192.168.100.81',NULL,NULL,NULL),(75,64,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-0/0/3',NULL,NULL,NULL),(76,75,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-0/0/3:link=xe-0/0/3.0##192.168.100.81',NULL,NULL,NULL),(77,64,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=ge-1/0/1',NULL,NULL,NULL),(78,77,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=ge-1/0/1:link=ge-1/0/1.0##192.168.100.97',NULL,NULL,NULL),(79,1,NULL,'urn:ogf:network:*:*:*:*',NULL,NULL),(80,1,NULL,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth10:link=eth4##192.168.100.58',NULL,NULL),(81,1,NULL,'urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=10GBE0/26##192.168.100.82',NULL,NULL),(82,1,NULL,'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth8:link=eth4##192.168.100.58',NULL,NULL),(83,1,NULL,'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth1:link=eth5##192.168.100.50',NULL,NULL);
/*!40000 ALTER TABLE `topology_networkobject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_networkobjectdescriptions`
--

DROP TABLE IF EXISTS `topology_networkobjectdescriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_networkobjectdescriptions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description_id` int(11) NOT NULL,
  `networkobject_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `description_id` (`description_id`),
  KEY `topology_networkobjectdescriptions_1646de4a` (`networkobject_id`),
  CONSTRAINT `description_id_refs_id_34116677` FOREIGN KEY (`description_id`) REFERENCES `topology_description` (`id`),
  CONSTRAINT `networkobject_id_refs_id_3c4b1cc` FOREIGN KEY (`networkobject_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_networkobjectdescriptions`
--

LOCK TABLES `topology_networkobjectdescriptions` WRITE;
/*!40000 ALTER TABLE `topology_networkobjectdescriptions` DISABLE KEYS */;
INSERT INTO `topology_networkobjectdescriptions` VALUES (1,1,4),(2,2,6),(3,3,8),(4,4,10),(5,5,3),(6,6,13),(7,7,15),(8,8,17),(9,9,19),(10,10,12),(11,11,22),(12,12,24),(13,13,21),(14,14,27),(15,15,29),(16,16,31),(17,17,33),(18,18,35),(19,19,37),(20,21,42),(21,20,39),(22,22,44),(23,24,58),(24,25,60),(25,26,62),(26,23,53),(27,27,65),(28,28,67),(29,29,69),(30,30,71),(31,31,73),(32,32,75),(33,33,77);
/*!40000 ALTER TABLE `topology_networkobjectdescriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_networkobjectnames`
--

DROP TABLE IF EXISTS `topology_networkobjectnames`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_networkobjectnames` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_id` int(11) NOT NULL,
  `networkobject_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_id` (`name_id`),
  KEY `topology_networkobjectnames_1646de4a` (`networkobject_id`),
  CONSTRAINT `name_id_refs_id_24a3e395` FOREIGN KEY (`name_id`) REFERENCES `topology_name` (`id`),
  CONSTRAINT `networkobject_id_refs_id_6ace01ee` FOREIGN KEY (`networkobject_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_networkobjectnames`
--

LOCK TABLES `topology_networkobjectnames` WRITE;
/*!40000 ALTER TABLE `topology_networkobjectnames` DISABLE KEYS */;
INSERT INTO `topology_networkobjectnames` VALUES (1,1,5),(2,2,4),(3,3,7),(4,4,6),(5,5,9),(6,6,8),(7,7,11),(8,8,10),(9,10,3),(10,9,3),(11,11,14),(12,12,13),(13,13,16),(14,14,15),(15,15,18),(16,16,17),(17,17,20),(18,18,19),(19,20,12),(20,19,12),(21,21,23),(22,22,22),(23,23,25),(24,24,24),(25,25,28),(26,26,27),(27,27,30),(28,28,29),(29,29,32),(30,30,31),(31,31,34),(32,32,33),(33,33,36),(34,34,35),(35,35,38),(36,36,37),(37,37,41),(38,38,40),(39,39,43),(40,40,42),(41,41,46),(42,42,48),(43,43,50),(44,44,52),(45,45,55),(46,46,54),(47,47,57),(48,48,56),(49,49,59),(50,50,58),(51,51,61),(52,52,60),(53,53,63),(54,54,62),(55,56,53),(56,55,53),(57,57,66),(58,58,68),(59,59,70),(60,60,72),(61,61,74),(62,62,76),(63,63,78);
/*!40000 ALTER TABLE `topology_networkobjectnames` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_networkproperties`
--

DROP TABLE IF EXISTS `topology_networkproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_networkproperties` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_networkproperties_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_networkobject_ptr_id_6a96789e` FOREIGN KEY (`parent_id`) REFERENCES `topology_network` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_networkproperties`
--

LOCK TABLES `topology_networkproperties` WRITE;
/*!40000 ALTER TABLE `topology_networkproperties` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_networkproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_node`
--

DROP TABLE IF EXISTS `topology_node`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_node` (
  `networkobject_ptr_id` int(11) NOT NULL,
  `location_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`networkobject_ptr_id`),
  UNIQUE KEY `location_id` (`location_id`),
  UNIQUE KEY `role_id` (`role_id`),
  CONSTRAINT `location_id_refs_id_81621d6` FOREIGN KEY (`location_id`) REFERENCES `topology_location` (`id`),
  CONSTRAINT `networkobject_ptr_id_refs_id_25ae6c71` FOREIGN KEY (`networkobject_ptr_id`) REFERENCES `topology_networkobject` (`id`),
  CONSTRAINT `role_id_refs_id_6b2a7381` FOREIGN KEY (`role_id`) REFERENCES `topology_role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_node`
--

LOCK TABLES `topology_node` WRITE;
/*!40000 ALTER TABLE `topology_node` DISABLE KEYS */;
INSERT INTO `topology_node` VALUES (3,NULL,NULL),(12,NULL,NULL),(21,NULL,NULL),(26,NULL,NULL),(39,NULL,NULL),(44,NULL,NULL),(53,NULL,NULL),(64,NULL,NULL);
/*!40000 ALTER TABLE `topology_node` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_nodeaddresses`
--

DROP TABLE IF EXISTS `topology_nodeaddresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_nodeaddresses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_id` int(11) NOT NULL,
  `address_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `address_id` (`address_id`),
  KEY `topology_nodeaddresses_474baebc` (`node_id`),
  CONSTRAINT `address_id_refs_id_5bc4958d` FOREIGN KEY (`address_id`) REFERENCES `topology_address` (`id`),
  CONSTRAINT `node_id_refs_networkobject_ptr_id_5b1da046` FOREIGN KEY (`node_id`) REFERENCES `topology_node` (`networkobject_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_nodeaddresses`
--

LOCK TABLES `topology_nodeaddresses` WRITE;
/*!40000 ALTER TABLE `topology_nodeaddresses` DISABLE KEYS */;
INSERT INTO `topology_nodeaddresses` VALUES (1,26,1),(2,64,2);
/*!40000 ALTER TABLE `topology_nodeaddresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_nodeproperties`
--

DROP TABLE IF EXISTS `topology_nodeproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_nodeproperties` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_nodeproperties_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_networkobject_ptr_id_23909c3c` FOREIGN KEY (`parent_id`) REFERENCES `topology_node` (`networkobject_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_nodeproperties`
--

LOCK TABLES `topology_nodeproperties` WRITE;
/*!40000 ALTER TABLE `topology_nodeproperties` DISABLE KEYS */;
INSERT INTO `topology_nodeproperties` VALUES (6,3),(7,12),(8,21),(5,26),(3,39),(4,44),(2,53),(1,64);
/*!40000 ALTER TABLE `topology_nodeproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_path`
--

DROP TABLE IF EXISTS `topology_path`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_path` (
  `networkobject_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`networkobject_ptr_id`),
  CONSTRAINT `networkobject_ptr_id_refs_id_682e9270` FOREIGN KEY (`networkobject_ptr_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_path`
--

LOCK TABLES `topology_path` WRITE;
/*!40000 ALTER TABLE `topology_path` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_path` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_pathproperties`
--

DROP TABLE IF EXISTS `topology_pathproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_pathproperties` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_pathproperties_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_networkobject_ptr_id_2dca54a6` FOREIGN KEY (`parent_id`) REFERENCES `topology_path` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_pathproperties`
--

LOCK TABLES `topology_pathproperties` WRITE;
/*!40000 ALTER TABLE `topology_pathproperties` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_pathproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_periscopedomainproperties`
--

DROP TABLE IF EXISTS `topology_periscopedomainproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_periscopedomainproperties` (
  `domainproperties_ptr_id` int(11) NOT NULL,
  `shape_id` int(11) NOT NULL,
  PRIMARY KEY (`domainproperties_ptr_id`),
  UNIQUE KEY `shape_id` (`shape_id`),
  CONSTRAINT `shape_id_refs_id_dbd6cb2` FOREIGN KEY (`shape_id`) REFERENCES `topology_periscopeshape` (`id`),
  CONSTRAINT `domainproperties_ptr_id_refs_id_75a24086` FOREIGN KEY (`domainproperties_ptr_id`) REFERENCES `topology_domainproperties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_periscopedomainproperties`
--

LOCK TABLES `topology_periscopedomainproperties` WRITE;
/*!40000 ALTER TABLE `topology_periscopedomainproperties` DISABLE KEYS */;
INSERT INTO `topology_periscopedomainproperties` VALUES (1,1);
/*!40000 ALTER TABLE `topology_periscopedomainproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_periscopenodeproperties`
--

DROP TABLE IF EXISTS `topology_periscopenodeproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_periscopenodeproperties` (
  `nodeproperties_ptr_id` int(11) NOT NULL,
  `shape_id` int(11) NOT NULL,
  PRIMARY KEY (`nodeproperties_ptr_id`),
  UNIQUE KEY `shape_id` (`shape_id`),
  CONSTRAINT `shape_id_refs_id_11935d0` FOREIGN KEY (`shape_id`) REFERENCES `topology_periscopeshape` (`id`),
  CONSTRAINT `nodeproperties_ptr_id_refs_id_78388eba` FOREIGN KEY (`nodeproperties_ptr_id`) REFERENCES `topology_nodeproperties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_periscopenodeproperties`
--

LOCK TABLES `topology_periscopenodeproperties` WRITE;
/*!40000 ALTER TABLE `topology_periscopenodeproperties` DISABLE KEYS */;
INSERT INTO `topology_periscopenodeproperties` VALUES (1,2),(2,10),(3,16),(4,19),(5,24),(6,31),(7,36),(8,41);
/*!40000 ALTER TABLE `topology_periscopenodeproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_periscopeportproperties`
--

DROP TABLE IF EXISTS `topology_periscopeportproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_periscopeportproperties` (
  `portproperties_ptr_id` int(11) NOT NULL,
  `shape_id` int(11) NOT NULL,
  PRIMARY KEY (`portproperties_ptr_id`),
  UNIQUE KEY `shape_id` (`shape_id`),
  CONSTRAINT `shape_id_refs_id_3ebab203` FOREIGN KEY (`shape_id`) REFERENCES `topology_periscopeshape` (`id`),
  CONSTRAINT `portproperties_ptr_id_refs_id_5af4681c` FOREIGN KEY (`portproperties_ptr_id`) REFERENCES `topology_portproperties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_periscopeportproperties`
--

LOCK TABLES `topology_periscopeportproperties` WRITE;
/*!40000 ALTER TABLE `topology_periscopeportproperties` DISABLE KEYS */;
INSERT INTO `topology_periscopeportproperties` VALUES (28,3),(29,4),(30,5),(31,6),(32,7),(33,8),(34,9),(35,11),(36,12),(37,13),(38,14),(39,15),(40,17),(41,18),(42,20),(43,21),(44,22),(45,23),(46,25),(47,26),(48,27),(49,28),(50,29),(51,30),(52,32),(53,33),(54,34),(55,35),(56,37),(57,38),(58,39),(59,40),(60,42),(61,43);
/*!40000 ALTER TABLE `topology_periscopeportproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_periscopesavedtopology`
--

DROP TABLE IF EXISTS `topology_periscopesavedtopology`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_periscopesavedtopology` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topo` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_periscopesavedtopology`
--

LOCK TABLES `topology_periscopesavedtopology` WRITE;
/*!40000 ALTER TABLE `topology_periscopesavedtopology` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_periscopesavedtopology` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_periscopeshape`
--

DROP TABLE IF EXISTS `topology_periscopeshape`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_periscopeshape` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shape` varchar(10) NOT NULL,
  `x` int(11) NOT NULL,
  `y` int(11) NOT NULL,
  `width` int(11) NOT NULL,
  `height` int(11) NOT NULL,
  `fill` varchar(20) NOT NULL,
  `text_xdisp` int(11) NOT NULL,
  `text_ydisp` int(11) NOT NULL,
  `text_align` varchar(6) NOT NULL,
  `text_display` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_periscopeshape`
--

LOCK TABLES `topology_periscopeshape` WRITE;
/*!40000 ALTER TABLE `topology_periscopeshape` DISABLE KEYS */;
INSERT INTO `topology_periscopeshape` VALUES (1,'rect',5,5,1070,490,'moccasin',10,20,'left',''),(2,'circle',116,316,40,40,'lightcyan',0,0,'middle','MX80 Router A (NEWY)'),(3,'circle',149,339,5,5,'aliceblue',-10,-10,'middle',''),(4,'circle',156,321,5,5,'aliceblue',-10,-10,'middle',''),(5,'circle',154,303,5,5,'aliceblue',-10,-10,'middle',''),(6,'circle',144,289,5,5,'aliceblue',-10,-10,'middle',''),(7,'circle',132,280,5,5,'aliceblue',-10,-10,'middle',''),(8,'circle',87,289,5,5,'aliceblue',-10,-10,'middle',''),(9,'circle',111,277,5,5,'aliceblue',-10,-10,'middle',''),(10,'circle',295,122,40,40,'lightcyan',0,0,'middle','RDMA Diskpt A (NEWY)'),(11,'circle',261,102,5,5,'aliceblue',-10,-10,'middle',''),(12,'circle',277,88,5,5,'aliceblue',-10,-10,'middle',''),(13,'circle',269,153,5,5,'aliceblue',-10,-10,'middle',''),(14,'circle',285,160,5,5,'aliceblue',-10,-10,'middle',''),(15,'circle',259,140,5,5,'aliceblue',-10,-10,'middle',''),(16,'circle',150,169,40,40,'lightcyan',0,0,'middle','VM Application Node (NEWY)'),(17,'circle',114,150,5,5,'aliceblue',-10,-10,'middle',''),(18,'circle',143,208,5,5,'aliceblue',-10,-10,'middle',''),(19,'circle',55,113,40,40,'lightcyan',0,0,'middle','OpenFlow NEC A (NEWY)'),(20,'circle',92,100,5,5,'aliceblue',-10,-10,'middle',''),(21,'circle',83,85,5,5,'aliceblue',-10,-10,'middle',''),(22,'circle',56,153,5,5,'aliceblue',-10,-10,'middle',''),(23,'circle',90,131,5,5,'aliceblue',-10,-10,'middle',''),(24,'circle',831,197,40,40,'lightcyan',0,0,'middle','MX80 Router B (BNL)'),(25,'circle',801,223,5,5,'aliceblue',-10,-10,'middle',''),(26,'circle',791,203,5,5,'aliceblue',-10,-10,'middle',''),(27,'circle',831,157,5,5,'aliceblue',-10,-10,'middle',''),(28,'circle',858,167,5,5,'aliceblue',-10,-10,'middle',''),(29,'circle',871,197,5,5,'aliceblue',-10,-10,'middle',''),(30,'circle',831,237,5,5,'aliceblue',-10,-10,'middle',''),(31,'circle',998,342,40,40,'lightcyan',0,0,'middle','RDMA DiskPT B (BNL)'),(32,'circle',998,302,5,5,'aliceblue',-10,-10,'middle',''),(33,'circle',962,326,5,5,'aliceblue',-10,-10,'middle',''),(34,'circle',962,359,5,5,'aliceblue',-10,-10,'middle',''),(35,'circle',958,342,5,5,'aliceblue',-10,-10,'middle',''),(36,'circle',832,342,40,40,'lightcyan',0,0,'middle','RDMA DiskPT C (BNL)'),(37,'circle',868,325,5,5,'aliceblue',-10,-10,'middle',''),(38,'circle',869,358,5,5,'aliceblue',-10,-10,'middle',''),(39,'circle',872,342,5,5,'aliceblue',-10,-10,'middle',''),(40,'circle',832,302,5,5,'aliceblue',-10,-10,'middle',''),(41,'circle',998,197,40,40,'lightcyan',0,0,'middle','OpenFlow NEC B2 (BNL)'),(42,'circle',958,197,5,5,'aliceblue',-10,-10,'middle',''),(43,'circle',998,237,5,5,'aliceblue',-10,-10,'middle','');
/*!40000 ALTER TABLE `topology_periscopeshape` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_port`
--

DROP TABLE IF EXISTS `topology_port`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_port` (
  `networkobject_ptr_id` int(11) NOT NULL,
  `capacity` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`networkobject_ptr_id`),
  CONSTRAINT `networkobject_ptr_id_refs_id_200c7e4` FOREIGN KEY (`networkobject_ptr_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_port`
--

LOCK TABLES `topology_port` WRITE;
/*!40000 ALTER TABLE `topology_port` DISABLE KEYS */;
INSERT INTO `topology_port` VALUES (4,'10000000000'),(6,'10000000000'),(8,'10000000000'),(10,'10000000000'),(13,'10000000000'),(15,'10000000000'),(17,'10000000000'),(19,'10000000000'),(22,'10000000000'),(24,'10000000000'),(27,'10000000000'),(29,'10000000000'),(31,'10000000000'),(33,'10000000000'),(35,'1000000000'),(37,'1000000000'),(40,'1000000000'),(42,'1000000000'),(45,'1000000000'),(47,'1000000000'),(49,'10000000000'),(51,'10000000000'),(54,'1000000000'),(56,'10000000000'),(58,'10000000000'),(60,'10000000000'),(62,'10000000000'),(65,'10000000000'),(67,'10000000000'),(69,'10000000000'),(71,'10000000000'),(73,'10000000000'),(75,'10000000000'),(77,'1000000000'),(79,NULL);
/*!40000 ALTER TABLE `topology_port` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_portaddresses`
--

DROP TABLE IF EXISTS `topology_portaddresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_portaddresses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `port_id` int(11) NOT NULL,
  `address_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `address_id` (`address_id`),
  KEY `topology_portaddresses_3af60259` (`port_id`),
  CONSTRAINT `address_id_refs_id_6cecc542` FOREIGN KEY (`address_id`) REFERENCES `topology_address` (`id`),
  CONSTRAINT `port_id_refs_networkobject_ptr_id_188d08e` FOREIGN KEY (`port_id`) REFERENCES `topology_port` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_portaddresses`
--

LOCK TABLES `topology_portaddresses` WRITE;
/*!40000 ALTER TABLE `topology_portaddresses` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_portaddresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_portproperties`
--

DROP TABLE IF EXISTS `topology_portproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_portproperties` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_portproperties_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_networkobject_ptr_id_338a6c2` FOREIGN KEY (`parent_id`) REFERENCES `topology_port` (`networkobject_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_portproperties`
--

LOCK TABLES `topology_portproperties` WRITE;
/*!40000 ALTER TABLE `topology_portproperties` DISABLE KEYS */;
INSERT INTO `topology_portproperties` VALUES (1,4),(55,4),(2,6),(54,6),(3,8),(53,8),(4,10),(52,10),(5,13),(58,13),(6,15),(57,15),(7,17),(56,17),(8,19),(59,19),(9,22),(61,22),(10,24),(60,24),(11,27),(47,27),(12,29),(46,29),(13,31),(51,31),(14,33),(50,33),(15,35),(49,35),(16,37),(48,37),(40,40),(17,42),(41,42),(45,45),(43,47),(42,49),(18,51),(44,51),(36,54),(35,56),(19,58),(39,58),(20,60),(37,60),(21,62),(38,62),(22,65),(29,65),(28,67),(23,69),(32,69),(24,71),(31,71),(25,73),(30,73),(26,75),(33,75),(27,77),(34,77);
/*!40000 ALTER TABLE `topology_portproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_pshopproperties`
--

DROP TABLE IF EXISTS `topology_pshopproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_pshopproperties` (
  `hopproperties_ptr_id` int(11) NOT NULL,
  `number` int(10) unsigned NOT NULL,
  PRIMARY KEY (`hopproperties_ptr_id`),
  CONSTRAINT `hopproperties_ptr_id_refs_id_1384df68` FOREIGN KEY (`hopproperties_ptr_id`) REFERENCES `topology_hopproperties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_pshopproperties`
--

LOCK TABLES `topology_pshopproperties` WRITE;
/*!40000 ALTER TABLE `topology_pshopproperties` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_pshopproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_psserviceproperties`
--

DROP TABLE IF EXISTS `topology_psserviceproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_psserviceproperties` (
  `serviceproperties_ptr_id` int(11) NOT NULL,
  `serviceName` varchar(255) DEFAULT NULL,
  `accessPoint` varchar(255) NOT NULL,
  `serviceType` varchar(255) NOT NULL,
  `serviceDescription` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`serviceproperties_ptr_id`),
  CONSTRAINT `serviceproperties_ptr_id_refs_id_61f5b0e0` FOREIGN KEY (`serviceproperties_ptr_id`) REFERENCES `topology_serviceproperties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_psserviceproperties`
--

LOCK TABLES `topology_psserviceproperties` WRITE;
/*!40000 ALTER TABLE `topology_psserviceproperties` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_psserviceproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_psservicepropertieseventtypes`
--

DROP TABLE IF EXISTS `topology_psservicepropertieseventtypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_psservicepropertieseventtypes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `psServiceProperties_id` int(11) NOT NULL,
  `eventtype_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_psservicepropertieseventtypes_2bc08890` (`psServiceProperties_id`),
  KEY `topology_psservicepropertieseventtypes_4d577e01` (`eventtype_id`),
  CONSTRAINT `eventtype_id_refs_id_5c06e83d` FOREIGN KEY (`eventtype_id`) REFERENCES `topology_eventtype` (`id`),
  CONSTRAINT `psServiceProperties_id_refs_serviceproperties_ptr_id_c896d08` FOREIGN KEY (`psServiceProperties_id`) REFERENCES `topology_psserviceproperties` (`serviceproperties_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_psservicepropertieseventtypes`
--

LOCK TABLES `topology_psservicepropertieseventtypes` WRITE;
/*!40000 ALTER TABLE `topology_psservicepropertieseventtypes` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_psservicepropertieseventtypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_psservicewatchlist`
--

DROP TABLE IF EXISTS `topology_psservicewatchlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_psservicewatchlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11) NOT NULL,
  `event_type_id` int(11) NOT NULL,
  `network_object_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `service_id` (`service_id`,`event_type_id`,`network_object_id`),
  KEY `topology_psservicewatchlist_6f1d73c2` (`service_id`),
  KEY `topology_psservicewatchlist_349f2f81` (`event_type_id`),
  KEY `topology_psservicewatchlist_26093e` (`network_object_id`),
  CONSTRAINT `event_type_id_refs_id_21fa1059` FOREIGN KEY (`event_type_id`) REFERENCES `topology_eventtype` (`id`),
  CONSTRAINT `network_object_id_refs_id_34f4565e` FOREIGN KEY (`network_object_id`) REFERENCES `topology_networkobject` (`id`),
  CONSTRAINT `service_id_refs_networkobject_ptr_id_3e7765e6` FOREIGN KEY (`service_id`) REFERENCES `topology_service` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_psservicewatchlist`
--

LOCK TABLES `topology_psservicewatchlist` WRITE;
/*!40000 ALTER TABLE `topology_psservicewatchlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_psservicewatchlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_relation`
--

DROP TABLE IF EXISTS `topology_relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `type` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_relation_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_id_698cac41` FOREIGN KEY (`parent_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_relation`
--

LOCK TABLES `topology_relation` WRITE;
/*!40000 ALTER TABLE `topology_relation` DISABLE KEYS */;
INSERT INTO `topology_relation` VALUES (1,5,'pair'),(2,5,'sink'),(3,5,'source'),(4,7,'pair'),(5,7,'sink'),(6,7,'source'),(7,9,'pair'),(8,9,'sink'),(9,9,'source'),(10,11,'pair'),(11,11,'sink'),(12,11,'source'),(13,14,'pair'),(14,14,'sink'),(15,14,'source'),(16,16,'pair'),(17,16,'sink'),(18,16,'source'),(19,18,'pair'),(20,18,'sink'),(21,18,'source'),(22,20,'pair'),(23,20,'sink'),(24,20,'source'),(25,23,'pair'),(26,23,'sink'),(27,23,'source'),(28,25,'pair'),(29,25,'sink'),(30,25,'source'),(31,28,'pair'),(32,28,'sink'),(33,28,'source'),(34,30,'pair'),(35,30,'sink'),(36,30,'source'),(37,32,'pair'),(38,32,'sink'),(39,32,'source'),(40,34,'pair'),(41,34,'sink'),(42,34,'source'),(43,36,'sink'),(44,36,'source'),(45,38,'sink'),(46,38,'source'),(47,41,'pair'),(48,41,'sink'),(49,41,'source'),(50,43,'pair'),(51,43,'sink'),(52,43,'source'),(53,46,'pair'),(54,46,'sink'),(55,46,'source'),(56,48,'pair'),(57,48,'sink'),(58,48,'source'),(59,50,'pair'),(60,50,'sink'),(61,50,'source'),(62,52,'pair'),(63,52,'sink'),(64,52,'source'),(65,55,'pair'),(66,55,'sink'),(67,55,'source'),(68,57,'pair'),(69,57,'sink'),(70,57,'source'),(71,58,'pair'),(72,59,'sink'),(73,59,'source'),(74,61,'pair'),(75,61,'sink'),(76,61,'source'),(77,63,'pair'),(78,63,'sink'),(79,63,'source'),(80,66,'pair'),(81,66,'sink'),(82,66,'source'),(83,68,'pair'),(84,68,'sink'),(85,68,'source'),(86,70,'pair'),(87,70,'sink'),(88,70,'source'),(89,72,'pair'),(90,72,'sink'),(91,72,'source'),(92,74,'pair'),(93,74,'sink'),(94,74,'source'),(95,76,'pair'),(96,76,'sink'),(97,76,'source'),(98,78,'pair'),(99,78,'sink'),(100,78,'source');
/*!40000 ALTER TABLE `topology_relation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_relation_targets`
--

DROP TABLE IF EXISTS `topology_relation_targets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_relation_targets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `relation_id` int(11) NOT NULL,
  `networkobject_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `relation_id` (`relation_id`,`networkobject_id`),
  KEY `topology_relation_targets_46154868` (`relation_id`),
  KEY `topology_relation_targets_1646de4a` (`networkobject_id`),
  CONSTRAINT `networkobject_id_refs_id_6de27606` FOREIGN KEY (`networkobject_id`) REFERENCES `topology_networkobject` (`id`),
  CONSTRAINT `relation_id_refs_id_47da76ba` FOREIGN KEY (`relation_id`) REFERENCES `topology_relation` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_relation_targets`
--

LOCK TABLES `topology_relation_targets` WRITE;
/*!40000 ALTER TABLE `topology_relation_targets` DISABLE KEYS */;
INSERT INTO `topology_relation_targets` VALUES (19,1,14),(28,2,13),(79,3,4),(83,4,16),(1,5,15),(24,6,6),(38,7,18),(2,8,17),(26,9,8),(70,10,23),(43,11,22),(94,12,10),(11,13,80),(96,14,4),(31,15,13),(63,16,82),(29,17,6),(98,18,15),(82,19,9),(88,20,8),(57,21,17),(56,22,32),(81,23,31),(15,24,19),(61,25,11),(4,26,10),(3,27,22),(51,28,34),(16,29,33),(75,30,24),(54,31,66),(37,32,65),(67,33,27),(77,34,68),(55,35,67),(59,36,29),(66,37,20),(36,38,19),(84,39,31),(80,40,25),(10,41,24),(33,42,33),(5,43,79),(12,44,35),(78,45,79),(73,46,37),(87,47,46),(44,48,45),(45,49,40),(35,51,77),(72,52,42),(71,53,41),(60,54,40),(32,55,45),(92,56,83),(21,57,54),(52,58,47),(42,59,57),(65,60,56),(58,61,49),(62,62,76),(34,63,75),(14,64,51),(13,65,48),(49,66,47),(23,67,54),(46,68,50),(90,69,49),(93,70,56),(6,71,70),(53,72,69),(50,73,58),(48,74,61),(91,75,71),(22,76,60),(9,77,74),(41,78,73),(69,79,62),(18,80,28),(40,81,27),(8,82,65),(95,83,30),(7,84,29),(76,85,67),(89,86,59),(17,87,58),(68,88,69),(64,89,72),(39,90,60),(86,91,71),(30,92,63),(47,93,62),(27,94,73),(25,95,81),(97,96,51),(85,97,75),(20,99,42),(74,100,77);
/*!40000 ALTER TABLE `topology_relation_targets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_relationproperty`
--

DROP TABLE IF EXISTS `topology_relationproperty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_relationproperty` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_relationproperty_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_id_620f0dfe` FOREIGN KEY (`parent_id`) REFERENCES `topology_relation` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_relationproperty`
--

LOCK TABLES `topology_relationproperty` WRITE;
/*!40000 ALTER TABLE `topology_relationproperty` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_relationproperty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_role`
--

DROP TABLE IF EXISTS `topology_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_role`
--

LOCK TABLES `topology_role` WRITE;
/*!40000 ALTER TABLE `topology_role` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_service`
--

DROP TABLE IF EXISTS `topology_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_service` (
  `networkobject_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`networkobject_ptr_id`),
  CONSTRAINT `networkobject_ptr_id_refs_id_7be104f5` FOREIGN KEY (`networkobject_ptr_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_service`
--

LOCK TABLES `topology_service` WRITE;
/*!40000 ALTER TABLE `topology_service` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_serviceproperties`
--

DROP TABLE IF EXISTS `topology_serviceproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_serviceproperties` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_serviceproperties_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_networkobject_ptr_id_6cc22d34` FOREIGN KEY (`parent_id`) REFERENCES `topology_service` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_serviceproperties`
--

LOCK TABLES `topology_serviceproperties` WRITE;
/*!40000 ALTER TABLE `topology_serviceproperties` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_serviceproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_timeseriesdata`
--

DROP TABLE IF EXISTS `topology_timeseriesdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_timeseriesdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `target_id` int(11) NOT NULL,
  `eventType` varchar(255) NOT NULL,
  `time` datetime NOT NULL,
  `value` decimal(23,5) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_timeseriesdata_6ca73769` (`target_id`),
  CONSTRAINT `target_id_refs_id_13bd3875` FOREIGN KEY (`target_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_timeseriesdata`
--

LOCK TABLES `topology_timeseriesdata` WRITE;
/*!40000 ALTER TABLE `topology_timeseriesdata` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_timeseriesdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_topology`
--

DROP TABLE IF EXISTS `topology_topology`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_topology` (
  `networkobject_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`networkobject_ptr_id`),
  CONSTRAINT `networkobject_ptr_id_refs_id_5c257db6` FOREIGN KEY (`networkobject_ptr_id`) REFERENCES `topology_networkobject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_topology`
--

LOCK TABLES `topology_topology` WRITE;
/*!40000 ALTER TABLE `topology_topology` DISABLE KEYS */;
INSERT INTO `topology_topology` VALUES (1);
/*!40000 ALTER TABLE `topology_topology` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_topologyproperties`
--

DROP TABLE IF EXISTS `topology_topologyproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_topologyproperties` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topology_topologyproperties_63f17a16` (`parent_id`),
  CONSTRAINT `parent_id_refs_networkobject_ptr_id_39f07d5a` FOREIGN KEY (`parent_id`) REFERENCES `topology_topology` (`networkobject_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_topologyproperties`
--

LOCK TABLES `topology_topologyproperties` WRITE;
/*!40000 ALTER TABLE `topology_topologyproperties` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_topologyproperties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topology_tpsportproperties`
--

DROP TABLE IF EXISTS `topology_tpsportproperties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topology_tpsportproperties` (
  `portproperties_ptr_id` int(11) NOT NULL,
  `vlan` varchar(6) DEFAULT NULL,
  `subnet` varchar(50) DEFAULT NULL,
  `base_ip` varchar(50) DEFAULT NULL,
  `subnet_mask` varchar(50) DEFAULT NULL,
  `ip_a` varchar(50) DEFAULT NULL,
  `ip_b` varchar(50) DEFAULT NULL,
  `broadcast_ip` varchar(50) DEFAULT NULL,
  `available` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`portproperties_ptr_id`),
  CONSTRAINT `portproperties_ptr_id_refs_id_3482366f` FOREIGN KEY (`portproperties_ptr_id`) REFERENCES `topology_portproperties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topology_tpsportproperties`
--

LOCK TABLES `topology_tpsportproperties` WRITE;
/*!40000 ALTER TABLE `topology_tpsportproperties` DISABLE KEYS */;
/*!40000 ALTER TABLE `topology_tpsportproperties` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-10-17  9:47:52
