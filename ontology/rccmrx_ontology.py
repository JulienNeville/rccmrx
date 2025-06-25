from owlready2 import *

onto = get_ontology("http://www.isiatech.com/ontologies/rccmrx.owl")

with onto:

# region - Entités
    class Code(Thing):
        pass
    Code.label = "RCC-MRx"
    class Subpart(Thing):
        pass
    Subpart.label = "Sous-partie"
    class Context(Thing):
        pass
    Context.label = "Contexte"
    class Rule(Thing):
        pass
    Rule.label = "Règle"

    class Stakeholder(Thing):
        pass
    Stakeholder.label = "Partie prenante"

    class Document(Thing):
        pass
    Document.label = "Document"

    class Workpackage(Thing):
        pass
    Workpackage.label = "Activité"

    class Lifecycle(Thing):
        pass
    Lifecycle.label = "Phase du cycle de vie"

    class Hardware(Thing):
        pass
    Hardware.label = "Matériel"
    class Material(Thing):
        pass
    Material.label = "Matériau"

    AllDisjoint([Code,Subpart,Context,Rule,Stakeholder,Document,Workpackage,Lifecycle,Hardware, Material])

    class Equipment(Hardware):
        pass
    Equipment.label = "Equipement"
    class Support(Hardware):
        pass
    Support.label = "Support"
    class Component(Hardware):
        pass
    Component.label = "Composant"
    AllDisjoint([Equipment, Support, Component])

# endregion
# region - Méthodes
# region - Méthodes des classes génériques
    class subpartOf(ObjectProperty, FunctionalProperty):
        domain = [Subpart]
        range = [Code | Subpart]
    subpartOf.label = "est une sous-partie de"
    class subpart_reference(ObjectProperty, FunctionalProperty):
        domain = [Thing]
        range = [Subpart]
    subpart_reference.label = "texte inclus dans la sous-partie"
    class includes_figure(DataProperty):
        domain = [Rule | Context]
        range = [str]
    includes_figure.label = "inclut la figure"
    class includes_table(DataProperty):
        domain = [Rule | Context]
        range = [str]
    includes_figure.label = "inclut le tableau"
    class includes_context(ObjectProperty):
        domain = [Code]
        range = [Context]
    includes_context.label = "contient le contexte"
    class includes_rule(ObjectProperty):
        domain = [Code]
        range = [Rule]
    includes_rule.label = "contient la règle"

    class states(DataProperty, FunctionalProperty):
        domain = [Context | Rule]
        range = [str]
    states.label = "stipule"
    class relates_to_object(ObjectProperty):
        domain = [Context | Rule]
        range = [Hardware | Material | Stakeholder]
    relates_to_object.label = "porte sur l'objet"
#    relates_to_object.class_property_type = "some" # ne crée pas d'erreur si la condition n'est pas vérifiée!?

    class relates_to_workpackage(ObjectProperty):
        domain = [Context | Rule | Document]
        range = [Workpackage]
    relates_to_workpackage.label = "porte sur l'activité"
#    relates_to_workpackage.class_property_type = "some"
   
    class relates_to_lifecycle(ObjectProperty):
        domain = [Context | Rule]
        range = [Lifecycle]
    relates_to_lifecycle.label = "porte sur la phase de cycle de vie"

    class relates_to_document(ObjectProperty):
        domain = [Context | Rule]
        range = [Document]
    relates_to_document.label = "porte sur le document"

    class relates_to_hardware(ObjectProperty):
        domain = [Document]
        range = [Hardware]
    relates_to_hardware.label = "porte sur le matériel"
# endregion
# region - Méthodes des classes Hardware
    class made_of_material(ObjectProperty):
        domain = [Hardware]
        range = [Material]
    made_of_material.label = "est fabriqué en matériau"
   
    class supportOf(ObjectProperty, TransitiveProperty):
        domain = [Support]
        range = [Hardware]
    supportOf.label = "est un support de"

    class componentOf(ObjectProperty,TransitiveProperty):
        domain = [Component]
        range = [Hardware]
    componentOf.label = "est un composant de"
    
    class quantity(DataProperty, FunctionalProperty):
        domain = [Component]
        range = [int]
    quantity.label = "quantité"

    class equipment_type_list(Datatype):
        equivalent_to = [ OneOf(["Matériel du réacteur et de ses auxiliaires", "Mécanisme de contrôle ou de manutention", "Dispositif d'irradiation"]) ]
    equipment_type_list.label = "Liste des types d'équipement"
    class equipment_type(DataProperty, FunctionalProperty):
        domain = [Equipment]
        range = [equipment_type_list]
    equipment_type.label = "type d'équipement"

    class rccmrx_level_list(Datatype):
        equivalent_to = [ OneOf(["N1Rx", "N2Rx", "N3Rx", "NC"]) ]
    rccmrx_level_list.label = "Liste des niveaux RCC-MRx"
    class rccmrx_level(DataProperty, FunctionalProperty):
        domain = [Hardware]
        range = [rccmrx_level_list]
    rccmrx_level.label = "niveau RCC-MRx"

    class component_type_list(Datatype):
        equivalent_to = [ OneOf(["coque-réservoir-récipient-cuve", "pompe", "robinet-vanne", "tuyauterie", "soufflet", "structure caissonnée", "échangeur", "boulonnerie", "soudure"]) ]
    component_type_list.label = "Liste des types de composants"
    class component_type(DataProperty, FunctionalProperty):
        domain = [Component]
        range = [component_type_list]
    component_type.label = "type de composant"

    class is_standard(DataProperty, FunctionalProperty):
        domain = [Component | Support | Equipment]
        range = [bool]
    is_standard.label = "est un matériel catalogue (Y/N)"
    is_standard.comment = "Seuls les supports, les dispositifs d'irradiation ou les matériels de réacteurs de niveau N3Rx ou NC peuvent être des matériels catalogue."

    class esp_espn(DataProperty, FunctionalProperty):
        domain = [Equipment | Component]
        range = [bool]
    esp_espn.label = "est soumis à la réglementation ESP/ESPN (Y/N)"

    class esp_category_list(Datatype):
        equivalent_to = [ OneOf(["I", "II", "III", "IV", "Non-ESP"]) ]
    esp_category_list.label = "Liste des catégories ESP"
    class esp_category(DataProperty, FunctionalProperty):
        domain = [Equipment | Component]
        range = [esp_category_list]
    esp_category.label = "catégorie de l'équipement ou du composant soumis à la réglementation ESP"

    class espn_level_list(Datatype):
        equivalent_to = [ OneOf(["N1", "N2", "N3", "NC"]) ]
    espn_level_list.label = "Liste des niveaux ESPN"
    class espn_level(DataProperty, FunctionalProperty):
        domain = [Equipment | Component]
        range = [espn_level_list]
    espn_level.label = "niveau de l'équipement ou du composant soumis à la réglementation ESPN"

    class support_type_list(Datatype):
        equivalent_to = [ OneOf(["linéaire", "plaque et coque", "standard"]) ]
    support_type_list.label = "Liste des types de support"
    class support_type(DataProperty, FunctionalProperty):
        domain = [Support]
        range = [support_type_list]
    support_type.label = "type de support"

    class is_integral_support(DataProperty, FunctionalProperty):
        domain = [Support]
        range = [bool]
    is_integral_support.label = "est un support intégral (Y/N)"
    
    class support_group_type_list(Datatype):
        equivalent_to = [ OneOf(["groupe 1", "groupe 2"]) ]
    support_group_type_list.label = "Liste des groupes d'élément de support"
    class support_group_type(DataProperty, FunctionalProperty):
        domain = [Support | Component]
        range = [support_group_type_list]
    support_group_type.label = "groupe de l'élément de support"
