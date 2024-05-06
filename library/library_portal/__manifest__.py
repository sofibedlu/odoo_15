{
    "name": "Library Portal",
    "description": "Portal for library members",
    "author": "sofi",
    "license": "AGPL-3",
    "depends": [
        "library_checkout", "portal"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/library_security.xml",
        "views/main_templates.xml",
        "views/portal_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "library_portal/static/src/css/library.css",
        ],
    },
}