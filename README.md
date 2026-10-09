# Custom Repair Management (`custom_repair_management`) - Odoo 17

Módulo personalizado desarrollado en **Odoo 17** para la gestión de órdenes de reparación de equipos informáticos/electrónicos, control de repuestos, generación de reportes PDF y facturación automatizada.

---

## 🛠️ Tecnologías y Herramientas

* **ERP Framework:** Odoo 17.0 (Community / Enterprise)
* **Lenguaje Backend:** Python 3.10+ (ORM de Odoo)
* **Frontend UI:** XML Views, Widgets Dinámicos, QWeb PDF Engine
* **Base de Datos:** PostgreSQL
* **Entorno de Desarrollo:** Docker / Docker Compose / VS Code

---

## ⚙️ Características Principales

1. **Secuencias y Folios Automáticos (`ir.sequence`):** Asignación dinámica de folios al crear órdenes (`REP/YYYY/XXXXX`).
2. **Modelo Relacional Máster-Detalle (`One2many` / `Many2one`):** Gestión de repuestos y servicios vinculados a cada orden de reparación.
3. **Lógica de Negocio y Campos Calculados:** Cálculo dinámico de subtotales y totales mediante `@api.depends` y asignación automática de precios con `@api.onchange`.
4. **Flujo de Trabajo y Estados (Workflow):** Máquina de estados (`Borrador` ➔ `En Reparación` ➔ `Reparado` / `Cancelado`) gestionada con botones y widget `statusbar`.
5. **Reportes PDF en QWeb:** Plantilla de impresión descargable para entregas al cliente con membrete oficial.
6. **Integración con Módulo de Facturación (`account.move`):** Método en Python para generar facturas borrador automáticas desde la orden de reparación.

---

## 📂 Estructura del Módulo

```text
custom_repair_management/
├── __manifest__.py          # Declaración e indexación de archivos
├── __init__.py              # Inicialización de paquetes Python
├── models/
│   ├── __init__.py
│   └── repair_order.py      # Modelos 'repair.order' y 'repair.order.line'
├── security/
│   └── ir.model.access.csv  # Reglas de acceso y permisos de seguridad
├── data/
│   └── repair_sequence_data.xml # Configuración de secuencia de folios
├── views/
│   └── repair_order_views.xml   # Vistas Tree, Form, Menús y Acciones
└── report/
    └── repair_order_report.xml  # Reporte PDF QWeb