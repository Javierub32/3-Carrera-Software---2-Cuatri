output "rutas_generadas" {
  description = "Rutas de todos los proyectos generados"
  
  # Iteramos sobre el resultado del módulo para mostrar: "Nombre Proyecto" = "Ruta"
  value = {
    for name, data in module.project : name => data.project_path
  }
}