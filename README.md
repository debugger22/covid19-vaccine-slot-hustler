# COVID-19 vaccine slot hustler
A simple Python script which continuously scraps COVID-19 vaccine slot data and alerts you when it's available using cowin-public-v2 API for India.

## Why?

The motivation behind this was to avoid the cumbersome process on the Arogya Setu app to keep looking for a slot and try to book if it's available before it gets full. You can just keep this script running in the background. The script currently lacks few features such as configuring age and dose(1st or 2nd) info for a user.

**Note:** _The script helped me book a slot and I thought it'd a good idea to make it available for others._

## How to use?

* **Step 1:** Download the repository and edit hustler.py to add your details at the top such as your mobile number and pin code.
* **Step 2:** Install Python 3 on your system which can be easily downloaded from https://www.python.org/downloads/.
* **Step 3:** Once you have Python installed, you can open command prompt/terminal/bash depending on your OS, navigate to the repository and run following commands

```
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ python hustler.py
```
