# importing packages
import numpy as np
import pandas as pd

# defining all colebrook-white functions

def a_vann(h, d):
    fyllingsgrad = h / d
    alpha = 2 * np.arccos(1 - 2 * fyllingsgrad) * 180 / np.pi

    avann = d**2/ 8 * ((alpha * np.pi) / 180 - np.sin(alpha * np.pi / 180))

    return avann, alpha


def hydraulisk_diameter(d, alpha, Avann):
    vaat_omkrets = (d * np.pi * alpha) / 360
    Dh = (4 * Avann) / vaat_omkrets

    return Dh


def roughness(material):
    pipe_materials = pd.Series(['plast', 'eternitt', 'nystål', 'støpejern', 'betong', 'stål'])
    ruhet = pd.Series([0.01, 0.1, 0.2, 0.5, 1, 2])
    ruhet = ruhet.divide(1000)

    d = {'MATERIAL': pipe_materials, 'RUHET': ruhet}

    ruhet_matrise = pd.DataFrame(d)
    ruhet = 0

    for i in range(len(ruhet_matrise.index)):
        if ruhet_matrise['MATERIAL'][i] == material:
            ruhet = ruhet_matrise['RUHET'][i]
            break
    return ruhet

def kinematisk(temp):

    vanntemp = pd.Series([2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40])
    kinematic = pd.Series([1.6736, 1.6191, 1.4716, 1.3849, 1.3063, 1.2347, 1.1692, 1.1092, 1.0541, 1.0034,
                           0.9565, 0.9131, 0.8729, 0.8355, 0.8007, 0.7682, 0.7379, 0.7095, 0.6828, 0.6579])
    kinematic = kinematic.divide(10**6)

    d = {'VANNTEMP [C]' : vanntemp, 'KINEMATIC [m2/s]' : kinematic}

    viskositet = pd.DataFrame(d)

    for i in range(len(viskositet.index)):
        if viskositet['VANNTEMP [C]'][i] == temp:
            my = viskositet['KINEMATIC [m2/s]'][i]
    return my

def fall(h1, h2, L):
    I = (h1-h2) / L
    return I

def colebrook(Avann, Dh, I, ruhet, my):
    g = 9.81
    Q = -2 * Avann * np.sqrt(2*g*Dh*I) * np.log10(ruhet/(3.71*Dh) + 2.51*my/(Dh*np.sqrt(2*g*Dh*I)))
    Q = Q*1000
    return Q


def velocity(Q, d):
    A_full = (np.pi / 4) * d ** 2
    v = Q / (A_full * 1000)

    return v

# combining all functions
def main(h, d, material, temp, h1, h2, L):
    Avann, alpha = a_vann(h, d)

    Dh = hydraulisk_diameter(d, alpha, Avann)

    ruhet = roughness(material)

    my = kinematisk(temp)

    I = fall(h1, h2, L)

    Q = colebrook(Avann, Dh, I, ruhet, my)

    v = velocity(Q, d)

    return Q, v

# printing output
x = main(0.3, 0.3, 'betong', 20, 1, 0, 1000)
print(f'VANNFØRINGEN I LEDNINGEN ER {round(x[0],1)} l/s')
print(f'HASTIGHETEN I LEDNINGEN ER {round(x[1],2)} m/s')