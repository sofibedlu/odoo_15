{
    "name": "Library Book Checkout",
    "description": "Members can borrow books from the library.",
    "author": "sofi",
    "depends": ["library_member", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/checkout_mass_message_wizard_view.xml",
        "views/library_menu.xml",
        "views/checkout_view.xml",
        "views/checkout_kanban_view.xml",
        "data/library_checkout_stage.xml",
    ],
}