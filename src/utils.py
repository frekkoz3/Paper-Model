r"""
     _____                        __  __           _      _ 
    |  __ \                      |  \/  |         | |    | |
    | |__) |_ _ _ __   ___ _ __  | \  / | ___   __| | ___| |
    |  ___/ _` | '_ \ / _ \ '__| | |\/| |/ _ \ / _` |/ _ \ |
    | |  | (_| | |_) |  __/ |    | |  | | (_) | (_| |  __/ |
    |_|   \__,_| .__/ \___|_|    |_|  |_|\___/ \__,_|\___|_|
                | |                                          
                |_|                         

    A simple rule-based model to generate realistical newspapers' pages for the training of the YOLO-Layout model.
"""
import random
from datetime import datetime, timedelta

import os
import time
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import shutil

MIN_YEAR = 1600
MAX_YEAR = 2026

def random_datetime():
    # generate a random datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(MIN_YEAR, 1, 1, 00, 00, 00)
    years = MAX_YEAR - MIN_YEAR + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

def start_server(directory=".", port=8000):

    os.chdir(directory)
    httpd = HTTPServer(("localhost", port), SimpleHTTPRequestHandler)

    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    time.sleep(0.5)  # time to start the server

    return httpd

def clean_folder(folder="data/"):

    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)

        if os.path.isdir(item_path):
            shutil.rmtree(item_path)