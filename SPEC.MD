# SPEC.MD

Especificacao tecnica e funcional do projeto Caminhos do Brasil.

Este documento existe para que outro agente de IA, ou outro desenvolvedor, consiga continuar o projeto sem reconstruir o contexto da conversa.

## 1. Visao Geral

Caminhos do Brasil e um jogo de plataforma 2D educativo sobre a historia do Brasil.

O personagem principal e Mig, um menino ficticio nascido em 2018. Ele viaja por diferentes periodos historicos, de 1500 ao Brasil contemporaneo, coletando fragmentos historicos e avancando por uma linha do tempo.

O jogo deve ser:

- leve;
- infantil;
- educativo;
- respeitoso;
- simples de executar;
- preparado para futura publicacao web com Pygbag.

## 2. Estado Atual Do Produto

A versao atual esta pronta para um primeiro teste publico local. Ela possui:

- tela inicial com `abertura.png`;
- menu com continuar, nova sessao temporaria, linha do tempo, colecao e ajuda;
- 16 fases historicas em ordem cronologica;
- movimento lateral, colisao, gravidade, coyote time e buffer curto de pulo;
- camera horizontal;
- HUD com ajuste discreto de fonte para titulos longos;
- controles por toque para celular em modo paisagem no navegador;
- fragmentos historicos coletaveis;
- mensagens historicas fixas no topo, com translucidez quando Mig passa por tras;
- checkpoints seguros;
- areas de cuidado;
- portal final bloqueado ate todos os fragmentos da fase serem coletados;
- feedback visual para fragmento, checkpoint, cuidado, portal e conclusao;
- colecao em formato de album;
- linha do tempo com destaque de fase concluida/proxima;
- sons simples gerados por codigo;
- save local tolerante a falhas;
- smoke tests permanentes;
- build Pygbag limpo validado por script.

## 3. Tecnologias

Dependencias:

```text
pygame-ce==2.5.7
pygbag==0.9.2
```

Arquitetura base:

- Python como linguagem principal.
- Pygame-CE para execucao local.
- Pygbag como alvo futuro de publicacao web.
- Dados das fases mantidos em Python em `src/level_data.py`.
- Cenarios desenhados por codigo em `src/backgrounds.py`.
- Sons simples gerados por codigo em `src/sounds.py`.
- Sem dependencias novas alem de Pygame-CE e Pygbag.

## 4. Estrutura De Arquivos

```text
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
```

## 5. Arquivos Principais

### `main.py`

Ponto de entrada.

Requisito importante:

- Deve manter loop `async` para facilitar compatibilidade com Pygbag.

Fluxo atual:

```python
game = Game()
await game.run()
```

### `src/game.py`

Controla:

- inicializacao do Pygame;
- loop principal;
- eventos de teclado, mouse e toque;
- estados do jogo;
- menu;
- ajuda rapida;
- abertura com `abertura.png`;
- linha do tempo;
- introducao de fase;
- gameplay;
- pausa;
- conclusao de fase;
- tela final;
- colecao historica;
- HUD;
- botoes virtuais de toque;
- camera;
- efeitos visuais leves;
- mensagens historicas e feedbacks curtos no topo da tela;
- coleta de fragmentos;
- checkpoints;
- areas de cuidado;
- salvamento de progresso.

O arquivo esta funcional, mas grande. Separar telas em `screens.py` ou `ui.py` pode ser uma melhoria futura, nao uma urgencia.

### `src/player.py`

Controla Mig:

- movimento horizontal;
- direcao e pulo vindos do teclado ou dos botoes virtuais;
- aceleracao e desaceleracao simples;
- controle no ar;
- pulo;
- coyote time;
- buffer curto de pulo;
- limite de velocidade de queda;
- gravidade;
- colisao horizontal e vertical;
- limites do mundo;
- estado `on_ground`;
- animacao com folha de sprites;
- fallback visual caso o sprite nao carregue.

