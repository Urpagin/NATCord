# How to run `backend` (for now)


1. `cd` into backend

2. `source venv/bin/activate`

3. `python app.py`

4. Go to http://127.0.0.1:5000



# Contexte

Nous aimerions créer une messagerie instantanée avec les fonctionnalités suivantes :


- Login et creation d'account

- Ajout d'amis

- Des salons de disscussions avec n utilisateurs (n >= 2)

- Rôles utilisateurs (e.g. admin d'un groupe)


- (optionel) Des serveurs privés (agglomérations de salons)

- (optionel) Pass premium (avantages : personnalisation de l'interface)

- (optionel) Partage de fichiers et appel vocaux

# Type de pages

- Une page de creation d'un compte (sign up)
- Une page de connection (login)
- Une page d'acceuil avec 
   - Un bouton pour accéder à la page pour ajouter des amis
   - Des boutons pour accéder aux conversations
   - Une zone de notification (demande d'ami d'une autre personne)
- Une page d'ajout d'amis
- Une page de conversation pour envoyer et reçevoir des messages

# Schéma relatif de la base de donnés

PK = Primary Key
FK = Foreign Key

- **USER**  
  - id_user (PK)  
  - email  
  - username  
  - password_hash  
  - is_premium (boolean)

- **FRIENDSHIP**  
  - user1_id (FK → USER.id_user)  
  - user2_id (FK → USER.id_user)  
  - status (e.g., pending, accepted)

- **SERVER** (optional)  
  - id_server (PK)  
  - server_name  
  - owner_id (FK → USER.id_user)

- **CHANNEL** (optional, associated with a SERVER)  
  - id_channel (PK)  
  - id_server (FK → SERVER.id_server)  
  - channel_name

- **CONVERSATION** (represents private chats or group channels)  
  - id_conversation (PK)  
  - type (e.g., private, group)  
  - (optional) id_channel (FK → CHANNEL.id_channel)

- **CONVERSATION_PARTICIPANT** (links users to conversations)  
  - id_conversation (FK → CONVERSATION.id_conversation)  
  - id_user (FK → USER.id_user)  
  - role (e.g., admin, member)

- **MESSAGE**  
  - id_message (PK)  
  - id_conversation (FK → CONVERSATION.id_conversation)  
  - id_user (FK → USER.id_user, author)  
  - content  
  - timestamp

- **FILE** (optional, for file sharing)  
  - id_file (PK)  
  - id_message (FK → MESSAGE.id_message)  
  - file_path (files would be stored as files, not in the DB)

