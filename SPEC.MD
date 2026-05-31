# SPEC.MD

Especificação técnica e funcional do projeto Caminhos do Brasil.

Este documento é a fonte de continuidade para outro agente de IA ou desenvolvedor trabalhar no projeto sem depender do histórico da conversa.

## 1. Visão Geral

Caminhos do Brasil é um jogo de plataforma 2D educativo sobre a história do Brasil.

O jogador controla Mig, um menino fictício nascido em 2018, que viaja por diferentes períodos históricos, de 1500 ao Brasil contemporâneo. O jogo combina plataforma simples, pílulas históricas coletáveis, linha do tempo e coleção.

Objetivos do produto:

- ensinar história de forma leve e respeitosa;
- ser adequado para crianças, com referência principal por volta de 8 anos;
- funcionar localmente com Python e Pygame-CE;
- funcionar no navegador via Pygbag e GitHub Pages;
- manter codigo simples, modular o suficiente e facil de continuar.

URL publicada:

```text
https://msimoes38.github.io/caminhos_brasil/
```

Branch de publicacao:

```text
yolo_melhoria
```

## 2. Estado Atual Do Produto

A versão atual está jogável e publicada para teste público. Ela possui:

- tela inicial com `abertura.png`;
- menu com continuar, nova sessão temporária, linha do tempo, coleção, ajuda e tela cheia no mobile;
- 16 fases históricas em ordem cronológica;
- introdução narrativa por fase;
- movimento lateral, pulo, gravidade, colisao, coyote time e buffer curto de pulo;
- câmera horizontal;
- HUD com ajuste discreto para títulos longos;
- controles por teclado, mouse e toque;
- interface mobile em modo paisagem com menu tocável, faixa de orientação e botões virtuais semitransparentes;
- detecção inicial de toque/mobile por `maxTouchPoints`, `matchMedia`, `ontouchstart` e user agent como fallback leve;
- faixa inferior no menu inicial para cobrir instruções fixas da arte de abertura e evitar redundância;
- dicas contextuais nos primeiros segundos da fase 1;
- banco com 10 pílulas de conhecimento por fase;
- seleção por sessão: 4 pílulas ativas na fase 1 e 5 pílulas ativas nas fases 2 a 16;
- pílulas históricas coletáveis;
- mensagens históricas fixas no topo, com translucidez quando Mig passa por trás;
- checkpoints seguros e respawn;
- áreas de cuidado;
- portal final bloqueado até todas as pílulas ativas da fase serem coletadas;
- Guardião do Portal com pergunta histórica obrigatória antes da conclusão, sorteada entre as pílulas ativas da jogada;
- feedback visual e texto positivo para pílula, checkpoint, cuidado, portal e conclusão;
- litoral inicial com ondas, espuma, vegetação baixa e destaque sutil na primeira pílula;
- coleção histórica acumulativa em formato de álbum, com cards de descobertas e descoberta recente destacada;
- linha do tempo com fases liberadas, bloqueadas, próximas aventuras e concluídas, reservando coluna de status;
- tela de pausa com botões grandes para toque;
- tela final com resumo da jornada;
- sons simples gerados por codigo;
- save local em JSON e save web em `localStorage`, ambos tolerantes a falhas;
- smoke tests permanentes;
- build Pygbag limpo com manifest/metadados web, orientação HTML acessível fora do canvas e deploy via GitHub Pages.

## 3. Tecnologias

Dependencias fixadas em `requirements.txt`:

```text
pygame-ce==2.5.7
pygbag==0.9.2
```

Base tecnica:

- Python.
- Pygame-CE para execucao local.
- Pygbag para execucao web.
- GitHub Actions e GitHub Pages para publicacao.
- Dados das fases em Python, principalmente `src/level_data.py`.
- Cenarios desenhados por codigo em `src/backgrounds.py`.
- Sons gerados por codigo em `src/sounds.py`.
- Sem dependencias novas alem de Pygame-CE e Pygbag.

## 4. Estrutura De Arquivos

