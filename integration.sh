#!/usr/bin/env bash

#Check si gittyleaks / flake8 / bandit / safety / black /  installer

# Check credentials
cd ./app
gittyleaks
cd ..

# Python linter : flake8
flake8 ./app
flake8 ./tests

#Safety : check dependencies vulns
safety check -r requirements.txt

#Bandit : check code vulns
bandit -r ./app

#Pyre : type checker
pyre --source-directory app check

#Black : Code formatting
#black ./app

# lancer tests unitaires