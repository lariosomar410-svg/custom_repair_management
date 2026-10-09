from odoo import models, fields, api  # type: ignore
from odoo.exceptions import UserError  # type: ignore

class RepairOrder(models.Model):
    _name = 'repair.order'
    _description = 'Orden de Reparación de Equipos'

    name = fields.Char(string='Número de Orden', required=True, copy=False, readonly=True, default='Nuevo')
    partner_id = fields.Many2one('res.partner', string='Cliente', required=True)
    equipment_name = fields.Char(string='Equipo / Modelo', required=True)
    serial_number = fields.Char(string='Número de Serie')
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('in_progress', 'En Reparación'),
        ('done', 'Reparado'),
        ('cancel', 'Cancelado'),
    ], string='Estado', default='draft', required=True)

    description = fields.Text(string='Diagnóstico / Fallo Reportado')
    guarantee = fields.Boolean(string='Aplica Garantía', default=False)

    line_ids = fields.One2many('repair.order.line', 'repair_id', string='Piezas y Repuestos')
    total_amount = fields.Float(string='Costo Total', compute='_compute_total_amount', store=True)

    # Campo relacional para conectar con la factura de Odoo
    invoice_id = fields.Many2one('account.move', string='Factura', readonly=True, copy=False)

    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(line.subtotal for line in order.line_ids)

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('repair.order') or 'Nuevo'
        return super(RepairOrder, self).create(vals)

    def action_start_repair(self):
        for record in self:
            record.state = 'in_progress'

    def action_set_to_done(self):
        for record in self:
            record.state = 'done'

    def action_cancel(self):
        for record in self:
            record.state = 'cancel'

    # Método Python para crear la factura en el módulo de Contabilidad/Facturación
    def action_create_invoice(self):
        for order in self:
            if order.invoice_id:
                raise UserError('Ya existe una factura creada para esta orden.')
            if not order.line_ids:
                raise UserError('No puedes generar una factura sin líneas de repuestos o servicios.')

            invoice_lines = []
            for line in order.line_ids:
                invoice_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'price_unit': line.unit_price,
                    'name': f"Reparación {order.name}: {line.product_id.display_name}",
                }))

            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': order.partner_id.id,
                'invoice_origin': order.name,
                'invoice_line_ids': invoice_lines,
            }

            invoice = self.env['account.move'].create(invoice_vals)
            order.invoice_id = invoice.id

            return {
                'name': 'Factura Generada',
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': invoice.id,
                'view_mode': 'form',
                'target': 'current',
            }


class RepairOrderLine(models.Model):
    _name = 'repair.order.line'
    _description = 'Línea de Piezas de Reparación'

    repair_id = fields.Many2one('repair.order', string='Orden de Reparación', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Repuesto / Servicio', required=True)
    quantity = fields.Float(string='Cantidad', default=1.0)
    unit_price = fields.Float(string='Precio Unitario')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.lst_price

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price