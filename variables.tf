variable "provider_profile" {
    type = string
    default = "default"
    description = "AWS Profile to use in provider configuration"
}

variable "deployed_by" {
    type = string
    description = "Name of the person who deployed the infrastructure"
}