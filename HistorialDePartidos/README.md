Este programa tiene como objetivo automatizar la extracción de datos de la web (https://www.adamchoi.co.uk/teamgoals/detailed)
Los datos corresponden al historial de partidos de la Bundesliga 22/23

Para comenzar, accedemos a la página web con Selenium mediante el ejecutable "chromedriver". Luego, para seleccionar los campos que necesitamos, analizamos el contenido HTML de la web para asociarla en Python
Una vez extraidos, los cargamos en una lista y terminamos el proceso en Selenium. Pasamos la lista a un dataframe para facilitar el almacenamiento de los datos a un dataframe

En caso de querer los registros de otra liga o agregar más filtros debemos revisar la identificación de código HTML con la qué fue cargada.
 