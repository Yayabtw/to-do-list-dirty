# to-do-list app
To-Do-List application built with django to Create, Update and Delete tasks.
<br>
<br>
![todolist](https://user-images.githubusercontent.com/65074901/125083144-a5e03900-e0e5-11eb-9092-da716a30a5f3.JPG)

## Gestion des commits

Nous utilisons la convention **Conventional Commits** pour nommer nos commits.

Format général :

`type(scope): message clair au présent`

Exemples de types utilisés :

- `feat` : ajout d’une nouvelle fonctionnalité  
- `fix` : correction de bug  
- `docs` : modification de la documentation  
- `refactor` : refonte du code sans changement de comportement  
- `test` : ajout ou modification de tests  
- `chore` : tâches diverses (config, dépendances, etc.)

Exemples :

- `feat(auth): ajouter la connexion par Google`
- `fix(api): corriger l’erreur 500 sur /users`
- `docs: mettre à jour le README`

Cette convention permet d’avoir un historique de commits lisible, de faciliter la génération de changelog et d’automatiser les versions.

---

## Gestion des versions

Nous utilisons la version sémantique (**Semantic Versioning / SemVer**), au format :

`MAJEURE.MINEURE.CORRECTIVE` (ex : `1.4.2`)

- **MAJEURE** : changement incompatible avec les versions précédentes  
  - Ex : `1.0.0` → `2.0.0`
- **MINEURE** : ajout de fonctionnalités rétro-compatibles  
  - Ex : `1.2.0` → `1.3.0`
- **CORRECTIVE** : corrections de bugs rétro-compatibles  
  - Ex : `1.2.3` → `1.2.4`

Les numéros de version sont mis à jour en fonction des changements introduits dans le projet, afin de refléter clairement l’impact pour les utilisateurs et les développeurs.