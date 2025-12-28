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

resource "azurerm_network_security_rule" "ssh_open" {
  name                        = "allow-ssh"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefix       = "0.0.0.0/0"
  destination_address_prefix  = "*"
  resource_group_name         = "rg"
  network_security_group_name = "nsg"
}

resource "azurerm_mssql_server" "sql" {
  name                         = "examplesqlserver"
  resource_group_name          = "rg"
  location                     = "eastus"
  version                      = "12.0"
  administrator_login          = "adminuser"
  administrator_login_password = "Password1234!"
  # public_network_access_enabled intentionally missing
}