O sprite usado durante o jogo fica em:

```text
assets/images/personagem.png
```

### `src/level_data.py`

Contem:

- dataclasses `FragmentData` e `LevelData`;
- constantes de chao;
- geradores simples de plataformas, perigos, checkpoints e fragmentos;
- lista `LEVELS` com 16 fases.

Observacoes importantes:

- O layout das fases usa um gerador comum.
- Fragmentos devem permanecer alcancaveis pelo pulo atual.
- Checkpoints e respawns nao devem ficar sobre areas de cuidado.
- A fase 2 ja exigiu cuidado especial com checkpoints e fragmentos.

### `src/levels.py`

Converte dados crus em objetos usados pelo Pygame.

Funcoes uteis:

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

Campos salvos:

- `highest_unlocked_level`
- `completed_levels`
- `collection_entries`

Requisitos:

- Falha de leitura nao pode quebrar o jogo.
- Falha de escrita nao pode quebrar o jogo.
- A sessao temporaria iniciada com `N` nao deve sobrescrever o save.
- Para web, este modulo e o ponto principal de adaptacao.

### `src/sounds.py`

Gera sons por codigo, sem depender de arquivos de audio.

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

Se o mixer falhar, o jogo deve continuar sem audio.

### `src/settings.py`

Define constantes:

- tamanho da tela;
- FPS;
- cores;
- fisica;
- coyote time;
- buffer de pulo;
- caminho do sprite;
- retangulos da folha de sprites.

### `scripts/smoke_tests.py`

Valida regras basicas sem abrir janela real:

- quantidade de fases;
- presenca de fragmentos, checkpoints e areas de cuidado;
- inicio, checkpoints e respawns fora de areas de cuidado;
- fragmentos apoiados em plataformas proximas e alcancaveis por criterio conservador;
- `Game` inicializa em SDL dummy;
- abertura e sprite carregam;
- fluxo basico de menu, nova sessao, colecao, checkpoint, cuidado, conclusao e final;
- comportamento do painel de mensagem historica: posicao estavel e translucidez quando Mig cruza sua area.

### `scripts/build_pygbag_clean.py`

Prepara uma copia minima em `build/pygbag_app` e executa:

```powershell
python -m pygbag --ume_block=0 --build build/pygbag_app
```

Motivo: `pygbag .` na raiz pode empacotar `.venv_brasil` e o save local quando esses arquivos existem dentro do projeto.

O `--ume_block=0` evita que celulares fiquem presos na tela "Ready to start !" antes do jogo iniciar. O script ainda mantem um fallback para ajustar o `index.html` caso uma versao futura do Pygbag volte a gerar esse bloqueio.

## 6. Estados Do Jogo

