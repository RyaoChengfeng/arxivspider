USE bingyanproject0;
DROP TABLE IF EXISTS documents;
CREATE TABLE documents(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL ,
    number VARCHAR(255) NOT NULL ,
    author VARCHAR(255) NOT NULL ,
    time VARCHAR(255) NOT NULL ,
    subject VARCHAR(255) NOT NULL ,
    url_pdf VARCHAR(255)
);