#endregion
# endregion
# region - Instanciation Sommaire
RCCMRX = Code(name='RCC_MRx', label='RCC_MRx')
SECTIONI = Subpart(name="SectionI",label="Dispositions Générales")
RDG1000 = Subpart(name="RDG1000",label="PRESENTATION DU RCC-MRX")
RDG1100 = Subpart(name="RDG1100",label="STRUCTURE DU CODE")
RDG1200 = Subpart(name="RDG1200",label="SOMMAIRE GENERAL DU CODE")
RDG1300 = Subpart(name="RDG1300",label="LISTE DES NORMES ET DE LEUR EDITION APPLICABLE")
RDG1400 = Subpart(name="RDG1400",label="REFERENCES A LA SPECIFICATION D'EQUIPEMENT")
RDG1500 = Subpart(name="RDG1500",label="DEMANDES DE MODIFICATION")
RDG2000 = Subpart(name="RDG2000", label="DISPOSITIONS GENERALES")
RDG2100 = Subpart(name="RDG2100", label="DEFINITIONS")
RDG2110 = Subpart(name="RDG2110", label="Phases de la vie d'une installation nucléaire")
RDG2120 = Subpart(name="RDG2120", label="Organismes et personnes impliquées pendant la conception et la construction")
RDG2121 = Subpart(name="RDG2121", label="Maître d'Ouvrage et Exploitant")
RDG21211 = Subpart(name="RDG2121.1", label="Maître d'Ouvrage")
RDG21212 = Subpart(name="RDG2121.2", label="Exploitant")
RDG2122 = Subpart(name="RDG2122", label="Maître d'œuvre")
RDG2123 = Subpart(name="RDG2123", label="Fabricant")
RDG2124 = Subpart(name="RDG2124", label="Sous-traitant")
RDG2125 = Subpart(name="RDG2125", label="Fournisseur (ou sous-commandier)")
RDG2126 = Subpart(name="RDG2126", label="Prestataire - Donneur d'ordre")
RDG2127 = Subpart(name="RDG2127", label="Contrôleur")
RDG2128 = Subpart(name="RDG2128", label="Inspecteur")
RDG2200 = Subpart(name="RDG2200", label="RESPONSABILITES")
RDG2210 = Subpart(name="RDG2210", label="Responsabilités du Maître d'Ouvrage")
RDG2220 = Subpart(name="RDG2220", label="Responsabilités du Prestataire")
RDG2300 = Subpart(name="RDG2300", label="OBJET ET APPLICATION DU RCC-MRX")
RDG2310 = Subpart(name="RDG2310", label="Objet")
RDG2320 = Subpart(name="RDG2320", label="Domaine d'application")
RDG2330 = Subpart(name="RDG2330", label="Application du RCC-MRx")
RDG2400 = Subpart(name="RDG2400", label="EXIGENCES DEFINIES A LA COMMANDE")
RDG2500 = Subpart(name="RDG2500", label="NON-CONFORMITE AUX EXIGENCES APPLICABLES")
RDG2510 = Subpart(name="RDG2510", label="Non-conformité aux exigences de la commande (autres que le RCC-MRx)")
RDG2520 = Subpart(name="RDG2520", label="Non-conformité aux exigences du RCC-MRx")
RDG3000 = Subpart(name="RDG3000", label="DOCUMENTS A ETABLIR")
RDG3100 = Subpart(name="RDG3100", label="SPECIFICATION D'EQUIPEMENT")
RDG3200 = Subpart(name="RDG3200", label="DOCUMENTS TECHNIQUES GENERAUX")
RDG3210 = Subpart(name="RDG3210", label="Documents d'ensemble et de repérage")
RDG3220 = Subpart(name="RDG3220", label="NOMENCLATURE")
RDG3230 = Subpart(name="RDG3230", label="Note de définition des ateliers de fabrication")
RDG3300 = Subpart(name="RDG3300", label="FICHE DE NON-CONFORMITE ET FICHE D'ANOMALIE")
RDG3310 = Subpart(name="RDG3310", label="Fiche de non-conformité")
RDG3320 = Subpart(name="RDG3320", label="Fiche d'anomalie")
RDG3400 = Subpart(name="RDG3400", label="DOCUMENTS DE PROGRAMMATION, DE SUIVI ET DE COMPTE-RENDU FINAL")
RDG3410 = Subpart(name="RDG3410", label="Documents de Suivi (DS)")
RDG3411 = Subpart(name="RDG3411", label="Objet")
RDG3412 = Subpart(name="RDG3412", label="Contenu des Documents de Suivi à l'état initial")
RDG3413 = Subpart(name="RDG3413", label="Evolution du Document de Suivi en cours de fabrication")
RDG3414 = Subpart(name="RDG3414", label="Document de Suivi à l'état final")
RDG3420 = Subpart(name="RDG3420", label="Déclaration de conformité")
RDG3421 = Subpart(name="RDG3421", label="Objet")
RDG3422 = Subpart(name="RDG3422", label="Contenu")
RDG3430 = Subpart(name="RDG3430", label="Rapport de Fin de Conception et de Fabrication (RFCF)")
RDG3431 = Subpart(name="RDG3431", label="Objet")
RDG3432 = Subpart(name="RDG3432", label="Contenu")
RDG4000 = Subpart(name="RDG4000", label="CLES D'ENTREE DANS LE RCC-MRX")
RDG5000 = Subpart(name="RDG5000", label="SYSTEME DE GESTION")
RDG5100 = Subpart(name="RDG5100", label="OBJET")
RDG5200 = Subpart(name="RDG5200", label="GESTION DES RESPONSABILITES")
RDG5300 = Subpart(name="RDG5300", label="MISE EN PLACE DES PROCESSUS")
RDG5400 = Subpart(name="RDG5400", label="AUTRES EXIGENCES DE QUALITE")
RDG5410 = Subpart(name="RDG5410", label="Exigences de qualité applicables aux laboratoires")
RDG5420 = Subpart(name="RDG5420", label="Exigences de qualité applicables aux opérations de soudage")
SECTIONII = Subpart(name="SectionII", label="Section II: EXIGENCES COMPLEMENTAIRES ET DISPOSITIONS PARTICULIERES")
REC1000 = Subpart(name="REC1000", label="PRESENTATION DE LA SECTION II")
REC1100 = Subpart(name="REC1100", label="STRUCTURE DE LA SECTION II")
REC1200 = Subpart(name="REC1200", label="SOMMAIRE DE LA SECTION II")
REC1300 = Subpart(name="REC1300", label="LISTE DES NORMES/TEXTES ET DE LEUR EDITION APPLICABLE")
REC1400 = Subpart(name="REC1400", label="REFERENCES A LA SPECIFICATION D'EQUIPEMENT")
REC2000 = Subpart(name="REC2000", label="EXIGENCES COMPLEMENTAIRES POUR L'UTILISATION DES NORMES NF EN")
REC2100 = Subpart(name="REC2100", label="PREAMBULE")
REC2110 = Subpart(name="REC2110", label="Règles générales pour la boulonnerie")
REC2200 = Subpart(name="REC2200", label="UTILISATION DE LA NORME NF EN 13445")
REC2210 = Subpart(name="REC2210", label="NF EN 13445-1: Généralités")
REC2220 = Subpart(name="REC2220", label="NF EN 13445-2: Matériaux")
REC2230 = Subpart(name="REC2230", label="NF EN 13445-3: Conception")
REC2240 = Subpart(name="REC2240", label="NF EN 13445-4: Fabrication")
REC2250 = Subpart(name="REC2250", label="NF EN 13445-5: Inspection et contrôles")
REC2260 = Subpart(name="REC2260", label="NF EN 13445-6: Récipients sous pression moulés en fonte à graphite sphéroïdal")
REC2270 = Subpart(name="REC2270", label="FD CR 13445-7: Guide pour l'utilisation des procédures d'évaluation de la conformité")
REC2280 = Subpart(name="REC2280", label="NF EN 13445-8: Exigences complémentaires pour les récipients sous pression en aluminium et alliage d'aluminium")
REC2300 = Subpart(name="REC2300", label="UTILISATION DE LA NORME NF EN 13480")
REC2310 = Subpart(name="REC2310", label="NF EN 13480-1: Généralités")
REC2320 = Subpart(name="REC2320", label="NF EN 13480-2: Matériaux")
REC2330 = Subpart(name="REC2330", label="NF EN 13480-3: Conception et Calcul")
REC2340 = Subpart(name="REC2340", label="NF EN 13480-4: Fabrication et installation")
REC2350 = Subpart(name="REC2350", label="NF EN 13480-5 : Inspection et contrôles")
REC2360 = Subpart(name="REC2360", label="NF EN 13480-6: Tuyauteries enterrées")
REC2370 = Subpart(name="REC2370", label="FD TR 13480-7: Guide pour l'utilisation des procédures d'évaluation de la conformité")
REC2400 = Subpart(name="REC2400", label="UTILISATION DE LA NORME NF EN 1993-1-1: EUROCODE 3")
REC3000 = Subpart(name="REC3000", label="DISPOSITIONS PARTICULIERES POUR LES MATERIELS SOUMIS A UNE REGLEMENTATION")
REC3100 = Subpart(name="REC3100", label="PREAMBULE")
REC3200 = Subpart(name="REC3200", label="MATERIELS SOUMIS A LA REGLEMENTATION DES EQUIPEMENTS SOUS PRESSION APPLICABLE EN FRANCE")
REC3210 = Subpart(name="REC3210", label="Généralités")
REC3220 = Subpart(name="REC3220", label="Mise en cohérence avec les dispositions générales du Code de l'environnement (R557-9-1 à 3 et R557-12-1 à 3) et celles de l'arrêté ESPN (Titre ler)")
REC3221 = Subpart(name="REC3221", label="Définitions et abréviations: dispositions particulières qui complètent RDG 2100")
REC3222 = Subpart(name="REC3222", label="Répartition des rôles: dispositions particulières incluses dans RDG 2100")
REC3223 = Subpart(name="REC3223", label="Dispositions particulières qui complètent RDG 2330")
REC3224 = Subpart(name="REC3224", label="Documentation technique: dispositions particulières qui complètent RDG 3430")
REC3230 = Subpart(name="REC3230", label="Mise en conformité : conception, fabrication et évaluation de la conformité")
REC3231 = Subpart(name="REC3231", label="ESP de catégorie I à IV: dispositions particulières qui complètent RDG 4000")
REC3232 = Subpart(name="REC3232", label="ESP de catégorie 0: dispositions particulières qui complètent RDG 4000")
REC3233 = Subpart(name="REC3233", label="ESPN classé N1ESPN et de catégorie I à IV: dispositions particulières qui complètent RDG 4000")
REC3234 = Subpart(name="REC3234", label="ESPN classé N2ESPN et de catégorie I à IV (1): dispositions particulières qui complètent RDG 4000")
REC3235 = Subpart(name="REC3235", label="ESPN classé N3ESPN et de catégorie I à IV: dispositions particulières qui complètent RDG 4000")
REC3236 = Subpart(name="REC3236", label="ESPN de catégorie 0 - classé N1ESPN: dispositions particulières qui complètent RDG 4000")
REC3237 = Subpart(name="REC3237", label="ESPN de catégorie 0 - classé N2ESPN: dispositions particulières qui complètent RDG 4000")
REC3238 = Subpart(name="REC3238", label="ESPN de catégorie 0 - classé N3ESPN: dispositions particulières qui complètent RDG 4000")
REC3239 = Subpart(name="REC3239", label="Ensembles: dispositions particulières qui complètent RDG 4000")
REC3240 = Subpart(name="REC3240", label="Numéro non utilisé")
REC3250 = Subpart(name="REC3250", label="Mise en cohérence avec l'annexe I de la Directive ESP : exigences essentielles de sécurité applicables aux ESP de catégorie I à IV")
REC3251 = Subpart(name="REC3251", label="Généralités : Remarques préliminaires et §1 de l'annexe I de la directive ESP")
REC3252 = Subpart(name="REC3252", label="Conception: §2 de l'annexe I de la directive ESP")
REC3253 = Subpart(name="REC3253", label="Fabrication: §3 de l'annexe I de la directive ESP")
REC3254 = Subpart(name="REC3254", label="Matériaux: §4 de l'annexe I de la directive ESP")
REC3255 = Subpart(name="REC3255", label="Equipements sous pression soumis à la flamme: §5 de l'annexe I de la directive ESP")
REC3256 = Subpart(name="REC3256", label="Tuyauterie au sens de l'article 3.3 du décret ESP: §6 de l'annexe I de la directive ESP")
REC3257 = Subpart(name="REC3257", label="Exigences quantitatives particulières : §7 de l'annexe I de la directive ESP")
REC3260 = Subpart(name="REC3260", label="Mise en cohérence avec l'annexe I de l'arrêté ESPN : Exigences essentielles de sécurité applicables aux ESPN de catégories I à IV et de niveau N1ESPN hormis certaines tuyauteries et leurs accessoires sous pression")
REC3261 = Subpart(name="REC3261", label="Préliminaire et généralités: §1 de l'annexe I de l'arrêté ESPN")
REC3262 = Subpart(name="REC3262", label="Conception: §2 de l'annexe I de l'arrêté ESPN")
REC3263 = Subpart(name="REC3263", label="Fabrication: §3 de l'annexe I de l'arrêté ESPN")
REC3264 = Subpart(name="REC3264", label="Matériaux: §4 de l'annexe I de l'arrêté ESPN")
REC3270 = Subpart(name="REC3270", label="Mise en conformité avec l'annexe II de l'arrêté ESPN : exigences essentielles de sécurité applicables aux ESPN de catégories I à IV et de niveau N2ESPN et à certaines tuyauteries de catégorie I à III et de niveau N1ESPN ainsi qu'aux accessoires sous pression qui leur sont raccordés")
REC3271 = Subpart(name="REC3271", label="Préliminaire et généralités: §1 de l'annexe II de l'arrêté ESPN")
REC3272 = Subpart(name="REC3272", label="Conception: §2 de l'annexe II de l'arrêté ESPN")
REC3273 = Subpart(name="REC3273", label="Fabrication: §3 de l'annexe II de l'arrêté ESPN")
REC3274 = Subpart(name="REC3274", label="Matériaux: §4 de l'annexe II de l'arrêté ESPN")
REC3280 = Subpart(name="REC3280", label="Mise en cohérence avec l'annexe III de l'arrêté ESPN : exigences essentielles de sécurité applicables aux ESPN de catégories I à IV et de niveau N3ESPN")
REC3281 = Subpart(name="REC3281", label="Préliminaire et généralités: §1 de l'annexe III de l'arrêté ESPN")
REC3282 = Subpart(name="REC3282", label="Conception: §2 de l'annexe III de l'arrêté ESPN")
REC3283 = Subpart(name="REC3283", label="Fabrication: §3 de l'annexe III de l'arrêté ESPN")
REC3290 = Subpart(name="REC3290", label="Mise en conformité avec l'Annexe IV de l'arrêté ESPN: prescriptions pour la détermination des exigences de radioprotection")
REC3291 = Subpart(name="REC3291", label="Matériaux: §1 de l'annexe IV de l'arrêté ESPN")
REC3292 = Subpart(name="REC3292", label="Conception: §2 de l'annexe IV de l'arrêté ESPN")
REC3293 = Subpart(name="REC3293", label="Moyens d'inspection et de maintenance: §3 de l'annexe IV de l'arrêté ESPN")
REC3300 = Subpart(name="REC3300", label="SUBSTANCES SOUMISES A LA REGLEMENTATION REACH")
REC3310 = Subpart(name="REC3310", label="Généralités")
REC3320 = Subpart(name="REC3320", label="Définitions et champ d'application: dispositions particulières qui complètent RDG 2100")
REC3330 = Subpart(name="REC3330", label="Substances citées dans le code RCC-MRx")
SECTIONIII = Subpart(name="SectionIII", label="Règles pour les matériels mécaniques des Installations Nucléaires")
TOME1 = Subpart(name="Tome1", label="Règles de conception et de construction")
VOLUMEA = Subpart(name="VolumeA", label="Dispositions générales relatives à la section III")
RA1000 = Subpart(name="RA1000", label="PRESENTATION DE LA SECTION III")
RA1100 = Subpart(name="RA1100", label="Structure de la section III")
RA1200 = Subpart(name="RA1200", label="Sommaire de la SECTION III")
RA1300 = Subpart(name="RA1300", label="LISTE DES NORMES ET DE LEUR EDITION APPLICABLE")
RA1400 = Subpart(name="RA1400", label="References a la Specification d'Equipement")
RA1500 = Subpart(name="RA1500", label="Demande de Modification de la section III")
RA2000 = Subpart(name="RA2000", label="DISPOSITIONS GENERALES DE LA SECTION III")
RA3000 = Subpart(name="RA3000", label="DOCUMENTS A ETABLIR EN APPLICATION DE LA SECTION III")
RA3100 = Subpart(name="RA3100", label="Specification d'Equipement")
RA3200 = Subpart(name="RA3200", label="Documents techniques generaux")
RA3210 = Subpart(name="RA3210", label="Documents d'ensemble et de repérage")
RA3220 = Subpart(name="RA3220", label="Nomenclature")
RA3230 = Subpart(name="RA3230", label="Note de définition des ateliers de fabrication")
RA3300 = Subpart(name="RA3300", label="DOCUMENTS LIES A LA CONCEPTION")
RA3310 = Subpart(name="RA3310", label="Notes de Dimensionnement et de Calcul - Dossier de Conception")
RA3400 = Subpart(name="RA3400", label="Documents LIES AUX APPROVISIONNEMENTS")
RA3410 = Subpart(name="RA3410", label="Programme Technique de Fabrication de pièces ou de produits (PTF)")
RA3420 = Subpart(name="RA3420", label="Sous-commandes de pièces ou de produits")
RA3430 = Subpart(name="RA3430", label="Procès-Verbaux associes aux approvisionnements de pièces ou de produits")
RA3500 = Subpart(name="RA3500", label="Documents lies a la FABRICATION (AUTRE QUE LE SOUDAGE)")
RA3510 = Subpart(name="RA3510", label="Procédures ou instructions de fabrication")
RA3600 = Subpart(name="RA3600", label="Documents lies au soudage")
RA3610 = Subpart(name="RA3610", label="Cahier de Soudage")
RA3620 = Subpart(name="RA3620", label="Documents de recette des produits d'apport et d'exécution")
RA3630 = Subpart(name="RA3630", label="Procès-Verbaux de soudage")
RA3640 = Subpart(name="RA3640", label="Conservation des Enregistrements")
RA3700 = Subpart(name="RA3700", label="Documents lies aux controles et aux essais")
RA3710 = Subpart(name="RA3710", label="Procédures ou instructions de contrôle et d'essai")
RA3720 = Subpart(name="RA3720", label="Procès-Verbaux de contrôle et d'essai")
RA3730 = Subpart(name="RA3730", label="Rapports d'épreuve")
RA3800 = Subpart(name="RA3800", label="FICHE DE NON-CONFORMITE ET FICHE D'ANOMALIE")
RA3900 = Subpart(name="RA3900", label="DOCUMENTS DE PROGRAMMATION, DE SUIVI ET DE COMPTE-RENDU FINAL")
RA3910 = Subpart(name="RA3910", label="Documents de suivi (DS)")
RA3920 = Subpart(name="RA3920", label="Déclaration de Conformité")
RA3930 = Subpart(name="RA3930", label="Rapport de Fin de Conception et de Fabrication (RFCF)")
RA4000 = Subpart(name="RA4000", label="CLES D'ENTREE DANS LA SECTION III")
RA5000 = Subpart(name="RA5000", label="SYSTEME DE GESTION")
VOLUMEB = Subpart(name="VolumeB", label="Composants de niveau 1")
VOLUMEC = Subpart(name="VolumeC", label="Composants de niveau 2")
VOLUMED = Subpart(name="VolumeD", label="Composants de niveau 3")
VOLUMEK = Subpart(name="VolumeK", label="Règles de conception et de construction des petits composants")
VOLUMEL = Subpart(name="VolumeL", label="Règles de surveillance en exploitation")
VOLUMEZ = Subpart(name="VolumeZ", label="Annexes techniques")
TOME2 = Subpart(name="Tome2", label="Règles de conception et de construction")
TOME3 = Subpart(name="Tome3", label="Règles de conception et de construction")
TOME4 = Subpart(name="Tome4", label="Règles de conception et de construction")
TOME5 = Subpart(name="Tome5", label="Règles de conception et de construction")
TOME6 = Subpart(name="Tome6", label="Règles de conception et de construction")

