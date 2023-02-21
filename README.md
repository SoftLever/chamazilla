# INSTALLATION
git clone git@github.com:SoftLever/chamazilla.git
cd chamazilla
sudo apt install libmysqlclient-dev
pip install -r requirements.txt


python manage.py loaddata dashboard_fixtures
