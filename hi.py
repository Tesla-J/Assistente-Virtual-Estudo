# -*- coding: utf-8 -*-

from gtts import gTTS as tts
from subprocess import  Popen
import speech_recognition as sr
import interpreter

texto = ''
senses = interpreter.Functions()
interp = interpreter.Functions()

senses.falar('Às suas ordens mestre.')

while True:
		try:
			texto = senses.ouvir()
			interp.interpret(texto)
			print (texto)
		except sr.UnknownValueError:
			#senses.falar('Entrada inválida!')
			pass
