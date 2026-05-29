from dataclasses import dataclass

from src.settings import SCREEN_HEIGHT


@dataclass(frozen=True)
class FragmentData:
    area: tuple[int, int, int, int]
    info: str


@dataclass(frozen=True)
class LevelData:
    title: str
    year: str
    mission: str
    historical_note: str
    intro_text: str
    theme: str
    width: int
    start_position: tuple[int, int]
    platforms: list[tuple[int, int, int, int]]
    goal: tuple[int, int, int, int]
    fragments: list[FragmentData]
    hazards: list[tuple[int, int, int, int]]
    checkpoints: list[tuple[int, int, int, int]]


GROUND_HEIGHT = 64
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT
START_POSITION = (70, GROUND_Y - 56)


def _course_platforms(width: int, variant: int) -> list[tuple[int, int, int, int]]:
    platforms = [(0, GROUND_Y, width, GROUND_HEIGHT)]
    heights = [410, 356, 306, 258, 382, 328, 282, 370]
    widths = [150, 145, 150, 135, 170, 155, 155, 165]
    x = 190 + (variant % 3) * 24
    step = 220 + (variant % 2) * 18
    index = 0

    while x < width - 250:
        y = heights[index % len(heights)]
        platform_width = widths[(index + variant) % len(widths)]
        platforms.append((x, y, platform_width, 28))
        x += step
        index += 1

    return platforms


