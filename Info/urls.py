#Archivo para gestionar las rutas internas dela aplicacion nomina
from django.urls import path
#Importamos la lógica de negocio de la aplicación
from . import views
#Listadp de rutas de la Aplicación
urlpatterns = [
    # LOGIN PRINCIPAL
    path('', views.iniciarSesion),
    path('login/', views.iniciarSesion),
    path('logout/', views.cerrarSesion),
    # INICIO DESPUES DEL LOGIN
    path('inicio/', views.inicio),

    path('nuevoTecnico/', views.nuevoTecnico),
    path('listadoTecnicos/', views.listadoTecnicos),
    path('guardarTecnico/', views.guardarTecnico),
    path('eliminarTecnico/<id>/', views.eliminarTecnico),
    path('editarTecnico/<id>/', views.editarTecnico),
    path('procesarActualizacionTecnico/', views.procesarActualizacionTecnico),
    path('reporteTecnicos/', views.reporteTecnicos),
    path('nuevoCurso/', views.nuevoCurso),
    path('guardarCurso/', views.guardarCurso),
    path('listadoCursos/', views.listadoCursos),
    path('eliminarCurso/<id>/', views.eliminarCurso),
    path('editarCurso/<id>/', views.editarCurso),
    path('procesarActualizacionCurso/', views.procesarActualizacionCurso),
    path('reporteCursos/', views.reporteCursos),


]