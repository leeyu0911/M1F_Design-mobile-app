DROP PROCEDURE IF EXISTS xp_insertFile;
DELIMITER //

CREATE PROCEDURE xp_insertFile(IN _AID int, IN _FileName nvarchar(500), IN _UploadDate nvarchar(100), IN _FileURL nvarchar(5000))
BEGIN
    insert into `file`(AID, FileName, UploadDate, FileURL) values(_AID, _FileName, _UploadDate, _FileURL);
END
//
DELIMITER ;