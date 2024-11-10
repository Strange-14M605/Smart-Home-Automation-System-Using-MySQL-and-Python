-- Drop database if exists and create new one
DROP DATABASE IF EXISTS smart_home;
CREATE DATABASE smart_home;

USE smart_home;

CREATE TABLE User (
    user_ID VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    mobile VARCHAR(15),
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20),
    dob DATE
);

CREATE TABLE Device (
    device_ID VARCHAR(10) PRIMARY KEY,
    status VARCHAR(20),
    name VARCHAR(50),
    model VARCHAR(50),
    version VARCHAR(20)
);

CREATE TABLE Logs (
    log_ID INT AUTO_INCREMENT PRIMARY KEY,
    device_ID VARCHAR(10),
    date DATE,
    time TIME,
    duration INT,
    FOREIGN KEY (device_ID) REFERENCES Device(device_ID)
);

CREATE TABLE Automation (
    automation_ID VARCHAR(10) PRIMARY KEY,
    device_ID VARCHAR(10),
    user_ID VARCHAR(10),
    start_time TIME,
    end_time TIME,
    FOREIGN KEY (device_ID) REFERENCES Device(device_ID),
    FOREIGN KEY (user_ID) REFERENCES User(user_ID)
);

CREATE TABLE Maintenance (
    session_ID VARCHAR(10) PRIMARY KEY,
    device_ID VARCHAR(10),
    date DATE,
    issue_reported TEXT,
    next_maintenance_date DATE,
    FOREIGN KEY (device_ID) REFERENCES Device(device_ID)
);

INSERT INTO User (user_ID, name, mobile, password, role, dob) VALUES
('U001', 'Alice Johnson', '123-456-7890', 'password1', 'Admin', '1985-01-15'),
('U002', 'Bob Smith', '123-456-7891', 'password2', 'User', '1990-02-20'),
('U003', 'Charlie Brown', '123-456-7892', 'password3', 'User', '1992-03-25');

INSERT INTO Device (device_ID, status, name, model, version) VALUES
('D001', 'Active', 'Thermostat', 'Model X', '1.0'),
('D002', 'Inactive', 'Security Camera', 'Model Y', '2.1'),
('D003', 'Active', 'Smart Light', 'Model Z', '1.5');

INSERT INTO Logs (device_ID, date, time, duration) VALUES
('D001', '2023-10-25', '08:00:00', 120),
('D002', '2023-10-25', '09:30:00', 45),
('D003', '2023-10-25', '10:00:00', 60);

INSERT INTO Automation (automation_ID, device_ID, user_ID, start_time, end_time) VALUES
('A001', 'D001', 'U001', '06:00:00', '08:00:00'),
('A002', 'D002', 'U002', '09:00:00', '11:00:00'),
('A003', 'D003', 'U003', '17:00:00', '19:00:00');

INSERT INTO Maintenance (session_ID, device_ID, date, issue_reported, next_maintenance_date) VALUES
('M001', 'D001', '2023-10-20', 'Battery issue', '2023-12-20'),
('M002', 'D002', '2023-10-21', 'Connectivity issue', '2024-01-21'),
('M003', 'D003', '2023-10-22', 'Firmware update needed', '2024-01-22');

DELIMITER //

-- FUNCTION
CREATE FUNCTION authenticate_user(user_id VARCHAR(50), user_password VARCHAR(50))
RETURNS VARCHAR(50)
DETERMINISTIC
BEGIN
    DECLARE user_role VARCHAR(50);
    
    SELECT role INTO user_role
    FROM User
    WHERE user_ID = user_id AND password = user_password;
    
    RETURN user_role;  -- Returns the user role or NULL if not found
END //

DELIMITER ;



-- TRIGGERS
DELIMITER //

CREATE TRIGGER after_device_deactivate
AFTER UPDATE ON Device
FOR EACH ROW
BEGIN
    DECLARE total_seconds INT DEFAULT 0;
    DECLARE total_minutes INT DEFAULT 0;
    DECLARE last_log_time DATETIME;

    IF NEW.status IN ('inactive', 'off') AND OLD.status IN ('active', 'on') THEN
        SELECT CONCAT(date, ' ', time) INTO last_log_time 
        FROM Logs 
        WHERE device_ID = OLD.device_ID 
        ORDER BY log_ID DESC LIMIT 1;

        SET total_seconds = TIMESTAMPDIFF(SECOND, last_log_time, NOW());
        SET total_minutes = FLOOR(total_seconds / 60);

        UPDATE Logs
        SET duration = total_minutes
        WHERE device_ID = OLD.device_ID
        ORDER BY log_ID DESC LIMIT 1;
    END IF;
END //

CREATE TRIGGER before_device_activate
BEFORE UPDATE ON Device
FOR EACH ROW
BEGIN
    IF NEW.status IN ('active', 'on') AND OLD.status NOT IN ('active', 'on') THEN
        -- Insert a log entry with current timestamp for the duration
        INSERT INTO Logs (device_ID, date, time, duration)
        VALUES (NEW.device_ID, CURDATE(), CURTIME(), 0);
    END IF;
END //

DELIMITER ;