# -*- coding: utf-8 -*-

from gtts import gTTS as tts
from subprocess import  Popen
import speech_recognition as sr
from subprocess import Popen
from os import system
from selenium import webdriver

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer #ListTrainer

#navegador (apenas firefox)
class Browser (object):
	def __init__(self):
		pass ##self.firefox = webdriver.Firefox()

#comunicação
class IO (object):
	def __init__(self):
		pass
	#ouvir
	def ouvir(self):
		rec = sr.Recognizer()
		with sr.Microphone() as fala:
			#rec.non_speaking_diration=0.1
			rec.adjust_for_ambient_noise(fala)
			print('Ouvindo...')
			frase = rec.listen(fala)
		return  rec.recognize_google(frase, language='pt')

	#falar (pelo vlc)
	def falar(self,afirmacao):
		voice = tts(afirmacao, lang='pt')
		voice.save('ensaio1.mp3')
		Popen(['cvlc', 'ensaio1.mp3'])


#acções
class Functions (IO, Browser):
	def __init__(self):
		IO.__init__(self)
		Browser.__init__(self)
		self.dicionario = dict()

	def interpret(self,comando):
		comando = comando.lower()
		if 'pesquisar' in comando: #and comando[:9] == 'pesquisar':

			if 'pesquisar vídeo' in comando:
				self.pesquisar(comando.replace('pesquisar vídeo', ''), site='https://youtube.com')

			elif 'pesquisar anime' in comando:
				self.pesquisar(comando.replace('pesquisar anime', ''), site='https://superanimes.com')
				
			else:
				self.pesquisar(comando.replace('pesquisar', ''))

		elif 'vamos conversar' == comando:
				self.conversar()

		elif comando == 'terminar':
				exit()

		elif comando == 'desligar computador' or comando == 'Desligar computador':
				system('shutdown 0')

	#pesquisar termos no navegador
	def pesquisar(self, string_pesquisa, site='https://startpage.com', id_bar='input'):
		#print('Diga o que quer pesquisar, mestre.')
		#IO.falar(self,'O que o mestre deseja pesquisar?')
		termo = string_pesquisa #IO.ouvir(self)
		try:
			abas = len(Browser.firefox.window_handles)
			print(abas)
			Browser.firefox.execute_script('''window.open("{}", "_blank")'''.format(site))
			Browser.firefox.switch_to_window(Browser.firefox.window_handles[abas]) #indice da ultima aba
		except:
			Browser.firefox = webdriver.Firefox()
		Browser.firefox.get(site)
		Browser.firefox.maximize_window()
		barra_pesquisa = Browser.firefox.find_element_by_tag_name(id_bar)
		barra_pesquisa.send_keys(termo)
		barra_pesquisa.submit()

	
	#aprender a conversat
	def conversar(self):
		bot = ChatBot('Lukénia')
		conversas = ['Oi', 'Olá', 'Tudo bem?', 'Estou bem, obrigada.', 'Bom dia.', 'Boa noite.', 'Boa tarde', 'Como te chamas?', 'Qual é o seu nome?', 'Me diga seu nome', 'Me chamo Lukénia', 'Meu mestre me nomeou Lukénia']
		trainer = ChatterBotCorpusTrainer(bot) #ListTrainer(bot)
		trainer.train('sugestoes')
		trainer.train('ensaio')
		
		#frase = ''
		IO.falar(self, 'Sim mestre!')
		frase=''
		resposta=''
		while frase != 'Tchau' or frase != 'tchau':
			try:
				frase = IO.ouvir(self)
				resposta = bot.get_response(frase)
				IO.falar(self,str(resposta))
					
			except sr.UnknownValueError:
				#IO.falar(self, 'Hã?!')
				pass
