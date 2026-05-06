# pyrefly: ignore [missing-import]
from odoo import models, fields, api

class TechRating(models.Model):
    _name = 'tech.rating'
    _description = 'Valoración de Equipo Tecnológico'
    _order = 'rating_date desc, id desc'

    equipment_id = fields.Many2one(
        'tech.equipment',
        string='Equipo',
        required=True,
        ondelete='cascade'
    )
    
    evaluated_by_id = fields.Many2one(
        'res.users',
        string='Evaluado por',
        required=True,
        default=lambda self: self.env.user
    )
    
    rating_date = fields.Date(
        string='Fecha de Valoración',
        required=True,
        default=fields.Date.context_today
    )
    
    rating = fields.Selection([
        ('malo', 'Malo'),
        ('regular', 'Regular'),
        ('bueno', 'Bueno'),
        ('excelente', 'Excelente')
    ], string='Valoración', required=True)
    
    is_recommended = fields.Boolean(
        string='¿Es Recomendado?',
        compute='_compute_is_recommended',
        store=True
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True
    )
    
    name = fields.Char(
        string='Referencia',
        compute='_compute_name',
        store=True
    )

    @api.depends('rating')
    def _compute_is_recommended(self):
        for record in self:
            record.is_recommended = (record.rating == 'excelente')

    @api.depends('equipment_id', 'rating_date')
    def _compute_name(self):
        for record in self:
            if record.equipment_id and record.rating_date:
                record.name = f"Valoración - {record.equipment_id.name} - {record.rating_date}"
            else:
                record.name = "Nueva Valoración"
