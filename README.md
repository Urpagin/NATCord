# ForumFlask
A Python Flask forum


# Context
Notre objectif est de permettre au dev de communiquer entre eux.

Une messagerie instantanée avec :

- Des disscussion privés entre deux utilisateurs

- Des salons entre plusieurs utilisateurs

- (optionel) Des serveurs privés (agglomérations de salons)

- Pass premium (avantages : personnalisation de l'interface)

- Ajout d'amis et recommendation

- Login et creation d'account

- (optionel) Partage de fichier et appel vocaux

- Hiérarchie utilisateurs

# Schéma relatif de la base de donnés

1. **Users** (Utilisateurs)
   - `id` (Primary Key)
   - `username`
   - `email`
   - `password`
   - `profile_picture`
   - `status` (en ligne, hors ligne, etc.)
   - `created_at`

2. **Servers** (Serveurs optionel)
   - `id` (Primary Key)
   - `name`
   - `owner_id` (Foreign Key vers `Users.id`)
   - `created_at`

3. **Channels** (Canaux)
   - `id` (Primary Key)
   - `name`
   - `server_id` (Foreign Key vers `Servers.id`)
   - `type` (texte, vocal, etc.)
   - `created_at`

4. **Messages** (Messages)
   - `id` (Primary Key)
   - `channel_id` (Foreign Key vers `Channels.id`)
   - `user_id` (Foreign Key vers `Users.id`)
   - `content`
   - `timestamp`
   - `edited_at`

5. **Roles** (Rôles)
   - `id` (Primary Key)
   - `name`
   - `permissions`
   - `server_id` (Foreign Key vers `Servers.id`)

6. **UserRoles** (Rôles attribués aux utilisateurs)
   - `user_id` (Foreign Key vers `Users.id`)
   - `role_id` (Foreign Key vers `Roles.id`)

7. **Friends** (Amis)
   - `user_id_1` (Foreign Key vers `Users.id`)
   - `user_id_2` (Foreign Key vers `Users.id`)
   - `status` (ami, bloqué, etc.)


### Relations principales
- **Un utilisateur peut appartenir à plusieurs serveurs.**
- **Un serveur a plusieurs canaux.**
- **Un canal peut contenir plusieurs messages.**
- **Un utilisateur peut avoir plusieurs rôles dans un serveur.**
- **Un utilisateur peut être ami avec un autre.**

# Type de pages
Une page de login et une page de about et une page de conversation (envoi de messages). Une page d'admin (optionnel)
