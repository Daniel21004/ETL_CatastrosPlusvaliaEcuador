import seaborn as sns

COLOR_NAMES = [
    "#08519C",  # azul oscuro
    "#006D2C",  # verde oscuro
    "#A50F15",  # rojo oscuro
    "#7B2D8B",  # morado
    "#D94801",  # naranja oscuro
    "#525252",  # gris oscuro
    "#8C6D31",  # marrón
    "#1D6B56",  # verde azulado
    "#6B2D3E",  # vino
    "#084594",  # azul marino
    "#3D6B21",  # verde oliva
    "#7F2704",  # rojo ladrillo
]


def generate_color_palete(i, num):
    # dark_palette va del color oscuro hacia el base, dando colores visibles
    colors = sns.dark_palette(COLOR_NAMES[i % len(COLOR_NAMES)], num, reverse=True)
    return [[int(r * 255), int(g * 255), int(b * 255), 220] for r, g, b in colors]
