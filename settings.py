CHILE_BOUNDING_BOX = [
    "-75.305615,-55.696134,-68.757684,-52.346932",
    "-75.530436,-52.364096,-72.411036,-50.703610",
    "-76.261107,-50.934418,-73.169809,-49.055888",
    "-76.148696,-49.550645,-71.680365,-39.814612",
    "-74.125301,-40.352148,-71.230722,-36.704065",
    "-73.507041,-36.973960,-69.628868,-32.637924",
    "-72.523447,-33.204080,-69.600765,-28.452409",
    "-71.539852,-28.477114,-69.207608,-23.579633",
    "-69.357915,-24.563140,-67.829796,-21.753553",
    "-71.011290,-23.671439,-69.057301,-18.294311",
    "-70.520535,-18.647303,-69.080728,-18.255537",
    "-69.777898,-18.241144,-69.482358,-17.538024",
]

LANGUAGES = ['es', 'en']

# Where On Earth ID for Chile
CL_WOEID = '23424782'

GAZETTEER_PATH = 'data/chile_gazetteer.tsv'

TRACK_KEYWORDS = []

BUFFER_SIZE = 10000

# cuantos minutos recolectar trending topics
MINUTES_TT = 15

# minutos para recolectar noticias
MINUTES_NEWS = 55

# cuantos sets de keywords buscar para las noticias
NUM_KEYWORDS = 20

MAINSTREAM_NEWS = [
    #'emol',
    '24HorasTVN',
    'lun',
    'biobio',
    't13',
    'meganoticiascl',
    'cooperativa',
    'elmostrador',
    'elmercurio_cl',
    'latercera',
    'chilevision',
    'el_ciudadano',
    'cnnchile',
    'lacuarta',
    'thecliniccl'
]

# top 100 comunas por poblacion
# la nº 100 tiene 42152 habitantes segun censo 2017
COMUNAS_100 = [
    "Puente Alto",
    "Maipú",
    "Santiago",
    "La Florida",
    "Antofagasta",
    "Viña del Mar",
    "San Bernardo",
    "Valparaíso",
    "Las Condes",
    "Temuco",
    "Puerto Montt",
    "Rancagua",
    "Peñalolén",
    "Pudahuel",
    "Coquimbo",
    "Concepción",
    "Arica",
    "La Serena",
    "Talca",
    "Quilicura",
    "Ñuñoa",
    # "Los Ángeles",
    "Iquique",
    "Chillán",
    "La Pintana",
    "Valdivia",
    "Calama",
    "El Bosque",
    "Osorno",
    "Recoleta",
    "Copiapó",
    "Talcahuano",
    "Quilpué",
    "Curicó",
    "Renca",
    "Estación Central",
    "Colina",
    "Providencia",
    "Cerro Navia",
    "San Pedro de la Paz",
    "Punta Arenas",
    "Conchalí",
    "Villa Alemana",
    "Melipilla",
    "La Granja",
    "Macul",
    "Coronel",
    "Ovalle",
    "Quinta Normal",
    "Alto Hospicio",
    "San Miguel",
    "Lo Barnechea",
    "Lampa",
    "Pedro Aguirre Cerda",
    "Independencia",
    "Lo Espejo",
    "Huechuraba",
    "Buin",
    "Lo Prado",
    "San Joaquín",
    "Linares",
    "La Reina",
    "Hualpén",
    # "San Antonio",
    "Quillota",
    "Peñaflor",
    "La Cisterna",
    "Chiguayante",
    "Vitacura",
    "San Ramón",
    "Cerrillos",
    "San Felipe",
    "Padre Las Casas",
    "Talagante",
    "San Fernando",
    "Paine",
    "Los Andes",
    "Padre Hurtado",
    "Rengo",
    "Coyhaique",
    "Villarrica",
    "Tomé",
    "Angol",
    "San Carlos",
    "Machali",
    "Vallenar",
    "La Calera",
    "Maule",
    "Penco",
    "San Vicente",
    "Limache",
    "Constitución",
    "Molina",
    "San Javier",
    "Puerto Varas",
    "Castro",
    "Lota",
    "San Clemente",
    "Concón",
]


# este BB es muy amplio y captura partes de argentina y de bolivia
# lat, lon
# -55.902393, -77.752535  (SW)
# -16.935069, -67.381581  (NE)
# CHILE_BOUNDING_BOX = ["-77.752535,-55.902393", "-67.381581,-16.935069"]


# lon, lat (mas detallados)
# -55.696134, -75.305615, -52.346932, -68.757684
# -52.364096, -75.530436, -50.703610, -72.411036
# -50.934418, -76.261107, -49.055888, -73.169809
# -49.550645, -76.148696, -39.814612, -71.680365
# -40.352148, -74.125301, -36.704065, -71.230722
# -36.973960, -73.507041, -32.637924, -69.628868
# -33.204080, -72.523447, -28.452409, -69.600765
# -28.477114, -71.539852, -23.579633, -69.207608
# -24.563140, -69.357915, -21.753553, -67.829796
# -23.671439, -71.011290, -18.294311, -69.057301
# -18.647303, -70.520535, -18.255537, -69.080728
# -18.241144, -69.777898, -17.538024, -69.482358
# lat, lon (mismo anterior) (SW, NE)
# -75.305615, -55.696134, -68.757684, -52.346932, 
# -75.530436, -52.364096, -72.411036, -50.703610, 
# -76.261107, -50.934418, -73.169809, -49.055888, 
# -76.148696, -49.550645, -71.680365, -39.814612, 
# -74.125301, -40.352148, -71.230722, -36.704065, 
# -73.507041, -36.973960, -69.628868, -32.637924, 
# -72.523447, -33.204080, -69.600765, -28.452409, 
# -71.539852, -28.477114, -69.207608, -23.579633, 
# -69.357915, -24.563140, -67.829796, -21.753553, 
# -71.011290, -23.671439, -69.057301, -18.294311, 
# -70.520535, -18.647303, -69.080728, -18.255537, 
# -69.777898, -18.241144, -69.482358, -17.538024, 