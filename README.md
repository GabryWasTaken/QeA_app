![QeA](https://cdn.discordapp.com/attachments/733391066136313879/1157741467205390438/qea_app.png?ex=6519b643&is=651864c3&hm=2503a78b63deb85fa98f0e39fcb92229c82427648a7f2c880abe6aef842bf973&)

![Logo](https://img.shields.io/badge/Created%20by-GabryWasTaken-red)
## DESCRIPTION
The app allows users to ask questions and get answers from experts (setted by an admin) on various topics. \
These questions are sent to experts who have been selected by the user, the choosed expert can then respond to the question on their dedicated page. \
Once the expert responds, the user can view their question and the answer directly on the home page.
## PREREQUISITES

![Python3](https://img.shields.io/badge/Install-Python%203%20or%20greater-blue?link=https%3A%2F%2Fwww.python.org%2Fdownloads%2F)

Install the external dependencies, they are located in
```bash
requirements.txt
```
## HOW TO RUN PROGRAM

* Install all of the prerequisites in your virtual environment or your machine with the following command:
```bash
pip install -r requirements.txt
```
* Write this command to run the webapp:
```bash
python3 ./app.py
``` 
* Or : 
```bash
flask run
``` 
if you wanna start the program with flask run you need to set the environment variable with the command:
```bash
set FLASK_APP=app.py
``` 
Once you runned the app you can access to the admin panel with the credentials:
* **Username**: admin
* **Password**: admin
## CREDITS

Application based on the guided exercise of the "The Ultimate Flask Course" on Udemy
