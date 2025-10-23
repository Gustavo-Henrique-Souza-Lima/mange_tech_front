terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.48.0"
    }
  }
}

provider "azurerm" {
  resource_provider_registrations = "none"
  subscription_id = "250ae9c3-6c33-4030-b72a-ed22fce22920"
  features {}
}

# Resource Group - Grupo de recursos para organizar tudo
resource "azurerm_resource_group" "mange_tech_rg" {
  name     = "mange-tech-rg"
  location = "West Europe"  
}

# Service Plan - Plano de hospedagem
resource "azurerm_service_plan" "mange_tech_sp" {
  name                = "mange-tech-service-plan"
  resource_group_name = azurerm_resource_group.mange_tech_rg.name
  location            = azurerm_resource_group.mange_tech_rg.location
  sku_name            = "S1"     
  os_type             = "Windows"
}

# Windows Web App - Aplicação Web
resource "azurerm_windows_web_app" "mange_tech_app" {
  name                = "mange-tech-webapp"
  resource_group_name = azurerm_resource_group.mange_tech_rg.name
  location            = azurerm_resource_group.mange_tech_rg.location
  service_plan_id     = azurerm_service_plan.mange_tech_sp.id

  site_config {
    always_on = false
    
    # Configuração para Node.js (seu frontend React)
    application_stack {
      current_stack = "node"
      node_version  = "~18"
    }

    # CORS para permitir requisições do frontend
    cors {
      allowed_origins = ["*"]
    }
  }

  # Configurações da aplicação
  app_settings = {
    "WEBSITE_NODE_DEFAULT_VERSION" = "~18"
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
  }

  # Logs da aplicação
  logs {
    detailed_error_messages = true
    failed_request_tracing  = true

    application_logs {
      file_system_level = "Information"
    }

    http_logs {
      file_system {
        retention_in_days = 7
        retention_in_mb   = 35
      }
    }
  }
}

# Output - Mostra a URL da aplicação após o deploy
output "webapp_url" {
  description = "URL da aplicação Mange Tech"
  value       = "https://${azurerm_windows_web_app.mange_tech_app.default_hostname}"
}

output "webapp_name" {
  description = "Nome da Web App"
  value       = azurerm_windows_web_app.mange_tech_app.name
}

output "resource_group_name" {
  description = "Nome do Resource Group"
  value       = azurerm_resource_group.mange_tech_rg.name
}