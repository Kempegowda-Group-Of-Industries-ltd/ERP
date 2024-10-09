# app/config.py

# General App Settings
APP_TITLE = "Advanced Reporting & Dashboards"
UPLOAD_FOLDER = "uploads"  # Folder where uploaded files will be saved

# Integration Settings
ERP_INTEGRATION_ENABLED = True  # Set to True if ERP integration is required
ECOMMERCE_INTEGRATION_ENABLED = True  # Set to True if eCommerce integration is required

# ERP and eCommerce Integration Credentials (for external API)
ERP_API_URL = "https://api.erp-system.com"  # Placeholder URL for ERP integration
ECOMMERCE_API_URL = "https://api.ecommerce-platform.com"  # Placeholder URL for eCommerce integration

# Credentials file (JSON) path
CREDENTIALS_FILE_PATH = "integration/credentials.json"

# Plotly Settings
PLOTLY_THEME = "plotly_dark"  # Set the Plotly theme for charts (e.g., "plotly_dark", "ggplot2", etc.)

# Logging Settings
ENABLE_LOGGING = True
LOG_FILE_PATH = "logs/app_log.log"
LOG_LEVEL = "INFO"  # Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Other UI Settings
SIDEBAR_STATE = "expanded"  # Sidebar initial state: "expanded" or "collapsed"
