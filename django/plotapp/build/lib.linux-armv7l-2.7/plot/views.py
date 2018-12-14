# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views import generic
from plot.models import Func
from django.urls import reverse_lazy
from plot.forms import FuncForm

from PIL import Image
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Create your views here.

def index(request):
    return render(request, 'form.html')

def graph(formula, x_range):
    x = np.array(x_range)
    y = eval(formula)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(formula)
    ax.plot(x, y)
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.savefig('img.png')

def doPlot(formula):
    DC = 25
    RST = 23
    SPI_P = 0
    SPI_D = 0
    print(formula, " drawing!")
    graph(formula, range(-5, 5))
    disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_P, SPI_D, max_speed_hz=64000000))
    disp.begin()
    image = Image.open('img.png')
    image = image.rotate(90).resize((320,240))
    disp.display(image)
    

def plot(request):
    f = request.POST.get('func', None)
    try:
        doPlot(f)
    except:
        return HttpResponse("Can't draw function!")
    return render(request, 'img.html')
    #return HttpResponse("Draw!")
