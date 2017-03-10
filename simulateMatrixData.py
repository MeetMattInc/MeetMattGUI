# -*- coding: utf-8 -*-

# simMatrix.py - Simulates random matrix, weight, and user data for testing the
# GUI.

from random import random

def simulateMatrixData():
    row = 29
    col = 43
    values = []

    for y in range(row):
            values.append([round(random()) for x in range(col)])

    num = round(random())
    user = ['User 1', 'User 2'][num]
    weight = ['180kg', '200kg'][num]

    return user, weight, values

