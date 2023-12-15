# smart-filesearch


## How to install ##

## Requirements ##
* Python 3.10


## Local setup ##

### Clone repo
Clone git repository:

```bash
git clone https://github.com/GoGei/smart-filesearch.git
```

Add line to **/etc/hosts** file
```
127.0.0.1	smart-filesearch.local
```

### Environment setup
Create virtual environment, setup packages:

```bash
python3.10 -m venv env
source env/bin/activate
pip install -r requirements.txt
``` 

Copy settings file `settings_example.py` to `settings.py` and change settings
```bash
cp config/example.py config/settings.py
```

## Usefull commands

### Run server
```bash
fab runserver
```

### Verify code before push
```bash
fab check
```
