---
name: aws-billing
description: >-
  Genera reportes de costos mensuales del mes actual o anterior de una cuenta de AWS usando Cost Explorer.
  Ideal para monitorear presupuestos y control de gastos en AWS de forma segura.
---

# AWS Billing Reporter Skill

Este skill permite a los asistentes de IA o al usuario local generar un reporte detallado del consumo mensual de AWS utilizando la API de AWS Cost Explorer. El script principal es capaz de obtener los datos desglosados por servicio de forma segura y sin exponer credenciales.

## Requisitos Previos

1. **Dependencias de Python**:
   Requiere `boto3`. Asegúrate de tenerlo instalado:
   ```bash
   pip install boto3
   ```
2. **Configuración de AWS**:
   El entorno debe tener un perfil configurado en `~/.aws/credentials` con permisos de lectura para Cost Explorer (`ce:GetCostAndUsage`). Por ejemplo, el perfil `rcsevsv`.

## Instrucciones de Uso

Para ejecutar el reporte del mes actual o anterior, ejecuta el script helper provisto:

### 1. Reporte del Mes Actual
```bash
./scripts/get_billing_report.py --profile rcsevsv --month current
```

### 2. Reporte del Mes Anterior
```bash
./scripts/get_billing_report.py --profile rcsevsv --month previous
```

### 3. Reporte de un Mes Específico (YYYY-MM)
```bash
./scripts/get_billing_report.py --profile rcsevsv --month 2026-07
```

## Componentes del Skill

* **Script Helper**: [get_billing_report.py](./scripts/get_billing_report.py) (Ejecuta la consulta hacia AWS Cost Explorer y formatea los resultados en tablas markdown).
* **Seguridad**: No almacena credenciales ni claves de acceso. Utiliza el mecanismo estándar de Boto3 para cargar las credenciales locales o roles IAM de la máquina de manera segura.
