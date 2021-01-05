from odoo import fields, models, api, _
from odoo import fields, models, api, _
import requests
import json
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class Moncash(models.Model):
    _name = "moncash.api"

    name = fields.Many2one('res.users', 'User')
    username = fields.Char("Username")
    password = fields.Char("Password")
    client_id = fields.Char("Client ID")
    client_secret = fields.Char("Client Secret")
    token = fields.Char("Token")
    token_exp = fields.Datetime("Token Expire in")
    refresh_token = fields.Char("Refresh Token")

    def get_auth_token(self):
        url = "https://%s:%s@sandbox.moncashbutton.digicelgroup.com/Api/oauth/token" % (
        self.client_id, self.client_secret)
        headers = {
            'Accept': 'application/json',
        }
        data = {
            'scope': 'read,write',
            'grant_type': 'client_credentials'
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            content = json.loads(response.content.decode('utf-8'))
            self.token = content.get('access_token')
            self.refresh_token = content.get('refresh_token')
            self.token_exp = datetime.now() + timedelta(seconds=content.get('expires_in'))
        else:
            raise UserError(_("Please Check the username or password or client ID or client secret"))

    def refresh_auth_token(self):
        if self.refresh_token:
            url = "https://sandbox-fl.voip-int.com/ns-api/oauth2/token/?grant_type=refresh_token" \
                  "&refresh_token=%s&client_id=%s&client_secret=%s" % (
                      self.refresh_token, self.client_id, self.client_secret)
            response = requests.get(url)
            if response.status_code == 200:
                content = json.loads(response.content.decode('utf-8'))
                self.token = content.get('access_token')
                self.refresh_token = content.get('refresh_token')
                self.token_exp = datetime.now() + timedelta(seconds=content.get('expires_in'))
            else:
                raise UserError(_("Please Check the client ID or client secret"))
        else:
            raise UserError(_("Please click on Get Token button"))
