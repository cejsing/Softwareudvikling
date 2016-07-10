CREATE DATABASE cafeensvarer;

 
-- Used for individual items in stock
CREATE TABLE wares (wareid INT(8) AUTO_INCREMENT PRIMARY KEY, warename VARCHAR(15), inbar INT(5), instockroom INT(5));


-- Used for grouping items in eg light/luxury-beer, snacks and so on
CREATE TABLE waregroups (wgid INT(6) AUTO_INCREMENT PRIMARY KEY, wgname VARCHAR(15), wgdescription VARCHAR(30));

-- Relevant because different eventtypes have different prices
CREATE TABLE events (eventid INT(4) AUTO_INCREMENT PRIMARY KEY, eventname VARCHAR(15), eventdescription VARCHAR(30));

-- Relations
-- Unsure if correct relation syntax


-- makes it possible for each ware to be a member of several groups. Is this smart?
CREATE TABLE waresingroups (wareid FOREIGN KEY REFERENCES wares(wareid), wgid FOREIGN KEY REFERENCES waregroups(wgid));

-- lists prices for all items for each event. It might be a good idea to have a fallback 'standard' event. 
CREATE TABLE pricesinevents (wareID FOREIGN KEY REFERENCES wares(wareid), eventid FOREIGN KEY REFERENCES events(eventid));



CREATE DATABASE cafeenshistorik;

-- first implementation/suggestion for keeping a record of changes. Does not make it easy to pull the data for later manipulation. A different approach could be to have a history for each table.
CREATE TABLE history (hisid int(11) AUTO_INCREMENT PRIMARY KEY, changedtable VARCHAR(15), affectsid INT(8), changedvalue VARCHAR(45), from VARCHAR(45), to VARCHAR());







CREATE DATABASE cafeensbrugere;

-- Used for login and management of priviliges
CREATE TABLE users (uid INT(8) AUTO_INCREMENT PRIMARY KEY, name VARCHAR(35), email VARCHAR(35), titel VARCHAR(15));

-- List of possible permissions for management of priviliges
CREATE TABLE rights (rightsid INT(3) AUTO_INCREMENT PRIMARY KEY, accessname VARCHAR(15));


-- Relations

-- Can be used to test if a given user is allowed to do what they are trying to do
CREATE table userrights (uid FOREIGN KEY REFERENCES users(uid), rightsid FOREIGN KEY REFERENCES rights(rightsid));