Estados definidos em `src/game.py`:

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
playing -> paused -> playing
telas relevantes -> collection -> estado anterior
telas relevantes -> help -> estado anterior
menu -> nova sessao temporaria -> intro da fase 1
```

## 7. Controles

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
- Esc: sair.

Toque em celular ou tela touch:

- Usar o aparelho deitado, em modo paisagem.
- Tocar nas opcoes do menu para continuar, nova sessao, linha do tempo, colecao e ajuda.
- Durante a fase, usar os botoes virtuais `<`, `>` e `Pular`.
- Tocar em `P` para pausar e em `C` para abrir a colecao.
- Na linha do tempo e na colecao, tocar nas opcoes ou arrastar para rolar.

## 8. Fases Implementadas

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

## 9. Modelo De Dados Da Fase

Cada fase usa `LevelData`:

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

Cada fragmento usa `FragmentData`:

```text
area
info
```

Regras esperadas:

- Cada fase deve ter pelo menos 3 fragmentos.
- Cada fase deve ter pelo menos 1 checkpoint.
- Cada fase deve ter pelo menos 1 area de cuidado.
- O objetivo final so deve concluir a fase apos todos os fragmentos serem coletados.
- O smoke test deve continuar passando quando layouts mudarem.

## 10. Conteudo Historico

Diretrizes obrigatorias:

- Linguagem simples.
- Frases curtas.
- Tom acolhedor.
- Sem descricoes graficas.
- Sem glorificar processos violentos ou controversos.
- Tratar temas sensiveis com cuidado e respeito.
- Valorizar povos indigenas, pessoas escravizadas, cidadania, diversidade e memoria.

Formula segura para temas sensiveis:

```text
Esse periodo trouxe mudancas importantes e tambem desafios para muitas pessoas. E um tema que deve ser estudado com cuidado e respeito.
```

Na interface, os fragmentos aparecem como mensagens curtas com "Voce sabia?". O texto salvo na colecao continua sendo o texto historico limpo, sem prefixo extra.

## 11. Feedback Visual E Motivacao

Elementos atuais:

- fragmentos brilham e flutuam levemente;
- titulos longos no HUD usam fonte um pouco menor para caber no painel;
- coleta gera pequenas particulas;
- mensagens historicas aparecem em painel fixo no topo; o painel fica translucido quando Mig passa por tras, evitando saltos de layout;
- checkpoint tem bandeira com movimento e efeito ao ativar;
- areas de cuidado mostram padrao listrado e avisos triangulares;
- portal muda de bloqueado para liberado;
- tocar no portal sem todos os fragmentos mostra mensagem curta;
- conclusao de fase mostra medalha, nota historica e pergunta;
- linha do tempo destaca fase concluida e proxima fase;
- tela final mostra fases concluidas e total de fragmentos.

## 12. Abertura E Assets

Tela inicial:

- Usa `abertura.png` em tela cheia.
- Se a imagem nao carregar, o jogo usa fallback desenhado em Pygame.
- O painel de menu e translucido, para nao cobrir totalmente a arte principal.

Assets atuais:

- `abertura.png`: imagem principal do menu.
- `assets/images/personagem.png`: sprite animado do Mig durante o jogo.

Observacao:

- Existe tambem `personagem.png` na raiz do projeto em alguns ambientes. O sprite usado pelo jogo e `assets/images/personagem.png`.

## 13. Salvamento

Comportamento atual:

- Ao abrir o jogo, `ProgressStore.load()` tenta carregar `caminhos_brasil_save.json`.
- `Enter` no menu continua a jornada salva.
- `N` no menu inicia nova jornada temporaria.
- Na nova jornada temporaria, `Game._save_progress()` nao grava em disco.
- Coletar fragmentos e concluir fases salva progresso apenas fora da sessao temporaria.

Formato do save:

```json
{
  "highest_unlocked_level": 0,
  "completed_levels": [0, 1],
  "collection_entries": [["Titulo da fase", "Texto do fragmento"]]
}
```

## 14. Compatibilidade Com Pygbag

Decisoes ja tomadas:

- `main.py` usa loop `async`.
- Cenarios sao desenhados com Pygame.
- Sons sao gerados por codigo.
- Dados usam estruturas simples.
- Assets usam caminhos relativos.
- Dependencias sao minimas.

Validacoes feitas:

- `pygbag .` foi tentado na raiz. Ele iniciou e gerou build, mas tentou empacotar `.venv_brasil` e o save local porque esses itens estavam dentro da pasta do projeto.
- `scripts/build_pygbag_clean.py` foi criado e validado. Ele empacotou apenas 13 arquivos do jogo.
- O build limpo usa `--ume_block=0` para nao depender do toque inicial do Pygbag na tela "Ready to start !", que pode falhar em navegadores de celular.

Comando recomendado para build web:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Saida:

```text
build/pygbag_app/build/web
```

Pendencias antes de publicacao:

- Abrir o build em navegador real.
- Testar audio no navegador.
- Adaptar ou complementar `src/progress.py` para armazenamento web.

## 15. Validacao Tecnica

Comando padrao:

```powershell
python -m compileall main.py src
```

Se usar ambiente virtual local:

```powershell
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
```

Smoke test:

```powershell
python scripts\smoke_tests.py
.\.venv_brasil\Scripts\python.exe scripts\smoke_tests.py
```

Use o comando da venv quando o Python global nao tiver `pygame-ce` instalado.

Tambem e util renderizar telas em SDL dummy quando houver mudancas de UI.
O smoke test tambem cobre fluxo basico por toque: menu, introducao, movimento, pulo, colecao, pausa e linha do tempo.

## 16. Teste Manual Recomendado

1. Abrir o jogo.
2. Verificar imagem de abertura.
3. Pressionar `Enter`.
4. Iniciar fase 1.
5. Testar `H`.
6. Mover e pular.
7. Coletar fragmentos.
8. Abrir colecao com `C`.
9. Ativar checkpoint.
10. Tocar em area de cuidado.
11. Confirmar retorno seguro.
12. Reiniciar fase com `R`.
13. Pausar com `P`.
14. Concluir fase.
15. Confirmar desbloqueio da fase seguinte.
16. Abrir linha do tempo com `S`.
17. Pressionar `N` no menu e confirmar nova jornada temporaria.
18. Testar fase 2.
19. Testar uma fase intermediaria.
20. Testar fase 16.
21. Ver tela final.
22. Fechar e abrir novamente para conferir save.

Teste mobile recomendado:

1. Abrir a versao publicada no celular.
2. Usar o aparelho em modo paisagem.
3. Confirmar que a tela "Ready to start !" nao fica travada.
4. Tocar em continuar e iniciar uma fase.
5. Mover com `<` e `>`.
6. Pular com `Pular`.
7. Abrir colecao com `C`.
8. Pausar com `P`.
9. Abrir linha do tempo pelo menu.

## 17. Como Adicionar Uma Nova Fase

1. Abrir `src/level_data.py`.
2. Adicionar uma chamada a `_make_level(...)`, ou criar `LevelData` manual se precisar de layout especial.
3. Definir:
   - `title`
   - `year`
   - `mission`
   - `historical_note`
   - `intro_text`
   - `theme`
   - `fragment_infos`
4. Usar tema existente ou adicionar novo em `src/backgrounds.py`.
5. Garantir fragmentos alcancaveis.
6. Garantir checkpoints seguros.
7. Rodar `python scripts\smoke_tests.py`.
8. Rodar validacao tecnica.
9. Testar manualmente.

## 18. Limites Conhecidos

- As fases compartilham gerador simples de layout.
- O salvamento atual e local por arquivo JSON.
- A interface esta otimizada para 960x540.
- A experiencia mobile e pensada para modo paisagem; modo retrato nao tem layout dedicado.
- `src/game.py` concentra muitas responsabilidades.
- O build Pygbag limpo passa e e publicado via GitHub Pages.
- Audio e save em navegador precisam de validacao especifica.

## 19. Regras Para Proximos Agentes

- Preserve o que ja funciona.
- Evite refatorar por vaidade.
- Nao adicione dependencias sem necessidade.
- Nao altere conteudo historico para tom pesado.
- Nao quebre a sessao temporaria com `N`.
- Nao deixe checkpoints ou respawns em areas de cuidado.
- Nao deixe fragmentos inalcancaveis.
- Preserve controles por toque em modo paisagem ao alterar HUD, pausa, colecao ou linha do tempo.
- Preserve `--ume_block=0` em `scripts/build_pygbag_clean.py` para evitar travamento no carregamento mobile do Pygbag.
- Rode `python scripts\smoke_tests.py` quando alterar fases, fisica, player, save ou fluxo.
- Ao alterar HUD ou mensagens historicas, preservar a posicao estavel do painel e a translucidez quando Mig passar por tras.
- Use `scripts/build_pygbag_clean.py` para build web enquanto `.venv_brasil` e save local existirem na raiz.
- Atualize este SPEC quando mudar comportamento, arquitetura, fases ou fluxo.