SECTIONI.subpartOf = RCCMRX
RDG1000.subpartOf = SECTIONI
RDG1100.subpartOf = RDG1000
RDG1200.subpartOf = RDG1000
RDG1300.subpartOf = RDG1000
RDG1400.subpartOf = RDG1000
RDG1500.subpartOf = RDG1000
RDG2000.subpartOf = SECTIONI
RDG2100.subpartOf = RDG2000
RDG2110.subpartOf = RDG2100
RDG2120.subpartOf = RDG2100
RDG2121.subpartOf = RDG2120
RDG21211.subpartOf = RDG2121
RDG21212.subpartOf = RDG2121
RDG2122.subpartOf = RDG2120
RDG2123.subpartOf = RDG2120
RDG2124.subpartOf = RDG2120
RDG2125.subpartOf = RDG2120
RDG2126.subpartOf = RDG2120
RDG2127.subpartOf = RDG2120
RDG2128.subpartOf = RDG2120
RDG2200.subpartOf = RDG2000
RDG2210.subpartOf = RDG2200
RDG2220.subpartOf = RDG2200
RDG2300.subpartOf = RDG2000
RDG2310.subpartOf = RDG2300
RDG2320.subpartOf = RDG2300
RDG2330.subpartOf = RDG2300
RDG2400.subpartOf = RDG2000
RDG2500.subpartOf = RDG2000
RDG2510.subpartOf = RDG2500
RDG2520.subpartOf = RDG2500
RDG3000.subpartOf = SECTIONI
RDG3100.subpartOf = RDG3000
RDG3200.subpartOf = RDG3000
RDG3210.subpartOf = RDG3200
RDG3220.subpartOf = RDG3200
RDG3230.subpartOf = RDG3200
RDG3300.subpartOf = RDG3000
RDG3310.subpartOf = RDG3300
RDG3320.subpartOf = RDG3300
RDG3400.subpartOf = RDG3000
RDG3410.subpartOf = RDG3400
RDG3411.subpartOf = RDG3410
RDG3412.subpartOf = RDG3410
RDG3413.subpartOf = RDG3410
RDG3414.subpartOf = RDG3410
RDG3420.subpartOf = RDG3400
RDG3421.subpartOf = RDG3420
RDG3422.subpartOf = RDG3420
RDG3430.subpartOf = RDG3400
RDG3431.subpartOf = RDG3430
RDG3432.subpartOf = RDG3430
RDG4000.subpartOf = SECTIONI
RDG5000.subpartOf = SECTIONI
RDG5100.subpartOf = RDG5000
RDG5200.subpartOf = RDG5000
RDG5300.subpartOf = RDG5000
RDG5400.subpartOf = RDG5000
RDG5410.subpartOf = RDG5400
RDG5420.subpartOf = RDG5400
SECTIONII.subpartOf = RCCMRX
REC1000.subpartOf = SECTIONII
REC1100.subpartOf = REC1000
REC1200.subpartOf = REC1000
REC1300.subpartOf = REC1000
REC1400.subpartOf = REC1000
REC2000.subpartOf = SECTIONII
REC2100.subpartOf = REC2000
REC2110.subpartOf = REC2100
REC2200.subpartOf = REC2000
REC2210.subpartOf = REC2200
REC2220.subpartOf = REC2200
REC2230.subpartOf = REC2200
REC2240.subpartOf = REC2200
REC2250.subpartOf = REC2200
REC2260.subpartOf = REC2200
REC2270.subpartOf = REC2200
REC2280.subpartOf = REC2200
REC2300.subpartOf = REC2000
REC2310.subpartOf = REC2300
REC2320.subpartOf = REC2300
REC2330.subpartOf = REC2300
REC2340.subpartOf = REC2300
REC2350.subpartOf = REC2300
REC2360.subpartOf = REC2300
REC2370.subpartOf = REC2300
REC2400.subpartOf = REC2000
REC3000.subpartOf = SECTIONII
REC3100.subpartOf = REC3000
REC3200.subpartOf = REC3000
REC3210.subpartOf = REC3200
REC3220.subpartOf = REC3200
REC3221.subpartOf = REC3220
REC3222.subpartOf = REC3220
REC3223.subpartOf = REC3220
REC3224.subpartOf = REC3220
REC3230.subpartOf = REC3200
REC3231.subpartOf = REC3230
REC3232.subpartOf = REC3230
REC3233.subpartOf = REC3230
REC3234.subpartOf = REC3230
REC3235.subpartOf = REC3230
REC3236.subpartOf = REC3230
REC3237.subpartOf = REC3230
REC3238.subpartOf = REC3230
REC3239.subpartOf = REC3230
REC3240.subpartOf = REC3200
REC3250.subpartOf = REC3200
REC3251.subpartOf = REC3250
REC3252.subpartOf = REC3250
REC3253.subpartOf = REC3250
REC3254.subpartOf = REC3250
REC3255.subpartOf = REC3250
REC3256.subpartOf = REC3250
REC3257.subpartOf = REC3250
REC3260.subpartOf = REC3200
REC3261.subpartOf = REC3260
REC3262.subpartOf = REC3260
REC3263.subpartOf = REC3260
REC3264.subpartOf = REC3260
REC3270.subpartOf = REC3200
REC3271.subpartOf = REC3270
REC3272.subpartOf = REC3270
REC3273.subpartOf = REC3270
REC3274.subpartOf = REC3270
REC3280.subpartOf = REC3200
REC3281.subpartOf = REC3280
REC3282.subpartOf = REC3280
REC3283.subpartOf = REC3280
REC3290.subpartOf = REC3200
REC3291.subpartOf = REC3290
REC3292.subpartOf = REC3290
REC3293.subpartOf = REC3290
REC3300.subpartOf = REC3000
REC3310.subpartOf = REC3300
REC3320.subpartOf = REC3300
REC3330.subpartOf = REC3300
SECTIONIII.subpartOf = RCCMRX
TOME1.subpartOf = SECTIONIII
VOLUMEA.subpartOf = TOME1
RA1000.subpartOf = VOLUMEA
RA1100.subpartOf = RA1000
RA1200.subpartOf = RA1000
RA1300.subpartOf = RA1000
RA1400.subpartOf = RA1000
RA1500.subpartOf = RA1000
RA2000.subpartOf = VOLUMEA
RA3000.subpartOf = VOLUMEA
RA3100.subpartOf = RA3000
RA3200.subpartOf = RA3000
RA3210.subpartOf = RA3200
RA3220.subpartOf = RA3200
RA3230.subpartOf = RA3200
RA3300.subpartOf = RA3000
RA3310.subpartOf = RA3300
RA3400.subpartOf = RA3000
RA3410.subpartOf = RA3400
RA3420.subpartOf = RA3400
RA3430.subpartOf = RA3400
RA3500.subpartOf = RA3000
RA3510.subpartOf = RA3500
RA3600.subpartOf = RA3000
RA3610.subpartOf = RA3600
RA3620.subpartOf = RA3600
RA3630.subpartOf = RA3600
RA3640.subpartOf = RA3600
RA3700.subpartOf = RA3000
RA3710.subpartOf = RA3700
RA3720.subpartOf = RA3700
RA3730.subpartOf = RA3700
RA3800.subpartOf = RA3000
RA3900.subpartOf = RA3000
RA3910.subpartOf = RA3900
RA3920.subpartOf = RA3900
RA3930.subpartOf = RA3900
RA4000.subpartOf = VOLUMEA
RA5000.subpartOf = VOLUMEA
VOLUMEB.subpartOf = TOME1
VOLUMEC.subpartOf = TOME1
VOLUMED.subpartOf = TOME1
VOLUMEK.subpartOf = TOME1
VOLUMEL.subpartOf = TOME1
VOLUMEZ.subpartOf = TOME1
TOME2.subpartOf = SECTIONIII
TOME3.subpartOf = SECTIONIII
TOME4.subpartOf = SECTIONIII
TOME5.subpartOf = SECTIONIII
TOME6.subpartOf = SECTIONIII
# endregion
# region - Instanciation Phases du cycle de vie
CONCEPTION = Lifecycle(name="Conception", label ="Conception")
FABRICATION = Lifecycle(name="Fabrication", label ="Fabrication")
STOCKAGE = Lifecycle(name="Stockage", label ="Stockage")
TRANSPORT = Lifecycle(name="Transport", label ="Transport")
MONTAGE = Lifecycle(name="Montage", label ="Montage")
MISE_EN_SERVICE = Lifecycle(name="Mise_en_service", label ="Mise en service")
EXPLOITATION = Lifecycle(name="Exploitation", label ="Exploitation")
DEMANTELEMENT = Lifecycle(name="Demantelement", label ="Démantèlement")
# endregion
# region - Instanciation Workpackages
TOUTES_ACTIVITES = Workpackage(name="Toutes_activites", label="Toutes les activités")
DOCUMENTATION = Workpackage(name="Documentation", label="Documentation")
SPECIFICATION = Workpackage(name="Specification", label="Spécification")
CONCEPTION_DIMENSIONNEMENT = Workpackage(name="Conception_et_dimensionnement", label="Conception et dimensionnement")
CHOIX_MATERIAUX = Workpackage(name="Choix_des_materiaux", label="Choix des matériaux")
APPROVISIONNEMENT_MATERIAUX = Workpackage(name="Approvisionnement_des_materiaux", label="Approvisionnement des matériaux")
FABRICATION_WP = Workpackage(name="Fabrication_wp", label="Fabrication_wp")
SOUDAGE = Workpackage(name="Soudage", label="Soudage")
IDENTIFICATION = Workpackage(name="Identification", label="Identification")
VALIDATION= Workpackage(name="Validation", label="Validation")
QUALIFICATION_TECHNIQUE = Workpackage(name="Qualification_technique", label="Qualification technique")
MONTAGE_WP = Workpackage(name="Montage_wp", label="Montage_wp")
MAINTENANCE = Workpackage(name="Maintenance", label="Maintenance")
ESSAI = Workpackage(name="Essai", label="Essai")
# endregion
# region - Instanciation Documents
SPECIFICATION_EQUIPEMENT = Document(name="Specification_d_equipement", label="Spécification d'équipement")
SPECIFICATION_EQUIPEMENT.isDefinedBy = "La Spécification d'Equipement est le document par lequel le Maître d'Ouvrage définit ses exigences aux sous-traitants tant sur le plan technique que sur celui de l’assurance de la qualité."
SPECIFICATION_EQUIPEMENT.subpart_reference = RDG3100
SPECIFICATION_EQUIPEMENT.relates_to_workpackage.append(SPECIFICATION)

