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
    user = ['Marc', 'Lucas'][num]
    weight = ['180', '200'][num]

    return user, weight, values

