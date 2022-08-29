CREATE USER yuvraj with encrypted password 'postgres';
CREATE DATABASE users;
GRANT ALL PRIVILEGES ON DATABASE users TO yuvraj;
