DROP TABLE chat_user;

CREATE TABLE chat_user (
    id      INTEGER       PRIMARY KEY AUTOINCREMENT,
    sid     INT,
    name    VARCHAR (40)  NOT NULL
                          DEFAULT "",
    passwd  VARCHAR (40)  DEFAULT ""
                          NOT NULL,
    sex     INTEGER (1)   NOT NULL
                          DEFAULT (1),
    score   INTEGER       NOT NULL
                          DEFAULT (0),
    grade   INTEGER       DEFAULT (0) 
                          NOT NULL,
    phone   VARCHAR (40)  NOT NULL
                          DEFAULT "",
    devid   VARCHAR (80)  DEFAULT ""
                          NOT NULL,
    country VARCHAR (100) DEFAULT ""
                          NOT NULL,
    city    VARCHAR (100) DEFAULT ""
                          NOT NULL,
    ctime   INTEGER       DEFAULT (0) 
                          NOT NULL,
    utime   INTEGER       NOT NULL
                          DEFAULT (0),
    ltime   INTEGER       NOT NULL
                          DEFAULT (0),
    status  INTEGER (1)   DEFAULT (1) 
                          NOT NULL
);