```text
.github/
  workflows/
    pages.yml
main.py
requirements.txt
README.md
AGENTS.md
SPEC.MD
PROMPT_YOLO.MD
abertura.png
caminhos_brasil_save.json       # gerado localmente em execucao
assets/
  images/
    personagem.png
scripts/
  build_pygbag_clean.py
  smoke_tests.py
src/
  __init__.py
  backgrounds.py
  game.py
  level_data.py
  levels.py
  player.py
  progress.py
  settings.py
  sounds.py
build/                           # artefato gerado, nao e fonte
```

## 5. Documentos Para Agentes De IA

Arquivos de continuidade:

- `README.md`: visao para usuario/desenvolvedor, execucao, controles, testes e publicacao.
- `AGENTS.md`: regras obrigatorias para agentes de IA que forem trabalhar no projeto.
- `SPEC.MD`: especificacao tecnica e funcional atualizada.
- `PROMPT_YOLO.MD`: prompt longo para rodadas autonomas futuras, quando o usuario quiser pedir uma revisao/polimento maior.

Regra: sempre atualize `README.md`, `AGENTS.md` e `SPEC.MD` quando mudar comportamento, arquitetura, publicacao, controles ou processo de teste. Atualize `PROMPT_YOLO.MD` quando o estado geral do projeto ou as prioridades de agentes mudarem.

## 6. Arquivos Principais

### `main.py`

Ponto de entrada.

Requisito importante:

- manter loop `async` para compatibilidade com Pygbag.

Fluxo:

```python
game = Game()
await game.run()
```

### `src/game.py`

Arquivo central do jogo.

Responsabilidades:

- inicializar Pygame;
- manter o loop principal;
- tratar eventos de teclado, mouse e toque;
- converter eventos `FINGER*` para coordenadas 960x540;
- ignorar eventos de mouse gerados por toque quando apropriado;
- detectar contexto touch no carregamento inicial usando APIs simples do navegador;
- controlar estados do jogo;
- desenhar menu, ajuda, linha do tempo, colecao, fase, pausa, quiz, conclusao e final;
- alternar textos e botoes para teclado ou toque quando o contexto mobile e detectado;
- gerenciar progresso, colecao e salvamento;
- desenhar HUD, mensagens historicas e botoes virtuais;
- mostrar dicas contextuais da fase 1 e feedback positivo de coleta;
- mostrar o Guardiao do Portal e validar resposta historica antes da conclusao;
- solicitar fullscreen no navegador quando possivel;
- acionar efeitos visuais e sons;
- coletar pílulas históricas;
- ativar checkpoints;
- reiniciar tentativa ao tocar em areas de cuidado;
- esconder a tela HTML de carregamento web pelo metodo `_hide_web_loading_overlay()`.

O arquivo esta funcional, mas grande. Separar telas em modulos como `screens.py` ou `ui.py` pode ser melhoria futura, sem urgencia.

### `src/player.py`

Controla Mig:

- movimento horizontal por teclado e toque;
- pulo por teclado e toque;
- pulo recem-tocado para preservar toques rapidos;
- aceleracao/desaceleracao;
- controle no ar;
- coyote time;
- jump buffer;
- gravidade;
- limite de queda;
- colisao horizontal e vertical;
- animacao por folha de sprites;
- fallback desenhado por Pygame se o sprite falhar.

Sprite usado:

```text
assets/images/personagem.png
```

### `src/level_data.py`

Contém:

- dataclasses `KnowledgePill` e `LevelData`;
- dataclass `QuizData` para pergunta, 3 alternativas, resposta correta e dica;
- constantes de chão;
- geradores simples de plataformas, áreas de cuidado e checkpoints;
- lista `LEVELS` com 16 fases.

Regras críticas:

- cada fase deve ter exatamente 10 pílulas no banco;
- pílulas ativas devem permanecer em plataformas alcançáveis;
- checkpoints não podem colidir com áreas de cuidado;
- respawn de checkpoint não pode cair em área de cuidado;
- fase 2 já exigiu cuidado especial com checkpoint e pílulas.

### `src/levels.py`

Converte os dados crus de `src/level_data.py` para objetos usados pelo Pygame.

Funções públicas:

