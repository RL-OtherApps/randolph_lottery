from odoo import api, models, fields, _


class Withdraw(models.TransientModel):
    _name = 'process.request'

    partner = fields.Many2one('res.partner', 'Customer')
    amount = fields.Float('Amount')
    transaction_id = fields.Char('Transaction ID')

    @api.model
    def default_get(self, fields):
        res = super(Withdraw, self).default_get(fields)
        active_id = self.env['withdraw.request'].browse(self._context.get('active_id'))
        if active_id:
            res.update({"partner": active_id.partner, "amount": active_id.amount})
            return res

    def make_payment(self):
        active_id = self.env['withdraw.request'].browse(self._context.get('active_id'))
        active_id.status = 'pass'
        active_id.partner.current_wallet_amount = active_id.partner.current_wallet_amount - self.amount
        msg_vals_manager = {}
        if active_id.partner.name and active_id.partner.email:
            msg_vals_manager.update({
                'body_html': """
                        <p>Dear """ + active_id.partner.name + """</p>
                        <p>Your withdrawal request has been passed.If you haven't received your money 
                        dont hesitate to contact us. Thank You</p>
                        <br/>
                        <b>Ydnar POS Lottery</b><br/>
                        <b>Accounting Department</b><br/>
                          """
            })
            msg_vals_manager.update({
                'subject': active_id.partner.name + '- Withdrawal Request',
                'email_to': active_id.partner.email,
            })
            msg_id_managaer = self.env['mail.mail'].create(msg_vals_manager)
            msg_id_managaer.send()
