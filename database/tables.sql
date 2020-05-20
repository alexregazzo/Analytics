CREATE TABLE IF NOT EXISTS `track`
(
    `tra_hash`        TEXT    NOT NULL PRIMARY KEY,
    `tra_total_tries` INTEGER NOT NULL,
    `tra_first_time`  TEXT    NOT NULL,
    `tra_last_time`   TEXT    NOT NULL,
    `tra_origin`      TEXT    NOT NULL,
    `tra_user_agent`  TEXT    NOT NULL,
    `tra_ip`          TEXT    NOT NULL,
    `pat_id_last`     INTEGER NULL,

    FOREIGN KEY (`pat_id_last`) REFERENCES `path` (`pat_id`)
);

CREATE TABLE IF NOT EXISTS `path`
(
    `pat_id`         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `tra_hash`       TEXT    NOT NULL,
    `pat_href`       TEXT    NOT NULL,
    `pat_first_time` TEXT    NOT NULL,
    `pat_last_time`  TEXT    NOT NULL,
    FOREIGN KEY (`tra_hash`) REFERENCES `track` (`tra_hash`)
);