from django.http import HttpResponse, HttpResponseNotFound, HttpRequest, HttpResponseForbidden
from MiResumen.models import usuarios,micronoteros,micronotas,microusuarios
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from django.template.loader import get_template
from django.template import Context

import parserRSS
import httplib
import xml.sax

	
def main(request):
	if request.user.is_authenticated():

		u=usuarios.objects.get(usuario=request.user.username)
		idioma=u.idioma
		if idioma=='es':		
			template = get_template("registration/autenticado.html")
		elif idioma=='en':
			template = get_template("registration/authenticated.html")


		if request.method=='GET':
			user=request.user.username
			print user
			u=usuarios.objects.get(usuario=user)
			nom=u.nombrePublico
			print nom
			if nom=="":
				nom=user
			x=micronotas.objects.order_by('-pubdate')[:50]
			return HttpResponse(template.render(Context({'usuario':nom,'body':x})))

	else:
		if request.method=='GET':
			template = get_template("registration/notitas.html")
			x=micronotas.objects.order_by('-pubdate')[:50]
			return HttpResponse(template.render(Context({'body':x})))

def micros(request):
	if request.user.is_authenticated():
		u=usuarios.objects.get(usuario=request.user.username)
		idioma=u.idioma
		if idioma=='es':		
			template = get_template("registration/autenticado.html")
		elif idioma=='en':
			template = get_template("registration/authenticated.html")
		if request.method=='GET':
			user=request.user.username
			print user
			u=usuarios.objects.get(usuario=user)
			nom=u.nombrePublico
			print nom
			if nom=="":
				nom=user
			x=micronoteros.objects.all()
			return HttpResponse(template.render(Context({'usuario':nom,'todos':x})))

	else:
		template = get_template("registration/notitas.html")
		if request.method=='GET':
			x=micronoteros.objects.all()
			return HttpResponse(template.render(Context({'todos':x})))

def usus(request):
	if request.user.is_authenticated():
		u=usuarios.objects.get(usuario=request.user.username)
		idioma=u.idioma
		if idioma=='es':		
			template = get_template("registration/autenticado.html")
		elif idioma=='en':
			template = get_template("registration/authenticated.html")

		if request.method=='GET':
			user=request.user.username
			print user
			u=usuarios.objects.get(usuario=user)
			nom=u.nombrePublico
			print nom
			if nom=="":
				nom=user
			x=User.objects.all()
			return HttpResponse(template.render(Context({'usuario':nom,'main':x})))

	else:
		template = get_template("registration/notitas.html")
		if request.method=='GET':
			x=User.objects.all()
			return HttpResponse(template.render(Context({'main':x})))

def noticiasMicronotero(request,micronotero):
	if request.user.is_authenticated():

		u=usuarios.objects.get(usuario=request.user.username)
		idioma=u.idioma
		if idioma=='es':		
			template = get_template("registration/autenticado.html")
		elif idioma=='en':
			template = get_template("registration/authenticated.html")

		
		if request.method=='GET':
			try:	
				user=request.user.username
				u=usuarios.objects.get(usuario=user)
				nom=u.nombrePublico
				if nom=="":
					nom=user
			except:
				nom=user
			x=micronotas.objects.extra(where=['notero=%s'], params=[micronotero]).order_by('-pubdate')
			return HttpResponse(template.render(Context({'usuario':nom,'micronotero': micronotero,'micronotas':x})))
	else:
		if request.method=='GET':
			template = get_template("registration/notitas.html")
			x=micronotas.objects.extra(where=['notero=%s'], params=[micronotero]).order_by('-pubdate')
			return HttpResponse(template.render(Context({'micronotero': micronotero,'micronotas':x})))

