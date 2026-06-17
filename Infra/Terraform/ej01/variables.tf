variable "projects" {
  description = "Mapa de proyectos a generar"
  
  # Definimos que es un mapa donde las claves son strings (nombres de proyecto)
  # y los valores son objetos con autor y entorno.
  type = map(object({
    author      = string
    environment = string
  }))

  # Estos son los datos reales de los 3 proyectos
  default = {
    "backend-api" = {
      author      = "Javier"
      environment = "dev"
    }
    "frontend-app" = {
      author      = "Javier"
      environment = "dev"
    }
    "data-pipeline" = {   # <-- ¡Tercer proyecto añadido aquí!
      author      = "Laura"
      environment = "prod"
    }
  }
}