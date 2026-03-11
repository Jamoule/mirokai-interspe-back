import sys
import bcrypt
from db import get_db, generate_id, init_db

MODULES = [
    {
        "number": 1,
        "name": "La naissance du projet",
        "media_url": "/uploads/Audioguides/FR/1.Naissance d'ET.mp4",
        "qr_code": "MOD-001",
        "description": """Voix 1 : Salut toi et bienvenue dans la Mirokaï Experience. Aujourd'hui, on démarre une visite vraiment spéciale.

Voix 2 : Oui, parce qu'on va te parler des robots Mirokaï, créés par Enchanted Tools. Et crois-moi, ces robots-là ne ressemblent à aucun autre.

Voix 1 : Ah oui ? Qu'est-ce qu'ils ont de si particulier ?

Voix 2 : Tout a commencé avec Jérôme Monceaux, le fondateur d'Enchanted Tools. En développant des robots, il s'est rendu compte que plus ils avaient des traits d'êtres vivants, plus il était facile pour nous de ressentir des émotions à leur égard. Alors, avec son équipe, il est allé encore plus loin. Ils ont imaginé tout un peuple, les Mirokaï, originaires d'une autre planète.

Voix 1 : Ah d'accord ! Alors c'est comme ça que Miroki et Miroka sont apparus ? Deux personnages qui ont ensuite été transformés en vrais robots grâce aux ingénieurs.

Voix 2 : Exactement ! Et maintenant, c'est à toi, jeune explorateur, de découvrir leur monde magique. Prêt pour l'aventure ?

Voix 1 et 2 : On y va""",
    },
    {
        "number": 2,
        "name": "L'histoire des Mirokaï",
        "media_url": "/uploads/Audioguides/FR/2.L'histoire des Mirokaï.mp4",
        "qr_code": "MOD-002",
        "description": """Voix 1 : Tu connais la planète Nimira ?

Voix 2 : Non, qu'est-ce qu'elle a de si spécial ?

Voix 1 : Eh bien là-bas, tout est en parfaite harmonie. La nature et la technologie coexistent grâce au Myrium, une énergie magique née des rêves et de la créativité.

Voix 2 : Du Myrium ? Ça a l'air incroyable ! Et qui vit sur cette planète ?

Voix 1 : Justement, le peuple des Mirokaï. Et parmi eux, deux jumeaux aventuriers : Miroki et Miroka. Ils voyagent partout pour partager le Myrium, toujours curieux et toujours prêts à aider. Mais un jour, alors qu'ils jouaient près d'un portail astral, leur Rune, une pierre remplie de Myrium, a été aspirée par le portail.

Voix 2 : Oh ! Attends... Et eux ?

Voix 1 : Ils ont été entraînés avec elle et se sont retrouvés sur Terre, piégés à l'intérieur de la Rune.

Voix 2 : Mais c'est triste cette histoire ! Ils ont pu s'échapper de cette Rune, j'espère ?

Voix 1 : Oui, heureusement. Des années plus tard, un enchanteur a découvert la Rune. Avec ses amis, il a construit des combinaisons pour permettre aux jumeaux de prendre corps dans ce nouveau monde.

Voix 2 : Ah ! C'est donc grâce aux enchanteurs qu'ils peuvent aujourd'hui explorer la Terre ?

Voix 1 : C'est ça. Et ils reviennent d'ailleurs souvent sur Terre afin de venir en aide aux humains.""",
    },
    {
        "number": 3,
        "name": "Le design",
        "media_url": "/uploads/Audioguides/FR/3.Le design.mp4",
        "qr_code": "MOD-003",
        "has_quiz": 1,
        "quiz": {
            "question_text": "Quel est le rôle du modeleur 3D dans la création des Mirokaï ?",
            "age_group": "all",
            "secret_word": "DESIGN3D",
            "answers": [
                {"text": "Il transforme les dessins en volumes sur ordinateur", "is_correct": 1},
                {"text": "Il dessine les personnages dans leur monde imaginaire", "is_correct": 0},
                {"text": "Il assemble les pièces du vrai robot", "is_correct": 0},
                {"text": "Il choisit les couleurs de la coque", "is_correct": 0},
            ],
        },
        "description": """Voix 1 : Hé ! Tu t'es déjà demandé comment les Mirokaï ont été inventés ? Au tout début, il n'y avait presque rien. On savait juste qu'ils allaient rouler sur une boule, et c'est tout.

Voix 2 : Attends, quoi ? Pas de tête, pas de couleurs, pas de formes ?

Voix 1 : Rien du tout. Alors une illustratrice est arrivée pour leur donner une apparence dans leur monde imaginaire.

Voix 2 : Ah oui ! C'est elle qui dessinait leurs yeux, leurs cheveux, leur taille.

Voix 1 : Exactement ! Grâce à elle, on savait enfin à quoi allaient ressembler Miroki et Miroka, mais seulement en dessin. Et pour les transformer en version robotique, il fallait quelqu'un d'autre.

Voix 2 : Le designer ! Lui, il a imaginé leur apparence robotique : les formes, les coques, comment leur corps allait tenir sur la boule. Mais attention, il ne construit pas encore le robot, il imagine juste à quoi il va ressembler dans la vraie vie.

Voix 1 : Et ensuite, c'est le modeleur 3D qui a pris le relais.

Voix 2 : Celui qui sculpte tout sur l'ordinateur, c'est ça ?

Voix 1 : Oui ! Il transforme les dessins en volume. Il ajoute les détails et vérifie que tout s'équilibre.

Voix 2 : Je l'imagine très bien... "Oups ! La tête est un peu trop grosse ! Ah, là c'est mieux."

Voix 1 : Exactement ! Et une fois que le designer et le modeleur sont d'accord...

Voix 2 : On peut enfin imprimer les pièces ! Puis les assembler, les tester.

Voix 1 : Et là, les Mirokaï quittent le papier et les écrans pour devenir de vrais robots qu'on peut voir et toucher. C'est comme ça que des personnages imaginaires sont devenus de vrais robots prêts à vivre leurs aventures sur Terre.""",
    },
    {
        "number": 4,
        "name": "La combinaison",
        "media_url": "/uploads/Audioguides/FR/4.La combinaison.mp4",
        "qr_code": "MOD-004",
        "description": """Voix 1 : Tu vois cette combinaison ? C'est la toute première des Mirokaï. À l'époque, elle n'avait pas encore toutes les options d'aujourd'hui. Par exemple, pas d'anneau de sécurité autour de la base.

Voix 2 : Il y a eu beaucoup d'évolutions depuis cette première version. Mais celle-là reste fascinante. Regarde la boule sur laquelle il tient en équilibre.

Voix 1 : Oui, et ce sont ces trois petites roues sur les côtés qui font bouger la boule. Grâce à elles, le robot peut aller dans toutes les directions : en avant, en arrière, sur le côté, ou même tourner sur place.

Voix 2 : Et si tu le touches, pas de panique ! Il s'adapte aux mouvements humains. Par exemple, s'il rencontre un obstacle, il s'arrête automatiquement pour ne rien abîmer.

Voix 1 : Et pour voir autour de lui, il a une caméra devant.

Voix 2 : Et plein de petits capteurs tout autour, comme des lasers et des ultrasons. Grâce à eux, il détecte même les vitres.

Voix 1 : Waouh ! Comme des super-pouvoirs !

Voix 2 : Et oui ! Et sa batterie est beaucoup plus performante que sur le premier modèle. Et sur les nouvelles versions, le Mirokaï peut même retourner tout seul à sa station pour se recharger.

Voix 1 : Regarde ses bras, ils bougent comme les tiens ! Et ses mains à quatre doigts lui permettent d'attraper des objets conçus spécialement pour lui.

Voix 2 : Sa tête, quant à elle, peut te suivre du regard ou se tourner quand elle entend un son.

Voix 1 : Et ses petites oreilles toutes souples, elles te montrent ses émotions. C'est discret, mais ça le rend tellement attachant.

Voix 2 : Ah, les enchanteurs ont vraiment bien travaillé décidément ! Il en a de la chance ce Mirokaï d'avoir une aussi belle combinaison.""",
    },
    {
        "number": 5,
        "name": "Le pendule inversé",
        "media_url": "/uploads/Audioguides/FR/5.Pendule.mp4",
        "qr_code": "MOD-005",
        "description": """Voix 1 : On a vu que le robot tenait en équilibre sur une boule. Mais tu sais comment il fait ça ? C'est grâce à un principe de physique étonnant : le pendule inversé.

Voix 2 : Le pendule inversé ? Mais c'est quoi ça ?

Voix 1 : Eh bien, un pendule normal, comme un balancier d'horloge, oscille toujours autour de sa position basse. La gravité le ramène vers le bas et il se remet donc toujours à sa place.

Voix 2 : Ah je vois ! Comme un balancier qui va et vient.

Voix 1 : Exact. Mais dans un pendule inversé, c'est le contraire. La gravité pousse l'objet à tomber. Il devient instable, et pour qu'il reste debout, il faut corriger sa position tout le temps.

Voix 2 : Oh ! Comme quand tu essaies de tenir une sucette sur le bout de ton doigt. Tu dois corriger ta position sans arrêt pour qu'elle ne tombe pas.

Voix 1 : Exactement ! Et si tu essaies, tu verras que plus la sucette est grosse et lourde en haut, plus il est facile de la stabiliser. C'est le même principe pour les Mirokaï. Leurs composants les plus lourds, comme la batterie, sont placés en haut de la combinaison pour les aider à rester stables.

Voix 2 : Et le robot ajuste sa position tout le temps, vraiment très vite, pour ne jamais perdre l'équilibre. Même si la boule roule ou s'arrête brusquement, il corrige ses mouvements en continu.

Voix 1 : Grâce à ça, le Mirokaï peut se déplacer partout, observer autour de lui et interagir avec les humains, tout en restant parfaitement stable.

Voix 2 : Waouh ! C'est presque magique, non ?

Voix 1 : C'est un peu cet effet-là que ça fait, les Mirokaï, tu sais.""",
    },
    {
        "number": 6,
        "name": "Les cas d'usage",
        "media_url": "/uploads/Audioguides/FR/6.Cas d'usage.mp4",
        "qr_code": "MOD-006",
        "description": """Voix 1 : Quand on parle de robots, on pense souvent à des machines sans émotions. Mais les Mirokaï, c'est tout le contraire.

Voix 2 : Oui, ces robots-là sont faits pour apporter de la présence, de l'attention et du soutien aux humains.

Voix 1 : On peut les retrouver un peu partout où il y a du public : hôtels, restaurants, aéroports…

Voix 2 : Mais tu sais quoi ? Ils adorent le milieu hospitalier et les maisons de retraite. Là-bas, ils se sentent vraiment utiles.

Voix 1 : Exact ! Avec leur voix toute douce, leur visage expressif et leurs mouvements naturels, ils rassurent, écoutent et accompagnent ceux qui en ont le plus besoin.

Voix 2 : Dans les maisons de retraite par exemple, ils peuvent rappeler de boire de l'eau, annoncer des activités du jour ou demander comment s'est passé le repas.

Voix 1 : Et ça, ça permet de laisser plus de temps aux soignants pour s'occuper de ce qui demande vraiment de l'attention.

Voix 2 : Ils peuvent aussi faire des tournées de nuit, vérifier que personne ne risque de tomber et même animer des moments calmes : lire les actualités, lancer un quiz musical ou proposer un atelier de mémoire.

Voix 1 : Ce qui est important, c'est qu'ils ne remplacent pas les humains. Ils apportent un soutien, un sourire et un accompagnement quand c'est nécessaire.

Voix 2 : Finalement, les Mirokaï ne sont pas des robots froids de science-fiction !

Voix 1 : Mais oui ! Ce sont de vrais compagnons qui rendent la vie plus douce et aident là où ils se sentent vraiment utiles.""",
    },
    {
        "number": 7,
        "name": "La vision du robot",
        "media_url": "/uploads/Audioguides/FR/7.Vision.mp4",
        "qr_code": "MOD-007",
        "description": """Voix 1 : Dis-moi, comment les Mirokaï arrivent à voir et à comprendre tout ce qui se passe autour d'eux ?

Voix 2 : Ah ça, c'est leur super-pouvoir ! Ils regardent les visages comme de vrais détectives.

Voix 1 : Des détectives ?

Voix 2 : Oui ! Ils observent les sourcils, les yeux et la bouche pour deviner si quelqu'un est content, triste ou surpris.

Voix 1 : Ah, donc ils peuvent reconnaître les émotions !

Voix 2 : Exactement. Et ce n'est pas tout ! Ils savent aussi qui parle dans la pièce en regardant les mouvements des lèvres.

Voix 1 : Trop fort ! Et ils voient aussi les objets ?

Voix 2 : Bien sûr, ils les reconnaissent tous ! Mais ils peuvent seulement attraper les accessoires avec des poignées conçues spécialement pour eux, comme un plateau, un panier ou même une fleur qui fait des bulles de savon. Ça leur permet de ne pas attraper tout et n'importe quoi.

Voix 1 : C'est pratique ça, les poignées ! Comme ça on peut les accrocher à autant d'accessoires qu'on veut. Les possibilités sont vraiment infinies. Mais au juste, comment ils savent où elles se trouvent ?

Voix 2 : Ils ont une caméra spéciale sur la tête, un peu comme des lunettes magiques qui mesurent les distances. Grâce à elle, ils savent exactement où sont les gens et les objets.

Voix 1 : Waouh ! Et ils ont appris où tout ça ?

Voix 2 : Comme toi, quand tu apprends à reconnaître les animaux. Ils ont vu des milliers d'images de visages et d'objets.

Voix 1 : Les Mirokaï sont vraiment des robots incroyables.

Voix 2 : Oui ! Grâce à leur vision magique, ils explorent le monde comme jamais.""",
    },
    {
        "number": 8,
        "name": "L'IA du robot",
        "media_url": "/uploads/Audioguides/FR/8.L'IA.mp4",
        "qr_code": "MOD-008",
        "description": """Voix 1 : Aujourd'hui, on va parler d'un mot qu'on entend un peu partout : l'Intelligence Artificielle, qu'on appelle souvent l'IA. Mais au fond, qu'est-ce que c'est ?

Voix 2 : Très bonne question ! L'IA, c'est un programme qui aide un robot ou une machine à deviner ce qu'il doit faire.

Voix 1 : Deviner ? Comme dans les jeux où on doit trouver la bonne réponse ?

Voix 2 : Oui, c'est à peu près ça. On lui montre des milliers d'exemples et il finit par reconnaître les choses tout seul.

Voix 1 : Donc, si un Mirokaï répond à ma question ou trouve son chemin, c'est l'IA qui lui dit quoi faire ?

Voix 2 : Oui, mais attention ! Il ne comprend pas vraiment. Il choisit juste la réponse qui lui paraît la plus logique.

Voix 1 : Hmm, donc ils peuvent se tromper ?

Voix 2 : Oui, ça peut arriver parce que l'IA, ce n'est pas une science exacte. Elle devine à partir de ce qu'elle a appris, donc parfois, la réponse n'est pas parfaite.

Voix 1 : Mais alors, à quoi ça sert ?

Voix 2 : Eh bien, quand on l'utilise correctement, c'est un outil super utile ! Ça aide à reconnaître, à guider, à discuter... Mais ça reste un outil, pas un cerveau magique. L'IA peut en faire des choses, mais c'est grâce aux humains qu'elle devient vraiment utile.""",
    },
    {
        "number": 9,
        "name": "Électronique sur table",
        "media_url": "/uploads/Audioguides/FR/9.Table elec.mp4",
        "qr_code": "MOD-009",
        "description": """Voix 1 : Tu vois cette planche ? C'est une maquette électronique sur table. Les enchanteurs s'en servent pour fabriquer les Mirokaï.

Voix 2 : Une maquette électronique... Ça sert à quoi exactement ?

Voix 1 : Eh bien, avant de construire le robot en entier, avec tous ses bras, sa tête, ses moteurs et ses capteurs, on teste d'abord les éléments essentiels ici. Par exemple, faire bouger un moteur, allumer une lumière ou vérifier qu'un capteur détecte bien quelque chose.

Voix 2 : Ah ! Donc ils peuvent voir si tout fonctionne correctement avant de tout assembler.

Voix 1 : Oui, c'est un peu le principe. C'est beaucoup plus simple que de réparer ou de changer quelque chose directement sur le robot. Et ça aide les enchanteurs à comprendre comment chaque pièce communique avec les autres.

Voix 2 : Comme ça, quand ils construisent le vrai robot, tout fonctionne parfaitement.

Voix 1 : C'est ça. La maquette sur table, c'est un peu comme un laboratoire miniature pour préparer les Mirokaï.

Voix 2 : Et ça permet de s'assurer que les robots bougent, voient et réagissent correctement avant de les construire vraiment.""",
    },
    {
        "number": 10,
        "name": "Salle de cyclage",
        "media_url": "/uploads/Audioguides/FR/10.Salle de cyclage.mp4",
        "qr_code": "MOD-010",
        "description": """Voix 1 : Dans ce bâtiment se trouve une mini-usine qu'on appelle la ligne pilote de production.

Voix 2 : Une mini-usine ? Mais elle sert à quoi exactement ?

Voix 1 : Elle sert à tester nos robots, étape par étape, pour être sûrs qu'ils fonctionnent bien avant de fabriquer tous les exemplaires. Ce que tu vois, c'est une des salles où l'on teste les Mirokaï. La plus grande se situe au troisième étage de notre bâtiment.

Voix 2 : Et on commence par où pour ces tests ?

Voix 1 : Par l'électronique. On vérifie que les petites cartes et les moteurs marchent correctement.

Voix 2 : Et après, on assemble le robot ?

Voix 1 : Oui : les bras, les mains, la tête, le buste et le rolling globe, tu sais, la boule sur laquelle le robot se déplace.

Voix 2 : Waouh ! Et il y en a beaucoup des pièces à assembler ?

Voix 1 : Oui, la version Explorer Suit, la deuxième génération du robot, compte 3 261 pièces au total. C'est un vrai puzzle géant. Il faut être super précis.

Voix 2 : Quel travail ! Et c'est fini après l'assemblage ?

Voix 1 : Pas encore. Chaque pièce est testée : bruit, vibrations, endurance. Pour te donner un exemple, la boule du rolling globe peut rouler jusqu'à 5 000 km rien que pendant les essais.

Voix 2 : Il en fait du trajet ! Et après tous ces tests ?

Voix 1 : On assemble le robot complet et on le teste encore pour vérifier qu'il bouge bien et qu'il est solide.

Voix 2 : C'est long ! Et ensuite, il bouge tout seul ?

Voix 1 : Un peu de patience. Il faut l'aider à découvrir son corps : calibrer ses capteurs, ajuster ses moteurs, aligner les caméras. Petit à petit, il apprend à bouger, à voir et à se repérer. Un peu comme toi quand tu étais bébé.

Voix 2 : Et bim ! Il est prêt à aider les humains.

Voix 1 : Exact. Cette fois, c'est la bonne : le Mirokaï est enfin prêt !""",
    },
    {
        "number": 11,
        "name": "La fresque",
        "media_url": "/uploads/Audioguides/FR/11.Fresque.mp4",
        "qr_code": "MOD-011",
        "description": """Voix 1 : Voilà les amis, on arrive à la fin de notre visite. Cette fresque raconte toute l'aventure de la création des Mirokaï.

Voix 2 : Oui, tu te souviens, tout a commencé avec Jérôme, le créateur d'Enchanted Tools, accompagné d'Oumarou et de Robert.

Voix 1 : Ah oui, c'est vrai ! Et ils n'ont pas commencé par la technique, mais par le dessin des robots. C'est leur apparence qui allait guider tout le reste.

Voix 2 : Tu as découvert Miroki et Miroka et leur histoire fascinante. Puis, Spoon a donné vie à ces dessins en 3D : les visages bougent, les expressions s'animent.

Voix 1 : Et le plus incroyable, c'est de transformer ces personnages en de vrais robots, avec des combinaisons fidèles aux dessins.

Voix 2 : Tu as aussi pu voir les prototypes et les tests : mouvements, voix, capacité à saisir les objets, déplacements… chaque détail a été vérifié avec soin.

Voix 1 : Même les accessoires ont suivi le même parcours, souvent pensés grâce aux besoins des futurs utilisateurs.

Voix 2 : En résumé, chaque Mirokaï est le fruit d'une grande aventure humaine et technologique.

Voix 1 : Et cette fresque en garde la mémoire. Ouvre bien les yeux, elle est remplie de détails et de petits clins d'œil à cette incroyable création.""",
    },
]