# Documents techniques généraux

DOCUMENTS_ENSEMBLE_REPERAGE = Document(name="Documents_d_ensemble_et_de_repérage", label="Documents d'ensemble et de repérage")
DOCUMENTS_ENSEMBLE_REPERAGE.isDefinedBy = "Donner une description d'ensemble d'un matériel ou d'un de ses principaux éléments constitutifs : - en fixer les caractéristiques géométriques, - permettre de comprendre l'articulation des différentes pièces constitutives notamment du point de vue fabrication et assemblage."
DOCUMENTS_ENSEMBLE_REPERAGE.subpart_reference = RDG3210
DOCUMENTS_ENSEMBLE_REPERAGE.relates_to_workpackage.append(CONCEPTION_DIMENSIONNEMENT)

NOMENCLATURE = Document(name = "Nomenclature", label="Nomenclature")
NOMENCLATURE.isDefinedBy = "Fixer la liste des éléments constitutifs faisant l'objet de prescriptions techniques : - dans le présent Code, - dans la commande."
NOMENCLATURE.subpart_reference = RDG3220
NOMENCLATURE.relates_to_workpackage.append(CONCEPTION_DIMENSIONNEMENT)

NOTE_DEFINITION_ATELIERS_FABRICATION = Document(name="Note_de_definition_des_ateliers_fabrication", label="Note de définition des ateliers de fabrication")
NOTE_DEFINITION_ATELIERS_FABRICATION.isDefinedBy = "La note de définition des ateliers de fabrication doit préciser les ateliers de fabrication et les travaux qui y seront effectués pour la réalisation du matériel."
NOTE_DEFINITION_ATELIERS_FABRICATION.subpart_reference = RDG3230
NOTE_DEFINITION_ATELIERS_FABRICATION.relates_to_workpackage.append(FABRICATION_WP)

# Documents liés à la conception
DOSSIER_CONCEPTION = Document(name="Dossier_de_conception", label="Dossier de conception")
DOSSIER_CONCEPTION.relates_to_workpackage.append(CONCEPTION_DIMENSIONNEMENT)

NOTE_DIMENSIONNEMENT_CALCUL = Document(name="Note_de_dimensionnement_et_de_calcul", label="Note de dimensionnement et de calcul")
NOTE_DIMENSIONNEMENT_CALCUL.relates_to_workpackage.append(CONCEPTION_DIMENSIONNEMENT)

# Documents liés aux approvisionnements
PROGRAMME_TECHNIQUE_FABRICATION = Document(name="Programme_technique_de_fabrication_de_pieces_ou_de_produits(PTF)", label="Programme technique de fabrication de pièces ou de produits")
PROGRAMME_TECHNIQUE_FABRICATION.relates_to_workpackage.append(APPROVISIONNEMENT_MATERIAUX)

SOUS_COMMANDE_PIECES_PRODUITS = Document(name="Sous_commande_de_pieces_ou_de_produits", label="Sous-commande de pièces ou de produits")
SOUS_COMMANDE_PIECES_PRODUITS.relates_to_workpackage.append(APPROVISIONNEMENT_MATERIAUX)

PV_APPRO_PIECES_PRODUITS = Document(name="Proces_verbaux_associes_aux_approvisionnements_de_pieces_ou_de_produits", label="Procès-verbaux associés aux approvisionnements de pièces ou de produits")
PV_APPRO_PIECES_PRODUITS.relates_to_workpackage.append(APPROVISIONNEMENT_MATERIAUX)

DOSSIER_MATERIAU = Document(name="Dossier_materiau", label="Dossier matériau")
DOSSIER_MATERIAU.relates_to_workpackage.append(APPROVISIONNEMENT_MATERIAUX)

# Documents liés à la fabrication
PROCEDURE_FABRICATION = Document(name="Procedure_ou_instruction_de_fabrication", label="Procédure ou instruction de fabrication")
PROCEDURE_FABRICATION.relates_to_workpackage.append(FABRICATION_WP)

CAHIER_SOUDAGE = Document(name="Cahier_de_soudage", label="Cahier de soudage")
CAHIER_SOUDAGE.relates_to_workpackage.append(SOUDAGE)

MODE_OPERATOIRE_SOUDAGE = Document(name="Mode_operatoire_de_soudage", label="Mode opératoire de soudage")
MODE_OPERATOIRE_SOUDAGE.relates_to_workpackage.append(SOUDAGE)

RECETTE_PRODUIT_APPORT = Document(name="Recette_de_produit_d_apport", label="Recette de produit d'apport")
RECETTE_PRODUIT_APPORT.relates_to_workpackage.append(SOUDAGE)

QUALIFICATION_MODE_OPERATOIRE_SOUDAGE = Document(name="Qualification_de_mode_operatoire_de_soudage(QMOS)", label="Qualification de mode opératoire de soudage (QMOS)")
QUALIFICATION_MODE_OPERATOIRE_SOUDAGE.relates_to_workpackage.append(SOUDAGE)

QUALIFICATION_SOUDEUR = Document(name="Qualification_de_soudeur_et_operateur_de_soudage", label="Qualification de soudeur et opérateur de soudage")
QUALIFICATION_SOUDEUR.relates_to_workpackage.append(SOUDAGE)
    
SOUDURE_PRODUCTION = Document(name="Soudures_de_production", label="Soudures de production")
SOUDURE_PRODUCTION.relates_to_workpackage.append(SOUDAGE)

RECHARGEMENT_DUR = Document(name="Rechargement_dur", label="Rechargement dur")
RECHARGEMENT_DUR.relates_to_workpackage.append(SOUDAGE)

PV_SOUDAGE = Document(name="Proces_verbaux_de_soudage", label="Procès-verbaux de soudage")
PV_SOUDAGE.relates_to_workpackage.append(SOUDAGE)

# Documents liés aux contrôles et aux essais
PROCEDURE_CONTROLE_ESSAI = Document(name="Procedure_ou_instruction_de_controle_et_d_essai", label="Procédure ou instruction de contrôle et d'essai")
PROCEDURE_CONTROLE_ESSAI.relates_to_workpackage.append(ESSAI)

