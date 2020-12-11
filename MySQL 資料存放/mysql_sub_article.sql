create table article
(
	AID int not null,
	Title nvarchar(500) null,
    URL nvarchar(5000) null,
	Content text,
	`Type` nvarchar(100) null,
	`Status` nvarchar(100) null,
    Author nvarchar(100) null,
    Since nvarchar(100) null,
	
	constraint FK_Article_AID foreign key(AID) references object(OID),
	constraint PK_Article primary key clustered (AID)
);

create table `file`
(
	FID int AUTO_INCREMENT,
    AID int not null,
	FileName nvarchar(500) null,
    UploadDate nvarchar(100) null,
    FileURL nvarchar(5000) null,
    
    constraint FK_File_AID foreign key(AID) references article(AID),
	constraint PK_File primary key clustered (FID)
);