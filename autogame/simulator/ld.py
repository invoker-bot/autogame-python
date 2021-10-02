# -*- coding: utf-8 -*-
# Author: Invoker
# Email : invoker-bot@outlook.com
# Site  : https://github.com/invokerrrr/autogame-python
# Data  : 2021/10/5

"""This module includes a class supports LDPlayer (https://www.ldplayer.net).

Note:
    * This module should be import explicitly.
    * LDPlayer must be installed on the computer.

"""
import os
import subprocess
from .base import AGameSimulatorAdb


class CGameSimulatorLD(AGameSimulatorAdb):
    """

    """
    def __init__(self, index=None, name=None, encoding="utf-8"):
        self.encoding = encoding
        if "LD_CONSOLE_PATH" in os.environ:
            self.console = os.environ["LD_CONSOLE_PATH"]
        else:
            raise NotImplementedError(
                "LD console ('ldconsole.exe') is not found (specify environment variable 'LD_CONSOLE_PATH' to set)")
        simulators = self.ldconsole("list").split()
        if index is None:
            if name is not None:
                index = simulators.index(name)
            else:
                raise TypeError("expect at least one of 'index' or 'name' should not be`None`")
        else:
            if name is not None:
                if index != simulators.index(name):
                    raise ValueError("'index' and 'name' must match")
            else:
                name = simulators[index]
        AGameSimulatorAdb.__init__(self, index, name)

    def ldconsole(self, cmd):
        cmd = '%s %s' % (self.console, cmd)
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return output.replace(b'\r', b'').decode(self.encoding)

    def adb(self, cmd):
        adb_command = cmd.replace(r'"', r'\"')
        cmd = '%s adb --index %d --command "%s"' % (self.console, self.index, adb_command)
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return output.replace(b'\r', b'').decode(self.encoding)
