# 2201-SAD-Bot-Trader

This project was developed by the students of [Prague City University](https://www.praguecityuniversity.cz/)
during the Summer Semester of 2022 as part of the "Secure Application Development" module.

## Running Bot Trader's API

Precondition: You have to be accepted to git secret of this repository.

```bash
git clone --recursive https://github.com/Aemilivs/2201-SAD-Bot-Trader.git 2201-SAD-Bot-Trader && cd $_
python3.10 -m venv venv
source venv/bin/activate
pip3 install -r API/requirements.txt
source API/run.sh
git secret reveal
```

Consequent runs can be performed by executing `flask run`

## Running Bot Trader's GUI

```bash
git clone --recursive https://github.com/Aemilivs/2201-SAD-Bot-Trader.git 2201-SAD-Bot-Trader && cd $_
python3.10 -m venv venv
source venv/bin/activate
pip3 install -r GUI/requirements.txt
python3.10 manage.py makemigrations
python3.10 manage.py migrate
python3.10 manage.py runserver
```

Consequent runs can be performed by executing

```bash
cd 2201-SAD-Bot-Trader
export DATABASE_NAME=$(readlink -f db.sqlite.3)
alias start_gui="python3 "$(readlink -f manage.py)" runserver"
```

and running `start_gui` following that.

## Feature-list

Feature list is available [here](./FEATURES.MD)

## Contributing

See the contribution [guideline](./CONTRIB.md)