odoo.define('randolph_pos.ActionButton', function (require) {
"use strict";

// require pos screens
var pos_screens = require('point_of_sale.screens');

// create a new button by extending the base ActionButtonWidget
var DashboardButton = pos_screens.ActionButtonWidget.extend({
    template: 'DashBoardButton',
    button_click: function(){
        alert("Dashboard button clicked");
    },
});

// define the dashboard button
pos_screens.define_action_button({
    'name': 'Dashboard',
    'widget': DashboardButton,
    'condition': function(){return this.pos;},
});

});