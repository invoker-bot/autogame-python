# -*- coding: utf-8 -*-
# Author: Invoker
# Email : invoker-bot@outlook.com
# Site  : https://github.com/invokerrrr/autogame-python
# Data  : 2021/10/4

"""This module includes base classes of game simulators.

Note:
    * This module does not need to be import explicitly.

TODO:
    * Supports Linux and MacOS.
    * Supports to run on mobile operation systems.
"""

import re
import cv2
import tempfile
from abc import *
from os import path


class AGameSimulator(object, metaclass=ABCMeta):
    """A game simulator interface provides inputs and outputs interface of a game.

    The current consideration is to run mobile phone simulators on a PC operating system.
    Therefore, simulators must be downloaded from the Internet and then connected by this class.

    Notes:
        * Considering the actual requirements, the interface is designed based on the operation of the mobile terminal currently.

    Attributes:
        index(int): The index of the simulator. The number is unique for the same kind of simulators.
        name(str): The name of the simulator. The number is unique for the same kind of simulators.
    """

    def __init__(self, index=None, name=None):
        """Initializes a game simulator.

        Args:
            index (int): The `index` attribute.
            name (str): The `name` attribute.
        Raises:
            TypeError: If a parameter is error.
            ValueError: If `index` or `name` is not found.
            OSError: If cannot connect to the simulator.
        """
        self.index = index
        self.name = name

    @abstractmethod
    def screen_shot(self, gray=False):
        """Get a screenshot of the simulator.

        Args:
            gray (bool): Whether returns a grayscale or color image.
        Returns:
            numpy.ndarray: A numpy array of image.
        Raises:
            OSError: If failed to obtain a screenshot.
        """
        pass

    @abstractmethod
    def tap(self, x, y):
        """An operation equivalent to touch screen or left click.

        Args:
            x (float): The horizontal ordinate range from 0.0 to 1.0.
            y (float): The longitudinal ordinate range from 0.0 to 1.0.
        Raises:
            OSError: If failed to touch.
        """
        pass

    @abstractmethod
    def swipe(self, x0, y0, x1, y1, duration=None):
        """An operation equivalent to swipe the first point to the second.

        Args:
            x0 (float): The horizontal ordinate of the first point range from 0.0 to 1.0.
            y0 (float): The longitudinal ordinate of the first point range from 0.0 to 1.0.
            x1 (float): The horizontal ordinate of the second point range from 0.0 to 1.0.
            y1 (float): The longitudinal ordinate of the second point range from 0.0 to 1.0.
            duration (float): Time required for sliding.
        Raises:
            OSError: If failed to swipe.
        """
        pass

    @abstractmethod
    def is_valid(self):
        """Check whether the simulator is valid and will not throw exceptions.

        Returns:
            bool: Whether valid.
        """
        pass


class AGameSimulatorAdb(AGameSimulator):
    """An Android simulator interface supporting ADB (Android Debug Bridge)."""

    size_pat = re.compile(r'^\s*Physical\s*size:\s*(\d+)[xX*](\d+)', re.MULTILINE | re.IGNORECASE)
    """A regular expression for getting the simulator resolution."""
    valid_pat = re.compile(r'^device\s*$', re.MULTILINE | re.IGNORECASE)
    """A regular expression for getting device operation status."""

    @abstractmethod
    def adb(self, cmd):
        """Execute an ADB command.

        Note:
            Exceptions may or may not be thrown when failed to execute, so it is better to check by using
            `is_valid()` before executed.
        Args:
            cmd (str): A command string to be executed.
        Returns:
            str: The output string of the command.
        Raises:
            OSError: If failed to execute.
        """
        pass

    def screen_shot(self, gray):
        command = "shell /system/bin/screencap -p /sdcard/screencap.png"
        self.adb(command)
        tmp_file = path.join(tempfile.gettempdir(), "screencap.png")
        pull_command = "pull /sdcard/screencap.png %s" % tmp_file
        self.adb(pull_command)
        screen = cv2.imread(tmp_file, cv2.IMREAD_GRAYSCALE if gray else cv2.IMREAD_COLOR)
        if screen is None:
            raise OSError("invalid simulator")
        return screen

    def tap(self, x, y):
        width, height = self.size()
        command = "shell input tap %d %d" % (
            int(x * width), int(y * height))
        self.adb(command)

    def size(self):
        result = self.adb("shell wm size")
        m = re.search(self.size_pat, result)
        if m is None:
            raise OSError("unable to get the size of the simulator: %s" % result)
        return int(m.group(1)), int(m.group(2))

    def swipe(self, x1, y1, x2, y2, duration=None):
        width, height = self.size()
        duration = str(int(duration * 1000)) if duration else ""
        command = "shell input swipe %d %d %d %d %s" % (x1 * width, y1 * height,
                                                        x2 * width, y2 * height, duration)
        self.adb(command)

    def is_valid(self):
        try:
            result = self.adb("get-state")
            if re.match(self.valid_pat, result) is not None:
                return True
        except OSError:
            pass
        return False
