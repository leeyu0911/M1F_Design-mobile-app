insert into class(CName, `Type`, nLevel) values('root', 1, 1);
insert into class(CName, `Type`, nLevel) values('學校', 1, 2);
insert into class(CName, `Type`, nLevel) values('成大', 1, 3);
insert into class(CName, `Type`, nLevel) values('資工系', 1, 4);

insert into inheritance(PCID, CCID) values(1, 2);
insert into inheritance(PCID, CCID) values(2, 3);
insert into inheritance(PCID, CCID) values(3, 4);