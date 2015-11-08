# Harmonic's new website

mobile friendly with django, sass and browserify

## setup

```
brew install node
npm install -g grunt
npm install
virtualenv --no-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
python src/manage.py migrate
python src/manage.py createsuperuser
python src/manage.py runserver
```

## disclaimer

This is a work in progress.
There is probably no interest for anyone except me in this code :)
Feel free to use some code found here.
