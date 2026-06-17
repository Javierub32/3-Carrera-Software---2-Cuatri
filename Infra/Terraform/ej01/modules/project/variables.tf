variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}

variable "author" {
  description = "Autor o autora del proyecto"
  type        = string
}

variable "environment" {
  description = "Entorno de despliegue"
  type        = string
}

variable "base_dir" {
  description = "Directorio base donde crear el proyecto"
  type        = string
}