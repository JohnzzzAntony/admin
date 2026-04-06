from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='blog_post';")
    print(cursor.fetchall())
    
    # Also add the missing columns if they aren't there! By just adding them.
    columns = [col[0] for col in cursor.fetchall()]
    
    # We need: excerpt, meta_title, meta_description
    if 'excerpt' not in columns:
        try:
            cursor.execute('ALTER TABLE blog_post ADD COLUMN excerpt text NOT NULL DEFAULT \'\';')
            print('Added excerpt')
        except Exception as e:
            print(f'Error excerpt: {e}')
    if 'meta_title' not in columns:
        try:
            cursor.execute('ALTER TABLE blog_post ADD COLUMN meta_title varchar(255) NOT NULL DEFAULT \'\';')
            print('Added meta_title')
        except Exception as e:
            print(f'Error meta_title: {e}')
    if 'meta_description' not in columns:
        try:
            cursor.execute('ALTER TABLE blog_post ADD COLUMN meta_description text NOT NULL DEFAULT \'\';')
            print('Added meta_description')
        except Exception as e:
            print(f'Error meta_description: {e}')
