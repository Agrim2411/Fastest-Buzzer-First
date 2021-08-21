# Fastest-Buzzer-First

**I. Description**

This project simulates a quiz with server client setup, using
**socket programming** in python. 

It uses the concept of **multithreading**.

Every time a user connects to the server, a separate thread is
created for that client and communication from server to client takes place along individual
threads.

Each client is identified by a unique socket object.

**II. Language used**
: Python 2.7

**III. Modules used** : sys, select, time ,socket , threading
random , termios

**V. RUNNING THE PROJECT**

On Terminal 1 –
```
python server.py
```

On Terminal 2nd,3rd,4th –
```
python client.py
```
