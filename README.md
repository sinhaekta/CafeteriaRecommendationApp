# Cafeteria Recommendation App

## Overview
-> This project is a Cafeteria Recommendation System designed to manage cafeteria operations such as menu management, food recommendation, and notifications. 

-> The project is implemented in Python and uses MySQL for the database.

-> The system includes functionalities for Admin, Chef, and Employee roles. 

-> The entry point for the client-side application is 'ClientMain.py'.

-> The entry point for the server-side application is 'ServerMain.py'.

## Project Structure:
```
├── Client
│   ├── Admin
│   │   ├── AddMenuItem.py
│   │   ├── DeleteMenuItem.py
│   │   ├── UpdateMenuItem.py
│   │   ├── ViewMenuItems.py
│   │   └── __init__.py
│   ├── Chef
│   │   ├── ManageDiscardMenu.py
│   │   ├── RollOutMenu.py
│   │   ├── SendNotification.py
│   │   ├── ViewDiscardMenu.py
│   │   ├── ViewRecommendation.py
│   │   └── __init__.py
│   ├── Client.py
│   ├── ClientController
│   │   ├── AdminMenu.py
│   │   ├── CafeteriaApp.py
│   │   ├── ChefMenu.py
│   │   ├── EmployeeMenu.py
│   │   └── __init__.py
│   ├── ClientMain.py
    ├── Config.py
│   ├── Employee
│   │   ├── CheckNotification.py
│   │   ├── DiscardItemFeedback.py
│   │   ├── GiveFeedback.py
│   │   ├── OrderFood.py
│   │   ├── UpdateProfile.py
│   │   └── __init__.py
│   └── __init__.py
├── README.md
└── Server
    ├── DB_Connection
    │   ├── AdminDBOperations.py
    │   ├── ChefDBOperations.py
    │   ├── DbConnect.py
    │   ├── EmployeeDBOperations.py
    │   └── __init__.py
    ├── Server.py
    ├── ServerController
    │   ├── RouteController.py
    │   └── __init__.py
    ├── ServerMain.py
    ├── Config.py
    ├── Services
    │   ├── AdminService.py
    │   ├── AuthenticationService.py
    │   ├── ChefService.py
    │   ├── EmployeeService.py
    │   └── __init__.py
    └── Test
        ├── Main.py
        ├── TestAdminServices.py
        ├── TestChefServices.py
        ├── TestEmployeeServices.py
        └── TestValues.json
```