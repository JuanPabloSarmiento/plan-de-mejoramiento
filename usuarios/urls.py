from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_usuarios, name='lista_usuarios'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
    path('exportar_pdf/', views.exportar_usuarios_pdf, name='exportar_usuarios_pdf'),
    path('enviar_correo/', views.enviar_correo_test, name='enviar_correo_test'),
    path('enviar_pdf_correo/', views.enviar_pdf_por_correo, name='enviar_pdf_por_correo'),


]  
