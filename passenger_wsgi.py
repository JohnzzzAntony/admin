import sys, os

# Set up paths for Hostinger/Phusion Passenger
# Replace 'admin_site' with the folder name you chose in Hostinger's Setup Python App
# if it is different from your current project folder name.
INTERP = os.path.expanduser("~/venv/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

# Point to your Django project's wsgi module
from jkr.wsgi import application
