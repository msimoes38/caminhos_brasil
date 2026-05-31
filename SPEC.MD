# SPEC.MD

Especificacao tecnica e funcional do projeto Caminhos do Brasil.

Este documento e a fonte de continuidade para outro agente de IA ou desenvolvedor trabalhar no projeto sem depender do historico da conversa.

## 1. Visao Geral

Caminhos do Brasil e um jogo de plataforma 2D educativo sobre a historia do Brasil.

O jogador controla Mig, um menino ficticio nascido em 2018, que viaja por diferentes periodos historicos, de 1500 ao Brasil contemporaneo. O jogo combina plataforma simples, fragmentos historicos coletaveis, linha do tempo e colecao.

Objetivos do produto:

- ensinar historia de forma leve e respeitosa;
- ser adequado para criancas, com referencia principal por volta de 8 anos;
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

A versao atual esta jogavel e publicada para teste publico. Ela possui:

- tela inicial com `abertura.png`;
- menu com continuar, nova sessao temporaria, linha do tempo, colecao, ajuda e tela cheia no mobile;
- 16 fases historicas em ordem cronologica;
- introducao narrativa por fase;
- movimento lateral, pulo, gravidade, colisao, coyote time e buffer curto de pulo;
- camera horizontal;
- HUD com ajuste discreto para titulos longos;
- controles por teclado, mouse e toque;
- interface mobile em modo paisagem com menu tocavel e botoes virtuais semitransparentes;
- dicas contextuais nos primeiros segundos da fase 1;
- fragmentos historicos coletaveis;
- mensagens historicas fixas no topo, com translucidez quando Mig passa por tras;
- checkpoints seguros e respawn;
- areas de cuidado;
- portal final bloqueado ate todos os fragmentos da fase serem coletados;
- feedback visual e texto positivo para fragmento, checkpoint, cuidado, portal e conclusao;
- colecao historica em formato de album, com descoberta recente destacada;
- linha do tempo com fases liberadas, bloqueadas, proximas aventuras e concluidas;
- tela de pausa com botoes grandes para toque;
- tela final com resumo da jornada;
- sons simples gerados por codigo;
- save local tolerante a falhas;
- smoke tests permanentes;
- build Pygbag limpo com manifest/metadados web e deploy via GitHub Pages.

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
- controlar estados do jogo;
- desenhar menu, ajuda, linha do tempo, colecao, fase, pausa, conclusao e final;
- alternar textos e botoes para teclado ou toque quando o contexto mobile e detectado;
- gerenciar progresso, colecao e salvamento;
- desenhar HUD, mensagens historicas e botoes virtuais;
- mostrar dicas contextuais da fase 1 e feedback positivo de coleta;
- solicitar fullscreen no navegador quando possivel;
- acionar efeitos visuais e sons;
- coletar fragmentos;
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

Contem:

- dataclasses `FragmentData` e `LevelData`;
- constantes de chao;
- geradores simples de plataformas, fragmentos, areas de cuidado e checkpoints;
- lista `LEVELS` com 16 fases.

Regras criticas:

- fragmentos devem permanecer em plataformas alcancaveis;
- checkpoints nao podem colidir com areas de cuidado;
- respawn de checkpoint nao pode cair em area de cuidado;
- fase 2 ja exigiu cuidado especial com checkpoint e fragmentos.

### `src/levels.py`

Converte os dados crus de `src/level_data.py` para objetos usados pelo Pygame.

Funcoes publicas:

- `get_level_count()`
- `get_level_title(index)`
- `get_level_plain_title(index)`
- `get_level_fragment_count(index)`
- `get_total_fragment_count()`
- `create_level(index)`

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

Salva e carrega progresso local em:

```text
caminhos_brasil_save.json
```

Campos:

- `highest_unlocked_level`
- `completed_levels`
- `collection_entries`

Requisitos:

- falha de leitura nao pode quebrar o jogo;
- falha de escrita nao pode quebrar o jogo;
- save corrompido deve voltar para progresso vazio;
- sessao temporaria iniciada com `N` nao deve sobrescrever o save;
- adaptacao de armazenamento web deve acontecer aqui quando for prioridade.

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
- cada fase tem fragmentos, checkpoint e area de cuidado;
- inicio, checkpoints e respawns nao caem em areas de cuidado;
- fragmentos ficam em plataformas proximas e alcancaveis por criterio conservador;
- `Game` inicializa;
- `abertura.png` carrega;
- sprite do Mig carrega;
- fluxo basico de menu, nova sessao, checkpoint, cuidado, conclusao e final;
- fluxo basico por toque: menu, introducao, movimento, pulo, colecao, pausa e linha do tempo;
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
- `completed`
- `collection`
- `final`
- `help`

