# Expense Tracker [ WIP ]

# TODO
- [x] User Login and Registration
- [x] Add Income and expenses
- [x] Different modes for income and expense ( Wallet, Cash, Bank )
- [ ] Cleaner Dashboard View
- [ ] User Entry for expense categories
- [ ] Display Expense accourding to source in User Dashboard

## Motivation :
- To learn how models and relation works with authentication and per user categories using `user_id`
- Arithmetic operations on DB data and save them


## Usage
- Clone the repo and enter it
```
git clone git@github.com:greed-d/expense-tracker.git
cd expense-tracker
```

- Install Python ( Command for Arch based distro)
```
sudo pacman -S python
```
- Start venv 
```
python -m venv venv
```

- Source the venv
```
source venv/bin/activate
```
use `activate.fish` if you're using fish terminal

- Install requirements
```
pip install -r requirements.txt
```
### - Run Project ( Requires 2 terminal with venv activated )
#### For tailwind
```
python manage.py tailwind start
```
#### For django
```
python manage.py runserver
```
- This should output something like :
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 19, 2024 - 04:06:05
Django version 5.1.4, using settings 'todo_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
- Go to the link it provides, `127.0.0.1:8000/` in my case


