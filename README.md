# PyMiner

Linux
--------
##Installation
The *requirements.txt* contains the necessary dependencies needed for the project.
To import them directly from the file, use:
```bash
pip install -r requirements.txt
```

##Usage
```bash
./miner.py -n NUMBER_OF_SEARCHES -e EMAIL_ADDRESS
```

##Development
In order to keep the *requirements.txt* dependencies file up-to-date, if a new package is required, use:
```bash
pip freeze > requirements.txt
```
==================
Windows
---------
##Installation
**Requirements:**
- Must have Python2 installed.
- Must have Python2 and Pip added to your system path.
```
pip install selenium
```

##Usage
```
python .\miner.py -n NUMBER_OF_SEARCHES -e EMAIL_ADDRESS
```
