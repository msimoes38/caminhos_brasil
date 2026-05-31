from dataclasses import dataclass

from src.settings import SCREEN_HEIGHT


@dataclass(frozen=True)
class QuizData:
    question: str
    options: tuple[str, str, str]
    correct_index: int
    hint: str


@dataclass(frozen=True)
class KnowledgePill:
    info: str
    question: str
    options: tuple[str, str, str]
    correct_index: int
    hint: str


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
    pill_bank: list[KnowledgePill]
    hazards: list[tuple[int, int, int, int]]
    checkpoints: list[tuple[int, int, int, int]]


GROUND_HEIGHT = 64
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT
START_POSITION = (70, GROUND_Y - 56)
LEVEL_WIDTH_SCALE = 1.3
PILLS_PER_LEVEL = 10


def _pill(
    info: str,
    question: str,
    correct_answer: str,
    wrong_answer_one: str,
    wrong_answer_two: str,
    hint: str,
) -> KnowledgePill:
    return KnowledgePill(
        info=info,
        question=question,
        options=(correct_answer, wrong_answer_one, wrong_answer_two),
        correct_index=0,
        hint=hint,
    )


def _course_platforms(width: int, variant: int) -> list[tuple[int, int, int, int]]:
    platforms = [(0, GROUND_Y, width, GROUND_HEIGHT)]
    heights = [410, 356, 306, 258, 382, 328, 282, 370]
    widths = [150, 145, 150, 135, 170, 155, 155, 165]
    x = 190 + (variant % 3) * 24
    step = 220 + (variant % 2) * 18
    index = 0

    while x < width - 420:
        y = heights[index % len(heights)]
        platform_width = widths[(index + variant) % len(widths)]
        platforms.append((x, y, platform_width, 28))
        x += step
        index += 1

    return platforms


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

    for hazard in hazards:
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
    pill_bank: list[KnowledgePill],
) -> LevelData:
    if len(pill_bank) != PILLS_PER_LEVEL:
        raise ValueError(f"{title} precisa ter exatamente {PILLS_PER_LEVEL} pílulas.")

    expanded_width = int(width * LEVEL_WIDTH_SCALE)
    platforms = _course_platforms(expanded_width, variant)
    hazards = _hazards(expanded_width, variant)
    return LevelData(
        title=title,
        year=year,
        mission=mission,
        historical_note=historical_note,
        intro_text=intro_text,
        theme=theme,
        width=expanded_width,
        start_position=START_POSITION,
        platforms=platforms,
        goal=(expanded_width - 118, GROUND_Y - 60, 42, 60),
        pill_bank=pill_bank,
        hazards=hazards,
        checkpoints=_checkpoints(expanded_width, hazards),
    )