- `get_level_count()`
- `get_level_title(index)`
- `get_level_plain_title(index)`
- `get_level_fragment_count(index)`
- `get_total_fragment_count()`
- `get_level_pill_count(index)`
- `get_level_pill_infos(index)`
- `get_level_pill_bank(index)`
- `get_active_pill_count(index)`
- `create_level(index, active_pill_indexes=None, quiz_pill_index=None)`

### `src/backgrounds.py`

Desenha cenarios por tema usando formas simples.

Temas atuais:

- `coast`
- `sugar`
- `interior`
- `mines`
- `colonial_city`
- `court`
- `independence`
- `empire`
- `republic`
- `rural_republic`
- `vargas`
- `democracy`
- `dictatorship`
- `redemocratization`
- `contemporary`

### `src/progress.py`

Salva e carrega progresso em arquivo local no desktop:

```text
caminhos_brasil_save.json
```

No navegador via Pygbag, tenta usar `localStorage` com a chave:

```text
caminhos_brasil_save_v1
```

Campos:

- `highest_unlocked_level`
- `completed_levels`
- `collection_entries`

Requisitos:

- falha de leitura nao pode quebrar o jogo;
- falha de escrita nao pode quebrar o jogo;
- save corrompido deve voltar para progresso vazio;
- `localStorage` indisponivel deve cair para o comportamento local sem quebrar;
- sessao temporaria iniciada com `N` nao deve sobrescrever o save;

### `src/sounds.py`

Gera sons simples por codigo.

Eventos com som:

- pulo;
- coleta;
- checkpoint;
- conclusao;
- final;
- menu;
- selecao;
- acao bloqueada;
- retorno por area de cuidado.

Se mixer/audio falhar, o jogo segue em silencio.

### `src/settings.py`

Define:

- resolucao 960x540;
- FPS;
- cores;
- fisica;
- tempos de coyote/jump buffer;
- caminho do sprite;
- recortes da folha de sprites.

### `scripts/smoke_tests.py`

Teste automatizado leve em SDL dummy.

Valida:

- existem 16 fases;
- cada fase tem banco com 10 pílulas, checkpoint e área de cuidado;
- cada pílula tem texto, pergunta, 3 alternativas, resposta correta e dica;
- a fase 1 ativa 4 pílulas, e as demais ativam 5;
- cada fase tem quiz do Guardião do Portal com 3 alternativas;
- o quiz vem de uma pílula ativa da jogada;
- inicio, checkpoints e respawns nao caem em areas de cuidado;
- pílulas ficam em plataformas próximas e alcançáveis por critério conservador;
- `Game` inicializa;
- `abertura.png` carrega;
- sprite do Mig carrega;
- `ProgressStore` salva/carrega em arquivo local e em `localStorage` simulado, com fallback seguro;
- coleção histórica acumula descobertas sem duplicar entradas;
- fluxo basico de menu, nova sessão, checkpoint, cuidado, quiz, conclusão e final;
- fluxo basico por toque: menu, introducao, movimento, pulo, colecao, pausa, quiz e linha do tempo;
- detecção touch inicial por `maxTouchPoints`, `matchMedia` e desktop simulado;
- botão virtual esquerdo nao cobre Mig no inicio da fase;
- mensagem historica fica fixa e fica translucida quando Mig passa por tras;
- teste nao altera o save local.

### `scripts/build_pygbag_clean.py`

Cria uma copia minima em:

```text
build/pygbag_app
```

Depois executa:

```powershell
python -m pygbag --ume_block=0 --build build/pygbag_app
```

Motivos para usar este script:

- evita empacotar `.venv_brasil`;
- evita empacotar `caminhos_brasil_save.json`;
- empacota apenas os arquivos necessarios;
- aplica patch no `index.html` gerado para celular;
- preserva `--ume_block=0`, evitando travamento em "Ready to start !";
- injeta tela HTML de carregamento do projeto;
- injeta uma área HTML visualmente oculta com orientação básica para leitores de tela;
- injeta helper JavaScript para tentativa de fullscreen/orientacao paisagem;
- injeta titulo, descricao, theme-color e `manifest.webmanifest` basico;
- a tela de carregamento some quando o jogo chama `window.caminhosHideLoading`, por toque/click ou automaticamente apos alguns segundos.

