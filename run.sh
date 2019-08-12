#!/bin/sh

clean() {
  rm -rf app/db.sqlite app/test.sqlite venv .idea
  find . -type d -name __pycache__ -a -prune -exec rm -rf {} \;
  find . -type d -name .pytest_cache -a -prune -exec rm -rf {} \;
}

run() {
  . ./venv/bin/activate
  flask run
}

setup() {
  clean
  virtualenv venv -p python3
  . ./venv/bin/activate
  pip install -r requirements.txt --user
  flask reset-db
}

test() {
  . ./venv/bin/activate
  python -m pytest tests/
}

case "$1" in
  "setup")
    setup
    ;;
  "clean")
    clean
    ;;
  "test")
    test
    ;;
  "run")
    run
    ;;
  *)
  echo "unknown command"
    echo "expected: setup / clean / run / test"
    exit 1
    ;;
esac
exit 0