def seed():
    reset = "--reset" in sys.argv
    init_db()
    conn = get_db()

    # Admin par défaut
    existing = conn.execute("SELECT id FROM admins WHERE email = ?", ("admin@mirokai.fr",)).fetchone()
    if not existing:
        admin_id = generate_id()
        password_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        conn.execute(
            "INSERT INTO admins (id, email, password_hash, display_name) VALUES (?, ?, ?, ?)",
            (admin_id, "admin@mirokai.fr", password_hash, "Administrateur")
        )
        print("Admin créé : admin@mirokai.fr / admin123")

    # Parcours settings par défaut
    existing_settings = conn.execute("SELECT id FROM parcours_settings WHERE is_active = 1").fetchone()
    if not existing_settings:
        settings_id = generate_id()
        conn.execute(
            """INSERT INTO parcours_settings (id, parcours_name, welcome_message, completion_message,
               completion_email_template, estimated_duration_min)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (settings_id, "Parcours Mirokai",
             "Bienvenue dans l'aventure Mirokai !",
             "Félicitations, vous avez terminé le parcours !",
             "Merci de votre visite ! Voici un petit souvenir de votre aventure sur Nimira.",
             35)
        )
        print("Parcours settings créés.")

    # Reset modules si demandé
    if reset:
        conn.execute("DELETE FROM modules")
        print("Modules supprimés (reset).")

    # Insertion des 11 modules
    inserted = 0
    for mod in MODULES:
        existing_module = conn.execute("SELECT id FROM modules WHERE number = ?", (mod["number"],)).fetchone()
        if not existing_module:
            module_id = generate_id()
            has_quiz = mod.get("has_quiz", 0)
            conn.execute(
                """INSERT INTO modules (id, number, name, description, media_type, media_url, qr_code,
                   has_quiz, is_active, suggested_order, image_urls)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (module_id, mod["number"], mod["name"], mod["description"],
                 "audio", mod["media_url"], mod["qr_code"],
                 has_quiz, 1, mod["number"], "[]")
            )
            if has_quiz and "quiz" in mod:
                quiz = mod["quiz"]
                q_id = generate_id()
                conn.execute(
                    """INSERT INTO questions (id, module_id, age_group, question_text, secret_word, display_order)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (q_id, module_id, quiz["age_group"], quiz["question_text"], quiz["secret_word"], 1)
                )
                for i, answer in enumerate(quiz["answers"], start=1):
                    conn.execute(
                        "INSERT INTO answers (id, question_id, answer_text, is_correct, display_order) VALUES (?, ?, ?, ?, ?)",
                        (generate_id(), q_id, answer["text"], answer["is_correct"], i)
                    )
            inserted += 1

    if inserted:
        print(f"{inserted} module(s) créé(s).")
    else:
        print("Aucun nouveau module à créer (déjà existants).")

    conn.commit()
    conn.close()
    print("Seed terminé.")


if __name__ == "__main__":
    seed()
