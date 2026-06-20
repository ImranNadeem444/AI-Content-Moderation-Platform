from app.database.mongodb import db

users_collection = db["users"]
submissions_collection = db["submissions"]
verdicts_collection = db["verdicts"]
appeals_collection = db["appeals"]
policies_collection = db["policies"]