# Setup
#### Clone Github Repository
```bash
git clone https://github.com/ineedme/Tekton.git
```

#### Create and activate a new Virtual Environment
```bash
cd Tekton
python -m venv venv
```
**Activate Environment**

- on windows
```bash 
venv\Scripts\activate.bat
```
- on linux
```bash
source venv/bin/activate
```

#### Install requirements
```bash
pip install -r requirements.txt
```

#### Migrate Database and load data
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py fixture.json
```

### Run Server
```bash
python manage.py runserver
```

## Testing
While the server is running
Go directly through the browser, by going to the URL [http://localhost:8000/api/v1/product/](http://localhost:8000/api/v1/product/)
