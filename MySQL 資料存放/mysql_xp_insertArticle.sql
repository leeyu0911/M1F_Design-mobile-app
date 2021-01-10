DROP PROCEDURE IF EXISTS xp_insertArticle;
DELIMITER //

CREATE PROCEDURE xp_insertArticle(IN _CID int, IN _articleURL nvarchar(5000), IN _Title nvarchar(500), IN _URL nvarchar(5000), IN _Content text, IN `_Type` nvarchar(100), IN `_Status` nvarchar(100), IN _Author nvarchar(100), IN _Since nvarchar(100))
BEGIN
	declare myoid int;
    
    start transaction;
    insert into object(`type`) values(1);
    set myoid = last_insert_id();
    insert into article(AID, articleURL, Title, URL, Content, `Type`, `Status`, Author, Since) values(myoid, _articleURL, _Title,  _URL, _Content, `_Type`, `_Status`, _Author, _Since);
    insert into co(CID, OID) values(_CID, myoid);
    commit;
    
    select myoid;
END
//
DELIMITER ;