# AI Content Moderation Platform – Backend

## Overview

The AI Content Moderation Platform is a backend system designed to automate the moderation of user-submitted content using Artificial Intelligence. The platform allows users to upload content, receive moderation verdicts, submit appeals, and enables administrators to review moderation outcomes through analytics and management endpoints.

This project was developed using FastAPI, MongoDB Atlas, JWT Authentication, and a modular backend architecture to demonstrate a scalable content moderation workflow.

---

# Features

## Authentication Module

* User Registration
* User Login
* JWT Token Generation
* Protected Routes
* Current User Information Endpoint

### Endpoints

```http
POST /auth/register
POST /auth/login
GET  /auth/me
```

---

## Submission Management

Users can upload content for moderation and retrieve their submission history.

### Features

* Secure file upload
* User-specific submissions
* Submission storage in MongoDB Atlas
* Moderation result association

### Endpoints

```http
GET  /submissions/
GET  /submissions/my
GET  /submissions/all
POST /submissions/upload
```

---

## AI Moderation Module

The moderation service analyzes uploaded content and generates moderation verdicts.

### Current Implementation

* Verdict generation pipeline
* Category-based moderation results
* Confidence scores
* Moderation reasoning

Example:

```json
{
  "overall_outcome": "Approved",
  "categories": [
    {
      "category": "Graphic Violence",
      "result": false,
      "confidence": 0.05,
      "reason": "No violence detected"
    }
  ]
}
```

---

## Appeals Management

Users can appeal moderation decisions.

Administrators can review appeals and update their status.

### Features

* Appeal submission
* Appeal tracking
* Approval workflow
* Rejection workflow

### Endpoints

```http
GET  /appeals/
POST /appeals/create
GET  /appeals/my
GET  /appeals/all
PUT  /appeals/{appeal_id}/approve
PUT  /appeals/{appeal_id}/reject
```

---

## Verdict Management

Stores and retrieves moderation outcomes.

### Endpoints

```http
GET /verdicts/
GET /verdicts/all
```

---

## Analytics Dashboard

Provides platform statistics for administrators.

### Features

* User statistics
* Submission statistics
* Appeal statistics
* Moderation statistics

### Endpoint

```http
GET /analytics/dashboard
```

Example Response:

```json
{
  "total_users": 1,
  "total_submissions": 4,
  "approved_submissions": 4,
  "rejected_submissions": 0,
  "total_appeals": 2,
  "approved_appeals": 1,
  "rejected_appeals": 0,
  "pending_appeals": 1
}
```

---

# Technology Stack

## Backend Framework

* FastAPI

## Database

* MongoDB Atlas
* PyMongo

## Authentication

* JWT (JSON Web Tokens)
* Passlib (Bcrypt)

## API Documentation

* Swagger UI
* OpenAPI 3.1

## Additional Libraries

* Python Dotenv
* Python-Jose
* BSON
* Uvicorn

---

# System Architecture

```text
+------------------+
|      Client      |
+--------+---------+
         |
         v
+------------------+
|     FastAPI      |
|   REST APIs      |
+--------+---------+
         |
         v
+------------------+
| Authentication   |
| JWT Validation   |
+--------+---------+
         |
         +-------------------+
         |                   |
         v                   v

+------------------+   +------------------+
| Moderation       |   | Appeals Module   |
| Service          |   |                  |
+--------+---------+   +--------+---------+
         |                      |
         +----------+-----------+
                    |
                    v

         +------------------+
         | MongoDB Atlas    |
         | Database         |
         +------------------+
```

---

# Database Collections

```text
users
submissions
appeals
verdicts
policies
```

---

# API Workflow

```text
User Registration
        |
        v
User Login
        |
        v
JWT Token Issued
        |
        v
Upload Content
        |
        v
AI Moderation
        |
        v
Verdict Generated
        |
        v
Appeal Submission
        |
        v
Admin Review
        |
        +------> Approve
        |
        +------> Reject
```

---

# Project Structure

```text
app/
│
├── api/
│   ├── auth.py
│   ├── submissions.py
│   ├── appeals.py
│   ├── verdicts.py
│   └── analytics.py
│
├── auth/
│   ├── jwt_handler.py
│   ├── password.py
│   ├── dependencies.py
│   └── roles.py
│
├── database/
│   ├── mongodb.py
│   └── collections.py
│
├── schemas/
│   ├── user.py
│   ├── auth.py
│   └── appeal.py
│
├── services/
│   └── moderation_service.py
│
└── main.py
```

---

# Future Enhancements

* Deep Learning Moderation Models
* Real-Time Content Monitoring
* Policy Management Module
* Admin Dashboard Frontend
* Role-Based Access Control
* Audit Logging
* Notification System
* Docker Deployment
* CI/CD Integration

---

# Note

Due to final examination commitments and limited development time, the project scope was focused on completing and demonstrating a fully functional backend system. The implemented backend includes authentication, content submission, moderation workflow, appeals management, verdict retrieval, analytics reporting, and MongoDB Atlas integration, providing a complete foundation for future frontend integration and production-level enhancements.
