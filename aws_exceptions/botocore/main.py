"""
Script: botocore_exceptions.py
Author: Dennis Barger
Date:   3/12/2022

Generate list of statically defined botocore exceptions.
"""

import botocore.exceptions

for key, value in sorted(botocore.exceptions.__dict__.items()):
    if isinstance(value, type):
        print(key)