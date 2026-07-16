from django.shortcuts import render, redirect
from .models import Tecnico, Cursos, Certificado
from django.contrib import messages
import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Perfil

from django.core.mail import EmailMessage
from django.conf import settings
from playwright.sync_api import sync_playwright
import tempfile



# Ruta de inicio
def inicio(request):
    # Presentando en pantalla el contenido de
    return render(request, 'inicio.html')

def nuevoTecnico(request):
    return render(request, 'nuevoTecnico.html')

def es_admin(request):
    return request.user.perfil.rol == "admin"


#--------------------- PARTE DEL TECNICO -----------------------------
# Funcion para capturar los datos ingresados en el formulario e insertar en la bd
# ¡Corregido siguiendo el patrón exacto de tu ejemplo de estadios!
def guardarTecnico(request):
    # Capturando valores via metodo POST
    nombreNuevoTecnico = request.POST["nombre"]
    apellidoNuevoTecnico = request.POST["apellido"]
    telefonoNuevoTecnico = request.POST["telefono"]
    especialidadNuevoTecnico = request.POST["especialidad"]
    correoNuevoTecnico = request.POST.get('correo', '')
    # Capturando el archivo de name=foto que se creo en nuevo tecnico
    fotoNuevoTecnico = request.FILES.get('foto')
    
    # Instanciar un objeto "Tecnico"
    nuevoTecnico = Tecnico.objects.create(
        nombre=nombreNuevoTecnico,
        apellido=apellidoNuevoTecnico,
        telefono=telefonoNuevoTecnico,
        especialidad=especialidadNuevoTecnico,
        correo=correoNuevoTecnico,
        foto=fotoNuevoTecnico
    )
    messages.success(request, "Técnico guardado exitosamente")
    return redirect('/listadoTecnicos/')

# Renderizando la GUI de listado de tecnicos
@login_required
def listadoTecnicos(request):

    tecnicos = Tecnico.objects.all()

    return render(
        request,
        'listadoTecnicos.html',
        {'tecnicos':tecnicos}
    )

# Eliminacion de tecnico por id
def eliminarTecnico(request,id):
    tecnicoEliminar = Tecnico.objects.get(id=id)
    if tecnicoEliminar.foto:
        tecnicoEliminar.foto.delete()  
    tecnicoEliminar.delete()
    messages.success(request, "Técnico eliminado exitosamente")
    return redirect('/listadoTecnicos/')

# Ubicando el tecnico que se quiere editar por su id
@login_required
def editarTecnico(request,id):

    if not es_admin(request):
        return redirect('/inicio/')


    tecnicoEditar = Tecnico.objects.get(id=id)

    return render(
        request,
        'editarTecnico.html',
        {'tecnico':tecnicoEditar}
    )

# Procesando actualizacion de tecnicos
def procesarActualizacionTecnico(request):
    id = request.POST['id']
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    telefono = request.POST['telefono']
    especialidad = request.POST['especialidad']
    
    tecnicoEditar = Tecnico.objects.get(id=id)
    
    tecnicoEditar.nombre = nombre
    tecnicoEditar.apellido = apellido
    tecnicoEditar.telefono = telefono
    tecnicoEditar.especialidad = especialidad
    tecnicoEditar.correo = request.POST.get('correo', '')  # Actualizar el correo si se proporciona
    
    # Si suben foto nueva, eliminar la anterior
    nueva_foto = request.FILES.get('foto')
    if nueva_foto:
        if tecnicoEditar.foto:
            if os.path.isfile(tecnicoEditar.foto.path):
                os.remove(tecnicoEditar.foto.path)
        tecnicoEditar.foto = nueva_foto
    
    tecnicoEditar.save()
    messages.success(request, 'Técnico actualizado correctamente')
    return redirect('/listadoTecnicos/')

# Funcion para renderizar en pantalla el reporte de tecnicos
def reporteTecnicos(request):
    tecnicos = Tecnico.objects.all()
    return render(request, 'reporteTecnicos.html', {'misTecnicos': tecnicos})

#--------------------- PARTE DEL CURSO -----------------------------

def nuevoCurso(request):
    # CORREGIDO: Buscamos todos los técnicos y los pasamos en el contexto del render
    tecnicos = Tecnico.objects.all()
    return render(request, 'nuevoCurso.html', {'tecnicos': tecnicos})

def guardarCurso(request):
    nombreNuevoCurso = request.POST["nombre"]
    descripcionNuevoCurso = request.POST["descripcion"]
    fechaInicioNuevoCurso = request.POST["fecha_inicio"]
    fechaFinNuevoCurso = request.POST["fecha_fin"]
    tecnicoId = request.POST.get("tecnico_id")  # Obtener el ID del técnico seleccionado
    tecnico = Tecnico.objects.get(id=tecnicoId)
    
    nuevoCurso = Cursos.objects.create(
        nombre=nombreNuevoCurso,
        descripcion=descripcionNuevoCurso,
        fecha_inicio=fechaInicioNuevoCurso,
        fecha_fin=fechaFinNuevoCurso,
        tecnico=tecnico
    )
    messages.success(request, "Curso guardado exitosamente")
    return redirect('/listadoCursos/')


@login_required
def listadoCursos(request):

    cursos = Cursos.objects.all()

    return render(
        request,
        'listadoCursos.html',
        {'cursos': cursos}
    )


@login_required
def eliminarCurso(request, id):
    cursoEliminar = Cursos.objects.get(id=id)
    cursoEliminar.delete()
    messages.success(request, "Curso eliminado exitosamente")
    return redirect('/listadoCursos/')