def _fragments_from_platforms(
    platforms: list[tuple[int, int, int, int]],
    infos: list[str],
) -> list[FragmentData]:
    fragments = []
    usable_platforms = platforms[1:]

    for index, info in enumerate(infos):
        platform = usable_platforms[min(index, len(usable_platforms) - 1)]
        x, y, width, _ = platform
        fragments.append(FragmentData((x + width // 2 - 12, y - 40, 24, 24), info))

    return fragments


def _hazards(width: int, variant: int) -> list[tuple[int, int, int, int]]:
    hazard_y = GROUND_Y - 18
    first = 720 + (variant % 3) * 70
    second = max(first + 430, width // 2 + 180)
    third = width - 420
    return [
        (first, hazard_y, 92, 18),
        (second, hazard_y, 108, 18),
        (third, hazard_y, 96, 18),
    ]


def _checkpoints(width: int, hazards: list[tuple[int, int, int, int]]) -> list[tuple[int, int, int, int]]:
    checkpoint_y = GROUND_Y - 70
    safe_positions = []

    for hazard in hazards[:2]:
        hazard_x, _, hazard_width, _ = hazard
        safe_x = hazard_x + hazard_width + 86
        safe_x = min(safe_x, width - 300)
        safe_x = _move_checkpoint_to_safe_x(safe_x, width, hazards)
        safe_positions.append(safe_x)

    checkpoints = []
    for safe_x in safe_positions:
        if checkpoints and safe_x - checkpoints[-1][0] < 260:
            safe_x = checkpoints[-1][0] + 260
        safe_x = min(safe_x, width - 300)
        safe_x = _move_checkpoint_to_safe_x(safe_x, width, hazards)
        checkpoints.append((safe_x, checkpoint_y, 34, 70))

    return checkpoints


def _move_checkpoint_to_safe_x(
    checkpoint_x: int,
    width: int,
    hazards: list[tuple[int, int, int, int]],
) -> int:
    min_x = 180
    max_x = width - 300
    desired_x = max(min_x, min(checkpoint_x, max_x))

    if _is_checkpoint_x_safe(desired_x, hazards):
        return desired_x

    right_x = desired_x
    while right_x <= max_x:
        if _is_checkpoint_x_safe(right_x, hazards):
            break
        right_x += 8

    left_x = desired_x
    while left_x >= min_x:
        if _is_checkpoint_x_safe(left_x, hazards):
            break
        left_x -= 8

    right_distance = abs(right_x - desired_x) if right_x <= max_x else 99999
    left_distance = abs(left_x - desired_x) if left_x >= min_x else 99999
    if left_distance < right_distance:
        return left_x
    if right_x <= max_x:
        return right_x
    return max(min_x, left_x)


def _is_checkpoint_x_safe(
    checkpoint_x: int,
    hazards: list[tuple[int, int, int, int]],
) -> bool:
    checkpoint_width = 34
    margin = 54

    for hazard_x, _, hazard_width, _ in hazards:
        forbidden_left = hazard_x - margin
        forbidden_right = hazard_x + hazard_width + margin
        if checkpoint_x < forbidden_right and checkpoint_x + checkpoint_width > forbidden_left:
            return False

    return True


def _make_level(
    title: str,
    year: str,
    mission: str,
    historical_note: str,
    intro_text: str,
    theme: str,
    width: int,
    variant: int,
    fragment_infos: list[str],
) -> LevelData:
    platforms = _course_platforms(width, variant)
    hazards = _hazards(width, variant)
    return LevelData(
        title=title,
        year=year,
        mission=mission,
        historical_note=historical_note,
        intro_text=intro_text,
        theme=theme,
        width=width,
        start_position=START_POSITION,
        platforms=platforms,
        goal=(width - 118, GROUND_Y - 60, 42, 60),
        fragments=_fragments_from_platforms(platforms, fragment_infos),
        hazards=hazards,
        checkpoints=_checkpoints(width, hazards),
    )


LEVELS = [
    _make_level(
        title="Chegada dos portugueses",
        year="1500",
        mission="Colete os fragmentos e alcance o marco verde no litoral.",
        historical_note=(
            "Em 1500, a expedicao portuguesa chegou ao litoral que depois seria "
            "chamado Brasil."
        ),
        intro_text=(
            "Mig chega a um litoral movimentado. Ele vai observar a paisagem, "
            "lembrando que muitos povos indigenas ja viviam aqui."
        ),
        theme="coast",
        width=1700,
        variant=0,
        fragment_infos=[
            "A chegada portuguesa fez parte das grandes navegacoes europeias.",
            "O litoral ja era habitado por diversos povos indigenas.",
            "O nome Brasil se relaciona ao pau-brasil, arvore de madeira valiosa.",
        ],
    ),
    _make_level(
        title="Ciclo do acucar",
        year="Seculo XVI",
        mission="Atravesse os engenhos e encontre o ponto de observacao.",
        historical_note=(
            "No periodo colonial, a producao de acucar se tornou uma atividade "
            "economica muito importante."
        ),
        intro_text=(
            "Mig visita uma regiao de engenhos. A fase mostra trabalho, plantio "
            "e comercio, sempre com cuidado ao falar das pessoas envolvidas."
        ),
        theme="sugar",
        width=1850,
        variant=1,
        fragment_infos=[
            "Os engenhos reuniam plantacao, moagem da cana e producao do acucar.",
            "A economia colonial dependia muito da exportacao para a Europa.",
            "A producao de acucar marcou fortemente o Nordeste colonial.",
            "Muitas pessoas foram obrigadas a trabalhar nos engenhos, um tema para estudar com respeito.",
        ],
    ),
    _make_level(
        title="Interiorizacao do territorio",
        year="Seculos XVII e XVIII",
        mission="Siga pelas trilhas e complete o mapa do interior.",
        historical_note=(
            "As expedicoes pelo interior ampliaram caminhos e mapas, mas tambem "
            "trouxeram desafios para muitos povos."
        ),
        intro_text=(
            "Mig entra por trilhas, rios e morros. Ele aprende que o interior ja "
            "tinha muitos saberes e caminhos antes dos novos mapas."
        ),
        theme="interior",
        width=2000,
        variant=2,
        fragment_infos=[
            "Muitos caminhos pelo interior ajudaram a criar novos mapas.",
            "Diferentes povos ja conheciam rios, florestas e trilhas antigas.",
            "A ocupacao do interior mudou vilas, rotas e formas de viver.",
            "Estudar esse periodo pede respeito pelas comunidades indigenas.",
        ],
    ),
    _make_level(
        title="Ciclo do ouro",
        year="Seculo XVIII",
        mission="Explore as montanhas e encontre o marco das minas.",
        historical_note=(
            "O ouro mudou a vida de muitas vilas e atraiu pessoas para a regiao "
            "das minas."
        ),
        intro_text=(
            "Mig chega a montanhas e caminhos de pedra. Ele observa como a busca "
            "por ouro transformou vilas, trabalho e comercio."
        ),
        theme="mines",
        width=2050,
        variant=3,
        fragment_infos=[
            "A descoberta de ouro fez crescer vilas em regioes montanhosas.",
            "Muitas rotas foram abertas para transportar pessoas e mercadorias.",
            "O trabalho nas minas foi dificil e envolveu muitas pessoas escravizadas.",
            "Cidades como Ouro Preto guardam marcas desse periodo.",
        ],
    ),
    _make_level(
        title="Inconfidencia Mineira",
        year="1789",
        mission="Junte ideias e alcance a praca colonial.",
        historical_note=(
            "A Inconfidencia Mineira reuniu ideias de mudanca em Minas Gerais no "
            "fim do seculo XVIII."
        ),
        intro_text=(
            "Mig visita uma cidade colonial. Ele encontra conversas sobre impostos, "
            "liberdade e planos de mudanca."
        ),
        theme="colonial_city",
        width=1900,
        variant=4,
        fragment_infos=[
            "Alguns moradores de Minas queriam menos controle da Coroa portuguesa.",
            "As ideias de liberdade circulavam em livros, encontros e conversas.",
            "Tiradentes ficou conhecido como um dos participantes do movimento.",
            "Esse tema deve ser estudado lembrando que havia muitos interesses diferentes.",
        ],
    ),
    _make_level(
        title="Vinda da familia real",
        year="1808",
        mission="Atravesse a cidade e chegue ao palacio.",
        historical_note=(
            "Em 1808, a chegada da familia real portuguesa trouxe mudancas para "
            "o Rio de Janeiro e para o Brasil."
        ),
        intro_text=(
            "Mig chega a uma cidade mais movimentada. Ele ve novas instituicoes, "
            "livros, portos e ideias circulando."
        ),
        theme="court",
        width=1950,
        variant=5,
        fragment_infos=[
            "A corte portuguesa veio para o Brasil em 1808.",
            "Portos foram abertos para comercio com outras partes do mundo.",
            "Bibliotecas, escolas e servicos urbanos ganharam mais destaque.",
            "As mudancas beneficiaram alguns grupos mais do que outros.",
        ],
    ),
    _make_level(
        title="Independencia",
        year="1822",
        mission="Colete simbolos de mudanca e encontre o marco da independencia.",
        historical_note=(
            "A independencia iniciou uma nova organizacao politica, mas muitos "
            "desafios sociais continuaram."
        ),
        intro_text=(
            "Mig observa um momento de mudanca politica. Ele aprende que a "
            "independencia foi um processo, nao apenas um dia."
        ),
        theme="independence",
        width=2000,
        variant=6,
        fragment_infos=[
            "A independencia do Brasil foi declarada em 1822.",
            "O processo envolveu disputas politicas e interesses diferentes.",
            "Muitas pessoas comuns sentiram as mudancas de formas variadas.",
            "Mesmo independente, o Brasil ainda manteve grandes desigualdades.",
        ],
    ),
    _make_level(
        title="Imperio",
        year="1822 a 1889",
        mission="Passe pelos jardins imperiais e encontre o ponto final.",
        historical_note=(
            "Durante o Imperio, o Brasil teve monarquia, crescimento urbano e "
            "debates sobre cidadania."
        ),
        intro_text=(
            "Mig visita o Brasil imperial. Entre jardins e cidades, ele percebe "
            "que politica, cultura e sociedade estavam mudando."
        ),
        theme="empire",
        width=2050,
        variant=7,
        fragment_infos=[
            "O Brasil imperial foi governado por imperadores.",
            "Ferrovias, cidades e lavouras cresceram em algumas regioes.",
            "A sociedade discutia quem podia participar da vida politica.",
            "A escravidao continuou por boa parte do periodo imperial.",
        ],
    ),
    _make_level(
        title="Abolicao da escravidao",
        year="1888",
        mission="Reuna memorias de liberdade e chegue ao jardim de encontro.",
        historical_note=(
            "A abolicao em 1888 foi uma conquista importante, ligada a muitas "
            "lutas por liberdade e dignidade."
        ),
        intro_text=(
            "Mig chega a uma fase sensivel e importante. Ele aprende sobre "
            "liberdade, respeito e a luta de muitas pessoas."
        ),
        theme="empire",
        width=1900,
        variant=8,
        fragment_infos=[
            "A Lei Aurea acabou oficialmente com a escravidao no Brasil em 1888.",
            "Pessoas escravizadas resistiram e buscaram liberdade de muitas formas.",
            "Abolicionistas tambem participaram de debates e campanhas.",
            "Depois da abolicao, muitos desafios de igualdade continuaram.",
        ],
    ),
    _make_level(
        title="Proclamacao da Republica",
        year="1889",
        mission="Atravesse a praca e encontre o marco republicano.",
        historical_note=(
            "Em 1889, o Brasil deixou de ser monarquia e passou a ser republica."
        ),
        intro_text=(
            "Mig chega a uma praca de mudancas politicas. Ele observa que uma "
            "nova forma de governo estava comecando."
        ),
        theme="republic",
        width=1850,
        variant=9,
        fragment_infos=[
            "A Republica foi proclamada em 1889.",
            "O Brasil passou a ter presidentes em vez de imperadores.",
            "Nem toda a populacao podia participar das decisoes politicas.",
            "Mudancas de governo tambem trazem perguntas sobre cidadania.",
        ],
    ),
    _make_level(
        title="Primeira Republica",
        year="1889 a 1930",
        mission="Siga pelos trilhos e chegue ao coreto da cidade.",
        historical_note=(
            "A Primeira Republica teve crescimento de cidades, lavouras, ferrovias "
            "e muitos debates sobre participacao politica."
        ),
        intro_text=(
            "Mig caminha por trilhos, fazendas e cidades. Ele percebe que o pais "
            "crescia, mas a participacao politica ainda era limitada."
        ),
        theme="rural_republic",
        width=2100,
        variant=10,
        fragment_infos=[
            "A producao de cafe teve grande importancia nesse periodo.",
            "Ferrovias ajudaram a ligar fazendas, portos e cidades.",
            "Muitas pessoas viviam no campo e buscavam melhores condicoes.",
            "O voto era restrito e nem todos tinham voz nas decisoes.",
        ],
    ),
    _make_level(
        title="Era Vargas",
        year="1930 a 1945",
        mission="Passe pela cidade industrial e encontre a estacao.",
        historical_note=(
            "A Era Vargas trouxe industrializacao, leis trabalhistas e tambem "
            "controle politico."
        ),
        intro_text=(
            "Mig visita fabricas e avenidas. Ele aprende que trabalho, industria "
            "e governo ganharam novos formatos."
        ),
        theme="vargas",
        width=2050,
        variant=11,
        fragment_infos=[
            "A industria cresceu em varias cidades brasileiras.",
            "Leis trabalhistas passaram a organizar direitos de muitos trabalhadores.",
            "O radio ajudou noticias e musicas a circularem pelo pais.",
            "Tambem houve momentos de controle politico que devem ser estudados com cuidado.",
        ],
    ),
    _make_level(
        title="Experiencia democratica",
        year="1946 a 1964",
        mission="Colete ideias de participacao e alcance a praca civica.",
        historical_note=(
            "Entre 1946 e 1964, o Brasil viveu eleicoes, projetos de desenvolvimento "
            "e debates publicos intensos."
        ),
        intro_text=(
            "Mig chega a uma fase de campanhas, construcao e conversas. A "
            "democracia aparece como participacao e responsabilidade."
        ),
        theme="democracy",
        width=2000,
        variant=12,
        fragment_infos=[
            "O periodo teve eleicoes e maior participacao politica.",
            "Brasilia foi inaugurada em 1960 como nova capital do Brasil.",
            "O pais discutia desenvolvimento, direitos e caminhos para o futuro.",
            "Democracia precisa de dialogo, regras e respeito as pessoas.",
        ],
    ),
    _make_level(
        title="Ditadura militar",
        year="1964 a 1985",
        mission="Atravesse com cuidado e encontre o ponto de memoria.",
        historical_note=(
            "A ditadura militar foi um periodo de pouca liberdade politica e deve "
            "ser estudada com cuidado e respeito."
        ),
        intro_text=(
            "Mig chega a um periodo delicado da historia. A fase usa simbolos de "
            "memoria e cuidado para falar de liberdade e direitos."
        ),
        theme="dictatorship",
        width=1950,
        variant=13,
        fragment_infos=[
            "Entre 1964 e 1985, o Brasil viveu um governo militar.",
            "A participacao politica e a liberdade de expressao foram limitadas.",
            "Muitas pessoas defenderam democracia e direitos nesse periodo.",
            "E um tema que deve ser estudado com cuidado, respeito e memoria.",
        ],
    ),
    _make_level(
        title="Redemocratizacao",
        year="1985 a 1988",
        mission="Junte vozes de participacao e encontre a Constituicao.",
        historical_note=(
            "A redemocratizacao marcou a volta de eleicoes mais amplas e a "
            "Constituicao de 1988."
        ),
        intro_text=(
            "Mig encontra praca cheia de cartazes, debates e esperanca. Ele aprende "
            "que direitos sao construidos com participacao."
        ),
        theme="redemocratization",
        width=1950,
        variant=14,
        fragment_infos=[
            "A redemocratizacao marcou a volta gradual da democracia.",
            "Movimentos sociais pediram participacao e direitos.",
            "A Constituicao de 1988 ficou conhecida como Constituicao Cidada.",
            "Cuidar da democracia e uma tarefa de toda a sociedade.",
        ],
    ),
    _make_level(
        title="Brasil contemporaneo",
        year="1988 ate hoje",
        mission="Complete a jornada e chegue ao portal do presente.",
        historical_note=(
            "O Brasil contemporaneo continua em construcao, com diversidade, "
            "desafios e muitas possibilidades."
        ),
        intro_text=(
            "Mig chega ao tempo mais proximo dele. A historia continua, e cada "
            "pessoa ajuda a construir novos caminhos."
        ),
        theme="contemporary",
        width=2200,
        variant=15,
        fragment_infos=[
            "O Brasil atual e diverso em culturas, regioes, sotaques e modos de viver.",
            "Tecnologia, educacao e meio ambiente fazem parte dos desafios atuais.",
            "Direitos e cidadania continuam sendo temas importantes.",
            "A historia do Brasil segue sendo estudada, contada e vivida.",
        ],
    ),
]
