DROP DATABASE IF EXISTS digihub2postgre;
DROP USER IF EXISTS "Jayson";

CREATE USER "Jayson" WITH PASSWORD 'iwzhia_.21';
CREATE DATABASE digihub2postgre OWNER "Jayson";
GRANT ALL PRIVILEGES ON DATABASE digihub2postgre TO "Jayson";




