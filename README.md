# Proyecto Software I

Este proyecto está alojado en GitHub y utiliza ramas separadas para cada miembro del equipo. Sigue los siguientes pasos para clonar el repositorio y activar la rama correspondiente de cada usuario.

## 1. Clonar el repositorio

1. Abre tu terminal.
2. Navega a la carpeta donde deseas clonar el repositorio:
   ```bash
   cd /ruta/donde/deseas/guardar/el/repositorio
   ```

3. Clona el repositorio utilizando el siguiente comando:
   ```bash
   git clone https://github.com/BGHcar/ProyectoSoftwareI.git
   ```

4. Una vez clonado el repositorio, navega al directorio del proyecto:
   ```bash
   cd ProyectoSoftwareI
   ```

## 2. Activar la rama correspondiente de cada usuario

Después de clonar el repositorio, sigue estos pasos para activar las ramas de cada usuario:

### Usuario Camilo

1. Cambia a la rama `camilo`:
   ```bash
   git checkout camilo
   ```

2. Verifica que estás en la rama correcta:
   ```bash
   git branch
   ```

### Usuario Juan

1. Cambia a la rama `juan`:
   ```bash
   git checkout juan
   ```

2. Verifica que estás en la rama correcta:
   ```bash
   git branch
   ```

### Usuario Nicolás

1. Cambia a la rama `nicolas`:
   ```bash
   git checkout nicolas
   ```

2. Verifica que estás en la rama correcta:
   ```bash
   git branch
   ```

## Notas adicionales

- **Restricción de la rama `main`**: La rama `main` está bloqueada para evitar que los cambios no autorizados sean subidos. Para realizar cambios en `main`, asegúrate de revisar las solicitudes de pull generadas en GitHub.
- **Enviar cambios**: Para enviar cambios a tu rama correspondiente y luego a `main`, asegúrate de seguir las instrucciones adecuadas para crear solicitudes de pull en GitHub.
- **Sincronización**: Recuerda que para sincronizar las ramas locales con las remotas, debes utilizar los comandos `git pull` en cada rama antes de hacer cualquier cambio.

---