def noticiasUsuario(request,user):
	if request.user.is_authenticated():
		u=usuarios.objects.get(usuario=request.user.username)
		idioma=u.idioma
		if idioma=='es':		
			template = get_template("registration/autenticado.html")
		elif idioma=='en':
			template = get_template("registration/authenticated.html")

		if request.method=='GET':	
			try:
				use=request.user.username
				u=usuarios.objects.get(usuario=use)
				nom=u.nombrePublico
				if nom=='':
					nom=use
				u=microusuarios.objects.extra(where=['usuario=%s'],params=[user])
				x=micronotas.objects.extra(where=['notero=%s'],params=[u[0].micronotero]).order_by('-pubdate')
				for i in u:
					x=x|micronotas.objects.extra(where=['notero=%s'],params=[i.micronotero]).order_by('-pubdate')
				return HttpResponse(template.render(Context({'usuario': nom, 'micros': u, 'notas': x})))
			except:
				return render_to_response('registration/error.html')
	else:
		template = get_template("registration/notitas.html")
		if request.method=='GET':	
			try:
				u=microusuarios.objects.extra(where=['usuario=%s'],params=[user])
				x=micronotas.objects.extra(where=['notero=%s'],params=[u[0].micronotero]).order_by('-pubdate')
				for i in u:
					x=x|micronotas.objects.extra(where=['notero=%s'],params=[i.micronotero]).order_by('-pubdate')
				return HttpResponse(template.render(Context({'usuario': user, 'micronoteros': u, 'notas': x})))
			except:
				return render_to_response('registration/error.html')


		
def confUsuario(request):
	if request.user.is_authenticated():

		u=usuarios.objects.get(usuario=request.user.username)
		idioma=u.idioma
		
		if idioma=='es':		
			template = get_template("registration/config.html")
			if request.method=='GET':
				user=request.user.username
				mensaje='Modifica tu perfil'	
				try:
					u=usuarios.objects.get(usuario=user)
					nom=u.nombrePublico	
					if nom=='':				
						nom=user
					return HttpResponse(template.render(Context({'usuario':nom ,'msg':mensaje})))
				except:
					nom = user				
					return HttpResponse(template.render(Context({'usuario':nom ,'msg':mensaje})))

			if request.method=='POST':
				user=request.user.username
				nom = request.POST['nombre']
				pas = request.POST['pass']
				che = request.POST['check']
				idi = request.POST['idioma']
				if pas==che:
					usu = User.objects.get(username__exact=user)
		        		usu.set_password(pas)
		        		usu.save()
					u = usuarios.objects.get(usuario=usu)
					u.nombrePublico = nom
					u.idioma = idi
					u.save()
				else:
					template = get_template("registration/config.html")
					mensaje='Password no valida'
					return HttpResponse(template.render(Context({'usuario': nom,'msg':mensaje})))
				return render_to_response('registration/cambiado.html')

		elif idioma=='en':
			template = get_template("registration/configuration.html")

			if request.method=='GET':
				user=request.user.username
				mensaje='Change your profile'	
				try:
					u=usuarios.objects.get(usuario=user)
					nom=u.nombrePublico	
					if nom=='':				
						nom=user
					return HttpResponse(template.render(Context({'usuario':nom ,'msg':mensaje})))
				except:
					nom = user				
					return HttpResponse(template.render(Context({'usuario':nom ,'msg':mensaje})))

			if request.method=='POST':
				user=request.user.username
				nom = request.POST['nombre']
				pas = request.POST['pass']
				che = request.POST['check']
				idi = request.POST['idioma']
				if pas==che:
					usu = User.objects.get(username__exact=user)
		        		usu.set_password(pas)
		        		usu.save()
					u = usuarios.objects.get(usuario=usu)
					u.nombrePublico = nom
					u.idioma = idi
					u.save()
				else:
					template = get_template("registration/configuration.html")
					mensaje='Password invalida'
					return HttpResponse(template.render(Context({'usuario': nom,'msg':mensaje})))
				return render_to_response('registration/changed.html')
	else:
		return render_to_response('registration/notitas.html')	
		

def confEstilo(request):
	if request.user.is_authenticated():
		u=usuarios.objects.get(usuario=request.user.username)
		idioma=u.idioma
		if idioma=='es':		
			template = get_template("registration/confEstilo.html")
			mensaje='CSS nuevo modificado correctamente'
		elif idioma=='en':
			template = get_template("registration/confStyle.html")
			mensaje='New CSS successfully changed'

		usu=request.user.username
		u=usuarios.objects.get(usuario=usu)
		nom=u.nombrePublico
		if nom=="":
			nom=usu


		if request.method == 'GET':	
			tod=User.objects.all()
			for i in tod:
				print i.username
			#le paso la lista de usuarios a la plantilla
			record=usuarios.objects.get(usuario=usu)	
			return HttpResponse(template.render(Context({'usuario': nom,'lista':tod, 'css':record.css})))

		if request.method == "POST":
			try:
				cssnew=request.POST['cssnuevo']
				u=usuarios.objects.get(usuario=usu)
				u.css=cssnew
				u.save()
				return HttpResponse(template.render(Context({'usuario': nom,'msg':mensaje})))
			except:			
				usuCopy=request.POST['usu']
				u=usuarios.objects.get(usuario=usu)
				uC=usuarios.objects.get(usuario=usuCopy)
				u.css=uC.css
				u.save()
				return HttpResponse(template.render(Context({'usuario': nom,'msg':mensaje})))
	else:
		return render_to_response('registration/notitas.html')	
				