LEVELS = [
    _make_level(
        title="Chegada dos portugueses",
        year="1500",
        mission="Colete as pílulas e alcance o marco verde no litoral.",
        historical_note=(
            "Em 1500, a expedição portuguesa com Pedro Álvares Cabral chegou ao litoral que depois seria "
            "chamado Brasil."
        ),
        intro_text=(
            "Mig chega a um litoral movimentado. Ele vai observar a paisagem, "
            "lembrando que muitos povos indígenas já viviam aqui."
        ),
        theme="coast",
        width=1700,
        variant=0,
        pill_bank=[
            _pill(
                "A chegada portuguesa fez parte das grandes navegações europeias.",
                "A chegada portuguesa fazia parte de qual movimento?",
                "Das grandes navegações europeias.",
                "Da corrida espacial.",
                "Da construção de Brasília.",
                "Pense nas viagens marítimas feitas por europeus.",
            ),
            _pill(
                "O litoral já era habitado por diversos povos indígenas.",
                "Quem já vivia no litoral quando os portugueses chegaram?",
                "Diversos povos indígenas.",
                "Robôs viajantes.",
                "Moradores de Marte.",
                "A pista está na pílula sobre quem já habitava o litoral.",
            ),
            _pill(
                "O nome Brasil se relaciona ao pau-brasil, árvore de madeira valiosa.",
                "A qual árvore o nome Brasil se relaciona?",
                "Ao pau-brasil.",
                "Ao ipê-amarelo.",
                "Ao pinheiro de Natal.",
                "Lembre da árvore de madeira valiosa.",
            ),
            _pill(
                "Caravelas ajudavam navegadores a cruzar longas distâncias no mar.",
                "Que embarcações ajudavam nas viagens pelo mar?",
                "Caravelas.",
                "Trens elétricos.",
                "Balões de ar quente.",
                "A pílula fala de embarcações usadas por navegadores.",
            ),
            _pill(
                "Mapas e cartas náuticas ajudavam a orientar as viagens.",
                "O que ajudava a orientar as viagens marítimas?",
                "Mapas e cartas náuticas.",
                "Semáforos modernos.",
                "Placas de shopping.",
                "Procure lembrar dos instrumentos de orientação.",
            ),
            _pill(
                "O encontro de 1500 mudou histórias de muitos povos.",
                "O encontro de 1500 mudou histórias de quem?",
                "De muitos povos.",
                "Apenas de uma pessoa.",
                "Somente dos animais da praia.",
                "A frase fala de mudanças para muitos povos.",
            ),
            _pill(
                "O território tinha muitas línguas, culturas e modos de viver.",
                "O que já existia no território antes da chegada portuguesa?",
                "Muitas línguas, culturas e modos de viver.",
                "Uma única cidade moderna.",
                "Uma fábrica de celulares.",
                "Lembre da diversidade que já existia aqui.",
            ),
            _pill(
                "Os navegadores observavam ventos, correntes e estrelas.",
                "O que os navegadores observavam para viajar?",
                "Ventos, correntes e estrelas.",
                "Televisores e celulares.",
                "Placas de trânsito.",
                "A dica está nos elementos da natureza e do céu.",
            ),
            _pill(
                "O território recebeu diferentes nomes ao longo do tempo.",
                "O que aconteceu com o nome do território ao longo do tempo?",
                "Recebeu diferentes nomes.",
                "Nunca teve nome.",
                "Foi chamado apenas de Lua.",
                "A pílula fala de nomes que mudaram com o tempo.",
            ),
            _pill(
                "Estudar 1500 pede respeito pelos povos que já viviam aqui.",
                "Por que estudar 1500 pede respeito?",
                "Porque povos já viviam aqui.",
                "Porque todos tinham videogames.",
                "Porque era uma história sem pessoas.",
                "Lembre dos povos que já estavam neste território.",
            ),
        ],
    ),
    _make_level(
        title="Ciclo do açúcar",
        year="Século XVI",
        mission="Atravesse os engenhos e encontre o ponto de observação.",
        historical_note=(
            "No período colonial, a produção de açúcar se tornou uma atividade "
            "econômica muito importante."
        ),
        intro_text=(
            "Mig visita uma região de engenhos. A fase mostra trabalho, plantio "
            "e comércio, sempre com cuidado ao falar das pessoas envolvidas."
        ),
        theme="sugar",
        width=1850,
        variant=1,
        pill_bank=[
            _pill(
                "Os engenhos reuniam plantação, moagem da cana e produção do açúcar.",
                "O que os engenhos produziam a partir da cana?",
                "Açúcar.",
                "Ouro.",
                "Rádio.",
                "Lembre da cana sendo moída para virar açúcar.",
            ),
            _pill(
                "A economia colonial dependia muito da exportação para a Europa.",
                "Para onde muito açúcar era exportado?",
                "Para a Europa.",
                "Para a Lua.",
                "Para cidades submarinas.",
                "A pílula fala do comércio com a Europa.",
            ),
            _pill(
                "A produção de açúcar marcou fortemente o Nordeste colonial.",
                "Qual região foi muito marcada pelo açúcar colonial?",
                "O Nordeste.",
                "A Antártida.",
                "O deserto do Saara.",
                "Pense na região citada junto aos engenhos.",
            ),
            _pill(
                "Muitas pessoas foram obrigadas a trabalhar nos engenhos, um tema para estudar com respeito.",
                "Como devemos estudar o trabalho forçado nos engenhos?",
                "Com respeito.",
                "Com piadas.",
                "Sem prestar atenção.",
                "A pílula lembra que é um tema sensível.",
            ),
            _pill(
                "A cana era cortada no campo antes de seguir para a moenda.",
                "Para onde a cana seguia depois do corte?",
                "Para a moenda.",
                "Para uma estação espacial.",
                "Para um cinema.",
                "A pista está na etapa depois do corte.",
            ),
            _pill(
                "A casa-grande era ligada ao poder dos senhores de engenho.",
                "A casa-grande era ligada ao poder de quem?",
                "Dos senhores de engenho.",
                "Dos pilotos de foguete.",
                "Dos jogadores de futebol.",
                "Lembre de quem mandava nos engenhos coloniais.",
            ),
            _pill(
                "Portos ajudavam o açúcar a seguir para outros lugares.",
                "O que ajudava o açúcar a seguir para outros lugares?",
                "Portos.",
                "Elevadores de prédio.",
                "Ônibus escolares.",
                "A pílula fala do caminho do comércio.",
            ),
            _pill(
                "O trabalho nos engenhos envolvia campo, fornalha e transporte.",
                "O trabalho nos engenhos envolvia quais espaços?",
                "Campo, fornalha e transporte.",
                "Praia, cinema e shopping.",
                "Nuvens, estrelas e cometas.",
                "A dica está nos lugares de trabalho citados.",
            ),
            _pill(
                "O açúcar era um produto muito valorizado no comércio colonial.",
                "Qual produto era muito valorizado no comércio colonial?",
                "Açúcar.",
                "Lápis de cor.",
                "Sorvete de morango.",
                "A própria fase tem esse produto no nome.",
            ),
            _pill(
                "O ciclo do açúcar também mostra desigualdades da sociedade colonial.",
                "O que o ciclo do açúcar também mostra?",
                "Desigualdades da sociedade colonial.",
                "Um país sem diferenças sociais.",
                "A invenção do computador.",
                "Lembre que a fase trata de trabalho e poder.",
            ),
        ],
    ),
    _make_level(
        title="Interiorização do território",
        year="Séculos XVII e XVIII",
        mission="Siga pelas trilhas e complete o mapa do interior.",
        historical_note=(
            "As expedições pelo interior ampliaram caminhos e mapas, mas também "
            "trouxeram desafios para muitos povos."
        ),
        intro_text=(
            "Mig entra por trilhas, rios e morros. Ele aprende que o interior já "
            "tinha muitos saberes e caminhos antes dos novos mapas."
        ),
        theme="interior",
        width=2000,
        variant=2,
        pill_bank=[
            _pill(
                "Muitos caminhos pelo interior ajudaram a criar novos mapas.",
                "O que os caminhos pelo interior ajudaram a criar?",
                "Novos mapas.",
                "Jogos eletrônicos.",
                "Satélites.",
                "Pense nos caminhos usados para conhecer o território.",
            ),
            _pill(
                "Diferentes povos já conheciam rios, florestas e trilhas antigas.",
                "O que diferentes povos já conheciam no interior?",
                "Rios, florestas e trilhas antigas.",
                "Arranha-céus modernos.",
                "Trens elétricos.",
                "A pílula fala de saberes sobre a natureza.",
            ),
            _pill(
                "A ocupação do interior mudou vilas, rotas e formas de viver.",
                "O que a ocupação do interior mudou?",
                "Vilas, rotas e formas de viver.",
                "A cor do céu.",
                "O formato da Lua.",
                "Lembre das mudanças nas vilas e nos caminhos.",
            ),
            _pill(
                "Estudar esse período pede respeito pelas comunidades indígenas.",
                "Por quem esse período pede respeito especial?",
                "Pelas comunidades indígenas.",
                "Por robôs de metal.",
                "Por personagens imaginários.",
                "A pílula lembra quem já vivia e conhecia o território.",
            ),
            _pill(
                "Rios eram caminhos importantes para viajar pelo interior.",
                "Que caminhos naturais eram importantes para viajar?",
                "Rios.",
                "Escadas rolantes.",
                "Tapetes mágicos.",
                "A pista está nos caminhos de água.",
            ),
            _pill(
                "Algumas expedições buscavam riquezas e novas rotas.",
                "O que algumas expedições buscavam?",
                "Riquezas e novas rotas.",
                "Brinquedos de praia.",
                "Faróis de carro.",
                "A pílula fala de buscas no interior.",
            ),
            _pill(
                "Pousos e pequenas vilas surgiam ao longo dos caminhos.",
                "O que surgia ao longo dos caminhos?",
                "Pousos e pequenas vilas.",
                "Aeroportos modernos.",
                "Castelos de gelo.",
                "Lembre dos lugares de parada nas rotas.",
            ),
            _pill(
                "Os mapas mudavam conforme viajantes aprendiam mais sobre o território.",
                "Por que os mapas mudavam?",
                "Porque viajantes aprendiam mais sobre o território.",
                "Porque o papel desaparecia sozinho.",
                "Porque ninguém observava nada.",
                "A pílula fala de aprendizado sobre o território.",
            ),
            _pill(
                "A interiorização aproximou regiões, mas também trouxe conflitos.",
                "A interiorização aproximou regiões e também trouxe o quê?",
                "Conflitos.",
                "Somente férias.",
                "Neve todos os dias.",
                "A dica está nos desafios desse período.",
            ),
            _pill(
                "O interior tinha saberes antigos sobre plantas, animais e caminhos.",
                "Que saberes antigos existiam no interior?",
                "Sobre plantas, animais e caminhos.",
                "Sobre videogames portáteis.",
                "Sobre foguetes para Marte.",
                "Lembre dos conhecimentos ligados à natureza.",
            ),
        ],
    ),
    _make_level(
        title="Ciclo do ouro",
        year="Século XVIII",
        mission="Explore as montanhas e encontre o marco das minas.",
        historical_note=(
            "O ouro mudou a vida de muitas vilas e atraiu pessoas para a região "
            "das minas."
        ),
        intro_text=(
            "Mig chega a montanhas e caminhos de pedra. Ele observa como a busca "
            "por ouro transformou vilas, trabalho e comércio."
        ),
        theme="mines",
        width=2050,
        variant=3,
        pill_bank=[
            _pill(
                "A descoberta de ouro fez crescer vilas em regiões montanhosas.",
                "O que fez crescer vilas em regiões montanhosas?",
                "A descoberta de ouro.",
                "A chegada de computadores.",
                "A construção de aeroportos.",
                "Lembre do que foi encontrado nas montanhas.",
            ),
            _pill(
                "Muitas rotas foram abertas para transportar pessoas e mercadorias.",
                "Para que muitas rotas foram abertas?",
                "Para transportar pessoas e mercadorias.",
                "Para brincar de esconde-esconde.",
                "Para plantar no fundo do mar.",
                "A pílula fala de transporte.",
            ),
            _pill(
                "O trabalho nas minas foi difícil e envolveu muitas pessoas escravizadas.",
                "Como devemos lembrar o trabalho nas minas?",
                "Como difícil e ligado a pessoas escravizadas.",
                "Como uma brincadeira leve.",
                "Como algo sem esforço.",
                "A pílula pede cuidado com esse tema.",
            ),
            _pill(
                "Cidades como Ouro Preto guardam marcas desse período.",
                "Qual cidade guarda marcas do ciclo do ouro?",
                "Ouro Preto.",
                "Brasília.",
                "Manaus moderna.",
                "Procure lembrar da cidade citada na pílula.",
            ),
            _pill(
                "A região das minas atraiu comerciantes, artesãos e trabalhadores.",
                "Quem a região das minas atraiu?",
                "Comerciantes, artesãos e trabalhadores.",
                "Astronautas e marcianos.",
                "Somente reis estrangeiros.",
                "A dica está nos grupos citados.",
            ),
            _pill(
                "Impostos sobre o ouro causavam tensão entre moradores e governo.",
                "O que causava tensão entre moradores e governo?",
                "Impostos sobre o ouro.",
                "Dias de chuva.",
                "Jogos de tabuleiro.",
                "Lembre das cobranças ligadas ao ouro.",
            ),
            _pill(
                "Tropeiros ajudavam a levar produtos por caminhos longos.",
                "Quem ajudava a levar produtos por caminhos longos?",
                "Tropeiros.",
                "Pilotos de avião a jato.",
                "Mergulhadores.",
                "A pílula fala de viajantes de caminhos longos.",
            ),
            _pill(
                "O comércio cresceu perto das áreas de mineração.",
                "O que cresceu perto das áreas de mineração?",
                "O comércio.",
                "A internet.",
                "Os shoppings modernos.",
                "A pista está nas trocas de produtos.",
            ),
            _pill(
                "A arte barroca deixou marcas em igrejas e cidades mineiras.",
                "Que arte deixou marcas em igrejas e cidades mineiras?",
                "A arte barroca.",
                "A arte digital.",
                "O grafite espacial.",
                "Lembre do estilo citado junto às igrejas.",
            ),
            _pill(
                "O ciclo do ouro mudou caminhos, vilas e relações de poder.",
                "O ciclo do ouro mudou caminhos, vilas e o quê?",
                "Relações de poder.",
                "O formato dos oceanos.",
                "O tamanho das estrelas.",
                "A pílula fala de mudanças na sociedade.",
            ),
        ],
    ),
    _make_level(
        title="Inconfidência Mineira",
        year="1789",
        mission="Junte ideias e alcance a praça colonial.",
        historical_note=(
            "A Inconfidência Mineira reuniu ideias de mudança em Minas Gerais no "
            "fim do século XVIII."
        ),
        intro_text=(
            "Mig visita uma cidade colonial. Ele encontra conversas sobre impostos, "
            "liberdade e planos de mudança."
        ),
        theme="colonial_city",
        width=1900,
        variant=4,
        pill_bank=[
            _pill(
                "Alguns moradores de Minas queriam menos controle da Coroa portuguesa.",
                "O que alguns moradores de Minas queriam?",
                "Menos controle da Coroa portuguesa.",
                "Mais dever de casa.",
                "Uma viagem de foguete.",
                "Lembre do desejo de mudança política.",
            ),
            _pill(
                "As ideias de liberdade circulavam em livros, encontros e conversas.",
                "Onde as ideias de liberdade circulavam?",
                "Em livros, encontros e conversas.",
                "Em jogos de videogame.",
                "Em estações espaciais.",
                "A pílula mostra como as ideias passavam de pessoa para pessoa.",
            ),
            _pill(
                "Tiradentes ficou conhecido como um dos participantes do movimento.",
                "Quem ficou conhecido como participante do movimento?",
                "Tiradentes.",
                "Santos Dumont.",
                "Mig.",
                "Lembre do nome citado na pílula.",
            ),
            _pill(
                "Esse tema deve ser estudado lembrando que havia muitos interesses diferentes.",
                "O que havia entre os participantes e grupos da época?",
                "Muitos interesses diferentes.",
                "Um pensamento único de todos.",
                "Nenhuma conversa.",
                "A dica está na variedade de interesses.",
            ),
            _pill(
                "A cobrança de impostos sobre o ouro incomodava muitos moradores.",
                "O que incomodava muitos moradores de Minas?",
                "A cobrança de impostos sobre o ouro.",
                "A falta de bicicletas.",
                "A chegada da televisão.",
                "Pense nas cobranças ligadas ao ouro.",
            ),
            _pill(
                "O movimento aconteceu em Minas Gerais no fim do século XVIII.",
                "Onde aconteceu a Inconfidência Mineira?",
                "Em Minas Gerais.",
                "No Amazonas.",
                "Em outro planeta.",
                "O nome da fase ajuda a lembrar o lugar.",
            ),
            _pill(
                "Muitos planos eram conversados de forma reservada.",
                "Como muitos planos eram conversados?",
                "De forma reservada.",
                "Em alto-falantes da cidade.",
                "Em transmissões pela internet.",
                "A pílula fala de conversas cuidadosas.",
            ),
            _pill(
                "A palavra inconfidência tem relação com falta de fidelidade à Coroa.",
                "A palavra inconfidência se relaciona a quê?",
                "À falta de fidelidade à Coroa.",
                "A uma festa junina.",
                "A um esporte moderno.",
                "Lembre da relação com a Coroa portuguesa.",
            ),
            _pill(
                "O ano de 1789 marca a Inconfidência Mineira.",
                "Que ano marca a Inconfidência Mineira?",
                "1789.",
                "1500.",
                "1988.",
                "O ano aparece no início da fase.",
            ),
            _pill(
                "A Inconfidência ajuda a estudar impostos, liberdade e política.",
                "Que temas a Inconfidência ajuda a estudar?",
                "Impostos, liberdade e política.",
                "Dinossauros, foguetes e magia.",
                "Somente culinária.",
                "A pílula reúne os temas principais da fase.",
            ),
        ],
    ),
    _make_level(
        title="Vinda da família real",
        year="1808",
        mission="Atravesse a cidade e chegue ao palácio.",
        historical_note=(
            "Em 1808, a chegada da família real portuguesa trouxe mudanças para "
            "o Rio de Janeiro e para o Brasil."
        ),
        intro_text=(
            "Mig chega a uma cidade mais movimentada. Ele vê novas instituições, "
            "livros, portos e ideias circulando."
        ),
        theme="court",
        width=1950,
        variant=5,
        pill_bank=[
            _pill(
                "A corte portuguesa veio para o Brasil em 1808.",
                "O que aconteceu em 1808?",
                "A corte portuguesa veio para o Brasil.",
                "Brasília foi inaugurada.",
                "A República foi proclamada.",
                "Lembre da chegada que mudou o Rio de Janeiro.",
            ),
            _pill(
                "Portos foram abertos para comércio com outras partes do mundo.",
                "O que foi aberto para o comércio?",
                "Portos.",
                "Túneis no espaço.",
                "Parques de diversão.",
                "A pílula fala de comércio com outras partes do mundo.",
            ),
            _pill(
                "Bibliotecas, escolas e serviços urbanos ganharam mais destaque.",
                "O que ganhou mais destaque com a corte no Brasil?",
                "Bibliotecas, escolas e serviços urbanos.",
                "Videogames e tablets.",
                "Castelos de areia.",
                "Pense nas instituições da cidade.",
            ),
            _pill(
                "As mudanças beneficiaram alguns grupos mais do que outros.",
                "As mudanças beneficiaram todos do mesmo jeito?",
                "Não, beneficiaram alguns grupos mais do que outros.",
                "Sim, todos igualmente.",
                "Ninguém foi afetado.",
                "A dica está na diferença entre grupos.",
            ),
            _pill(
                "O Rio de Janeiro ficou mais movimentado com a presença da corte.",
                "Qual cidade ficou mais movimentada com a corte?",
                "Rio de Janeiro.",
                "Ouro Preto.",
                "Porto Alegre no gelo.",
                "Lembre da cidade citada na pílula.",
            ),
            _pill(
                "A Impressão Régia ajudou livros e jornais a circular.",
                "O que a Impressão Régia ajudou a circular?",
                "Livros e jornais.",
                "Bolas de futebol.",
                "Satélites.",
                "A pista está nos materiais de leitura.",
            ),
            _pill(
                "O Banco do Brasil foi criado nesse período.",
                "Que banco foi criado nesse período?",
                "Banco do Brasil.",
                "Banco Lunar.",
                "Banco dos Dinossauros.",
                "A pílula cita o nome do banco.",
            ),
            _pill(
                "Novas instituições mudaram a administração do território.",
                "O que mudou a administração do território?",
                "Novas instituições.",
                "Brinquedos novos.",
                "Um cometa colorido.",
                "Pense nas estruturas criadas com a corte.",
            ),
            _pill(
                "A abertura dos portos aumentou contatos comerciais.",
                "O que a abertura dos portos aumentou?",
                "Contatos comerciais.",
                "Viagens para Marte.",
                "Aulas de natação.",
                "A pílula fala de comércio.",
            ),
            _pill(
                "A presença da família real aproximou decisões políticas do Brasil.",
                "O que a presença da família real aproximou do Brasil?",
                "Decisões políticas.",
                "Montanhas nevadas.",
                "Fábricas de robôs.",
                "Lembre das decisões tomadas mais perto daqui.",
            ),
        ],
    ),
    _make_level(
        title="Independência",
        year="1822",
        mission="Colete pílulas de mudança e encontre o marco da independência.",
        historical_note=(
            "A independência iniciou uma nova organização política, mas muitos "
            "desafios sociais continuaram."
        ),
        intro_text=(
            "Mig observa um momento de mudança política. Ele aprende que a "
            "independência foi um processo, não apenas um dia."
        ),
        theme="independence",
        width=2000,
        variant=6,
        pill_bank=[
            _pill(
                "A independência do Brasil foi declarada em 1822.",
                "Em que ano a independência do Brasil foi declarada?",
                "1822.",
                "1500.",
                "1960.",
                "O ano aparece no início da fase.",
            ),
            _pill(
                "O processo envolveu disputas políticas e interesses diferentes.",
                "A independência envolveu o quê?",
                "Disputas políticas e interesses diferentes.",
                "Uma viagem de avião.",
                "Uma festa sem desafios.",
                "A introdução lembra que foi um processo.",
            ),
            _pill(
                "Muitas pessoas comuns sentiram as mudanças de formas variadas.",
                "Quem sentiu as mudanças de formas variadas?",
                "Muitas pessoas comuns.",
                "Somente imperadores.",
                "Apenas personagens de desenho.",
                "Pense nas pessoas além dos líderes.",
            ),
            _pill(
                "Mesmo independente, o Brasil ainda manteve grandes desigualdades.",
                "O que continuou no Brasil mesmo após a independência?",
                "Grandes desigualdades.",
                "Igualdade completa para todos.",
                "Viagens espaciais diárias.",
                "A pílula fala de desafios que continuaram.",
            ),
            _pill(
                "D. Pedro declarou a independência, mas o processo foi maior que um gesto.",
                "A independência foi maior que o gesto de quem?",
                "D. Pedro.",
                "Tiradentes.",
                "Santos Dumont.",
                "A pílula lembra que foi mais que um gesto.",
            ),
            _pill(
                "Algumas províncias aceitaram a independência em ritmos diferentes.",
                "Como algumas províncias aceitaram a independência?",
                "Em ritmos diferentes.",
                "Todas no mesmo minuto.",
                "Nenhuma ouviu falar.",
                "Lembre que o processo não foi igual em todo lugar.",
            ),
            _pill(
                "Depois de 1822, o Brasil continuou sendo uma monarquia.",
                "Depois da independência, o Brasil continuou sendo o quê?",
                "Uma monarquia.",
                "Uma república com presidentes.",
                "Uma cidade única.",
                "Pense no governo com imperador.",
            ),
            _pill(
                "Símbolos como bandeiras e hinos ajudam a contar mudanças políticas.",
                "O que bandeiras e hinos ajudam a contar?",
                "Mudanças políticas.",
                "Receitas de bolo.",
                "Jogos de tabuleiro.",
                "A pílula fala de símbolos.",
            ),
            _pill(
                "A independência não acabou com a escravidão.",
                "O que a independência não acabou?",
                "A escravidão.",
                "O oceano Atlântico.",
                "As montanhas.",
                "A dica está nos desafios sociais que continuaram.",
            ),
            _pill(
                "Estudar a independência ajuda a entender mudanças e continuidades.",
                "Estudar a independência ajuda a entender o quê?",
                "Mudanças e continuidades.",
                "Somente datas soltas.",
                "Apenas jogos antigos.",
                "Lembre que algumas coisas mudaram e outras continuaram.",
            ),
        ],
    ),
    _make_level(
        title="Império",
        year="1822 a 1889",
        mission="Passe pelos jardins imperiais e encontre o ponto final.",
        historical_note=(
            "Durante o Império, o Brasil teve monarquia, crescimento urbano e "
            "debates sobre cidadania."
        ),
        intro_text=(
            "Mig visita o Brasil imperial. Entre jardins e cidades, ele percebe "
            "que política, cultura e sociedade estavam mudando."
        ),
        theme="empire",
        width=2050,
        variant=7,
        pill_bank=[
            _pill(
                "O Brasil imperial foi governado por imperadores.",
                "Durante o Império, o Brasil era governado por quem?",
                "Imperadores.",
                "Presidentes.",
                "Astronautas.",
                "O próprio nome da fase ajuda: Brasil imperial.",
            ),
            _pill(
                "Ferrovias, cidades e lavouras cresceram em algumas regiões.",
                "O que cresceu em algumas regiões do Império?",
                "Ferrovias, cidades e lavouras.",
                "Foguetes e estações espaciais.",
                "Castelos de gelo.",
                "A pílula cita três crescimentos do período.",
            ),
            _pill(
                "A sociedade discutia quem podia participar da vida política.",
                "O que a sociedade discutia?",
                "Quem podia participar da vida política.",
                "Qual planeta era maior.",
                "Como fazer neve no verão.",
                "Lembre dos debates sobre cidadania.",
            ),
            _pill(
                "A escravidão continuou por boa parte do período imperial.",
                "O que continuou por boa parte do Império?",
                "A escravidão.",
                "A internet.",
                "A República.",
                "A dica está no tema sensível da fase.",
            ),
            _pill(
                "O café ganhou grande importância econômica no Império.",
                "Qual produto ganhou grande importância no Império?",
                "Café.",
                "Computadores.",
                "Diamantes espaciais.",
                "Pense nas lavouras do período.",
            ),
            _pill(
                "A Constituição de 1824 organizou regras do Império.",
                "Qual Constituição organizou regras do Império?",
                "A Constituição de 1824.",
                "A Constituição de 1988.",
                "Um manual de videogame.",
                "A pílula cita o ano 1824.",
            ),
            _pill(
                "O voto era restrito e não incluía toda a população.",
                "Como era o voto no Império?",
                "Restrito.",
                "Aberto para todas as crianças.",
                "Feito por celular.",
                "A pílula fala de participação limitada.",
            ),
            _pill(
                "Debates abolicionistas cresceram no fim do Império.",
                "Que debates cresceram no fim do Império?",
                "Debates abolicionistas.",
                "Debates sobre foguetes.",
                "Debates sobre dinossauros.",
                "Lembre das conversas contra a escravidão.",
            ),
            _pill(
                "A cultura urbana ganhou teatros, jornais e novas ideias.",
                "O que a cultura urbana ganhou?",
                "Teatros, jornais e novas ideias.",
                "Robôs de estimação.",
                "Naves espaciais.",
                "A pílula fala de vida cultural nas cidades.",
            ),
            _pill(
                "O Império terminou em 1889, com a Proclamação da República.",
                "Quando o Império terminou?",
                "Em 1889.",
                "Em 1500.",
                "Em 2018.",
                "A pílula liga o fim do Império à República.",
            ),
        ],
    ),
    _make_level(
        title="Abolição da escravidão",
        year="1888",
        mission="Reúna memórias de liberdade e chegue ao jardim de encontro.",
        historical_note=(
            "A abolição em 1888 foi uma conquista importante, ligada a muitas "
            "lutas por liberdade e dignidade."
        ),
        intro_text=(
            "Mig chega a uma fase sensível e importante. Ele aprende sobre "
            "liberdade, respeito e a luta de muitas pessoas."
        ),
        theme="empire",
        width=1900,
        variant=8,
        pill_bank=[
            _pill(
                "A Lei Áurea acabou oficialmente com a escravidão no Brasil em 1888.",
                "O que a Lei Áurea fez oficialmente em 1888?",
                "Acabou com a escravidão no Brasil.",
                "Criou a primeira rádio.",
                "Fundou Brasília.",
                "Lembre da lei de 1888.",
            ),
            _pill(
                "Pessoas escravizadas resistiram e buscaram liberdade de muitas formas.",
                "O que pessoas escravizadas buscaram de muitas formas?",
                "Liberdade.",
                "Computadores.",
                "Férias na Lua.",
                "A pílula fala de resistência e busca por liberdade.",
            ),
            _pill(
                "Abolicionistas também participaram de debates e campanhas.",
                "Quem participou de debates e campanhas?",
                "Abolicionistas.",
                "Astronautas.",
                "Robôs escolares.",
                "Lembre do grupo que defendia a abolição.",
            ),
            _pill(
                "Depois da abolição, muitos desafios de igualdade continuaram.",
                "O que continuou depois da abolição?",
                "Desafios de igualdade.",
                "A escravidão oficial pela Lei Áurea.",
                "A corrida espacial brasileira.",
                "A dica está nos desafios que permaneceram.",
            ),
            _pill(
                "Quilombos foram espaços de resistência e comunidade.",
                "O que os quilombos representaram?",
                "Resistência e comunidade.",
                "Estações de trem modernas.",
                "Parques de diversão.",
                "A pílula fala de espaços criados por resistência.",
            ),
            _pill(
                "A liberdade foi conquistada por muitas lutas, não por uma única pessoa.",
                "A liberdade foi conquistada por quê?",
                "Por muitas lutas.",
                "Por uma única pessoa sozinha.",
                "Por mágica.",
                "Lembre da participação de muitas pessoas.",
            ),
            _pill(
                "A data de 13 de maio lembra a assinatura da Lei Áurea.",
                "Que data lembra a assinatura da Lei Áurea?",
                "13 de maio.",
                "7 de setembro.",
                "15 de novembro.",
                "A pílula fala do dia da assinatura.",
            ),
            _pill(
                "Muitas famílias negras precisaram lutar por trabalho, escola e moradia.",
                "Depois da abolição, muitas famílias negras lutaram por quê?",
                "Trabalho, escola e moradia.",
                "Viagens espaciais.",
                "Castelos de brinquedo.",
                "A pílula cita necessidades de vida digna.",
            ),
            _pill(
                "A memória da abolição deve valorizar dignidade e respeito.",
                "Como a memória da abolição deve ser tratada?",
                "Com dignidade e respeito.",
                "Com descuido.",
                "Como uma piada.",
                "A dica está no tom respeitoso da pílula.",
            ),
            _pill(
                "A luta contra o racismo continua importante no Brasil.",
                "Que luta continua importante no Brasil?",
                "A luta contra o racismo.",
                "A luta contra as estrelas.",
                "A luta para apagar a história.",
                "Lembre dos desafios de igualdade.",
            ),
        ],
    ),
    _make_level(
        title="Proclamação da República",
        year="1889",
        mission="Atravesse a praça e encontre o marco republicano.",
        historical_note=(
            "Em 1889, o Brasil deixou de ser monarquia e passou a ser república."
        ),
        intro_text=(
            "Mig chega a uma praça de mudanças políticas. Ele observa que uma "
            "nova forma de governo estava começando."
        ),
        theme="republic",
        width=1850,
        variant=9,
        pill_bank=[
            _pill(
                "A República foi proclamada em 1889.",
                "Em que ano a República foi proclamada?",
                "1889.",
                "1500.",
                "1964.",
                "O ano aparece no início da fase.",
            ),
            _pill(
                "O Brasil passou a ter presidentes em vez de imperadores.",
                "Depois de 1889, o Brasil passou a ter quem no governo?",
                "Presidentes.",
                "Imperadores.",
                "Reis europeus.",
                "Lembre da mudança de forma de governo.",
            ),
            _pill(
                "Nem toda a população podia participar das decisões políticas.",
                "Quem podia participar das decisões políticas?",
                "Nem toda a população.",
                "Todas as pessoas igualmente.",
                "Somente crianças.",
                "A pílula fala de participação limitada.",
            ),
            _pill(
                "Mudanças de governo também trazem perguntas sobre cidadania.",
                "Mudanças de governo trazem perguntas sobre o quê?",
                "Cidadania.",
                "Receitas de doce.",
                "Brincadeiras de praia.",
                "A dica está no tema da participação.",
            ),
            _pill(
                "A monarquia terminou no Brasil com a Proclamação da República.",
                "O que terminou com a Proclamação da República?",
                "A monarquia.",
                "A história do Brasil.",
                "A escola.",
                "Lembre que o governo deixou de ter imperador.",
            ),
            _pill(
                "Militares e políticos participaram da mudança de 1889.",
                "Quem participou da mudança de 1889?",
                "Militares e políticos.",
                "Astronautas e marcianos.",
                "Somente artistas de circo.",
                "A pílula cita os grupos envolvidos.",
            ),
            _pill(
                "A nova bandeira republicana ganhou o lema Ordem e Progresso.",
                "Que lema aparece na bandeira republicana?",
                "Ordem e Progresso.",
                "Açúcar e Ouro.",
                "Lua e Marte.",
                "Lembre do lema escrito na bandeira.",
            ),
            _pill(
                "A Constituição de 1891 organizou a nova República.",
                "Qual Constituição organizou a nova República?",
                "A Constituição de 1891.",
                "A Constituição de 1824.",
                "Uma carta de piratas.",
                "A pílula cita o ano 1891.",
            ),
            _pill(
                "Os estados ganharam mais autonomia na nova organização política.",
                "Quem ganhou mais autonomia na República?",
                "Os estados.",
                "As nuvens.",
                "Os brinquedos.",
                "A dica está na organização política.",
            ),
            _pill(
                "A República começou com muitos desafios para ampliar a participação.",
                "Com quais desafios a República começou?",
                "Ampliar a participação.",
                "Inventar o celular.",
                "Construir foguetes.",
                "Lembre da participação política limitada.",
            ),
        ],
    ),
    _make_level(
        title="Primeira República",
        year="1889 a 1930",
        mission="Siga pelos trilhos e chegue ao coreto da cidade.",
        historical_note=(
            "A Primeira República teve crescimento de cidades, lavouras, ferrovias "
            "e muitos debates sobre participação política."
        ),
        intro_text=(
            "Mig caminha por trilhos, fazendas e cidades. Ele percebe que o país "
            "crescia, mas a participação política ainda era limitada."
        ),
        theme="rural_republic",
        width=2100,
        variant=10,
        pill_bank=[
            _pill(
                "A produção de café teve grande importância nesse período.",
                "Qual produto teve grande importância na Primeira República?",
                "Café.",
                "Computadores.",
                "Ouro espacial.",
                "Lembre das lavouras desse período.",
            ),
            _pill(
                "Ferrovias ajudaram a ligar fazendas, portos e cidades.",
                "O que as ferrovias ajudaram a ligar?",
                "Fazendas, portos e cidades.",
                "Planetas distantes.",
                "Castelos de areia.",
                "A pílula fala dos trilhos.",
            ),
            _pill(
                "Muitas pessoas viviam no campo e buscavam melhores condições.",
                "O que muitas pessoas buscavam no campo?",
                "Melhores condições.",
                "Uma nave espacial.",
                "Um mapa da Lua.",
                "A dica está nas necessidades de vida.",
            ),
            _pill(
                "O voto era restrito e nem todos tinham voz nas decisões.",
                "Como era o voto na Primeira República?",
                "Restrito.",
                "Universal para todos.",
                "Feito pela internet.",
                "Lembre que nem todos tinham voz.",
            ),
            _pill(
                "O poder de líderes locais influenciava muitas eleições.",
                "Quem influenciava muitas eleições?",
                "Líderes locais.",
                "Robôs professores.",
                "Pilotos de foguete.",
                "A pílula fala do poder local.",
            ),
            _pill(
                "Cidades cresceram com reformas, comércio e novos serviços.",
                "O que cresceu com reformas e novos serviços?",
                "Cidades.",
                "Vulcões.",
                "Satélites.",
                "A pista está na vida urbana.",
            ),
            _pill(
                "Imigrantes vieram trabalhar em lavouras e cidades.",
                "Quem veio trabalhar em lavouras e cidades?",
                "Imigrantes.",
                "Habitantes de Marte.",
                "Personagens de conto de fadas.",
                "Lembre das pessoas que chegaram de outros países.",
            ),
            _pill(
                "Trabalhadores organizaram pedidos por direitos e melhores salários.",
                "O que trabalhadores organizaram?",
                "Pedidos por direitos e melhores salários.",
                "Caças ao tesouro espacial.",
                "Festas sem motivo.",
                "A pílula fala de direitos no trabalho.",
            ),
            _pill(
                "Revoltas mostraram insatisfações de grupos diferentes.",
                "O que algumas revoltas mostraram?",
                "Insatisfações de grupos diferentes.",
                "Que todos estavam satisfeitos.",
                "Que a história tinha acabado.",
                "Pense nos conflitos e pedidos de mudança.",
            ),
            _pill(
                "A cidadania ainda era limitada para muitas pessoas.",
                "O que ainda era limitada para muitas pessoas?",
                "A cidadania.",
                "A luz do sol.",
                "A água dos rios.",
                "Lembre da participação política restrita.",
            ),
        ],
    ),
    _make_level(
        title="Era Vargas",
        year="1930 a 1945",
        mission="Passe pela cidade industrial e encontre a estação.",
        historical_note=(
            "A Era Vargas trouxe industrialização, leis trabalhistas e também "
            "controle político."
        ),
        intro_text=(
            "Mig visita fábricas e avenidas. Ele aprende que trabalho, indústria "
            "e governo ganharam novos formatos."
        ),
        theme="vargas",
        width=2050,
        variant=11,
        pill_bank=[
            _pill(
                "A indústria cresceu em várias cidades brasileiras.",
                "O que cresceu em várias cidades na Era Vargas?",
                "A indústria.",
                "As caravelas.",
                "As minas de ouro.",
                "A fase mostra fábricas e fala de industrialização.",
            ),
            _pill(
                "Leis trabalhistas passaram a organizar direitos de muitos trabalhadores.",
                "O que as leis trabalhistas passaram a organizar?",
                "Direitos de muitos trabalhadores.",
                "Rotas para Marte.",
                "Jogos de cartas.",
                "Lembre dos direitos ligados ao trabalho.",
            ),
            _pill(
                "O rádio ajudou notícias e músicas a circularem pelo país.",
                "O que ajudou notícias e músicas a circularem?",
                "O rádio.",
                "O pau-brasil.",
                "A caravela.",
                "A pílula fala de um meio de comunicação.",
            ),
            _pill(
                "Também houve momentos de controle político que devem ser estudados com cuidado.",
                "Como devemos estudar os momentos de controle político?",
                "Com cuidado.",
                "Com descuido.",
                "Como se não importassem.",
                "A pílula pede atenção respeitosa.",
            ),
            _pill(
                "A carteira de trabalho se tornou um símbolo de direitos trabalhistas.",
                "Que documento virou símbolo de direitos trabalhistas?",
                "A carteira de trabalho.",
                "A carteira de estudante de Mig.",
                "Um passaporte lunar.",
                "A pista está no documento dos trabalhadores.",
            ),
            _pill(
                "A CLT reuniu regras importantes sobre trabalho.",
                "O que a CLT reuniu?",
                "Regras importantes sobre trabalho.",
                "Receitas de bolo.",
                "Mapas de piratas.",
                "Lembre das leis trabalhistas.",
            ),
            _pill(
                "As cidades industriais atraíram muitas pessoas em busca de trabalho.",
                "Por que muitas pessoas foram para cidades industriais?",
                "Em busca de trabalho.",
                "Para ver neve.",
                "Para morar em foguetes.",
                "A pílula fala de trabalho nas cidades.",
            ),
            _pill(
                "O governo usou propaganda para divulgar suas ideias.",
                "O que o governo usou para divulgar ideias?",
                "Propaganda.",
                "Pipas coloridas.",
                "Cartas de Marte.",
                "A dica está na comunicação do governo.",
            ),
            _pill(
                "Escolas e símbolos nacionais ganharam destaque nesse período.",
                "O que ganhou destaque nesse período?",
                "Escolas e símbolos nacionais.",
                "Dinossauros e cavernas.",
                "Naves e planetas.",
                "A pílula fala de educação e símbolos.",
            ),
            _pill(
                "A Era Vargas misturou avanços trabalhistas e limites à liberdade política.",
                "A Era Vargas misturou avanços trabalhistas e o quê?",
                "Limites à liberdade política.",
                "Viagens no tempo.",
                "Festas sem conflitos.",
                "Lembre dos dois lados citados.",
            ),
        ],
    ),
    _make_level(
        title="Experiência democrática",
        year="1946 a 1964",
        mission="Colete ideias de participação e alcance a praça cívica.",
        historical_note=(
            "Entre 1946 e 1964, o Brasil viveu eleições, projetos de desenvolvimento "
            "e debates públicos intensos."
        ),
        intro_text=(
            "Mig chega a uma fase de campanhas, construção e conversas. A "
            "democracia aparece como participação e responsabilidade."
        ),
        theme="democracy",
        width=2000,
        variant=12,
        pill_bank=[
            _pill(
                "O período teve eleições e maior participação política.",
                "O que o período teve?",
                "Eleições e maior participação política.",
                "Uma monarquia com imperador.",
                "Viagens espaciais.",
                "A pílula fala de democracia e participação.",
            ),
            _pill(
                "Brasília foi inaugurada em 1960 como nova capital do Brasil.",
                "Qual cidade foi inaugurada em 1960?",
                "Brasília.",
                "Ouro Preto.",
                "Porto Seguro.",
                "Procure lembrar da nova capital citada.",
            ),
            _pill(
                "O país discutia desenvolvimento, direitos e caminhos para o futuro.",
                "O país discutia desenvolvimento, direitos e o quê?",
                "Caminhos para o futuro.",
                "Mapas de tesouro pirata.",
                "Férias na Lua.",
                "A dica está nos debates públicos.",
            ),
            _pill(
                "Democracia precisa de diálogo, regras e respeito às pessoas.",
                "Do que a democracia precisa?",
                "Diálogo, regras e respeito.",
                "Silêncio de todos.",
                "Mágica.",
                "Lembre dos cuidados para participar.",
            ),
            _pill(
                "Partidos políticos apresentavam projetos diferentes para o país.",
                "O que partidos políticos apresentavam?",
                "Projetos diferentes para o país.",
                "Cardápios de restaurante.",
                "Brinquedos secretos.",
                "A pílula fala de ideias para governar.",
            ),
            _pill(
                "A televisão começou a ganhar espaço na vida urbana.",
                "Que meio começou a ganhar espaço na vida urbana?",
                "A televisão.",
                "A caravela.",
                "O pergaminho medieval.",
                "Lembre do aparelho de comunicação citado.",
            ),
            _pill(
                "Indústrias e obras públicas faziam parte dos planos de desenvolvimento.",
                "O que fazia parte dos planos de desenvolvimento?",
                "Indústrias e obras públicas.",
                "Castelos flutuantes.",
                "Dinossauros de estimação.",
                "A pílula fala de crescimento econômico.",
            ),
            _pill(
                "A construção de Brasília levou trabalhadores de muitas regiões.",
                "Quem a construção de Brasília levou de muitas regiões?",
                "Trabalhadores.",
                "Astronautas.",
                "Piratas.",
                "Lembre das pessoas que construíram a cidade.",
            ),
            _pill(
                "Debates sobre reformas mostravam diferentes ideias para o Brasil.",
                "O que os debates sobre reformas mostravam?",
                "Diferentes ideias para o Brasil.",
                "Que todos pensavam igual.",
                "Que ninguém queria conversar.",
                "A dica está na diversidade de ideias.",
            ),
            _pill(
                "A participação política cresceu, mas ainda tinha limites.",
                "A participação política cresceu, mas ainda tinha o quê?",
                "Limites.",
                "Superpoderes.",
                "Viagens no tempo.",
                "Lembre que democracia também exige melhorar a participação.",
            ),
        ],
    ),
    _make_level(
        title="Ditadura militar",
        year="1964 a 1985",
        mission="Atravesse com cuidado e encontre o ponto de memória.",
        historical_note=(
            "A ditadura militar foi um período de pouca liberdade política e deve "
            "ser estudada com cuidado e respeito."
        ),
        intro_text=(
            "Mig chega a um período delicado da história. A fase usa símbolos de "
            "memória e cuidado para falar de liberdade e direitos."
        ),
        theme="dictatorship",
        width=1950,
        variant=13,
        pill_bank=[
            _pill(
                "Entre 1964 e 1985, o Brasil viveu um governo militar.",
                "Entre 1964 e 1985, que tipo de governo o Brasil viveu?",
                "Um governo militar.",
                "Uma monarquia medieval.",
                "Um governo de robôs.",
                "A pista está no nome da fase.",
            ),
            _pill(
                "A participação política e a liberdade de expressão foram limitadas.",
                "Na ditadura militar, o que foi limitado?",
                "A participação política e a liberdade de expressão.",
                "A curiosidade das crianças.",
                "O nascer do sol.",
                "A pílula fala de limites à liberdade.",
            ),
            _pill(
                "Muitas pessoas defenderam democracia e direitos nesse período.",
                "O que muitas pessoas defenderam nesse período?",
                "Democracia e direitos.",
                "Silêncio para sempre.",
                "Viagens para Marte.",
                "Lembre das pessoas que pediram liberdade.",
            ),
            _pill(
                "É um tema que deve ser estudado com cuidado, respeito e memória.",
                "Como esse tema deve ser estudado?",
                "Com cuidado, respeito e memória.",
                "Com piadas.",
                "Sem atenção.",
                "A própria pílula mostra o tom correto.",
            ),
            _pill(
                "A censura impediu a circulação livre de algumas ideias e notícias.",
                "O que a censura impediu?",
                "A circulação livre de algumas ideias e notícias.",
                "A chuva.",
                "O movimento das nuvens.",
                "A dica está nas ideias e notícias.",
            ),
            _pill(
                "Artistas, estudantes e trabalhadores participaram de movimentos por direitos.",
                "Quem participou de movimentos por direitos?",
                "Artistas, estudantes e trabalhadores.",
                "Personagens de outro planeta.",
                "Apenas reis antigos.",
                "A pílula cita grupos da sociedade.",
            ),
            _pill(
                "Direitos humanos ajudam a proteger a dignidade das pessoas.",
                "O que os direitos humanos ajudam a proteger?",
                "A dignidade das pessoas.",
                "Tesouros escondidos.",
                "Castelos de areia.",
                "Lembre do respeito às pessoas.",
            ),
            _pill(
                "A memória desse período ajuda a valorizar a democracia.",
                "A memória desse período ajuda a valorizar o quê?",
                "A democracia.",
                "O esquecimento.",
                "A falta de diálogo.",
                "A dica está no aprendizado para o presente.",
            ),
            _pill(
                "Movimentos por eleições diretas cresceram no fim do período.",
                "O que cresceu no fim do período?",
                "Movimentos por eleições diretas.",
                "Construções de castelos.",
                "Corridas de foguete.",
                "Lembre dos pedidos por voto e participação.",
            ),
            _pill(
                "Liberdade de imprensa é importante para uma sociedade democrática.",
                "O que é importante para uma sociedade democrática?",
                "Liberdade de imprensa.",
                "Censura permanente.",
                "Silêncio obrigatório.",
                "Pense na circulação de notícias.",
            ),
        ],
    ),
    _make_level(
        title="Redemocratização",
        year="1985 a 1988",
        mission="Junte vozes de participação e encontre a Constituição.",
        historical_note=(
            "A redemocratização marcou a volta de eleições mais amplas e a "
            "Constituição de 1988."
        ),
        intro_text=(
            "Mig encontra praça cheia de cartazes, debates e esperança. Ele aprende "
            "que direitos são construídos com participação."
        ),
        theme="redemocratization",
        width=1950,
        variant=14,
        pill_bank=[
            _pill(
                "A redemocratização marcou a volta gradual da democracia.",
                "O que a redemocratização marcou?",
                "A volta gradual da democracia.",
                "O início do ciclo do ouro.",
                "A chegada das caravelas.",
                "Lembre da volta da participação democrática.",
            ),
            _pill(
                "Movimentos sociais pediram participação e direitos.",
                "O que movimentos sociais pediram?",
                "Participação e direitos.",
                "Brinquedos importados.",
                "Viagens espaciais.",
                "A pílula fala de pedidos da sociedade.",
            ),
            _pill(
                "A Constituição de 1988 ficou conhecida como Constituição Cidadã.",
                "Como ficou conhecida a Constituição de 1988?",
                "Constituição Cidadã.",
                "Mapa das Minas.",
                "Carta dos Navegadores.",
                "Lembre do apelido da Constituição.",
            ),
            _pill(
                "Cuidar da democracia é uma tarefa de toda a sociedade.",
                "Cuidar da democracia é tarefa de quem?",
                "De toda a sociedade.",
                "De uma pessoa só.",
                "De ninguém.",
                "A pílula fala de responsabilidade coletiva.",
            ),
            _pill(
                "A campanha Diretas Já pediu eleições diretas para presidente.",
                "O que a campanha Diretas Já pediu?",
                "Eleições diretas para presidente.",
                "Mais ouro nas minas.",
                "Mais caravelas.",
                "A dica está na palavra diretas.",
            ),
            _pill(
                "A nova Constituição reuniu direitos e deveres dos cidadãos.",
                "O que a nova Constituição reuniu?",
                "Direitos e deveres dos cidadãos.",
                "Receitas de cozinha.",
                "Mapas de planetas.",
                "Pense nas regras da cidadania.",
            ),
            _pill(
                "O voto voltou a ser um símbolo forte de participação.",
                "O que voltou a ser símbolo forte de participação?",
                "O voto.",
                "O pau-brasil.",
                "A moenda.",
                "Lembre da participação nas eleições.",
            ),
            _pill(
                "Saúde e educação aparecem como direitos importantes.",
                "Quais direitos importantes aparecem na Constituição?",
                "Saúde e educação.",
                "Foguetes e magia.",
                "Brinquedos infinitos.",
                "A pílula cita direitos sociais.",
            ),
            _pill(
                "Debates públicos ajudaram a escrever novas regras para o país.",
                "O que ajudou a escrever novas regras para o país?",
                "Debates públicos.",
                "Silêncio completo.",
                "Jogos de adivinhação.",
                "A dica está nas conversas da sociedade.",
            ),
            _pill(
                "A redemocratização mostra que direitos precisam de participação.",
                "A redemocratização mostra que direitos precisam de quê?",
                "Participação.",
                "Esquecimento.",
                "Viagens no tempo.",
                "Lembre dos cartazes e debates da fase.",
            ),
        ],
    ),
    _make_level(
        title="Brasil contemporâneo",
        year="1988 até hoje",
        mission="Complete a jornada e chegue ao portal do presente.",
        historical_note=(
            "O Brasil contemporâneo continua em construção, com diversidade, "
            "desafios e muitas possibilidades."
        ),
        intro_text=(
            "Mig chega ao tempo mais próximo dele. A história continua, e cada "
            "pessoa ajuda a construir novos caminhos."
        ),
        theme="contemporary",
        width=2200,
        variant=15,
        pill_bank=[
            _pill(
                "O Brasil atual é diverso em culturas, regiões, sotaques e modos de viver.",
                "O Brasil atual é diverso em quê?",
                "Culturas, regiões, sotaques e modos de viver.",
                "Um único jeito de viver.",
                "Somente castelos antigos.",
                "Lembre da diversidade do Brasil contemporâneo.",
            ),
            _pill(
                "Tecnologia, educação e meio ambiente fazem parte dos desafios atuais.",
                "O que faz parte dos desafios atuais?",
                "Tecnologia, educação e meio ambiente.",
                "Caravelas e engenhos.",
                "Dragões e castelos.",
                "A pílula fala de temas do presente.",
            ),
            _pill(
                "Direitos e cidadania continuam sendo temas importantes.",
                "Quais temas continuam importantes?",
                "Direitos e cidadania.",
                "Piratas e tesouros.",
                "Somente jogos.",
                "Pense nas responsabilidades de viver em sociedade.",
            ),
            _pill(
                "A história do Brasil segue sendo estudada, contada e vivida.",
                "O que acontece com a história do Brasil hoje?",
                "Segue sendo estudada, contada e vivida.",
                "Acabou para sempre.",
                "Foi esquecida por todos.",
                "A pílula lembra que a história continua.",
            ),
            _pill(
                "Cidades, campos, florestas e rios fazem parte do Brasil atual.",
                "Quais lugares fazem parte do Brasil atual?",
                "Cidades, campos, florestas e rios.",
                "Somente uma ilha pequena.",
                "Apenas estações espaciais.",
                "A dica está na variedade de paisagens.",
            ),
            _pill(
                "A internet mudou formas de estudar, brincar e conversar.",
                "O que a internet mudou?",
                "Formas de estudar, brincar e conversar.",
                "A cor dos oceanos.",
                "A forma das montanhas.",
                "Pense nas atividades do dia a dia.",
            ),
            _pill(
                "Cuidar do meio ambiente é um desafio de todos.",
                "Cuidar do meio ambiente é desafio de quem?",
                "De todos.",
                "De ninguém.",
                "Só de personagens de livros.",
                "A pílula fala de responsabilidade coletiva.",
            ),
            _pill(
                "A democracia precisa de participação, respeito e informação.",
                "Do que a democracia precisa hoje?",
                "Participação, respeito e informação.",
                "Silêncio e censura.",
                "Mágica e segredo.",
                "Lembre dos cuidados com a cidadania.",
            ),
            _pill(
                "Culturas indígenas, africanas, europeias e de muitos povos formam o Brasil.",
                "Que culturas ajudam a formar o Brasil?",
                "Indígenas, africanas, europeias e de muitos povos.",
                "Somente uma cultura.",
                "Apenas cultura espacial.",
                "A dica está na mistura de origens.",
            ),
            _pill(
                "Mig também faz parte da história que continua sendo construída.",
                "Quem também faz parte da história em construção?",
                "Mig.",
                "Somente pessoas do passado.",
                "Apenas reis antigos.",
                "A pílula aproxima a história do presente de Mig.",
            ),
        ],
    ),
]