@login_required
def editarCurso(request, id):
    cursoEditar = Cursos.objects.get(id=id)
    tecnicos = Tecnico.objects.all()  # Obtener todos los técnicos para el dropdown
    return render(request, 'editarCurso.html', {'curso': cursoEditar, 'tecnicos': tecnicos})

def procesarActualizacionCurso(request):
    id = request.POST['id']
    nombre = request.POST['nombre']
    descripcion = request.POST['descripcion']
    fecha_inicio = request.POST['fecha_inicio']
    fecha_fin = request.POST['fecha_fin']
    tecnicoId = request.POST.get("tecnico_id")  # Obtener el ID del técnico seleccionado
    tecnico = Tecnico.objects.get(id=tecnicoId)
    
    cursoEditar = Cursos.objects.get(id=id)
    
    cursoEditar.nombre = nombre
    cursoEditar.descripcion = descripcion
    cursoEditar.fecha_inicio = fecha_inicio
    cursoEditar.fecha_fin = fecha_fin
    cursoEditar.tecnico = tecnico
    
    cursoEditar.save()
    messages.success(request, 'Curso actualizado correctamente')
    return redirect('/listadoCursos/')

def reporteCursos(request):
    cursos = Cursos.objects.all()
    return render(request, 'reporteCursos.html', {'misCursos': cursos})


#--------------------- PARTE DEL PERFIL -----------------------------
def iniciarSesion(request):

    if request.method == "POST":

        usuario = request.POST["username"]
        clave = request.POST["password"]

        user = authenticate(
            username=usuario,
            password=clave
        )

        if user is not None:

            login(request,user)

            return redirect('/inicio/')

        else:
            messages.error(request,"Usuario o contraseña incorrectos")


    return render(request,"login.html")



def cerrarSesion(request):

    logout(request)

    return redirect('/login/')

#--------------------- PARTE DEL CERTIFICADO -----------------------------
@login_required
def nuevoCertificado(request):

    tecnicos = Tecnico.objects.all()
    cursos = Cursos.objects.all()

    return render(
        request,
        'nuevoCertificado.html',
        {
            'tecnicos': tecnicos,
            'cursos': cursos
        }
    )

@login_required
def guardarCertificado(request):

    tecnico = Tecnico.objects.get(
        id=request.POST["tecnico"]
    )

    curso = Cursos.objects.get(
        id=request.POST["curso"]
    )

    aprobacion = request.POST["aprobacion"]

    Certificado.objects.create(
        tecnico=tecnico,
        curso=curso,
        aprobacion=aprobacion
    )

    messages.success(request,"Certificado registrado correctamente")

    return redirect('/listadoCertificados/')

@login_required
def listadoCertificados(request):

    certificados = Certificado.objects.all()

    return render(
        request,
        'listadoCertificados.html',
        {
            'certificados': certificados
        }
    )

@login_required
def eliminarCertificado(request,id):

    certificado = Certificado.objects.get(id=id)

    certificado.delete()

    messages.success(request,"Certificado eliminado correctamente")

    return redirect('/listadoCertificados/')

@login_required
def editarCertificado(request,id):

    certificado = Certificado.objects.get(id=id)

    tecnicos = Tecnico.objects.all()
    cursos = Cursos.objects.all()

    return render(
        request,
        'editarCertificado.html',
        {
            'certificado': certificado,
            'tecnicos': tecnicos,
            'cursos': cursos
        }
    )

@login_required
def procesarActualizacionCertificado(request):

    certificado = Certificado.objects.get(
        id=request.POST["id"]
    )

    certificado.tecnico = Tecnico.objects.get(
        id=request.POST["tecnico"]
    )

    certificado.curso = Cursos.objects.get(
        id=request.POST["curso"]
    )

    certificado.aprobacion = request.POST["aprobacion"]

    certificado.save()

    messages.success(request,"Certificado actualizado correctamente")

    return redirect('/listadoCertificados/')

@login_required
def reporteCertificados(request):

    certificados = Certificado.objects.all()

    return render(
        request,
        'reporteCertificados.html',
        {
            'certificados': certificados
        }
    )


def reporteCertificado(request, id):

    certificado = Certificado.objects.get(id=id)

    return render(
        request,
        "reporteCertificado.html",
        {
            'certificado': certificado
        }
    )



@login_required
def enviarCertificado(request,id):

    certificado=Certificado.objects.get(id=id)

    archivo=tempfile.NamedTemporaryFile(
        suffix=".pdf",
        delete=False
    )

    archivo.close()

    url=request.build_absolute_uri(
        f"/reporteCertificado/{id}/"
    )

    generar_pdf(url,archivo.name)

    correo=EmailMessage(

        subject="Certificado del Curso",

        body=f"""
Estimado(a) {certificado.tecnico.nombre}:

Adjunto encontrará su certificado correspondiente al curso:

{certificado.curso.nombre}

Saludos cordiales.
""",

        from_email=settings.EMAIL_HOST_USER,

        to=[certificado.tecnico.correo]

    )

    correo.attach_file(archivo.name)

    correo.send()

    os.remove(archivo.name)

    messages.success(
        request,
        "Certificado enviado correctamente."
    )

    return redirect("/listadoCertificados/")

def generar_pdf(url, archivo):

    with sync_playwright() as p:

        navegador = p.chromium.launch(headless=True)

        pagina = navegador.new_page()

        pagina.goto(url)

        pagina.wait_for_timeout(3000)

        pagina.pdf(
            path=archivo,
            format="A4",
            landscape=True,
            print_background=True
        )

        navegador.close()