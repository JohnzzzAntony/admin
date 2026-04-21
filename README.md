# JKR - Premium E-commerce Platform

JKR is a high-end, premium e-commerce platform built with Django. It features a modern design, integrated payment gateways (Stripe, Tabby, Tamara), and a comprehensive admin dashboard.

## 🚀 Features

- **Modern UI/UX**: Premium aesthetic with dark mode and glassmorphism.
- **Product Management**: Multi-category products with variations, brands, and collections.
- **Order Management**: Robust order processing with status tracking.
- **Payment Integration**: Support for Stripe, Tabby, and Tamara.
- **CMS Pages**: Custom sections for About Us, Services, Gallery, and Store Locations.
- **SEO Optimized**: Dynamic meta tags and social media preview support.

## 🛠️ Tech Stack

- **Backend**: Django 5+
- **Database**: SQLite (Development), PostgreSQL (Production)
- **Styling**: Vanilla CSS with modern HSL palettes
- **Media**: Cloudinary for image storage
- **Payments**: Stripe, Tabby, Tamara

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Pro
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

## 🧪 Testing

Run tests using pytest:
```bash
pytest
```

## 🌐 Deployment

The project is configured for deployment on platforms like Railway or Hostinger.
- Ensure `IS_PRODUCTION=True` in your environment variables.
- Configure `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.

## 📄 License

This project is proprietary.