PV_ESSAI = Document(name="Proces_verbaux_de_controle_et_d_essai", label="Procès-verbaux de contrôle et d'essai")
PV_ESSAI.relates_to_workpackage.append(ESSAI)

RAPPORT_EPREUVE = Document(name="Rapport_d_epreuve", label="Rapport d'épreuve")
RAPPORT_EPREUVE.relates_to_workpackage.append(ESSAI)

FICHE_NON_CONFORMITE = Document(name="Fiche_de_non_conformite", label="Fiche de non-conformité")
FICHE_NON_CONFORMITE.isDefinedBy = "Définir par écrit la nature et l'étendue de la non-conformité et indiquer la solution retenue pour permettre l'utilisation du matériel."
FICHE_NON_CONFORMITE.subpart_reference = RDG3310
FICHE_NON_CONFORMITE.relates_to_workpackage.append(TOUTES_ACTIVITES)

FICHE_ANOMALIE = Document(name="Fiche_d_anomalie", label="Fiche d'anomalie")
FICHE_ANOMALIE.isDefinedBy = "Permettre le traitement de la non-conformité dans les cas décrits en RDG 2500."
FICHE_ANOMALIE.subpart_reference = RDG2500
FICHE_ANOMALIE.relates_to_workpackage.append(TOUTES_ACTIVITES)

DOCUMENT_SUIVI = Document(name="Document_de_suivi(DS)", label="Document de suivi (DS)")
DOCUMENT_SUIVI.relates_to_workpackage.append(FABRICATION_WP)
    
DECLARATION_CONFORMITE = Document(name="Declaration_de_conformite", label="Déclaration de conformité")
DECLARATION_CONFORMITE.isDefinedBy = "Son objet est de certifier que la fourniture satisfait aux exigences techniques et qualité de la commande. Elle est établie par le Prestataire."
DECLARATION_CONFORMITE.subpart_reference = RDG3421
DECLARATION_CONFORMITE.relates_to_workpackage.append(FABRICATION_WP)

RAPPORT_FIN_CONCEPTION_FABRICATION = Document(name="Rapport_de_Fin_de_Conception_et_de_Fabrication(RFCF)", label="Rapport de Fin de Conception et de Fabrication (RFCF)")
RAPPORT_FIN_CONCEPTION_FABRICATION.isDefinedBy = "Le Rapport de Fin de Conception et de Fabrication a pour objet de réunir une partie des documents établis pour s'assurer que la qualité finale du matériel est conforme à la qualité requise et pouvoir en faire la démonstration. Il est établi par le Prestataire."
RAPPORT_FIN_CONCEPTION_FABRICATION.subpart_reference = RDG3431
RAPPORT_FIN_CONCEPTION_FABRICATION.relates_to_workpackage.append(FABRICATION_WP)
# endregion
# region - Instanciation Acteurs
MAITRE_OUVRAGE = Stakeholder(name="Maitre_d_Ouvrage", label="Maître d'Ouvrage")
MAITRE_OUVRAGE.isDefinedBy = "Personne physique ou morale qui décide de l'engagement de la conception et de la construction des ouvrages de l'Installation Nucléaire."
MAITRE_OUVRAGE.subpart_reference = RDG21211
EXPLOITANT = Stakeholder(name="Exploitant", label="Exploitant")
EXPLOITANT.isDefinedBy = "Personne titulaire de l’autorisation de création de l’Installation Nucléaire dans lequel l’équipement est installé ou destiné à l’être."
EXPLOITANT.subpart_reference = RDG21212
MAITRE_OEUVRE = Stakeholder(name="Maitre_d_Oeuvre", label="Maître d'Oeuvre")
MAITRE_OEUVRE.isDefinedBy = "Personne physique ou morale chargée de la conception d'ensemble et du contrôle de la réalisation des ouvrages de l'Installation Nucléaire, exécutés pour le compte du Maître d'Ouvrage."
MAITRE_OEUVRE.subpart_reference = RDG2122
FABRICANT = Stakeholder(name="Fabricant", label="Fabricant")
FABRICANT.isDefinedBy = "Personne physique ou morale chargée de la conception et de la construction d'une partie de l'Installation Nucléaire (par exemple la chaudière nucléaire, le circuit primaire, un dispositif d'irradiation ...)."
FABRICANT.subpart_reference = RDG2123
ORGANISME = Stakeholder(name="Organisme", label="Organisme")
SOUS_TRAITANT = Stakeholder(name="Sous_traitant", label="Sous-traitant")
SOUS_TRAITANT.isDefinedBy = "Personne physique ou morale qui réalise en usine ou sur le site, pour le compte du Fabricant, un matériel ou une partie de matériel de l'Installation Nucléaire, ou certaines prestations. Parmi ces sous-traitants figurent les fabricants de produits qui seront indiqués explicitement sous la forme fabricant de tubes, fabricant de tôles (lamineur), fabricant de pièces forgées (forgeron), fabricant de pompes, fabricant de robinets, etc …."
SOUS_TRAITANT.subpart_reference = RDG2124
FOURNISSEUR = Stakeholder(name="Fournisseur", label="Fournisseur")
FOURNISSEUR.isDefinedBy = "Personne physique ou morale (aciériste, forgeron, tubiste, fondeur ...) qui fabrique des produits ou des pièces pour le compte du Fabricant ou d’un sous-traitant."
FOURNISSEUR.subpart_reference = RDG2125
PRESTATAIRE = Stakeholder(name="Prestataire_Donneur_d_ordre", label="Prestataire - Donneur d'ordre")
PRESTATAIRE.isDefinedBy = "Le Prestataire est le titulaire d'un contrat passé avec un Donneur d'Ordre qui peut être le Maître d'Ouvrage lui-même ou un autre prestataire. Selon les cas, le Prestataire désigne donc le Maître d'Oeuvre, un Fabricant, un sous-traitant ou un Fournisseur."
PRESTATAIRE.subpart_reference = RDG2126
CONTROLEUR = Stakeholder(name="Controleur", label="Contrôleur")
CONTROLEUR.isDefinedBy = "Personne chargée par un Prestataire d'effectuer des contrôles de conformité aux documents joints à la commande reçue par ce Prestataire, au présent Code et aux documents établis en application de ce dernier. Le Contrôleur peut appartenir ou non au personnel du Prestataire."
CONTROLEUR.subpart_reference = RDG2127
INSPECTEUR = Stakeholder(name="Inspecteur", label="Inspecteur")
INSPECTEUR.isDefinedBy = "Personne sans lien de subordination avec le Prestataire concerné, mandatée pour surveiller que le matériel est réalisé et contrôlé en conformité avec les documents joints à la commande passée à ce Prestataire, avec le présent Code et avec les documents établis en application de ce dernier. Le présent Code ne désigne pas les organismes auxquels appartiennent les Inspecteurs, l'étendue de leur mission et leursmoyens d'action, ces dispositions étant précisées contractuellement par ailleurs. Nota : Les fonctions visées en RDG 2122 à 2125 peuvent être assurées, en tout ou en partie, par la même personne physique ou morale. Les Fournisseurs sont réputés Fabricants pour l'application des chapitres ou paragraphes du présent Code qui les concernent."
INSPECTEUR.subpart_reference = RDG2128
# endregion
# region - Instanciation Règles
# region - Instanciation Contexte
CTX_RDG1100 = Context(name="CTX_RDG1100",label="CTX_RDG1100")
CTX_RDG1100.subpart_reference = RDG1100
CTX_RDG1100.states = "Le présent Code RCC-MRx dont l'objet et l'application sont décrits en RDG 2300 est un des ouvrages publiés par l’AFCEN de la collection des règles de conception et de construction des centrales électronucléaires initiée avec le RCC-M pour les Réacteurs à Eau Pressurisée (REP). Le présent Code comprend trois sections : • Section I : dispositions générales, • Section II : exigences complémentaires et dispositions particulières, • Section III : règles pour les matériels mécaniques des Installations Nucléaires. Cette section III comprend six Tomes : - Le Tome 1 regroupe les règles de conception et de construction. Il est composé de volumes numérotés alphabétiquement : * volume A : dispositions générales de la Section III, * volume B : matériels du réacteur, de ses auxiliaires et supports de niveau N1Rx, * volume C : matériels du réacteur, de ses auxiliaires et supports de niveau N2Rx, * volume D : matériels du réacteur, de ses auxiliaires et supports de niveau N3Rx, * volume K : mécanismes de contrôle ou de manutention, * volume L : dispositifs d'irradiation, * volume Z : annexes techniques. - Les Tomes 2 à 5 regroupent des règles correspondant à différents domaines techniques : * Tome 2 : conditions d'approvisionnement des pièces et produits, * Tome 3 : mise en œuvre des différentes méthodes d'essais destructifs et non destructifs, * Tome 4 : qualifications des opérations de soudage et leur mise en œuvre, * Tome 5 : opérations de fabrication, autres que les opérations de soudage. - Le Tome 6 regroupe l’ensemble des règles en phase probatoire"

CTX_RDG1200 = Context(name="CTX_RDG1200", label="CTX_RDG1200")
CTX_RDG1200.subpart_reference = RDG1200
CTX_RDG1200.states = "Ce sommaire illustre la présentation générale du présent Code faite au RDG 1100 et fournit les sigles associés aux Sections, aux Tomes et aux Volumes. Il est complété en tête des Sections et de chacun des Tomes et Volumes par des sommaires détaillés."
CTX_RDG1200.includes_table.append("Tableau RDG1200")

CTX_RDG1300 = Context(name="CTX_RDG1300", label="CTX_RDG1300")
CTX_RDG1300.subpart_reference = RDG1300
CTX_RDG1300.states = "Les listes des normes citées dans chacune des Sections du présent Code sont regroupées au début de chacune des sections : • Section I : tableau RDG 1300, • Section II : tableau REC 1300, • Section III : tableau RA 1300. avec les mentions de leur édition et des amendements applicables. Une édition postérieure ne peut être utilisée que suite à une modification de ces tableaux."
CTX_RDG1300.includes_table.append("Tableau RDG1300")

CTX_RDG1400 = Context(name="CTX_RDG1400", label="CTX_RDG1400")
CTX_RDG1400.subpart_reference = RDG1400
CTX_RDG1400.states = "Les listes des paragraphes se référant à la Spécification d'Equipement sont données au début de chacune des sections : • Section I : tableau RDG 1400, • Section II : tableau REC 1400, • Section III : tableau RA 1400."
CTX_RDG1400.relates_to_document = [SPECIFICATION_EQUIPEMENT]
CTX_RDG1400.includes_table.append("Tableau RDG1400")

CTX_RDG1500 = Context(name="CTX_RDG1500", label="CTX_RDG1500")
CTX_RDG1500.subpart_reference = RDG1500
CTX_RDG1500.states = "Le présent Code fait l'objet de révisions. Des Demandes de Modification peuvent être présentées. Chaque demande est formulée par écrit en précisant la date d'édition du Code et la partie du texte concernée. Une proposition de rédaction accompagnée d'une justification est jointe par le demandeur à sa demande. Les demandes de modification sont instruites par l’AFCEN et, lorsqu'elles sont acceptées, elles font l'objet de fiches de modification qui sont ensuite intégrées soit dans un modificatif soit dans l'édition suivante. Ces modifications ont pour objet de tenir compte de l'évolution de la technologie ou de préciser certains points."

