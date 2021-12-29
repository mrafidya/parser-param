#!/bin/bash

cd $(dirname "$0")
source venv/bin/activate

python pull.py
retVal=$?
if [ $retVal -ne 0 ];
then
    echo "$(date):pull.py:ERROR - Error on pull.py script"
    echo "$(date):pull.py:INFO - Stop the execution"
    exit $retVal
else
    echo "$(date):pull.py:INFO - pull.py has been successfully executed"
fi

python main.py db data/function.db persist
retVal=$?
if [ $retVal -ne 0 ];
then
    echo "$(date):main.py:ERROR - Error on main.py script"
    echo "$(date):main.py:INFO - Stop the execution"
    exit $retVal
else
    echo "$(date):main.py:INFO - main.py has been successfully executed"
fi

python push.py
retVal=$?
if [ $retVal -ne 0 ];
then
    echo "$(date):push.py:ERROR - Error on push.py script"
    echo "$(date):push.py:ERROR - Stop the execution"
    exit $retVal
else
    echo "$(date):push.py:INFO - push.py has been successfully executed"
fi

echo "$(date):run_all.sh:INFO - All script has been successfully execute"
deactivate