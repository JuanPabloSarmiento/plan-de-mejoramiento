from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuarios
from .forms import UsuariosForm, LoginForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import send_mail
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64




def lista_usuarios(request):
    usuario_actual = None
    if 'usuario_id' in request.session:
        usuario_actual = get_object_or_404(Usuarios, id=request.session['usuario_id'])

    usuarios = Usuarios.objects.all()
    return render(request, 'usuarios/lista.html', {
        'usuarios': usuarios,
        'usuario_actual': usuario_actual
    })

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuariosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuariosForm()
    return render(request, 'usuarios/formulario.html', {'form': form})


def editar_usuario(request, id):
    usuario = get_object_or_404(Usuarios, id=id)
    if request.method == 'POST':
        form = UsuariosForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuariosForm(instance=usuario)
    return render(request, 'usuarios/formulario.html', {'form': form})

def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuarios, id=id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')
    return render(request, 'usuarios/confirmar_eliminar.html', {'usuario': usuario})


def login_usuario(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            try:
                usuario = Usuarios.objects.get(correo=correo, contrasena=contrasena)
                request.session['usuario_id'] = usuario.id  # Guardamos sesión
                return redirect('lista_usuarios')  # Redirigir a una vista protegida
            except Usuarios.DoesNotExist:
                error = "Correo o contraseña incorrectos"
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form, 'error': error})

def logout_usuario(request):
    request.session.flush()  # Borra toda la sesión
    return redirect('login_usuario')


def exportar_usuarios_pdf(request):
    imagen_base64 = generar_grafico_edad()
    usuarios = Usuarios.objects.all()
    template = get_template('usuarios/usuarios_pdf.html')
    html = template.render({
        'usuarios': usuarios,
        'grafico_base64': imagen_base64
    })
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="usuarios.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF")
    return response


def enviar_correo_test(request):
    send_mail(
        subject='Prueba de correo desde Django',
        message='Hola Juan Pablo, este es un correo de prueba.',
        from_email='juanpnavarrete0@gmail.com',
        recipient_list=['richardo0_0@hotmail.com'],
        fail_silently=False,
    )
    return HttpResponse("Correo enviado correctamente")




def generar_grafico_edad():
    usuarios = Usuarios.objects.all().values('nombre', 'edad')
    df = pd.DataFrame(list(usuarios))

    plt.figure(figsize=(6,4))
    plt.hist(df['edad'], bins=5, color='skyblue', edgecolor='black')
    plt.title("Distribución de edades")
    plt.xlabel("Edad")
    plt.ylabel("Cantidad de usuarios")

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return imagen_base64  # Se usará en el HTML como <img src="data:image/png;base64,...">



from django.core.mail import EmailMessage

def enviar_pdf_por_correo(request):
    imagen_base64 = generar_grafico_edad()
    usuarios = Usuarios.objects.all()

    template = get_template('usuarios/usuarios_pdf.html')
    html = template.render({
        'usuarios': usuarios,
        'grafico_base64': imagen_base64
    })

    buffer = BytesIO()
    pisa.CreatePDF(html, dest=buffer)
    buffer.seek(0)

    email = EmailMessage(
        subject='Informe de usuarios',
        body='Adjunto encontrarás el informe con gráfico de edades.',
        from_email='juanpnavarrete0@gmail.com',
        to=['richardo0_0@hotmail.com'],
    )
    email.attach('informe_usuarios.pdf', buffer.read(), 'application/pdf')
    email.send()

    return HttpResponse('Correo con PDF enviado correctamente')
