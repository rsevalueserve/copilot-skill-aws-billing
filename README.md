# AWS Billing Agent Skill

Este directorio contiene un **Agent Skill** diseñado para el asistente Antigravity y otros entornos basados en agentes. Permite reportar y auditar de forma segura y estructurada los costos de servicios de AWS en el mes en curso o anterior.

## Estructura del Skill

```text
aws-billing/
├── SKILL.md                 # Definición del skill para el agente de IA
├── README.md                # Esta guía de documentación
└── scripts/
    └── get_billing_report.py # Script en Python que consulta Cost Explorer API
```

## Configuración y Portabilidad en GitHub

Este repositorio o directorio puede guardarse en tu GitHub y clonarse en cualquier otra máquina en la carpeta `.agents/skills/`.

### Uso en otra máquina

1. **Clona el skill** en la carpeta de configuraciones de agentes de tu proyecto local:
   ```bash
   git clone <tu-repositorio-de-skills> .agents/skills
   ```
2. **Configura tus credenciales de AWS**:
   Define tu perfil en `~/.aws/credentials` o configura las variables de entorno de AWS:
   ```bash
   export AWS_PROFILE=rcsevsv
   ```
3. **Ejecuta el script**:
   ```bash
   python3 .agents/skills/aws-billing/scripts/get_billing_report.py --profile rcsevsv --month current
   ```

## Seguridad

* **Sin Hardcoding de Claves**: El script utiliza `boto3.Session()`, lo que significa que hereda de forma nativa las variables de entorno estándar (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`) o perfiles configurados mediante la CLI de AWS, garantizando que tus credenciales nunca se guarden en el código base o en repositorios de GitHub.
* **Permiso IAM Mínimo**: El perfil o rol IAM que ejecute este script solo requiere el permiso de lectura en Cost Explorer:
  ```json
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "ce:GetCostAndUsage"
              ],
              "Resource": "*"
          }
      ]
  }
  ```