def mcss(request):

	if request.user.is_authenticated():
		user=request.user.username
		u=usuarios.objects.get(usuario=user)
		myResponse = HttpResponse(u.css)
		myResponse['Content-Type'] = 'text/css'
		return myResponse

	else:
		fichero=open('estilo.css')
		basicCss=fichero.read()	
		myResponse = HttpResponse(basicCss)
		myResponse['Content-Type'] = 'text/css'
		return myResponse


			
def micronoterosUsuario(request):
	if request.user.is_authenticated():
		u=usuarios.objects.get(usuario=request.user.username)
		idioma=u.idioma
		if idioma=='es':		
			template = get_template("registration/autenticado.html")
		elif idioma=='en':
			template = get_template("registration/authenticated.html")

		user=request.user.username
		u=usuarios.objects.get(usuario=user)
		nom=u.nombrePublico
		if nom=="":
			nom=usu


		if request.method=='GET':			
			#user=request.user.username
			u=microusuarios.objects.extra(where=['usuario=%s'],params=[user])
			return HttpResponse(template.render(Context({'usuario': nom, 'micronoteros': u})))

		if request.method=='POST':
			user=request.user.username   # metemos el nuevo micronotero
			try:
				noter = request.POST['micronotero']		
					
				try:
					u=microusuarios.objects.get(usuario=user,micronotero=noter)
					u.delete()
					m=microusuarios.objects.extra(where=['usuario=%s'],params=[user])
					return HttpResponse(template.render(Context({'usuario': nom, 'micronoteros':m})))


				except microusuarios.DoesNotExist:
					u=microusuarios(usuario=user,micronotero=noter)
					u.save()

					#descargamos la pagina del usuario para saber cual es su ID
					conn = httplib.HTTPConnection("identi.ca")
					notero = "/"+u.micronotero
					conn.request("GET", notero)
					r1 = conn.getresponse()
					data1 = r1.read()
					conn.close()
					#ahora nos quedaremos con su ID troceando
					data11=data1.partition('" type="application/rss+xml"')
					ID=data11[0].partition('href="http://identi.ca/api/statuses/user_timeline/')
					numeroIDrss=str(ID[2])
					numeroID=str(ID[2]).split('.',1)[0]
					print 'esto es el numeroID '+ numeroID
					#pedimos su rss para parsearlo
					conn2 = httplib.HTTPConnection("identi.ca")
					conn2.request("GET", "/api/statuses/user_timeline/"+numeroIDrss)
					r2 = conn2.getresponse()
					data2 = r2.read()
					conn2.close()
					#parseamos
					testParser=parserRSS.myContentHandler()
					myContentHandler = parserRSS.make_parser()
					myContentHandler = parserRSS.myContentHandler()
					xml.sax.parseString(data2, myContentHandler)

					m=microusuarios.objects.extra(where=['usuario=%s'],params=[user])
					return HttpResponse(template.render(Context({'usuario': nom, 'micronoteros':m})))


			except:
				m=microusuarios.objects.extra(where=['usuario=%s'],params=[user])
				otroUsuario = request.POST['copy']
				x=microusuarios.objects.extra(where=['usuario=%s'],params=[otroUsuario])
				for i in x:
					try:
						m=microusuarios.objects.get(usuario=user,micronotero=i.micronotero)
					except:
						m=microusuarios(usuario=user,micronotero=i.micronotero)
						m.save()
				m=microusuarios.objects.extra(where=['usuario=%s'],params=[user])
				return HttpResponse(template.render(Context({'usuario': nom, 'micronoteros':m})))
				
	else:
		return render_to_response('registration/notitas.html')	




