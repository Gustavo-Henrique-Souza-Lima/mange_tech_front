variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
  default     = "250ae9c3-6c33-4030-b72a-ed22fce22920"
}

variable "location" {
  description = "Azure Region"
  type        = string
  default     = "West Europe"
}

variable "resource_group_name" {
  description = "Resource Group Name"
  type        = string
  default     = "andre_savedra_test_rg"
}