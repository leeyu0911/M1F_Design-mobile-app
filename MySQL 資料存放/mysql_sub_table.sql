use subscriptApp;

create table class
(
	CID int AUTO_INCREMENT,
	`Type` smallint null,
	CName nvarchar(100) null,
	CDes nvarchar(500) null,
	EName varchar(100) null,
	EDes varchar(500) null,
	IDpath varchar(1000) null,
	Namepath nvarchar(1000) null,
	Since datetime default now(),
	LastModifyDT datetime null,
	nLevel smallint null,
	nObject int default 0,
	nClick int default 0,
	constraint PK_Class primary key clustered (CID)
);

create table inheritance
(
	PCID int not null,
	CCID int not null,
	constraint FK_Inheritance_PCID foreign key(PCID) references class(CID),
	constraint FK_Inheritance_CCID foreign key(CCID) references class(CID),
	constraint PK_Inheritance primary key clustered (PCID, CCID)
);

create table object
(
	OID int AUTO_INCREMENT,
	`Type` smallint null,
	nClick int default 0,
	Since datetime default now(),
	constraint PK_Object primary key clustered (OID)
);

create table co
(
	CID int not null,
	OID int not null,
	constraint FK_CO_CID foreign key(CID) references class(CID),
	constraint FK_CO_OID foreign key(OID) references object(OID),
	constraint PK_CO primary key clustered (CID, OID)
);