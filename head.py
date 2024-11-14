import tkinter as tk
from tkinter import filedialog
from tkinter import *
from collections import Counter
from tkinter import messagebox
import sys
import os 
import re
import time
import win32console
import win32gui
import sc2reader
import pandas as pd
from alive_progress import alive_bar

from BuildInformation import *

global ErrorReport
global FUllTIME

ErrorReport=""
FULLTIME="n"
