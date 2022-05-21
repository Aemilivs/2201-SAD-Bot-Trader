# 2201-SAD-Bot-Trader

This project was developed by the students of [Prague City University](https://www.praguecityuniversity.cz/)
during the Summer Semester of 2022 as part of the "Secure Application Development" module.

## Running Bot Trader's API

```bash
git clone --recursive https://github.com/Aemilivs/2201-SAD-Bot-Trader.git 2201-SAD-Bot-Trader && cd $_
python3.10 -m venv venv
source venv/bin/activate
pip3 install -r API/requirements.txt
source API/run.sh
```

Consequent runs can be performed by executing `flask run`

## Running Bot Trader's GUI

```bash
git clone --recursive https://github.com/Aemilivs/2201-SAD-Bot-Trader.git 2201-SAD-Bot-Trader && cd $_
python3.10 -m venv venv
source venv/bin/activate
pip3 install -r Flask-UI/requirements.txt
```

Consequent runs can be performed by executing

```bash
#For Unix
cd 2201-SAD-Bot-Trader
export FLASK_APP=run.py

# Start the application (development mode)
# --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
# --port=5001    - specify the app port (default 5000)  
flask run --host=0.0.0.0 --port=5001

# Access the dashboard in browser: http://127.0.0.1:5001/
```


## Running Trading Bot

To tun the trading bot API and GUI concurrently and allow their interconnectivity on the same server. Execute the following commands:

```bash
cd 2201-SAD-Bot-Trader
sh run.sh

# GUI accessible on: http://127.0.0.1:5000
# API accessible on: http://127.0.0.1:5001
```

## Feature-list

Feature list is available [here](./FEATURES.MD)

## Contributing

See the contribution [guideline](./CONTRIB.md)