Fluxo principal:

```text
menu -> intro -> playing -> completed -> intro da proxima fase
ultima fase completed -> final -> menu
```

Fluxos auxiliares:

```text
menu -> level_select -> intro
menu -> collection -> menu
menu -> help -> menu
playing -> paused -> playing
playing -> collection -> playing
playing -> help -> playing
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
- pausa com botoes grandes para continuar, reiniciar, menu e colecao;
- linha do tempo aceita toque em fases e arraste vertical;
- colecao aceita arraste vertical e botao Voltar.

## 9. Fases

1. `1500 - Chegada dos portugueses` (`coast`)
2. `Seculo XVI - Ciclo do acucar` (`sugar`)
3. `Seculos XVII e XVIII - Interiorizacao do territorio` (`interior`)
4. `Seculo XVIII - Ciclo do ouro` (`mines`)
5. `1789 - Inconfidencia Mineira` (`colonial_city`)
6. `1808 - Vinda da familia real` (`court`)
7. `1822 - Independencia` (`independence`)
8. `1822 a 1889 - Imperio` (`empire`)
9. `1888 - Abolicao da escravidao` (`empire`)
10. `1889 - Proclamacao da Republica` (`republic`)
11. `1889 a 1930 - Primeira Republica` (`rural_republic`)
12. `1930 a 1945 - Era Vargas` (`vargas`)
13. `1946 a 1964 - Experiencia democratica` (`democracy`)
14. `1964 a 1985 - Ditadura militar` (`dictatorship`)
15. `1985 a 1988 - Redemocratizacao` (`redemocratization`)
16. `1988 ate hoje - Brasil contemporaneo` (`contemporary`)

Cada fase deve ter:

- introducao curta;
- missao;
- nota historica de conclusao;
- pergunta de reflexao;
- pelo menos 3 fragmentos;
- pelo menos 1 checkpoint;
- pelo menos 1 area de cuidado;
- portal final.

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
fragments
hazards
checkpoints
```

`FragmentData`:

```text
area
info
```

`Level` em `src/levels.py` converte tuplas para `pygame.Rect`.

## 11. Conteudo Historico

Diretrizes obrigatorias:

- linguagem simples;
- frases curtas;
- tom acolhedor;
- sem descricoes graficas;
- sem glorificar processos violentos ou controversos;
- tratar temas sensiveis com respeito;
- valorizar povos indigenas, pessoas escravizadas, cidadania, diversidade e memoria;
- manter perspectiva educativa, nao panfletaria.

Formula segura para temas sensiveis:

```text
Esse periodo trouxe mudancas importantes e tambem desafios para muitas pessoas. E um tema que deve ser estudado com cuidado e respeito.
```

## 12. Salvamento

Comportamento atual:

- `ProgressStore.load()` tenta carregar `caminhos_brasil_save.json`;
- se falhar, retorna progresso vazio;
- `Enter` no menu continua a jornada salva;
- `N` no menu cria nova jornada temporaria;
- em nova jornada temporaria, `_save_progress()` nao grava em disco;
- coletar fragmentos e concluir fases grava progresso apenas fora da sessao temporaria.

Formato:

```json
{
  "highest_unlocked_level": 0,
  "completed_levels": [0, 1],
  "collection_entries": [["Titulo da fase", "Texto do fragmento"]]
}
```

Limite conhecido:

- no navegador, o save por arquivo JSON pode nao persistir como esperado. A adaptacao futura deve ser feita em `src/progress.py`, preferencialmente preservando tolerancia a falhas.

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

Quando alterar UI, tambem faca teste visual local ou em SDL dummy com screenshot.

Quando alterar publicacao, aguarde GitHub Actions ficar verde e teste a URL publicada.

Checklist curto de publicacao:

