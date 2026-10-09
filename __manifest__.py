{
    'name': 'Gestión de Reparaciones y Garantías',
    'version': '1.0',
    'summary': 'Módulo para gestionar órdenes de reparación de equipos',
    'category': 'Services',
    'author': 'Tu Nombre',
    'depends': ['base', 'product', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/repair_sequence_data.xml',
        'views/repair_order_views.xml',
        'report/repair_order_report.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}