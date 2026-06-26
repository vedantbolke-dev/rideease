-- RideEase Bike Rental System
-- MySQL Database Schema
-- Run this AFTER Django migrations to understand the structure.
-- Use: python manage.py migrate (Django will create these tables automatically)

CREATE DATABASE IF NOT EXISTS rideease_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE rideease_db;

-- Custom User Table (created by Django migration from apps.users)
-- users_customuser
-- id, password, last_login, is_superuser, username, first_name, last_name, email,
-- is_staff, is_active, date_joined, phone_number, address, city, state, pincode,
-- profile_picture, driving_license, is_blocked, created_at, updated_at

-- Bike Table (created by Django migration from apps.bikes)
-- bikes_bike
-- id, name, brand, model_year, category, fuel_type, transmission,
-- engine_cc, mileage, color, top_speed, price_per_day, helmet_deposit,
-- description, features, image, is_available, is_featured, location,
-- created_at, updated_at

-- Contact Messages Table
-- bikes_contactmessage
-- id, name, email, phone, subject, message, is_read, created_at

-- Bookings Table (created by Django migration from apps.bookings)
-- bookings_booking
-- id, user_id (FK -> users_customuser), bike_id (FK -> bikes_bike),
-- pickup_date, return_date, pickup_location, drop_location,
-- total_days, price_per_day, helmet_deposit, total_cost,
-- status, special_requests, admin_notes, created_at, updated_at

-- Reviews Table
-- bookings_review
-- id, booking_id (FK -> bookings_booking, UNIQUE),
-- user_id (FK -> users_customuser), bike_id (FK -> bikes_bike),
-- rating, comment, created_at

-- Sample INSERT statements (use seed_data command instead)
-- python manage.py seed_data
