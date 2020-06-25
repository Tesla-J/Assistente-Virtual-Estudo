from gtts import gTTS as tts
from subprocess import  Popen
import speech_recognition as sr
from subprocess import Popen
from os import system
from selenium import webdriver

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

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
		if 'pesquisar' in comando: #and comando[:9] == 'pesquisar':

			if 'pesquisar vídeo' in comando:
				self.pesquisar(comando.replace('pesquisar vídeo', ''), site='https://youtube.com')

			elif 'pesquisar anime' in comando:
				self.pesquisar(comando.replace('pesquisar anime', ''), site='https://superanimes.com')
				
			else:
				self.pesquisar(comando.replace('pesquisar', ''))

		elif 'vamos conversar' == comando:
				self.aprender()

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

	#carregar dicionario de conversa
	def carregar_dicionario(self):
		in_audio_list = []
		out_audio_list = []
		
		try:
			in_audio = open('in_audio.dat', 'r')
			out_audio = open('out_audio.dat', 'r')
			
			#guardar dados no dicionario interno
			try:
				for i in print(in_audio.read()):
					in_audio_list.append(i)
			except TypeError:
				pass
				
			try:
				for o in print(out_audio.read()):
					out_audio_list.append(o)
			except TypeError:
				pass
				
			try:
				for p in range(len(in_audio_list)):
					self.dicionario[in_audio_list[p]] = out_audio_list[p]
			except IndexError:
					pass
			
			#fechar arquivos
			in_audio.close()
			out_audio.close()
					
		except FileNotFoundError:
			IO.falar(self, 'Mestre, não encontro os meus arquivos de dicionário! Vou tentar criar novos para substituí-los.')
			try:
				in_audio = open('in_audio.dat', 'a')
				out_audio = open('out_audio.dat', 'a')
				in_audio.close()
				out_audio.close()
				self.carregar_dicionario()
			except: #caso não consiga criar um arquivo
				IO.falar(self, 'Mestre, não consegui criar os meus arquivos de dicionário. Vou encerrar-me por enquanto...')
				exit(1)
									

	#aprender a conversat
	def aprender(self):
		#self.carregar_dicionario()
		#in_audio = open('in_audio.dat', 'a')
		#out_audio = open('out_audio.dat', 'a')
		frase = ''
		IO.falar(self, 'Está bem sensei')
		while frase != 'Tchau' or frase != 'tchau':
			try:
				frase = IO.ouvir(self)
				if frase in self.dicionario:
					IO.falar(self,self.dicionario[frase])
				else:
					try: #guardar dados aprendidos
						IO.falar(self,'Como?')
						in_audio.write(frase+'\n')
						self.dicionario[frase] = IO.ouvir(self)
						out_audio.write(self.dicionario[frase]+'\n')
						IO.falar(self, 'Entendido mestre')
					except:
						IO.falar(self, 'Desculpe mestre, mas não consegui aprender')
			except sr.UnknownValueError:
				IO.falar(self, 'Hã?!')
