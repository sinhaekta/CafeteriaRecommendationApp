CREATE DATABASE Cafeteria;
USE Cafeteria;

CREATE TABLE User (
    user_id int PRIMARY KEY AUTO_INCREMENT,
    name varchar(255) NOT NULL UNIQUE, 
    password varchar(255) NOT NULL,
    role enum('admin', 'chef', 'employee') NOT NULL DEFAULT 'employee',
    notification_number int NOT NULL DEFAULT 0
);
 
CREATE TABLE Menu_Item (
    item_id int PRIMARY KEY AUTO_INCREMENT,
    name varchar(255) NOT NULL UNIQUE,
    price decimal(10, 2) NOT NULL,
    description text NOT NULL,
    category enum('breakfast', 'lunch', 'dinner', 'all day') NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE
);
 
CREATE TABLE Comment (
    comment_id int PRIMARY KEY AUTO_INCREMENT,
    user_id int NOT NULL,
    item_id int NOT NULL,
    comment text NOT NULL,
    comment_date date NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES Menu_Item (item_id) ON DELETE CASCADE
);

CREATE TABLE Rating (
    rating_id INT PRIMARY KEY AUTO_INCREMENT,
    item_id INT NOT NULL,
    rating_value FLOAT NOT NULL,
    CONSTRAINT fk_item_id FOREIGN KEY (item_id) REFERENCES Menu_Item(item_id)
);
 
CREATE TABLE Notification (
    notification_id int PRIMARY KEY AUTO_INCREMENT,
    message text NOT NULL,
    notification_date date NOT NULL
);
 
CREATE TABLE Daily_Menu (
    menu_date date NOT NULL,
    item_id int NOT NULL,
    item_name  varchar(255) NOT NULL,
    item_category  varchar(255) NOT NULL,
    PRIMARY KEY(item_id, menu_date),
    FOREIGN KEY (item_id) REFERENCES Menu_Item(item_id) ON DELETE CASCADE
);
 
 CREATE TABLE Employee_Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    breakfast_item_id INT NOT NULL,
    lunch_item_id INT NOT NULL,
    dinner_item_id INT NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (breakfast_item_id) REFERENCES Menu_Item(item_id),
    FOREIGN KEY (lunch_item_id) REFERENCES Menu_Item(item_id),
    FOREIGN KEY (dinner_item_id) REFERENCES Menu_Item(item_id)
);

CREATE TABLE Discard_Items (
    discard_id INT PRIMARY KEY AUTO_INCREMENT,
    item_id INT NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    rating_value FLOAT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES Menu_Item(item_id),
    FOREIGN KEY (item_name) REFERENCES Menu_Item(name)
);

CREATE TABLE Discard_Item_Notification (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    item_id INT NOT NULL,
    message TEXT NOT NULL,
    notification_date DATE NOT NULL,
    FOREIGN KEY (item_id) REFERENCES Menu_Item(item_id)
);

CREATE TABLE Employee_Discard_Item_Feedback (
    feedback_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    notification_id INT NOT NULL,
    feedback TEXT NOT NULL,
    feedback_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (notification_id) REFERENCES Discard_Item_Notification(notification_id)
);

CREATE TABLE Employee_Profile (
    profile_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    diet_type ENUM('Vegetarian', 'Non Vegetarian', 'Eggetarian') NOT NULL,
    spice_level ENUM('High', 'Medium', 'Low') NOT NULL,
    cuisine_preference ENUM('North Indian', 'South Indian', 'Other') NOT NULL,
    sweet_tooth ENUM('Yes', 'No') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);