CTX_RDG2110 = Context(name="CTX_RDG2110", label="CTX_RDG2110")
CTX_RDG2110.subpart_reference = RDG2110
CTX_RDG2110.states = "Durant la vie d’une Installation Nucléaire, on distingue : la phase de Recherche et Développement (R&D stage), la phase de Choix du Site (Siting stage), la phase de Conception (Design stage), la phase de Construction (Construction stage), la phase de Mise en Service (Commissioning stage), la phase d'Exploitation (Operation stage) et la phase de Démantèlement (Decommissioning stage)."

CTX_RDG2310 = Context(name="CTX_RDG2310", label="CTX_RDG2310")
CTX_RDG2310.subpart_reference = RDG2310
CTX_RDG2310.states = "Le présent Code constitue un ensemble de règles techniques applicables à la conception et la construction des matériels mécaniques des Installations Nucléaires relevant de son domaine d'application (RDG 2320)."
CTX_RDG2310.seeAlso = ["RDG 2320"]

CTX_RDG2320 = Context(name="CTX_RDG2320", label="CTX_RDG2320")
CTX_RDG2320.subpart_reference = RDG2320
CTX_RDG2320.states = "Le présent Code, développé en particulier pour les Réacteurs au Sodium (SFR), les Réacteurs de Recherche (RR) et les Réacteurs de Fusion (FR-ITER) peut être également utilisé pour des matériels mécaniques d’autres types d’Installations Nucléaires. Les règles de conception des composants soumis à l’irradiation ont été établies sur la base de données issues d’installations nucléaires courantes (flux neutronique). L’utilisation de ces règles pour d’autres types d’irradiation (par exemple irradiation aux protons, avec forte production d’hélium…) n’est pas couverte par le Code. Le domaine d'application du présent Code comprend exclusivement les matériels mécaniques des Installations Nucléaires : • jugés importants sur le plan de la sûreté ou de la disponibilité, • ayant une fonction d'étanchéité, de cloisonnement, de guidage, de maintien ou de supportage, • de type coques-réservoirs-récipients-cuves, pompes, robinets-vannes, tuyauteries, soufflets, structures caissonnées, échangeurs, dispositifs d’irradiation, ainsi que leurs supports, mécanismes de contrôle ou de manutention."
# endregion
# region - Instanciation Règles
RUL_RDG2330= Rule(name="RUL_RDG2330", label="RUL_RDG2330")
RUL_RDG2330.subpart_reference = RDG2330
RUL_RDG2330.states = "Il incombe au Maître d'Ouvrage, au Maître d'Oeuvre et aux Fabricants de fixer dans le cadre contractuel la liste des matériels mécaniques et les supports à concevoir et construire suivant le présent Code en précisant les clés d'entrée (RDG 4000). Cette liste doit être incluse ou référencée dans la Spécification d'Equipement (RDG 3100). Le tableau RDG 2330 indique la répartition des tâches entre le Maître d’Ouvrage ou l’Exploitant, le Fabricant et l’Organisme (REC 3221) pour des équipements soumis au présent Code, qu’ils soient ou non également soumis à la règlementation des équipements sous pression (ESP/ESPN - REC 3200). Chacun des organismes en charge des phases de Conception et de Construction de ces matériels doit identifier et mettre en place les processus associés ainsi qu’un Système de Gestion adéquat selon RDG 5000."
RUL_RDG2330.relates_to_object = [EXPLOITANT,MAITRE_OUVRAGE,MAITRE_OEUVRE,FABRICANT]
RUL_RDG2330.relates_to_workpackage = [SPECIFICATION]
RUL_RDG2330.relates_to_document = [SPECIFICATION_EQUIPEMENT]
RUL_RDG2330.seeAlso = [RDG4000, RDG3100, REC3221, REC3200, RDG5000]
RUL_RDG2330.includes_table = ["Table RDG2330"]

RUL_RDG2110 = Rule(name="RUL_RDG2110", label="RUL_RDG2110")
RUL_RDG2110.subpart_reference = RDG2110
RUL_RDG2110.states = "Pour les phases de Conception et de Construction, l’Organisme Responsable de l’Installation Nucléaire (Maître d'Ouvrage ou Exploitant) désigne le ou les Maîtres d'Oeuvre : • le Responsable de la Conception (souvent appelé Principal Designer) qui a la responsabilité de spécifier les exigences de conception et de valider la conception finale, • et le Responsable de la Construction."
RUL_RDG2110.relates_to_object = [EXPLOITANT,MAITRE_OUVRAGE,MAITRE_OEUVRE]
RUL_RDG2110.relates_to_workpackage = [SPECIFICATION]

RUL_RDG2210 = Rule(name="RUL_RDG2210", label="RUL_RDG2210")
RUL_RDG2210.subpart_reference = RDG2210
RUL_RDG2210.states = "Le Maître d'Ouvrage est le responsable de la sûreté de l'installation dont il a la charge. Cette responsabilité est formalisée, préalablement à la réalisation, par une commande. La commande mentionne notamment les objectifs et les exigences en terme de qualité."
RUL_RDG2210.relates_to_object = [MAITRE_OUVRAGE]
RUL_RDG2210.relates_to_workpackage = [SPECIFICATION]

RUL_RDG2220 = Rule(name="RUL_RDG2220", label="RUL_RDG2220")
RUL_RDG2220.subpart_reference = RDG2220
RUL_RDG2220.states = "Le Prestataire assume la responsabilité technique d'ensemble de la réalisation de l'activité notifiée par le contrat. Il est responsable : • du respect des exigences qui lui sont notifiées dans la commande (RDG 2400), • de l'application des dispositions réglementaires qui régissent l'activité."
RUL_RDG2220.relates_to_object = [PRESTATAIRE]
RUL_RDG2220.relates_to_workpackage = [SPECIFICATION]
RUL_RDG2220.seeAlso = [RDG2400]

RUL_RDG2400 = Rule(name="RUL_RDG2400", label="RUL_RDG2400")
RUL_RDG2400.subpart_reference = RDG2400
RUL_RDG2400.states = "Les commandes passées par le Maître d'Ouvrage, le Maître d'Oeuvre, les Fabricants et les sous-traitants pour la conception et la construction de matériels suivant RCC-MRx se réfèrent au présent Code en le complétant si nécessaire dans les documents joints à la commande. Les règles contenues dans ce Code et dans les documents complémentaires joints à la commande sont traduites en exigences définies pour la qualité, la conception, l'approvisionnement, le soudage, les contrôles, la fabrication. La Spécification d'Equipement (RDG 3100) et son évolution dans le cadre d'une commande indique l'édition du présent Code, c'est-à-dire l'édition de base, les modificatifs et fiches de modification et règles en phase probatoires à laquelle le matériel doit être conforme. Il en est de même pour les propres commandes émises vers des prestataires. Le Prestataire doit être en mesure d'indiquer, pour chaque instruction ou procédure qu'il utilise dans le cadre de la commande, l'édition du présent Code, c'est-à-dire l'édition de base, les modificatifs et fiches de modification et règles en phase probatoires applicables lors de l'exécution des opérations concernées. La décision de réaliser un matériel suivant RCC-MRx implique que toutes les dispositions du présent Code qui lui sont applicables soient suivies."
RUL_RDG2400.relates_to_object = [Hardware]
RUL_RDG2400.relates_to_workpackage = [SPECIFICATION]
RUL_RDG2400.relates_to_document = [SPECIFICATION_EQUIPEMENT]
RUL_RDG2400.seeAlso = [RDG3100]

RUL_RDG2500 = Rule(name="RUL_RDG2500", label="RUL_RDG2500")
RUL_RDG2500.subpart_reference = RDG2500
RUL_RDG2500.states = "Deux cas sont à distinguer, selon que l'exigence, par rapport à laquelle la non-conformité est établie : 1. est particulière au Fabricant, mais n'existe ni dans les documents joints à la commande du matériel, ni dans le RCC-MRx (premier cas), 2. existe dans les documents techniques joints à la commande du matériel ou dans le RCC-MRx (deuxième cas). Dans le premier cas, le règlement de la non-conformité est du seul ressort du Fabricant. Il doit être consigné par écrit. Dans le deuxième cas, si le Fabricant est en mesure de mettre le matériel en conformité, le traitement de la non-conformité est effectué selon les mêmes règles que dans le premier cas. Si le Fabricant n'est pas en mesure de mettre le matériel en conformité, les dispositions du RDG 2510 ou du RDG 2520, sont applicables selon les cas."
RUL_RDG2500.relates_to_object = [Hardware]
RUL_RDG2500.relates_to_workpackage = [FABRICATION_WP]
RUL_RDG2500.relates_to_document = [FICHE_NON_CONFORMITE,FICHE_ANOMALIE]
RUL_RDG2500.seeAlso = [RDG2510,RDG2520]

RUL_RDG2510 = Rule(name="RUL_RDG2510", label="RUL_RDG2510")
RUL_RDG2510.subpart_reference = RDG2510
RUL_RDG2510.states = "Lorsqu'un matériel, est conforme au RCC-MRx, mais non conforme à l’une des exigences de la commande, et que le Fabricant n’est pas en mesure de le mettre en conformité, le traitement de la non-conformité sera effectué conformément aux documents joints à la commande."
RUL_RDG2510.relates_to_object = [Hardware]
RUL_RDG2510.relates_to_workpackage = [FABRICATION_WP]
RUL_RDG2510.relates_to_document = [FICHE_NON_CONFORMITE,FICHE_ANOMALIE]

RUL_RDG2520 = Rule(name="RUL_RDG2520", label="RUL_RDG2520")
RUL_RDG2520.subpart_reference = RDG2520
RUL_RDG2520.states = "La décision de réaliser un matériel suivant RCC-MRx implique que toutes les dispositions du présent Code qui lui sont applicables soient suivies. La conduite à tenir dans le cas d'une non-conformité au RCC-MRx sans possibilité de remise en conformité, ne relève pas du domaine du présent Code, mais du cadre contractuel qui désigne les organismes impliqués. Le traitement de la non-conformité sera effectué par écrit sur une Fiche d'Anomalie (RDG 3320)."
RUL_RDG2520.relates_to_object = [Hardware]
RUL_RDG2510.relates_to_workpackage = [FABRICATION_WP]
RUL_RDG2520.relates_to_document = [FICHE_NON_CONFORMITE,FICHE_ANOMALIE]
RUL_RDG2520.seeAlso = [RDG3320]

RUL_RDG3000 = Rule(name="RUL_RDG3000", label="RUL_RDG3000")
RUL_RDG3000.subpart_reference = RDG3000
RUL_RDG3000.states = "Les documents établis sont conservés en archives par le Maître d'Ouvrage ou l’Exploitant pendant une durée déterminée suivant les types de documents, afin de satisfaire aux exigences légales ou réglementaires et conserver les connaissances en vue d'améliorer la conception ou l'exploitation de l'installation."
RUL_RDG3000.relates_to_object = [Hardware]
RUL_RDG3000.relates_to_workpackage = [DOCUMENTATION]

