import json
import pandas as pd

ruta_base = ""

with open(ruta_base + 'estudiantes.json', 'r', encoding='utf-8') as archivo:
    estudiantes = json.load(archivo)

with open(ruta_base + 'notas.json', 'r', encoding='utf-8') as archivo:
    notas = json.load(archivo)

with open(ruta_base + "materias.json", "r", encoding="utf-8") as file:
    materias = json.load(file)  # Se carga como una lista

with open(ruta_base + 'barrios.json', 'r', encoding='utf-8') as archivo:
    barrios = json.load(archivo)


# Verifica que se cargaron los datos
print("Datos cargados correctamente.")

# Convertimos a DataFrame
df_estudiantes = pd.DataFrame(estudiantes)
df_notas = pd.DataFrame(notas)
df_materias = pd.DataFrame(materias)
df_barrios = pd.DataFrame(barrios)

"""1. ¿Cuál es el promedio de edad de los estudiantes?"""

promedio_edad = df_estudiantes['edad'].mean()#calculamos el promedio
print(f"El promedio de edad de los estudiantes es: {promedio_edad:.2f} años")

"""2. ¿Cuántos estudiantes viven en el barrio "San Benito"?"""

estudiantes_san_benito=df_barrios[df_barrios['barrio']=='San Benito'].shape[0]
print(f"La cantidad de estudiantes que viven en el barrio San Benito son: {estudiantes_san_benito} ")

"""3. ¿Cuántos barrios están registrados?"""

barrios_registrados=df_barrios['barrio'].nunique()
print(f"Hay {barrios_registrados} barrios registrados")

"""4. ¿Cuántos estudiantes aprobaron la materia "Base de Datos"?"""

aprobados_base_datos = df_notas[(df_notas['nombre_materia'] == 'Base de Datos')
& (df_notas['nota_final'] >= 3)].shape[0]
print(f"Aprobaron Base de Datos {aprobados_base_datos} estudiantes ")

"""5. ¿Cuál es el promedio para la materia "Herramientas III"?"""

notas_herramientas3 = df_notas[df_notas['nombre_materia'] == 'Herramientas III']
promedio_herramientas3 =notas_herramientas3['nota_final'].mean()
print(f"El promedio para Herramientas III es de {promedio_herramientas3}")

"""6. ¿Cuál es la nota mínima de la materia "Ética y Valores"?"""

notas_etica = df_notas[df_notas['nombre_materia'] == 'Ética y Valores']
nota_minima_etica =notas_etica['nota_final'].min()

print(f"La nota mas bajita en Ética y Valores es {nota_minima_etica}")

"""7. ¿Cuántos estudiantes que vivan en el barrio "Guayaquil" han obtenido un promedio general por encima de 3.8?"""

# Filtrar estudiantes que viven en "Guayaquil"
estudiantes_guayaquil = df_barrios[df_barrios['barrio'] == 'Guayaquil']

# Calcular el promedio de notas por estudiante
promedios_estudiantes = df_notas.groupby('identificacion')['nota_final'].mean().reset_index()

# Unir los datos de estudiantes con sus promedios
estudiantes_con_promedio = estudiantes_guayaquil.merge(promedios_estudiantes, on='identificacion')

# Filtrar estudiantes con promedio > 3.8
aprobados = estudiantes_con_promedio[estudiantes_con_promedio['nota_final'] > 3.8]

# Contar cuántos estudiantes cumplen la condición
cantidad_aprobados = aprobados.shape[0]

print(f"Cantidad de estudiantes en Guayaquil con promedio mayor de 3.8: {cantidad_aprobados}")

"""8. ¿Cuál es la materia con mayor cantidad de estudiantes que han reprobado?"""

# Definir la nota mínima para aprobar
nota_minima_aprobatoria = 3
# Filtrar las notas reprobadas
reprobados = df_notas[df_notas['nota_final'] < 3]
# Contar cuántos estudiantes reprobaron por materia
materia_mas_reprobados = (
    reprobados.groupby('nombre_materia')['identificacion']
    .nunique()
    .idxmax()
)
# Mostrar el resultado
print(f"La materia con más estudiantes reprobados es: {materia_mas_reprobados}")

"""9. ¿Cuál o cuáles materias no han sido matriculadas por los estudiantes?"""

df_materias = pd.DataFrame({'nombre_materia': materias})

# Obtener las materias con al menos un estudiante matriculado en df_notas
materias_con_estudiantes = set(df_notas['nombre_materia'].unique())

# Encontrar las materias que NO han sido matriculadas
materias_no_matriculadas = set(df_materias['nombre_materia']) - materias_con_estudiantes

# Mostrar los resultados
print(f"Cantidad de materias no matriculadas: {len(materias_no_matriculadas)}")
print("Materias no matriculadas:", materias_no_matriculadas)