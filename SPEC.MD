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

## 2. Objetivos Do Produto

- Criar uma experiencia de plataforma 2D acessivel para criancas.
- Ensinar historia do Brasil com frases curtas e cuidadosas.
- Ter progressao clara por fases cronologicas.
- Manter jogabilidade simples: andar, pular, coletar e chegar ao objetivo.
- Permitir expansao incremental sem grandes refatoracoes.
- Preservar compatibilidade futura com navegador.

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

## 4. Estrutura De Arquivos

```text
main.py
requirements.txt
README.md
AGENTS.md
SPEC.MD
abertura.png
caminhos_brasil_save.json       # gerado localmente em execucao
assets/
  images/
    personagem.png
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
- eventos de teclado;
- estados do jogo;
- menu;
- abertura com `abertura.png`;
- linha do tempo;
- introducao de fase;
- gameplay;
- pausa;
- conclusao de fase;
- tela final;
- colecao historica;
- HUD;
- camera;
- coleta de fragmentos;
- checkpoints;
- areas de cuidado;
- salvamento de progresso.

O arquivo esta funcional, mas grande. Separar telas em `screens.py` ou `ui.py` pode ser uma melhoria futura, nao uma urgencia.

### `src/player.py`

Controla Mig:

- movimento horizontal;
- pulo;
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

Observacao importante:

- O layout das fases usa um gerador comum.
- Fragmentos devem permanecer alcancaveis pelo pulo atual.
- Checkpoints e respawns nao devem ficar sobre areas de cuidado.

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
- caminho do sprite;
- retangulos da folha de sprites.

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
menu -> nova sessao temporaria -> intro da fase 1
```

## 7. Controles

- A/D ou setas esquerda/direita: mover.
- W, seta para cima ou espaco: pular.
- Enter: confirmar, iniciar fase ou avancar.
- N: nova jornada temporaria no menu.
- S: linha do tempo no menu.
- C: colecao historica.
- P: pausar ou continuar.
- R: reiniciar fase.
- M: voltar ao menu em telas internas.
- Esc: sair.

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

## 11. Abertura E Assets

Tela inicial:

- Usa `abertura.png` em tela cheia.
- Se a imagem nao carregar, o jogo usa fallback desenhado em Pygame.
- O painel de menu e pequeno e translucido, para nao cobrir a arte principal.

Assets atuais:

- `abertura.png`: imagem principal do menu.
- `assets/images/personagem.png`: sprite animado do Mig durante o jogo.

Observacao:

- Existe tambem `personagem.png` na raiz do projeto em alguns ambientes. O sprite usado pelo jogo e `assets/images/personagem.png`.

## 12. Salvamento

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

## 13. Compatibilidade Com Pygbag

Decisoes ja tomadas:

- `main.py` usa loop `async`.
- Cenarios sao desenhados com Pygame.
- Sons sao gerados por codigo.
- Dados usam estruturas simples.
- Assets usam caminhos relativos.
- Dependencias sao minimas.

Pendencias para publicacao:

- Rodar `pygbag .`.
- Confirmar carregamento de `abertura.png`.
- Confirmar carregamento de `assets/images/personagem.png`.
- Avaliar se `src/progress.py` precisa de armazenamento especifico para navegador.
- Testar audio no navegador.

## 14. Validacao Tecnica

Comando padrao:

```powershell
python -m compileall main.py src
```

Se usar ambiente virtual local:

```powershell
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
```

Smoke tests recomendados por codigo:

- Importar `LEVELS` e conferir 16 fases.
- Garantir que cada fase tem fragmentos, hazards e checkpoints.
- Garantir que checkpoints nao colidem com hazards.
- Garantir que respawns nao caem em hazards.
- Inicializar `Game` com SDL dummy quando necessario.

## 15. Teste Manual Recomendado

1. Abrir o jogo.
2. Verificar imagem de abertura.
3. Pressionar `Enter`.
4. Iniciar fase 1.
5. Mover e pular.
6. Coletar fragmentos.
7. Abrir colecao com `C`.
8. Ativar checkpoint.
9. Tocar em area de cuidado.
10. Confirmar retorno seguro.
11. Reiniciar fase com `R`.
12. Pausar com `P`.
13. Concluir fase.
14. Confirmar desbloqueio da fase seguinte.
15. Abrir linha do tempo com `S`.
16. Pressionar `N` no menu e confirmar nova jornada temporaria.
17. Testar fase 2.
18. Testar uma fase intermediaria.
19. Testar fase 16.
20. Ver tela final.

## 16. Como Adicionar Uma Nova Fase

1. Abrir `src/level_data.py`.
2. Adicionar uma chamada a `_make_level(...)` em `LEVELS`, ou criar `LevelData` manual se precisar de layout especial.
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
7. Rodar validacao tecnica.
8. Testar manualmente.

## 17. Limites Conhecidos

- As fases compartilham gerador simples de layout.
- O jogo ainda precisa de teste completo com Pygbag.
- O salvamento atual e local por arquivo JSON.
- A interface esta otimizada para 960x540.
- `src/game.py` concentra muitas responsabilidades.
- Ainda ha espaco para melhorar sensacao de pulo e feedback visual.

## 18. Plano De Melhorias Sugerido

Prioridade curta e pragmatica:

1. Melhorar sensacao do pulo e controle no ar.
2. Adicionar feedback visual para fragmentos, checkpoint e objetivo final.
3. Melhorar plataformas e itens por tema sem usar assets pesados.
4. Criar tela simples de ajuda.
5. Melhorar colecao como album historico.
6. Testar `pygbag .`.
7. Adaptar salvamento para web se necessario.
8. Fazer rodada manual completa em todas as fases.

## 19. Regras Para Proximos Agentes

- Preserve o que ja funciona.
- Evite refatorar por vaidade.
- Nao adicione dependencias sem necessidade.
- Nao altere conteudo historico para tom pesado.
- Nao quebre a sessao temporaria com `N`.
- Nao deixe checkpoints ou respawns em areas de cuidado.
- Nao deixe fragmentos inalcancaveis.
- Atualize este SPEC quando mudar comportamento, arquitetura, fases ou fluxo.
