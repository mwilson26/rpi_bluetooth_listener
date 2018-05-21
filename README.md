# rpi_bluetooth_listener
A simple bluetooth listener for routing commands over bluetooth to Python functions on the Raspberry Pi.

## Introduction

The goal of this project was to produce a simple way to communicate and execute commands in Python on a 
Raspberry Pi over bluetooth with function routing similar to Python's Flask interface.  The `PiBluetoothListener`
class will set up a seperate thread waiting for bluetooth commands in the form of a JSON string, which specifies
which function to run and the arguments that will be passed to the function.  More information can be found below.

## Requirements

This module uses the `bluedot` module for the bluetooth connection.  Information on installing the bluedot package
on the raspberry pi [can be found here](http://bluedot.readthedocs.io/en/latest/gettingstarted.html#python-library).
    
This module will not pair your devices, so be sure to pair your devices before using this module.  To allow serial
communication on the raspberry pi.  To do this, edit the following file:

    sudo nano /etc/systemd/system/dbus-org.bluez.service

and add `-C` to the end of the following line, followed by a new line as written below:

    ExecStart=/usr/lib/bluetooth/bluetoothd -C
    ExecStartPost=/usr/bin/sdptool add SP

Restart the raspberry pi to use these settings.  When your Python program with the listener is running, you can then
connect to the raspberry pi over a bluetooth serial connection using the app of your choosing.  For myself, I was
writing an android controller app to communicate over bluetooth, but for testing purposes, a bluetooth serial terminal
app will work fine.

## Installation

To install, clone this repository and run the setup.py script in the python environment of your choosing as:

    python setup.py install

The listener can then be imported as:

```python

from rpi_bluetooth_listener import PiBluetoothListener

```

## Usage

Usage is similar to how flask routes functions when receiving HTTP requests.  In this case, you need to initialize the
listener instance and start the thread.  You can then use the `route` method to add functions to the listener as seen
below:

```python
from rpi_bluetooth_listener import PiBluetoothListener

bt = PiBluetoothListener()
bt.start()

@bt.route('cmd1')
def first_command(arg1,arg2):

    print(arg1)
    print(arg2)
    print(type(arg1))

    return None

@bt.route('cmd2')
def second_command():

    print('in second command')

    return None

print('commands registered')

```

When you run this, you'll see the `commands registered` print statement in this test example, showing you that the
commands have been added.  The command parser uses JSON strings in order to feed the command into the defined functions.
In the outer part of the JSON, the key is the command string, which is what you put into the `route` method.  The object
will be a sub JSON string with the argument names (matching the ones defined in the function), and the argument values,
such as:

    {"cmd1": {"arg1": 1.2, "arg2": "a"}}

For functions without arguments, send an empty JSON after the command like:

    {"cmd2": {}}

When running the first command, you will see the following output in your Python terminal.

    1.2
    a
    <class 'float'>

So, you can see that the JSON parser recognizes the data type for simple data types.  You should now be able to execute
more complex commands over bluetooth with given input arguments.

## Still to do

I need to work on some error handling for badly formatted inputs, so that the program will still listen instead of
needing to be restarted.  In my current usage, the android apps forces the JSON format to be what I want, so it is
not an issue for me at the moment, but I'll want to make the usage more general.  Also, I need to handle data returns
over bluetooth as well, so that I can retrieve the responses.  Currently it only works to send commands to my connected
devices.

