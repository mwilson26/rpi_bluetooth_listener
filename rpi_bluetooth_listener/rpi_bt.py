import json
import threading
from bluedot.btcomm import BluetoothServer
from signal import pause


class PiBluetoothListener(threading.Thread):

    def __init__(self):
        self.ser = None
        self.command_register = {}
        threading.Thread.__init__(self)

    def run(self):
        self.ser = BluetoothServer(self._parse_command)
        pause()

        return None

    def close(self):
        self.ser.stop()
        return None  # Figure out how to close the serial connection

    def route(self, command_string):
        """This creates the decorator that adds the function to the command register."""
        def decorator(in_func):
            self._add_to_command_register(command_string,in_func)
            return in_func
        return decorator

    def _parse_command(self, data):
        pkg = json.loads(data)
        if not len(pkg.keys()) == 1:
            raise ValueError('The command JSON should only contain a single key referencing the function in the outer scope.')

        command = list(pkg.keys())[0]
        args = pkg[command]
        self._run_command(command, args)

        return None

    def _run_command(self, command, kwargs):
        """This will run the command that is routed."""
        if command not in self.command_register:
            raise KeyError('This command is not in the command register.')
        func = self.command_register[command]['function']
        names = self.command_register[command]['arg_names']
        if not sorted(kwargs.keys()) == sorted(names):
            raise ValueError('Command arguments are different than expected')

        func(**kwargs)
        return None

    def _add_to_command_register(self, command_string, func):
        """Adds the function and arguments to the command registry referencing the command string."""
        if command_string in self.command_register:
            raise KeyError('This command string is already used on a different function.')

        self.command_register[command_string] = {
            'function': func,
            'arg_names': func.__code__.co_varnames[:func.__code__.co_argcount],
        }

        return None
