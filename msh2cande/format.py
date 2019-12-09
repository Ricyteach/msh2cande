import numpy as np


def optional(value, fmt):
    if value in (None, np.nan):
        return f"{'':{fmt[:-1]+'s':s}}"
    return f"{value:{fmt:s}}"


def c2(steps, nodes, elements, boundaries, materials, interfaces=None):
    return f"{steps: >5d}    3    1    3    0{nodes: >5d}{elements: >5d}{boundaries: >5d}{materials: >5d}{optional(interfaces, ' >5d'):s}    1"


def c3(n, x, y):
    return f"{n: >4.0f}  000{x: >10.2f}{y: >10.2f}"


def c4(e, i, j, k, l, mat, step, interf=None):
    return f"{e: >4.0f}{i: >5.0f}{j: >5.0f}{k: >5.0f}{l: >5.0f}{mat: >5.0f}{step: >5.0f}{optional(interf, ' >5.0f'):s}"


def c5(n, xcode=0, xvalue=0, ycode=0, yvalue=0, angle=0, step=0):
    return f"{n: >4.0f}{xcode: >5.0f}{xvalue: >10.2f}{ycode: >5.0f}{yvalue: >10.2f}{angle: >10.2f}{step: >5.0f}"