Saida:

```text
build/pygbag_app/build/web
```

## 7. Estados Do Jogo

Estados em `src/game.py`:

- `menu`
- `level_select`
- `intro`
- `playing`
- `paused`
- `quiz`
- `completed`
- `collection`
- `final`
- `help`

Fluxo principal:

```text
menu -> intro -> playing -> quiz -> completed -> intro da proxima fase
ultima fase playing -> quiz -> completed -> final -> menu
```

Fluxos auxiliares:

```text
menu -> level_select -> intro
menu -> collection -> menu
menu -> help -> menu
playing -> paused -> playing
playing -> collection -> playing
playing -> help -> playing
quiz -> collection -> quiz
quiz -> help -> quiz
menu -> nova sessao temporaria -> intro da fase 1
```

## 8. Controles

Teclado:

- A/D ou setas esquerda/direita: mover.
- W, seta para cima ou espaco: pular.
- Enter: confirmar, iniciar fase ou avancar.
- N: nova jornada temporaria no menu.
- S: linha do tempo no menu.
- H: ajuda rapida.
- C: colecao historica.
- No Guardiao do Portal, setas ou W/S escolhem e Enter confirma.
- P: pausar ou continuar.
- R: reiniciar fase.
- M: voltar ao menu.
- Esc: reiniciar a tentativa atual e voltar para a tela inicial.

Toque:

- aparelho em modo paisagem;
- menu com botoes grandes para continuar, nova jornada, linha do tempo, colecao, ajuda e tela cheia;
- intro/conclusao/final avancam por toque no painel;
- botoes virtuais `<`, `>` e `Pular` durante a fase;
- botoes virtuais `P` e `C` durante a fase;
- Guardiao do Portal com alternativas grandes por toque;
- pausa com botoes grandes para continuar, reiniciar, menu e colecao;
- linha do tempo aceita toque em fases e arraste vertical;
- colecao aceita arraste vertical e botao Voltar.

## 9. Fases

1. `1500 - Chegada dos portugueses` (`coast`)
2. `Século XVI - Ciclo do açúcar` (`sugar`)
3. `Séculos XVII e XVIII - Interiorização do território` (`interior`)
4. `Século XVIII - Ciclo do ouro` (`mines`)
5. `1789 - Inconfidência Mineira` (`colonial_city`)
6. `1808 - Vinda da família real` (`court`)
7. `1822 - Independência` (`independence`)
8. `1822 a 1889 - Império` (`empire`)
9. `1888 - Abolição da escravidão` (`empire`)
10. `1889 - Proclamação da República` (`republic`)
11. `1889 a 1930 - Primeira Republica` (`rural_republic`)
12. `1930 a 1945 - Era Vargas` (`vargas`)
13. `1946 a 1964 - Experiência democrática` (`democracy`)
14. `1964 a 1985 - Ditadura militar` (`dictatorship`)
15. `1985 a 1988 - Redemocratização` (`redemocratization`)
16. `1988 até hoje - Brasil contemporâneo` (`contemporary`)

Cada fase deve ter:

- introdução curta;
- missão;
- nota histórica de conclusão;
- pergunta de reflexão;
- banco com 10 pílulas de conhecimento;
- seleção ativa de 4 pílulas na fase 1 e 5 pílulas nas demais;
- quiz do Guardião do Portal com 3 alternativas e dica de erro, ligado a uma pílula ativa;
- pelo menos 1 checkpoint;
- pelo menos 1 área de cuidado;
- portal final.

Regras atuais das pílulas:

- o sorteio das pílulas vale enquanto o jogo está aberto;
- voltar para a mesma fase na mesma sessão mantém a mesma seleção;
- iniciar nova jornada temporária com `N` refaz o sorteio;
- o Guardião do Portal só pergunta sobre uma pílula ativa da jogada;
- a coleção mostra progresso do banco completo da fase, por exemplo `7/10 descobertas`.