- desktop: abrir, iniciar fase, andar, pular, coletar, pausar, colecao e linha do tempo;
- celular paisagem: carregamento, menu por toque, tela cheia, fase, botoes `<`, `>`, `Pular`, `P` e `C`;
- progresso: concluir fase, voltar ao menu, abrir linha do tempo e recarregar pagina;
- web: confirmar titulo da aba, manifest basico e ausencia de bloqueio na tela de carregamento.

## 15. Teste Manual Minimo

Local:

1. Abrir com `python main.py`.
2. Confirmar `abertura.png`.
3. Pressionar `Enter`.
4. Iniciar fase.
5. Mover e pular, conferindo dicas iniciais na fase 1.
6. Coletar fragmento e observar "Boa descoberta!".
7. Abrir colecao com `C` e conferir contador de descobertas.
8. Abrir ajuda com `H`.
9. Pausar com `P` e conferir botoes de pausa para toque.
10. Reiniciar com `R`.
11. Voltar ao menu com `M`.
12. Abrir linha do tempo com `S`.
13. Testar `N` para nova jornada temporaria.
14. Concluir uma fase.
15. Confirmar desbloqueio da fase seguinte.

Mobile web:

1. Abrir `https://msimoes38.github.io/caminhos_brasil/`.
2. Usar celular deitado.
3. Confirmar tela de carregamento com mensagem.
4. Se demorar, tocar para continuar.
5. Confirmar menu com convite para tocar.
6. Testar botao `Tela cheia`.
7. Tocar em continuar.
8. Tocar na introducao.
9. Usar `<`, `>` e `Pular`.
10. Abrir `C`, voltar.
11. Pausar com `P`, continuar pelos botoes grandes.
12. Abrir linha do tempo pelo menu.

## 16. Como Adicionar Uma Fase

1. Abrir `src/level_data.py`.
2. Adicionar `_make_level(...)` ou `LevelData` manual.
3. Definir titulo, ano, missao, nota historica, intro, tema e fragmentos.
4. Reusar tema existente ou criar novo em `src/backgrounds.py`.
5. Garantir plataformas alcancaveis.
6. Garantir fragmentos alcancaveis.
7. Garantir checkpoints e respawns seguros.
8. Rodar smoke tests.
9. Atualizar README e SPEC se a quantidade/ordem de fases mudar.

## 17. Limites Conhecidos

- As fases compartilham gerador simples de layout.
- A interface base e 960x540.
- Mobile e paisagem apenas; retrato nao tem layout dedicado.
- Save web ainda precisa de validacao/adaptacao.
- Audio em navegador pode variar por politica do browser.
- `src/game.py` concentra muitas responsabilidades.
- A tela de carregamento HTML usa fallback por tempo/toque porque o sinal de carregamento do Pygbag pode variar no celular.

## 18. Prioridades Futuras

1. Adaptar save para armazenamento web.
2. Testar audio e save em navegadores reais.
3. Polir fases especificas sem aumentar complexidade.
4. Separar telas de `src/game.py` quando houver motivo claro.
5. Melhorar tela de carregamento com progresso real se houver API confiavel.
6. Fazer teste com criancas/familiares e observar leitura/dificuldade.

## 19. Regras Para Proximos Agentes

- Leia `README.md`, `AGENTS.md`, `SPEC.MD`, `PROMPT_YOLO.MD`, `requirements.txt`, `main.py`, `src/`, `scripts/smoke_tests.py` e `scripts/build_pygbag_clean.py` antes de alterar.
- Preserve Python, Pygame-CE e Pygbag.
- Preserve loop `async` em `main.py`.
- Preserve controles de teclado e toque.
- Preserve `--ume_block=0`.
- Preserve a tela de carregamento web e seus fallbacks.
- Preserve metadados/manifest web e helper de tela cheia do build limpo.
- Preserve menu e pausa tocaveis em mobile.
- Nao empacote venv nem save local no build.
- Nao adicione dependencias sem necessidade clara.
- Nao altere conteudo historico para tom pesado.
- Nao quebre nova jornada temporaria com `N`.
- Nao deixe checkpoints, respawns ou inicio em areas de cuidado.
- Nao deixe fragmentos inalcancaveis.
- Preserve painel historico fixo com translucidez quando Mig passa por tras.
- Atualize documentacao quando mudar comportamento, arquitetura, publicacao ou testes.
- Rode validacoes proporcionais ao risco da mudanca.
