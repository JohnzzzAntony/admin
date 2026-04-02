# Deployment Guide: admin.creativegradientz.com (Hostinger)

Following these steps will host your project on your subdomain without affecting its functionality.

## 1. Prepare Your Subdomain
1. Log in to **Hostinger hPanel**.
2. Go to **Domains** > **Subdomains**.
3. In the "Create a New Subdomain" form, enter `admin`.
4. Check the box **"Custom folder for subdomain"** and enter `admin_site`.
5. Click **Create**.

## 2. Setup Python Application
1. In hPanel, search for **Python** and select **Setup Python App**.
2. Click **Create Application**.
3. **Python Version**: Select `3.11` (or latest available).
4. **Application Root**: Enter `admin_site` (this is the folder we just created).
5. **Application URL**: Select `admin.creativegradientz.com`.
6. **Application Startup File**: Enter `passenger_wsgi.py`.
7. **Application Entry Point**: Enter `application`.
8. Click **Setup**.

## 3. Upload Project Files
1. Use Hostinger's **File Manager** (or FTP) to navigate into the `admin_site` folder.
2. If there are any default files like `.htaccess` or `default.php`, you can delete them.
3. Upload your project files from your computer to this folder. 
   *(Note: You can skip uploading the `.venv` folder as we will create a new one in Hostinger).*

## 4. Install Dependencies
1. In the **Setup Python App** page, find the "Run pip install" section.
2. Enter `requirements.txt` and click **Run**.
3. *(Alternative)*: You can use the **Terminal** (SSH) in hPanel to activate the virtual environment and run `pip install -r requirements.txt`.

## 5. Final Steps
1. **Migrations**:
   In the Hostinger Terminal:
   ```bash
   python manage.py migrate
   ```
2. **Collect Static Files**:
   In the Hostinger Terminal:
   ```bash
   python manage.py collectstatic --noinput
   ```
3. **SSL Certificate**:
   Go to **Security** > **SSL** and install a Let's Encrypt SSL certificate for `admin.creativegradientz.com`.

## 6. Project is Live!
Visit `https://admin.creativegradientz.com/admin/` and log in with your credentials. Everything you've configured locally will now be active on the web.
