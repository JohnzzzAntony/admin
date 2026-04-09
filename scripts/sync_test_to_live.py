import os
import sys
import subprocess
import time

def run_sync():
    # 1. Configuration
    SOURCE_DB = "postgresql://neondb_owner:npg_UXBiNGh80Orw@ep-dry-moon-a1owxnuf-pooler.ap-southeast-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require"
    TARGET_DB = "postgresql://neondb_owner:npg_jbT9kgXAy6cW@ep-muddy-tree-a1lgf0n8-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    DUMP_FILE = "transfer_dump.json"
    
    print("🌅 Starting Database Sync: Test -> Live (UTF-8 Mode)")
    print("-" * 50)

    # 2. Extract Data from Test
    print("📦 Phase 1: Extracting data from Test Environment...")
    env = os.environ.copy()
    env['DATABASE_URL'] = SOURCE_DB
    env['PYTHONIOENCODING'] = 'utf-8'
    
    # We use a manual open with utf-8 to avoid Windows encoding issues
    try:
        with open(DUMP_FILE, 'w', encoding='utf-8') as f:
            dump_cmd = [
                "python", "manage.py", "dumpdata", 
                "--natural-foreign", "--natural-primary",
                "-e", "contenttypes", "-e", "auth.permission", "-e", "sessions", "-e", "admin.logentry",
                "--indent", "2"
            ]
            subprocess.run(dump_cmd, check=True, stdout=f, env=env)
        print(f"✅ Data extracted successfully to {DUMP_FILE}")
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return

    # 3. Inject Data to Live
    print("\n🚀 Phase 2: Injecting data into Live Database...")
    print("⚠️  Warning: This will overwrite data in the target database.")
    time.sleep(2)
    
    env['DATABASE_URL'] = TARGET_DB
    
    # First, run migrations to ensure schema is ready
    print("🛠️  Ensuring Live schema is up to date...")
    try:
        subprocess.run(["python", "manage.py", "migrate"], check=True, env=env)
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return

    # Now load the data
    print("📥 Loading data...")
    # On Windows, we need to be careful with loaddata reading the file
    load_cmd = ["python", "manage.py", "loaddata", DUMP_FILE]
    
    try:
        # We specify the encoding in the environment just in case
        subprocess.run(load_cmd, check=True, env=env)
        print("\n✨ SUCCESS! Your Live database is now a perfect clone of your Test database.")
        print("You can now refresh your live website to see the changes.")
        
        # Cleanup only on success
        if os.path.exists(DUMP_FILE):
            os.remove(DUMP_FILE)
            print("Cleanup: Temporary transfer file removed.")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during injection: {e}")
        print(f"DEBUG: The file '{DUMP_FILE}' has been kept for inspection.")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    run_sync()