def autenticado(request):
	if request.user.is_authenticated():

		u=usuarios.objects.get(usuario=request.user.username)
		idioma=u.idioma
		if idioma=='es':		
			template = get_template("registration/autenticado.html")
		elif idioma=='en':
			template = get_template("registration/authenticated.html")


		user=request.user.username
		u=usuarios.objects.get(usuario=user)
		nom=u.nombrePublico
		if nom=="":
			nom=usu

		return HttpResponse(template.render(Context({'usuario': nom})))
		
	else:
		return render_to_response('registration/notitas.html')	
	

def actualiza(request):	
	if request.user.is_authenticated():

		u=usuarios.objects.get(usuario=request.user.username)
		idioma=u.idioma
		if idioma=='es':		
			template = get_template("registration/autenticado.html")
			micronoticias='Se actualizaron las micronoticias de sus micronoteros'
		elif idioma=='en':
			template = get_template("registration/authenticated.html")
			micronoticias='We updated the little notes Noter'


		user=request.user.username
		u=usuarios.objects.get(usuario=user)
		nom=u.nombrePublico
		if nom=="":
			nom=usu
		if request.method=='GET':
			u=microusuarios.objects.extra(where=['usuario=%s'],params=[user])
			for i in u:				
				notero=i.micronotero
				#descargamos la pagina del usuario para saber cual es su ID
				conn = httplib.HTTPConnection("identi.ca")
				noter = "/"+notero
				conn.request("GET", noter)
				r1 = conn.getresponse()
				data1 = r1.read()
				conn.close()
				#ahora nos quedaremos con su ID troceando
				data11=data1.partition('" type="application/rss+xml"')
				ID=data11[0].partition('href="http://identi.ca/api/statuses/user_timeline/')
				numeroIDrss=str(ID[2])
				numID=str(ID[2]).split('.',1)[0]
				print 'esto es el numeroID '+ numID
				#pedimos su rss para parsearlo
				conn2 = httplib.HTTPConnection("identi.ca")
				conn2.request("GET", "/api/statuses/user_timeline/"+numeroIDrss)
				r2 = conn2.getresponse()
				data2 = r2.read()
				conn2.close()
				#parseamos
				testParser=parserRSS.myContentHandler()
				myContentHandler = parserRSS.make_parser()
				myContentHandler = parserRSS.myContentHandler()
				xml.sax.parseString(data2, myContentHandler)
			return HttpResponse(template.render(Context({'usuario':user,'msg':micronoticias,'lista':u})))
	else:
		return render_to_response('registration/notitas.html')	
	
# descargo canal y guardo numeroID en tabla micronoteros
def inicio(request,notero):
	usuario = request.user.username
	if request.method=='GET':
		template = get_template("registration/inicio.html")
		u=usuarios.objects.get(usuario=usuario)
		u1=usuarios.objects.get(usuario='jorge')
		u2=usuarios.objects.get(usuario='pepe')
		u3=usuarios.objects.get(usuario='pepa')
		fichero=open('./css/estilo.css')
		cssestandar=fichero.read()
		u3.css=cssestandar
		u3.save()
		u2.css=cssestandar
		u2.save()
		u1.css=cssestandar
		u1.save()
		u.css=cssestandar
		u.save()
		#descargamos la pagina del usuario para saber cual es su ID
		conn = httplib.HTTPConnection("identi.ca")
		noter = "/"+notero
		conn.request("GET", noter)
		r1 = conn.getresponse()
		data1 = r1.read()
		conn.close()
		#ahora nos quedaremos con su ID troceando
		data11=data1.partition('" type="application/rss+xml"')
		ID=data11[0].partition('href="http://identi.ca/api/statuses/user_timeline/')
		numeroIDrss=str(ID[2])
		numeroID=str(ID[2]).split('.',1)[0]
		print 'esto es el numeroID '+ numeroID
		#pedimos su rss para parsearlo
		conn2 = httplib.HTTPConnection("identi.ca")
		conn2.request("GET", "/api/statuses/user_timeline/"+numeroIDrss)
		r2 = conn2.getresponse()
		data2 = r2.read()
		conn2.close()
		#parseamos
		testParser=parserRSS.myContentHandler()
		myContentHandler = parserRSS.make_parser()
		myContentHandler = parserRSS.myContentHandler()
		xml.sax.parseString(data2, myContentHandler)
		micronoticias='todas mis noticias'
		return HttpResponse(template.render(Context({'user':usuario,'body':micronoticias})))
	else:
		return HttpResponseForbidden('')


