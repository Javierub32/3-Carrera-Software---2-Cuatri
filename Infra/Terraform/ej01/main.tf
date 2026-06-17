terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

# Llamamos al módulo UNA sola vez, pero iteramos sobre él
module "project" {
  source   = "./modules/project"
  
  # La magia ocurre aquí: le pasamos el mapa completo
  for_each = var.projects

  # each.key es el nombre del proyecto (la clave del mapa: "backend-api", etc.)
  project_name = each.key
  
  # each.value contiene el objeto interno con los atributos
  author       = each.value.author
  environment  = each.value.environment
  
  base_dir     = "${path.module}/output"
}