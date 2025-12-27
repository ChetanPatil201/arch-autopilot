resource "azurerm_storage_account" "sa" {
  name                     = "examplestorageacct"
  resource_group_name      = "rg"
  location                 = "eastus"
  account_tier             = "Standard"
  account_replication_type = "LRS"
  # enable_https_traffic_only intentionally missing
}

resource "azurerm_key_vault" "kv" {
  name                = "examplekv"
  location            = "eastus"
  resource_group_name = "rg"
  tenant_id           = "00000000-0000-0000-0000-000000000000"
  sku_name            = "standard"
  # purge_protection_enabled intentionally missing
}
