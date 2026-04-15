# Isolated Testing Environment Setup

I have prepared an isolated test environment for you by leveraging **Neon's Database Branching**. This provides an exact copy of your live data without any risk to your live site.

### 1. The Isolated Database
I have created a `development` branch of your Neon database.
*   **Branch ID**: `br-rapid-cake-a1b7ey45`
*   **Testing URI (for your .env)**: 
    `postgresql://neondb_owner:npg_UXBiNGh80Orw@ep-dry-moon-a1owxnuf-pooler.ap-southeast-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require`

### 2. Configured Environment Switch
To activate the test environment on your local machine, I recommend updating your `.env` as follows:

```env
# [LIVE DB - LIVE SITE] (Commented out for safety)
# DATABASE_URL=postgresql://neondb_owner:npg_jbT9kgXAy6cW@ep-muddy-tree-a1lgf0n8-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# [TEST DB - ISOLATED BRANCH]
DATABASE_URL=postgresql://neondb_owner:npg_UXBiNGh80Orw@ep-dry-moon-a1owxnuf-pooler.ap-southeast-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require

# Development Toggles
DEBUG=True
IS_PRODUCTION=False
```

### 3. How to Test
1.  Open your terminal and run your server:
    ```powershell
    python manage.py runserver
    ```
2.  Go to `http://127.0.0.1:8000/admin`.
3.  Modify any data or add new products. 
4.  **Verify Isolated Site**: Observe that your modifications only show up in your local browser and do not affect the live site at `ecom.creativegradientz.com`.

### 4. What if I want to "Sync" the live data to my test bench?
Since this is a Neon branch, you can easily "reset" it to match the current live site at any time using the Neon Console.

---

Would you like me to apply these changes to your `.env` now, or would you prefer me to create a separate `.env.local` for you?
