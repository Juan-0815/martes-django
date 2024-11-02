from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Importamos el módulo de mensajes
from store.models import Customer


@login_required(login_url='login')
def HomePage(request):
    return render(request, 'store/store.html')  # Asegúrate de que 'store.html' esté en la carpeta correcta


from django.contrib import messages  # Importamos messages para mostrar errores


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Verifica que todos los campos están llenos
        if not uname or not email or not pass1 or not pass2:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'signup.html')

        # Verifica que las contraseñas coincidan
        if pass1 != pass2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'signup.html')

        # Si pasa todas las validaciones, crea el usuario
        try:
            my_user = User.objects.create_user(username=uname, email=email, password=pass1)
            my_user.save()

            # Crear el Customer asociado al nuevo User
            customer = Customer(user=my_user, name=uname, email=email)
            customer.save()
            messages.success(request, "Usuario creado exitosamente. Inicia sesión.")
            return redirect('login')
        except ValueError as e:
            messages.error(request, f"Error: {str(e)}")
            return render(request, 'signup.html')

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('store')  # Cambiado a redirigir a la URL de la vista 'store'
        else:
            messages.error(request, "Credenciales incorrectas. Inténtalo de nuevo.")

    return render(request, 'login.html')



def LogoutPage(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login')