RUL_RDG3100 = Rule(name="RUL_RDG3100", label="RUL_RDG3100")
RUL_RDG3100.subpart_reference = RDG3100
RUL_RDG3100.states = "La Spécification d'Equipement précise notamment : - l'objet, - l'étendue et les limites de la fourniture, - les documents de référence et notamment le présent Code, en précisant si nécessaire leurs conditions d'application."
RUL_RDG3100.relates_to_object = [Hardware]
RUL_RDG3100.relates_to_workpackage = [DOCUMENTATION]
RUL_RDG3100.relates_to_document = [SPECIFICATION_EQUIPEMENT]

RUL_RDG3210 = Rule(name="RUL_RDG3210", label="RUL_RDG3210")
RUL_RDG3210.subpart_reference = RDG3210
RUL_RDG3210.states = "Les documents d'ensemble et de repérage qui peuvent être constitués par des plans, croquis, dessins, schémas ou notices, décrivent un matériel ou l'un de ses principaux éléments constitutifs et, éventuellement, son implantation. Ils peuvent soit se suffire à eux-mêmes dans certains cas simples, soit annoncer des documents de détail et en assurer la liaison. Ils précisent : - le repérage des pièces constitutives qui doit être celui qui est utilisé dans la nomenclature, - les cotes principales avec leurs tolérances, - certaines caractéristiques (jeux fonctionnels, ...)."
RUL_RDG3210.relates_to_object = [Hardware]
RUL_RDG3210.relates_to_workpackage = [DOCUMENTATION]
RUL_RDG3210.relates_to_document = [DOCUMENTS_ENSEMBLE_REPERAGE]

RUL_RDG3220 = Rule(name="RUL_RDG3220", label="RUL_RDG3220")
RUL_RDG3220.subpart_reference = RDG3220
RUL_RDG3220.states = "Elle indique pour chaque pièce constitutive : - sa désignation, - son repère dans les documents d'ensemble et de repérage, - ses caractéristiques ou les références du document qui les définit."
RUL_RDG3220.relates_to_object = [Hardware]
RUL_RDG3220.relates_to_workpackage = [DOCUMENTATION]
RUL_RDG3220.relates_to_document = [NOMENCLATURE]

RUL_RDG3310 = Rule(name="RUL_RDG3310", label="RUL_RDG3310")
RUL_RDG3310.subpart_reference = RDG3310
RUL_RDG3310.states = "La fiche de non-conformité doit comporter au minimum : - l'identification du matériel et du document par rapport auquel existe la non-conformité,- la description de la non-conformité et la comparaison aux critères spécifiés,- la solution retenue par le Prestataire,- les actions correctives envisagées pour éviter qu’elle ne se reproduise. La conduite à tenir en cas de non-conformité est précisée en RDG 2500."
RUL_RDG3310.relates_to_object = [Hardware, Material]
RUL_RDG3310.relates_to_workpackage = [DOCUMENTATION]
RUL_RDG3310.relates_to_document = [FICHE_NON_CONFORMITE]
RUL_RDG3310.seeAlso = [RDG2500]

RUL_RDG3320 = Rule(name="RUL_RDG3320", label="RUL_RDG3320")
RUL_RDG3320.subpart_reference = RDG3320
RUL_RDG3320.states = "En plus des informations données par la fiche de non-conformité correspondante, la fiche d'anomalie traitée comporte au minimum la solution retenue par l'émetteur de la commande au Fabricant."
RUL_RDG3320.relates_to_object = [Hardware, Material]
RUL_RDG3320.relates_to_workpackage = [DOCUMENTATION]
RUL_RDG3320.relates_to_document = [FICHE_ANOMALIE]

RUL_RDG3411 = Rule(name="RUL_RDG3411", label="RUL_RDG3411")
RUL_RDG3411.subpart_reference = RDG3411
RUL_RDG3411.states = "Pour toutes les activités de conception, de fabrication, de montage et d’essais, la démonstration doit pouvoir être apportée que la qualité recherchée a été définie de façon appropriée, que ces activités ont été accomplies de façon satisfaisante et que la qualité recherchée a été obtenue. Le document de suivi évolue suivant trois états successifs : • un état 'initial' : le document de suivi à l'état initial définit la liste prévisionnelle des opérations de conception, d'approvisionnement, de fabrication, de contrôle et d'essais relative au matériel par ordre logique. • une phase « réalisation » : le document de suivi est complété par le Fabricant, au fur et à mesure de l'exécution des opérations mentionnées.• un état 'final' : le document de suivi complètement renseigné constitue l'état final et fait partie du Rapport de Fin de Conception et de Fabrication (RDG 3430). En fonction de l’organisation industrielle choisie, ce document de suivi peut être constitué de plusieurs parties établies soit par le Fabricant soit par les sous-traitants. Le document de suivi peut être établi sur tout type de support au choix de l’industriel. Le document de suivi peut revêtir des formes différentes ou désignations différentes, selon les états, à condition que l'on puisse facilement faire la relation entre les opérations décrites dans les documents utilisés pour chaque phase. Le document de suivi peut, en outre, être établi soit pour l'ensemble du matériel et de ses éléments constitutifs, soit par élément, soit par phase de réalisation. En outre, des documents de suivi regroupant des opérations ou des phases de réalisation, peuvent être établis. Ces documents de suivi doivent alors être référencés dans le document de suivi de l'ensemble, à la phase concernée. Dans ces deux derniers cas, les documents de suivi relatifs à l'ensemble du matériel doivent être accompagnés d'un sommaire qui en donne la liste. L'état initial de chaque document de suivi ou de chaque groupe de documents de suivi doit être accompagné de la liste de ces documents de suivi et de ceux qui restent à établir."
RUL_RDG3411.relates_to_object = [Hardware, Material]
RUL_RDG3411.relates_to_workpackage = [DOCUMENTATION]
RUL_RDG3411.relates_to_document = [DOCUMENT_SUIVI]
RUL_RDG3411.seeAlso = [RDG3430]

RUL_RDG3412 = Rule(name="RUL_RDG3412", label="RUL_RDG3412")
RUL_RDG3412.subpart_reference = RDG3412
RUL_RDG3412.states = "Les documents de suivi doivent mentionner au minimum : 1. La référence de la Spécification d'Equipement ou, le cas échéant, de la pièce technique de la commande. 2. La désignation des éléments constitutifs, sous-ensembles ou ensembles concernés. Les joints soudés et les revêtements sont assimilés à des constituants. En règle générale, pour les éléments constitutifs couverts par le présent Code mais pour lesquels aucune prescription relative à leur fabrication n’a été définie dans ce Code ou dans la Spécification d'Equipement, le document de suivi ne mentionne que les opérations relatives à l’approvisionnement de ces éléments. 3. La liste des opérations dans l’ordre logique, effectuées en conception, approvisionnement, fabrication, montage, contrôles et essais. Les contrôles et essais mentionnés doivent être situés par rapport aux opérations de fabrication et comprennent au minimum les contrôles et essais requis par le présent Code et par la Spécification d'Equipement, notamment : a. les approvisionnements (pour un matériel, les types d’opérations à mentionner sont les opérations essentielles pour lesquelles le présent Code ou la commande requièrent une documentation, c’est-à-dire l’acceptation des approvisionnements nécessaires à la réalisation de ce matériel), b. les procédés spéciaux tels soudage, rechargement dur y compris les témoins de soudage, c. les traitements thermiques, 4. Pour chaque opération du paragraphe 3, le numéro du document technique que le Prestataire prévoit d'appliquer (plans, procédures, instructions internes, paragraphes du présent Code) sans indication de l'indice de révision. L’indice de révision peut ne figurer que dans la phase « réalisation » du document de suivi. 5. Pour chaque opération du paragraphe 3, les actions de surveillance que le Prestataire prévoit d'effectuer sur les opérations de fabrication ou les prestations des sous-traitants, et sur ses propres opérations de fabrication, si cela est nécessaire au vu de son organisation. En outre, pour chaque opération du paragraphe 3, un emplacement doit être prévu pour permettre d'indiquer à quelles opérations le Prestataire doit convoquer les Inspecteurs. Ces opérations constituent des 'points de notification' de deux types : - Un point de convocation. Ce point, noté 'C', concerne une opération pour laquelle l'Inspecteur demande à être convoqué, mais que le Prestataire peut exécuter dans les conditions prévues par la commande, si l'Inspecteur n'est pas présent. - Un point d'arrêt. Ce point, noté 'A', concerne une opération pour laquelle l’Inspecteur est convoqué et que le Prestataire ne peut pas exécuter ou engager sans accord de l’Inspecteur (sauf autorisation écrite notifiée par l'organisme qui l’a demandé). Si un inspecteur dont le Prestataire s'est assuré qu'il a été dûment informé, avec le préavis contractuel, ne se présente pas, le Prestataire peut passer outre au point d'arrêt, 48 heures après notification par écrit, à l'organisme auquel l'Inspecteur appartient. Pour chaque opération du paragraphe 3, un emplacement doit être prévu pour permettre d'indiquer les opérations pour lesquelles l’émission d’un rapport noté « R » est exigée."
RUL_RDG3412.relates_to_object = [Hardware, Material]
RUL_RDG3412.relates_to_workpackage = [DOCUMENTATION]
RUL_RDG3412.relates_to_document = [DOCUMENT_SUIVI]

RUL_RDG3413 = Rule(name="RUL_RDG3413", label="RUL_RDG3413")
RUL_RDG3413.subpart_reference = RDG3413
RUL_RDG3413.states = "Le Document de Suivi en phase de réalisation reprend les indications de l'état initial. Il est complété au fur et à mesure de la réalisation du matériel. Si en cours de fabrication, d’autres opérations que celles prévues à l’état initial s’avèrent nécessaires, le document de suivi est modifié, ou complété, par un autre document de suivi référencé dans le document. En regard de chaque opération citée, doivent apparaître : a. la procédure ou l'instruction utilisée avec son indice de révision ou la référence du paragraphe concerné du présent Code lorsque celui-ci se suffit à lui seul pour effectuer l'opération. b. le numéro du procès-verbal des contrôles et essais prévus dans le document de suivi et tous ceux effectués à titre interne ayant conduit soit à une non-conformité, soit à une réparation. Dans le cas des contrôles par ressuage, par magnétoscopie, par examen visuel, des contrôles des états de surface de décapage, de passivation et du contrôle dimensionnel s'avérant conformes, il n'est pas obligatoirement établi de rapport d'examen, sauf indication contraire dans la Spécification d’Equipement. Dans ce cas, le document de suivi fait alors apparaître les indications suivantes : - la date, le nom, la signature (papier ou informatique) du ou des contrôleurs, - l'indication de la conformité du résultat au paragraphe du présent Code ou à la procédure ou instruction mentionnée dans le DS. Dans le cas d'une réparation par soudure, le document de suivi est complété par un renvoi à un dossier de réparation. Ce dossier donnera, en plus de la cartographie lorsque requise, les mêmes informations pour ces réparations que celles qui sont fournies pour les opérations normales. c. la référence aux documents de traçabilité des opérations de soudage et aux procès-verbaux ou aux rapports d’essais des témoins de production. d. la référence de l'enregistrement du diagramme ou du relevé de traitement thermique. e. les numéros des fiches du traitement de non-conformité et, succinctement, la suite donnée telle que refus, acceptation en l'état, réparation avec renvoi au dossier correspondant."
RUL_RDG3413.relates_to_object = [Hardware, Material]
RUL_RDG3413.relates_to_workpackage = [DOCUMENTATION]
RUL_RDG3413.relates_to_document = [DOCUMENT_SUIVI]

