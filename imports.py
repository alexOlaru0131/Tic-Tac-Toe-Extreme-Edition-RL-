###### imports.py ######
# -> imports all necessary libraries in order for the project to run
# -> also here are imported all the files to make a global bin

# OPENAI GYMNASIUM //
import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register

# OpenCV
import cv2

# OTHER IMPORTS //
import numpy as np
from collections import defaultdict
from typing import Optional
from tqdm import tqdm # looking professional B) and seeing progress
from matplotlib import pyplot as plt
import pygame
from pygame.locals import *
import sys
import time
import pyautogui
import PIL
import math
from threading import Thread, Event, Lock

# FILE IMPORTS //
from tic_tac_toe_env import TicTacToe
from gui import GUI

###### END IMPORTS ######