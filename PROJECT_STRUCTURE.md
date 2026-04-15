# JKR E-commerce Project Structure

This document outlines the organized structure of the JKR International LLC codebase after the cleanup and restructuring phase.

## 📁 Directory Overview

### 📦 Root Directories
- **`jkr/`**: Core project configuration (settings, URLs, WSGI/ASGI).
- **`data/`**: JSON data dumps, migration templates, and CSV files for import/export.
- **`deployment/`**: Deployment-specific configurations (`Procfile`, `passenger_wsgi.py`, deployment docs).
- **`backups/`**: Archived items and old settings for safety.
- **`scripts/`**: Utility scripts for database population, SKUs fixing, and maintenance.
- **`static/`**: Global static assets (CSS, JS, Images).
- **`templates/`**: Global HTML templates, organized by app.
- **`media/`**: Local media storage (synced with Cloudinary in production).

### 🚀 Application logic
- **`accounts/`**: User authentication, profiles, and custom widgets.
- **`products/`**: Product management, categories, collections, and search API.
- **`orders/`**: Cart logic, order processing, and payment status management.
- **`core/`**: General site settings, homepage logic, and shared context processors.
- **`blog/`**: Content management for the site's blog section.
- **`pages/`**: Static page management (About Us, Terms, etc.).
- **`contact/`**: Contact forms and newsletter subscriptions.
- **`sliders/`**: Management for Hero banners and promotional sections.

## 🛠️ Key Configurations
- **Database**: Uses PostgreSQL (Neon/Supabase) in production and SQLite3 locally.
- **Storage**: Cloudinary for media and WhiteNoise for static files in production.
- **Payments**: Integrated with Stripe, Tabby, and Tamara.
- **Admin**: Enhanced with Jazzmin theme and custom UX scripts.

## 🧹 Cleanup Rules
- **No Scratch Files**: Do not keep debug or temporary scripts in the root. Use the `scripts/` directory.
- **Strict Media/Static separation**: Always use the defined directories; do not create ad-hoc folders.
- **Environment Variables**: All secrets must stay in `.env` and never be hardcoded.