RUL_RDG3414 = Rule(name="RUL_RDG3414", label="RUL_RDG3414")
RUL_RDG3414.subpart_reference = RDG3414
RUL_RDG3414.states = "Le Document de Suivi à l'état final comporte toutes les informations portées pendant la réalisation. Si le Document de Suivi à l’état final figurant au Rapport de Fin de Conception et de Fabrication (RFCF) se présente sous une autre forme que le Document de Suivi utilisé en atelier, le visa du Contrôleur pourra être remplacé par celui de la personne chargée d’établir le Document de Suivi à l’état final dans le cadre du Système de Gestion. Toutefois, la date effective du contrôle, le nom du Contrôleur, ainsi que l’indication de la conformité figurant sur le document de suivi, doivent être reportés sur l’état final du Document de Suivi inclus dans le Rapport de Fin de Conception et de Fabrication."
RUL_RDG3414.relates_to_object = [Hardware, Material]
RUL_RDG3414.relates_to_workpackage = [DOCUMENTATION]
RUL_RDG3414.relates_to_document = [DOCUMENT_SUIVI]

RUL_RDG3422 = Rule(name="RUL_RDG3422", label="RUL_RDG3422")
RUL_RDG3422.subpart_reference = RDG3422
RUL_RDG3422.states = "La déclaration de conformité doit être établie suivant les critères de la norme NF EN ISO/CEI 17050-1. Elle doit contenir les indications suffisantes pour permettre à l’utilisateur d’identifier le Prestataire qui établit la déclaration, le produit, les documents associés à la commande et le signataire de la déclaration. Elle comporte au minimum les informations suivantes : • le nom et l’adresse du Prestataire, • l'identification du matériel considéré (désignation, référence, type), • la référence des prescriptions techniques contractuelles et, dans le cas où ces prescriptions n’ont pas été respectées, la liste des dérogations, • dans le cas de matériels qualifiés, la déclaration de conformité comporte la référence du Dossier de Référence avec l’indice en vigueur. La déclaration de conformité doit être datée et signée par le représentant mandaté du titulaire de la commande."
RUL_RDG3422.relates_to_object = [Hardware, Material]
RUL_RDG3422.relates_to_workpackage = [DOCUMENTATION]
RUL_RDG3422.relates_to_document = [DECLARATION_CONFORMITE]
RUL_RDG3422.seeAlso = ["NF_EN_ISO/CEI 17050-1"]

RUL_RDG3432 = Rule(name="RUL_RDG3432", label="RUL_RDG3432")
RUL_RDG3432.subpart_reference = RDG3432
RUL_RDG3432.states = "Le Rapport de Fin de Conception et de Fabrication se compose au minimum : 1. de la (ou des) déclaration(s) de conformité (RDG 3420), 2. du (ou des) document(s) de suivi à l'état final (RDG 3414), 3. des documents ci-après mentionnés : a. les procès-verbaux des contrôles et des essais (RDG 3413.b), b. la référence aux documents de traçabilité des opérations de soudage et aux procès-verbaux ou aux rapports d’essais des témoins de production (RDG 3413.c), c. les enregistrements ou relevés de traitement thermique (RDG 3413.d), d. les fiches de non-conformité et les fiches d'anomalie (RDG 3300), e. Les documents relatifs aux approvisionnements (RDG 3412.3) y compris le procès-verbal, 4. du cahier de soudage ou des descriptifs de mode opératoire de soudage utilisés, 5. des éléments des procédures ou instructions de contrôle et d'essais permettant de définir les conditions de contrôle ou d'essai si les procès-verbaux ne suffisent pas à eux seuls, 6. des procédures ou instructions de fabrication dont l'introduction dans le rapport de fin de fabrication est requise par la Spécification d'Equipement, 7. des plans de réalisation « conformes à l’exécution ». Le Rapport de Fin de Conception et de Fabrication est constitué au fur et à mesure de la réalisation du matériel concerné. Il peut cependant être commun à plusieurs matériels. Les documents relatifs aux approvisionnements, les cahiers de soudage, les dossiers de qualification des produits d'apport, les procédures et instructions visées en RDG 3432.5 et 6 peuvent faire l'objet de sous-dossiers communs à plusieurs matériels. L’indication de la conformité aux exigences définies à la commande (RDG 2400), doit apparaître dans le Rapport de Fin de Conception et de Fabrication."
RUL_RDG3432.relates_to_object = [Hardware, Material]
RUL_RDG3432.relates_to_workpackage = [DOCUMENTATION]
RUL_RDG3432.seeAlso = [RDG3420,RDG3414,RDG3413,RDG3300,RDG3412,RDG3432,RDG3432,RDG2400]
RUL_RDG3432.relates_to_document = [RAPPORT_FIN_CONCEPTION_FABRICATION]

RUL_RDG4000= Rule(name="RUL_RDG4000", label="RUL_RDG4000")
RUL_RDG4000.subpart_reference = RDG4000
RUL_RDG4000.includes_table = ["Table RDG4000"]
RUL_RDG4000.states = "Pour appliquer le présent Code, la liste des matériels ou partie de matériels et les supports soumis au RCC-MRx (RDG 2330) doit préciser les clés d'entrée dans le présent Code qui permettent de déterminer les règles applicables. Ces clés d'entrée sont les suivantes : • clé 1. Cette clé définit s'il s'agit : - d'un matériel du réacteur et de ses auxiliaires, - ou d'un matériel des mécanismes de contrôle ou de manutention, - ou d'un matériel des dispositifs d'irradiation. • clé 2. Cette clé donne le niveau RCC-MRx exigé : - Niveau N1Rx ou - Niveau N2Rx ou - Niveau N3Rx. Dans le cas d'un matériel classé Sûreté, les règles de correspondance entre 'Classes de Sûreté' et les 'niveaux RCC-MRx' qui doivent être appliquées sont définies en amont de l’application du présent Code. Le Fabricant applique à chaque matériel ainsi qu’à leurs supports le niveau exigé. Il peut toutefois, s'il a par exemple le souci d'harmoniser ses fabrications, leur conférer des niveaux supérieurs. Il informe le Maître d’Oeuvre de ce surclassement qui doit rester l'exception. Il leur applique alors l'ensemble des dispositions qui correspondent à ce niveau. Une soudure entre deux pièces soumises au présent Code est du niveau des pièces qu'elle assemble. Si les pièces ont un niveau différent, elle est du niveau le plus sévère. Une soudure entre deux pièces dont une seule est soumise au présent Code est du même niveau que cette pièce. Dans le cas où un support est commun à des matériels de niveau différent, il est du niveau le plus contraignant. • clé 3. Cette clé donne le type de composant auquel le matériel se rattache - coques-réservoirs-récipients-cuves, - pompes, - robinets-vannes, - tuyauteries, - soufflets, - structures caissonnées, - échangeurs. • clé 4. Cette clé précise, pour un matériel des dispositifs d’irradiation, un matériel de niveau 3 du réacteur ou de ses auxiliaires, s’il s'agit d’un « matériel sur catalogue » ou non. • clé 5. Cette clé indique si le matériel est soumis ou non à une règlementation (0 : non soumis, ESP/ESPN : soumis à la réglementation des équipements sous pression – décret ESP/arrêté ESPN, …). • clé 6. En fonction de la valeur des clés 2 et 3, cette clé définit l’Ensemble de Règles applicables parmi les Ensembles suivants (Tableau RDG 4000) : - Section III, - Section II REC 2200 dans le cadre de l’application de la norme NF EN 13445, - Section II REC 2300 dans le cadre de l’application de la norme NF EN 13480, - Section II REC 2400 dans le cadre de l’application de la norme NF EN 1993-1-1. Dans les limites de juridiction du matériel et de son support relevant d’un Ensemble de Règles applicable donné (par exemple NF EN 13445), la boulonnerie est également soumise, pour son approvisionnement et son dimensionnement, aux dispositions de ce même ensemble. Complété, en fonction de la valeur de la clé 5, par : - la Section II REC 3200 si le matériel est soumis à la réglementation des équipements sous pression – décret ESP/arrêté ESPN. Le choix de l’Ensemble de Règles applicables est précisé dans la Spécification d'Equipement"
RUL_RDG4000.relates_to_workpackage = [SPECIFICATION]
RUL_RDG4000.relates_to_document = [SPECIFICATION_EQUIPEMENT]
RUL_RDG4000.seeAlso = [RDG2330]
RUL_RDG4000.includes_table = ["Table RDG4000"]
# endregion
# region - Liaison du Contexte et des Règles
RCCMRX.includes_context = Context.instances()
RCCMRX.includes_rule = Rule.instances()
# endregion
# endregion
# region - Instanciation du système
acier_316L = Material(name = "Acier_316L", label="Acier 316L")

pompe_rcp = Equipment(name = "Pompe_RCP", label="Pompe RCP")
pompe_rcp.equipment_type = "Matériel du réacteur et de ses auxiliaires"
pompe_rcp.rccmrx_level = "N1Rx"
pompe_rcp.esp_espn = True
pompe_rcp.espn_level = "N1"
pompe_rcp.esp_category = "I"

rotor = Component(name = "Rotor_pompe_RCP", label="Rotor Pompe RCP")
rotor.component_type = "pompe"
rotor.rccmrx_level = "N1Rx"
rotor.esp_espn = False
rotor.espn_level = "NC"
rotor.esp_category = "Non-ESP"
rotor.made_of_material.append(acier_316L)

stator = Component(name = "Stator_pompe_RCP", label="Stator Pompe RCP")
stator.component_type = "pompe"
stator.rccmrx_level = "N1Rx"
stator.esp_espn = True
stator.espn_level = "N1"
stator.esp_category = "I"
stator.made_of_material.append(acier_316L)

garniture = Component(name = "Garniture_pompe_RCP", label="Garniture Pompe RCP")
garniture.component_type = "soufflet"
garniture.rccmrx_level = "NC"
garniture.esp_espn = True
garniture.espn_level = "N1"
garniture.esp_category = "I"

support_pompe_rcp = Support(name = "Support_pompe_RCP", label="Support Pompe RCP")
support_pompe_rcp.support_type = "linéaire"
support_pompe_rcp.is_integral_support = False
support_pompe_rcp.support_group_type = "groupe 1"
support_pompe_rcp.is_standard = False

rotor.componentOf.append(pompe_rcp)
stator.componentOf.append(pompe_rcp)
garniture.componentOf.append(pompe_rcp)
support_pompe_rcp.supportOf.append(pompe_rcp)
support_pompe_rcp.made_of_material.append(acier_316L)
# endregion

# Fermeture de l'ontologie
close_world(onto)

# Raisonnement
reasoning = get_ontology("http://www.isiatech.com/ontologies/reasoning.owl")
owlready2.JAVA_EXE = "C:\\Program Files (x86)\\Java\\jre1.8.0_451\\bin\\java.exe"

with reasoning:
    owlready2.reasoning.JAVA_MEMORY = 512
    sync_reasoner_pellet(infer_property_values = True, debug = 2)

reasoning.save(file = "ontology/reasoning.xml", format = "rdfxml")

# Sérialisation de l'ontologie
onto.save(file = "ontology/rccmrx_ontology.xml", format = "rdfxml")