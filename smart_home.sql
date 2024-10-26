-- Drop database if exists and create new one
DROP DATABASE IF EXISTS smart_home;
CREATE DATABASE smart_home;

-- Make sure to select the database
USE smart_home;
-- Create User table
CREATE TABLE User (
    user_ID VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    mobile VARCHAR(15),
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20),
    dob DATE
);

-- Create Device table
CREATE TABLE Device (
    device_ID VARCHAR(10) PRIMARY KEY,
    status VARCHAR(20),
    name VARCHAR(50),
    model VARCHAR(50),
    version VARCHAR(20)
);

-- Create Logs table
CREATE TABLE Logs (
    log_ID INT AUTO_INCREMENT PRIMARY KEY,
    device_ID VARCHAR(10),
    date DATE,
    time TIME,
    duration INT,
    FOREIGN KEY (device_ID) REFERENCES Device(device_ID)
);


-- Create Automation table
CREATE TABLE Automation (
    automation_ID VARCHAR(10) PRIMARY KEY,
    device_ID VARCHAR(10),
    user_ID VARCHAR(10),
    start_time TIME,
    end_time TIME,
    FOREIGN KEY (device_ID) REFERENCES Device(device_ID),
    FOREIGN KEY (user_ID) REFERENCES User(user_ID)
);

-- Create Maintenance table
CREATE TABLE Maintenance (
    session_ID VARCHAR(10) PRIMARY KEY,
    device_ID VARCHAR(10),
    date DATE,
    issue_reported TEXT,
    next_maintenance_date DATE,
    FOREIGN KEY (device_ID) REFERENCES Device(device_ID)
);

-- Now insert the data
-- Make sure to run these INSERT statements one at a time to ensure proper execution

-- 1. Insert User data
INSERT INTO User (user_ID, name, mobile, password, role, dob) VALUES
('U001', 'John Doe', '+1234567890', '1234', 'admin', '1990-05-15'),
('U002', 'Jane Smith', '+1987654321', '2345', 'admin', '1992-08-22'),
('U003', 'Mike Johnson', '+1122334455', '9876', 'user', '1988-12-03'),
('U004', 'Sarah Wilson', '+1555666777', '8765', 'user', '1995-03-30'),
('U005', 'Tom Brown', '+1999888777', '3456', 'user', '1991-11-18');

-- 2. Insert Device data
INSERT INTO Device (device_ID, status, name, model, version) VALUES
('D001', 'active', 'Smart Thermostat', 'Nest v3', '2.1'),
('D002', 'inactive', 'Security Camera', 'SecureCam Pro', '1.5'),
('D003', 'active', 'Smart Light', 'Philips Hue', '3.0'),
('D004', 'maintenance', 'Door Lock', 'SafeLock X1', '2.2'),
('D005', 'active', 'Smart Speaker', 'Echo Plus', '4.0');

-- 3. Insert Logs data
INSERT INTO Logs (device_ID, date, time, duration) VALUES
('D001', '2024-10-01', '08:00:00', 120),
('D002', '2024-10-01', '09:30:00', 60),
('D003', '2024-10-01', '10:15:00', 45),
('D001', '2024-10-02', '14:20:00', 90),
('D005', '2024-10-02', '16:45:00', 30);

-- 4. Insert Automation data
INSERT INTO Automation (automation_ID, device_ID, user_ID, start_time, end_time) VALUES
('A001', 'D001', 'U001', '06:00:00', '08:00:00'),
('A002', 'D003', 'U002', '18:00:00', '22:00:00'),
('A003', 'D002', 'U001', '20:00:00', '06:00:00'),
('A004', 'D005', 'U003', '07:00:00', '09:00:00'),
('A005', 'D001', 'U002', '22:00:00', '05:00:00');

-- 5. Insert Maintenance data
INSERT INTO Maintenance (session_ID, device_ID, date, issue_reported, next_maintenance_date) VALUES
('M001', 'D001', '2024-09-15', 'Regular checkup', '2024-12-15'),
('M002', 'D002', '2024-09-20', 'Camera alignment issue', '2024-10-20'),
('M003', 'D004', '2024-09-25', 'Battery replacement', '2024-11-25'),
('M004', 'D003', '2024-09-30', 'Firmware update', '2024-12-30'),
('M005', 'D005', '2024-10-05', 'Speaker calibration', '2025-01-05');


-- TRIGGERS

DELIMITER //

CREATE TRIGGER after_device_deactivate
AFTER UPDATE ON device
FOR EACH ROW
BEGIN
    -- Declare a variable to store the last log duration in seconds
    DECLARE last_log_duration INT;

    IF NEW.status IN ('inactive', 'off') AND OLD.status IN ('active', 'on') THEN
        -- Calculate the new duration based on the latest log entry
        SET last_log_duration = TIMESTAMPDIFF(SECOND,
            (SELECT CONCAT(date, ' ', time) 
             FROM logs 
             WHERE device_ID = OLD.device_ID 
             ORDER BY log_ID DESC LIMIT 1),
            NOW()
        );

        -- Update the latest log entry for the device with the new duration
        UPDATE logs
        SET duration = last_log_duration
        WHERE device_ID = OLD.device_ID
        ORDER BY log_ID DESC LIMIT 1;
    END IF;
END;
//

DELIMITER ;



DELIMITER //

CREATE TRIGGER after_device_deactivate
AFTER UPDATE ON device
FOR EACH ROW
BEGIN
    -- Declare a variable to store the total duration in minutes
    DECLARE total_minutes INT DEFAULT 0;
    DECLARE last_log_time DATETIME;

    IF NEW.status IN ('inactive', 'off') AND OLD.status IN ('active', 'on') THEN
        -- Get the latest log entry time
        SELECT CONCAT(date, ' ', time) INTO last_log_time 
        FROM logs 
        WHERE device_ID = OLD.device_ID 
        ORDER BY log_ID DESC LIMIT 1;

        -- Calculate the total duration in minutes using integer difference
        SET total_minutes = TIMESTAMPDIFF(MINUTE, last_log_time, NOW());

        -- Update the duration as total minutes
        UPDATE logs
        SET duration = total_minutes
        WHERE device_ID = OLD.device_ID
        ORDER BY log_ID DESC LIMIT 1;
    END IF;
END;
//

DELIMITER ;

