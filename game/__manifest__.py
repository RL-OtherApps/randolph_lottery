{
    'name': 'Game',
    'version': '1.0',
    'category': 'Private',
    'complexity': 'easy',
    'description': "Game in odoo",
    'depends': ['base', 'website', 'web', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/game_template_view.xml',
        'views/game_one_view.xml',
        'views/game_two_view.xml',
        'views/game_data_view.xml',
        'views/lottery_draw_view.xml',
        'views/pdf_receipt_view.xml',
    ],
    'installable': True,
}
