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

import RPi.GPIO as GPIO
import smbus

# Create your views here.
global pwm

def index(request):
    clearPwm()
    return render(request, 'form.html')

def alarmDiods(string):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    diods = [7, 8, 18, 16, 15, 13, 12, 11]
    c = 0
    for i in diods:
        GPIO.setup(i, GPIO.OUT)
        if string[c]=='1':
            GPIO.output(i, True)
        else:
            GPIO.output(i, False)
        c+=1

def clearPwm():
    global pwm
    pwm = []

def getResp():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    diods = [7, 8, 18, 16, 15, 13, 12, 11]
    s = ""
    for i in diods:
        GPIO.setup(i, GPIO.OUT)
        s+=str(GPIO.input(i))
    return s


def plot(request):
    f = request.POST.get('func', None)
    if len(f)<8:
        return HttpResponse("Too short input! Must me 8!")
    try:
        alarmDiods(f)
    except Exception, e:
        return HttpResponse(str(e))
    return HttpResponse("Diods alarmed! (" + getResp() + ")")

def diods(request):
    return render(request,'diods.html')



def doAnalog(br):
    global pwm
    pwm = []
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    diods = [7, 8, 18, 16, 15, 13, 12, 11]
    c = 0
    for i in diods:
        GPIO.setup(i, GPIO.OUT)
        p = GPIO.PWM(i, 100)
        pwm.append(p)
        pwm[c].start(1)
        pwm[c].ChangeDutyCycle(br[c])
        c+=1


def analog(request):
    d1 = request.POST.get('d1', None)
    d2 = request.POST.get('d2', None)
    d3 = request.POST.get('d3', None)
    d4 = request.POST.get('d4', None)
    d5 = request.POST.get('d5', None)
    d6 = request.POST.get('d6', None)
    d7 = request.POST.get('d7', None)
    d8 = request.POST.get('d8', None)
    arr = [float(d1),float(d2),float(d3),float(d4),float(d5),float(d6),float(d7),float(d8)]
    doAnalog(arr)
    return HttpResponse("Yeah! " + str(arr))

def light(request):
    bus = smbus.SMBus(1)
    address = 0x29
    bus.write_byte(address, 0xa0)
    bus.write_byte(address, 0x03)
    bus.write_byte(address, 0xac)
    a = bus.read_byte(address)
    bus.write_byte(address, 0xad)
    b = bus.read_byte(address)
    return HttpResponse("<html><head><meta http-equiv='refresh' content='1'><title>Light Level</title></head><body>Light level = " + str(a+b*256) + "</body></html>")
