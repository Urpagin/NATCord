my_discord_clone/
│
├── chat_app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── forms.py         # Optionnel, si tu utilises Flask-WTF pour les formulaires
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── index.html       # Page principale de chat
│   └── channel.html     # Page pour une channel spécifique
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── chat.js      # pour gérer la partie Socket côté client
│   └── images/
│
├── requirements.txt
├── config.py            # Configuration de Flask, DB, etc.
├── run.py               # Point d'entrée pour démarrer l'app
└── README.md

