ALTER TABLE FB.torrent MODIFY COLUMN releaser VARCHAR(255)  CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
ALTER TABLE FB.torrent MODIFY COLUMN torr_name VARCHAR(255)  CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
ALTER TABLE FB.torrent MODIFY COLUMN category VARCHAR(255)  CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

ALTER TABLE ani_torr.Anime MODIFY COLUMN name VARCHAR(50)  CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
ALTER TABLE ani_torr.Releaser MODIFY COLUMN name VARCHAR(50)  CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

DELETE FROM `Record` WHERE 1;
DELETE FROM `upload` WHERE 1;
DELETE FROM `Torrent` WHERE 1;