## 10. Modelo De Dados

`LevelData`:

```text
title
year
mission
historical_note
intro_text
theme
width
start_position
platforms
goal
pill_bank
hazards
checkpoints
```

`KnowledgePill`:

```text
info
question
options
correct_index
hint
```

`QuizData` mantém o mesmo formato para a pergunta apresentada pelo Guardião do Portal.

`Level` em `src/levels.py` converte tuplas para `pygame.Rect` e recebe a seleção ativa da sessão.

## 11. Conteúdo Histórico

Diretrizes obrigatórias:

- linguagem simples;
- frases curtas;
- tom acolhedor;
- sem descrições gráficas;
- sem glorificar processos violentos ou controversos;
- tratar temas sensíveis com respeito;
- valorizar povos indígenas, pessoas escravizadas, cidadania, diversidade e memória;
- manter perspectiva educativa, não panfletária.

Formula segura para temas sensiveis:

```text
Esse período trouxe mudanças importantes e também desafios para muitas pessoas. É um tema que deve ser estudado com cuidado e respeito.
```

## 12. Salvamento

Comportamento atual:

- `ProgressStore.load()` tenta carregar `localStorage` no navegador e `caminhos_brasil_save.json` no desktop;
- a chave web é `caminhos_brasil_save_v1`;
- se `localStorage`, arquivo ou JSON falharem, retorna progresso vazio ou cai para o comportamento local sem quebrar;
- `Enter` no menu continua a jornada salva;
- `N` no menu cria nova jornada temporária;
- em nova jornada temporária, `_save_progress()` não grava em disco nem em `localStorage`;
- iniciar nova jornada temporária refaz o sorteio das pílulas ativas e mantém a coleção acumulativa na sessão;
- coletar pílulas e concluir fases grava progresso apenas fora da sessão temporária.
- respostas do Guardião do Portal não são salvas nesta versão.

Formato:

```json
{
  "highest_unlocked_level": 0,
  "completed_levels": [0, 1],
  "collection_entries": [["Título da fase", "Texto da pílula"]]
}
```

Observacao:

- no navegador, a persistencia depende de `localStorage`; se o navegador bloquear esse recurso, o jogo continua funcionando sem quebrar.

## 13. Publicacao Web

Workflow:

```text
.github/workflows/pages.yml
```

Acionamento:

- push na branch `yolo_melhoria`;
- `workflow_dispatch` manual.

Etapas:

1. checkout;
2. Python 3.12;
3. `python -m pip install -r requirements.txt`;
4. `python scripts/build_pygbag_clean.py`;
5. upload de `build/pygbag_app/build/web`;
6. deploy para ambiente `github-pages`.

Comando local equivalente:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Cuidados:

- nao usar `pygbag .` como build final se `.venv_brasil` ou save local existirem na raiz;
- preservar `--ume_block=0`;
- preservar patch de `Ready to start !`;
- preservar a tela HTML de carregamento;
- preservar manifest/metadados web e helper de fullscreen;
- testar em celular real apos deploy;
- usar URL com query string para evitar cache, por exemplo `?v=5`.

## 14. Validacao Tecnica

Comandos recomendados:

```powershell
python -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall scripts
.\.venv_brasil\Scripts\python.exe scripts\smoke_tests.py
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Use `python scripts\smoke_tests.py` se o Python global tiver `pygame-ce`.

Quando alterar UI, também faça teste visual local ou em SDL dummy com screenshot.

Quando alterar publicacao, aguarde GitHub Actions ficar verde e teste a URL publicada.

Checklist curto de publicacao:

- desktop: abrir, iniciar fase, andar, pular, coletar pílula, quiz, pausar, coleção e linha do tempo;
- celular paisagem: carregamento, menu por toque, tela cheia, fase, botões `<`, `>`, `Pular`, `P`, `C` e quiz por toque;
- progresso: concluir fase, voltar ao menu, abrir linha do tempo e recarregar página;
- web: confirmar título da aba, manifest básico e ausência de bloqueio na tela de carregamento.

## 15. Teste Manual Mínimo

Local:

1. Abrir com `python main.py`.
2. Confirmar `abertura.png`.
3. Pressionar `Enter`.
4. Iniciar fase.
5. Mover e pular, conferindo dicas iniciais na fase 1.
6. Coletar pílula e observar "Boa descoberta!".
7. Abrir coleção com `C` e conferir contador de descobertas.
8. Abrir ajuda com `H`.
9. Pausar com `P` e conferir botões de pausa para toque.
10. Reiniciar com `R`.
11. Voltar ao menu com `M`.
12. Abrir linha do tempo com `S`.
13. Testar `N` para nova jornada temporária.
14. Responder ao Guardião do Portal.
15. Concluir uma fase.
16. Confirmar desbloqueio da fase seguinte.

Mobile web:

1. Abrir `https://msimoes38.github.io/caminhos_brasil/`.
2. Usar celular deitado.
3. Confirmar tela de carregamento com mensagem.
4. Se demorar, tocar para continuar.
5. Confirmar menu com convite para tocar.
6. Testar botão `Tela cheia`.
7. Tocar em continuar.
8. Tocar na introdução.
9. Usar `<`, `>` e `Pular`.
10. Abrir `C`, voltar.
11. Pausar com `P`, continuar pelos botões grandes.
12. Responder ao Guardião do Portal tocando em uma alternativa.
13. Abrir linha do tempo pelo menu.

## 16. Como Adicionar Uma Fase

1. Abrir `src/level_data.py`.
2. Adicionar `_make_level(...)` ou `LevelData` manual.
3. Definir título, ano, missão, nota histórica, intro, tema e banco com 10 pílulas.
4. Reusar tema existente ou criar novo em `src/backgrounds.py`.
5. Garantir plataformas alcançáveis.
6. Garantir pílulas ativas alcançáveis.
7. Garantir checkpoints e respawns seguros.
8. Garantir pergunta simples, 3 alternativas, resposta correta e dica curta em cada pílula.
9. Rodar smoke tests.
10. Atualizar README e SPEC se a quantidade/ordem de fases mudar.

## 17. Limites Conhecidos

- As fases compartilham gerador simples de layout.
- A interface base é 960x540.
- Mobile é paisagem apenas; retrato não tem layout dedicado.
- Save web usa `localStorage`, mas ainda deve ser validado em navegadores reais.
- Áudio em navegador pode variar por política do browser.
- `src/game.py` concentra muitas responsabilidades.
- A tela de carregamento HTML usa fallback por tempo/toque porque o sinal de carregamento do Pygbag pode variar no celular.

## 18. Prioridades Futuras

1. Testar audio e save web em navegadores reais.
2. Polir fases específicas sem aumentar complexidade.
3. Separar telas de `src/game.py` quando houver motivo claro.
4. Melhorar tela de carregamento com progresso real se houver API confiável.
5. Fazer teste com crianças/familiares e observar leitura/dificuldade.

## 19. Regras Para Proximos Agentes

- Leia `README.md`, `AGENTS.md`, `SPEC.MD`, `PROMPT_YOLO.MD`, `requirements.txt`, `main.py`, `src/`, `scripts/smoke_tests.py` e `scripts/build_pygbag_clean.py` antes de alterar.
- Preserve Python, Pygame-CE e Pygbag.
- Preserve loop `async` em `main.py`.
- Preserve controles de teclado e toque.
- Preserve `--ume_block=0`.
- Preserve a tela de carregamento web e seus fallbacks.
- Preserve metadados/manifest web e helper de tela cheia do build limpo.
- Preserve menu e pausa tocáveis em mobile.
- Não empacote venv nem save local no build.
- Não adicione dependências sem necessidade clara.
- Não altere conteúdo histórico para tom pesado.
- Não quebre nova jornada temporária com `N`.
- Não deixe checkpoints, respawns ou início em áreas de cuidado.
- Não deixe pílulas inalcançáveis.
- Preserve painel histórico fixo com translucidez quando Mig passa por trás.
- Atualize documentação quando mudar comportamento, arquitetura, publicação ou testes.
- Rode validações proporcionais ao risco da mudança.
