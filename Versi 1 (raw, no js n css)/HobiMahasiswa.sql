/* Dibuat oleh Galih Hermawan (https://galih.eu) */
CREATE DATABASE IF NOT EXISTS `proyek_hobimahasiswa`;

USE `proyek_hobimahasiswa`;

/*Table structure for table `hobi` */

DROP TABLE IF EXISTS `hobi`;

CREATE TABLE `hobi` (
  `kodehobi` tinyint(2) NOT NULL,
  `namahobi` varchar(20) NOT NULL,
  PRIMARY KEY (`kodehobi`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;

/*Data for the table `hobi` */

insert  into `hobi`(`kodehobi`,`namahobi`) values (1,'Game'),(2,'Sepak bola'),(3,'Basket'),(4,'Musik'),(5,'Membaca'),(6,'Tidur'),(7,'Koding'),(8,'Renang'),(9,'Travelling'),(10,'Makan');

/*Table structure for table `mahasiswa` */

DROP TABLE IF EXISTS `mahasiswa`;

CREATE TABLE `mahasiswa` (
  `nim` char(2) NOT NULL,
  `nama` varchar(30) NOT NULL,
  `tempat_lahir` varchar(30) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `kota` varchar(30) DEFAULT NULL,
  `tanggal_masuk` date DEFAULT NULL,
  `tinggi_badan` tinyint(4) unsigned DEFAULT NULL,
  PRIMARY KEY (`nim`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;

/*Data for the table `mahasiswa` */

insert  into `mahasiswa`(`nim`,`nama`,`tempat_lahir`,`tanggal_lahir`,`kota`,`tanggal_masuk`,`tinggi_badan`) values ('1','Adi','Malang','1990-01-01','bandung','2009-08-01',170),('2','Astri','Jakarta','1990-01-02','bandung','2009-08-01',165),('3','Atep','Bandung','1989-12-12','jakarta','2009-08-01',169),('4','Rudi','Surabaya','1991-03-02','bandung','2009-08-01',172),('5','Indah','Jakarta','1992-12-02','jakarta','2009-08-01',158),('6','Rully','Surabaya','1992-04-05','bandung','2009-08-01',170);

/*Table structure for table `mhshobi` */

DROP TABLE IF EXISTS `mhshobi`;

CREATE TABLE `mhshobi` (
  `nim` char(2) DEFAULT NULL,
  `kodehobi` tinyint(2) DEFAULT NULL,
  KEY `FK_mhshobi` (`kodehobi`),
  KEY `FK_mhshobi2` (`nim`),
  CONSTRAINT `FK_mhshobi` FOREIGN KEY (`kodehobi`) REFERENCES `hobi` (`kodehobi`),
  CONSTRAINT `FK_mhshobi2` FOREIGN KEY (`nim`) REFERENCES `mahasiswa` (`nim`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;

/*Data for the table `mhshobi` */

insert  into `mhshobi`(`nim`,`kodehobi`) values ('1',1),('1',2),('1',3),('2',1),('2',5),('3',10),('3',2),('4',2),('4',4),('4',7),('5',9),('5',1),('5',8);
