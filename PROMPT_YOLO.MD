# PROMPT YOLO - Caminhos do Brasil

Voce e um agente de IA trabalhando no projeto `caminhos_brasil`, um jogo educativo 2D em Python/Pygame-CE sobre a historia do Brasil para criancas. Trabalhe em modo autonomo, incremental e pragmatico: leia o contexto, implemente melhorias pequenas e funcionais, valide, atualize documentacao e entregue um resumo claro.

## Contexto Obrigatorio

Antes de alterar codigo, leia:

- `AGENTS.md`
- `README.md`
- `SPEC.MD`
- `requirements.txt`
- `main.py`
- `src/game.py`
- `src/progress.py`
- `src/backgrounds.py`
- `src/level_data.py`
- `src/levels.py`
- `scripts/smoke_tests.py`
- `scripts/build_pygbag_clean.py`

Estado atual importante:

- O jogo tem 16 fases historicas, controles por teclado/toque, colecao, linha do tempo, quiz do Guardiao e build Pygbag limpo.
- A versao publicada fica em `https://msimoes38.github.io/caminhos_brasil/`.
- O build web usa `scripts/build_pygbag_clean.py`, preservando `--ume_block=0`, tela HTML de carregamento, manifest/metadados e helper de tela cheia.
- O save desktop usa `caminhos_brasil_save.json`.
- O save web usa `localStorage` com a chave `caminhos_brasil_save_v1`, preferindo helpers JS injetados pelo build limpo.
- A colecao ja tem visual de album com cards.
- A linha do tempo ja reserva uma coluna de status.
- O menu touch ja tenta cobrir texto confuso do rodape da abertura.
- Nao adicione dependencias novas ao projeto sem necessidade clara.
- Nao adicione Selenium ao `requirements.txt`; se precisar dele para teste publicado, instale apenas na venv local e nao versionar.
- Preserve Python, Pygame-CE, Pygbag e o loop `async` de `main.py`.
- Preserve linguagem infantil, acolhedora e respeitosa.

## Atualizacao Da Ultima Rodada

Ja foram implementados nesta rodada:

- ponte JS no build limpo com `window.caminhosTouchContext`, `window.caminhosReadSave()`, `window.caminhosWriteSave(data)` e `window.caminhosClearSave()`;
- `Game._detect_touch_context()` consulta a flag JS antes dos fallbacks e rechecagem tardia no menu antes de qualquer uso do teclado;
- `ProgressStore` usa os helpers JS de save como caminho principal e preserva fallback direto para `platform.window.localStorage`;
- smoke tests para flag JS de touch, helpers JS de save e injeção idempotente da ponte web no `index.html`;
- deteccao inicial de touch/mobile reforcada em `src/game.py`, usando `maxTouchPoints`, `matchMedia`, `ontouchstart` e user agent como fallback leve;
- faixa inferior consistente no menu inicial para cobrir a chamada fixa da arte de abertura e evitar instrucoes duplicadas;
- polimento leve do litoral da fase 1, destaque sutil da primeira pilula e portal liberado com brilho mais claro;
- orientacao HTML acessivel injetada pelo build limpo fora do canvas;
- smoke tests para a nova deteccao touch simulada.

Proximas rodadas devem priorizar validacao em celular real, teste publicado de persistencia web e novos polimentos pequenos de fase.

## Diagnostico Da Versao Publicada

Uma verificacao com Selenium em Chrome headless conseguiu abrir a URL publicada, carregar o canvas `960x540`, esconder a tela de carregamento e interagir com:

- menu desktop;
- introducao da fase 1;
- inicio da fase 1;
- movimento e pulo;
- colecao;
- linha do tempo;
- ajuda.

Tambem foi confirmado que o pacote publicado `pygbag_app.apk` contem as melhorias recentes, incluindo `localStorage`, album da colecao e novos detalhes visuais.

Problemas ou oportunidades observados antes da ultima rodada:

1. Em emulacao mobile/touch, o navegador reportou `navigator.maxTouchPoints = 1`, `pointer: coarse` e `hover: none`, mas o jogo ainda abriu com menu de teclado. Ha correcao local via `window.caminhosTouchContext`, mas ela ainda precisa ser validada apos deploy.
2. No menu desktop, a imagem `abertura.png` ainda mostra "PRESSIONE ENTER..." enquanto o painel tambem mostra atalhos. Isso e redundante e pode poluir a leitura.
3. O save web agora tem helpers JS no build local, mas ainda precisa de um teste real de persistencia no navegador publicado: concluir uma fase, recarregar e confirmar fase 2 liberada.
4. A fase 1 funciona, mas o visual do gameplay e bem mais simples do que a tela de abertura. Pequenos detalhes e feedbacks podem reduzir essa diferenca.
5. Como o jogo roda em canvas, leitores de tela e ferramentas de acessibilidade enxergam pouco. Vale adicionar alguma orientacao HTML simples/sem impacto visual.

## Objetivo Da Rodada

Melhorar a experiencia publicada, principalmente em mobile/touch e primeiro contato do jogador, sem grandes refatoracoes.

Priorize nesta ordem:

1. Validar no publicado a deteccao inicial de touch/mobile corrigida pela flag JS.
2. Validar persistencia web real com os helpers JS.
3. Criar teste Selenium opcional, se isso ajudar a repetir a validacao sem nova dependencia versionada.
4. Polir primeira fase e feedbacks visuais leves.
5. Melhorar acessibilidade/instrucoes fora do canvas.

## Melhorias A Implementar

### 1. Deteccao Touch/Mobile Mais Robusta

Problema observado:

- Em Chrome com emulacao mobile, `navigator.maxTouchPoints`, `pointer: coarse` e `hover: none` indicavam toque, mas o jogo desenhou o menu desktop.

Comportamento esperado:

- Em navegador mobile/touch, o menu inicial deve abrir diretamente no layout touch.
- O menu touch deve mostrar botoes grandes e a faixa "Toque em uma opcao para comecar".
- Os botoes virtuais da fase devem aparecer quando o contexto touch for detectado.
- Teclado em desktop deve continuar usando layout desktop.
- Se o usuario tocar/clicar na tela, o jogo tambem deve ativar o modo touch como ja acontece.

Sugestao tecnica:

- Reforcar `Game._detect_touch_context()` em `src/game.py`.
- Alem de `navigator.maxTouchPoints`, verificar com cuidado:
  - `window.matchMedia("(pointer: coarse)").matches`
  - `window.matchMedia("(hover: none)").matches`
  - `"ontouchstart" in window`
  - `navigator.userAgent` apenas como fallback leve, sem depender exclusivamente dele.
- Usar `try/except` para nao quebrar desktop nem Pygbag.
- Se alguma API nao existir, ignorar e continuar.

Testes esperados:

- Atualizar `scripts/smoke_tests.py` com simulacao simples de `platform.window`, `navigator` e `matchMedia`.
- Verificar que `_detect_touch_context()` retorna `True` quando:
  - `maxTouchPoints > 0`;
  - `matchMedia("(pointer: coarse)")` retorna `matches=True`.
- Verificar que retorna `False` em contexto desktop simulado.
- Renderizar screenshot dummy do menu touch, se possivel.

### 2. Limpeza Visual Do Menu Inicial

Problema observado:

- No desktop publicado, a imagem de abertura mostra "PRESSIONE ENTER PARA COMECAR" no rodape, enquanto o painel do jogo mostra "Enter: continuar".
- Em mobile, esse texto da imagem pode competir com a faixa de orientacao por toque.

Comportamento esperado:

- O menu deve ter uma mensagem principal clara, sem duplicidade visual confusa.
- No desktop, pode manter uma faixa discreta ou cobrir o texto da imagem quando o painel estiver aberto.
- No touch, a faixa "Toque em uma opcao para comecar" deve cobrir totalmente qualquer texto fixo da imagem.
- Nao edite `abertura.png` se uma solucao por desenho no Pygame for suficiente.

Sugestao tecnica:

- Centralizar a regra em `src/game.py`, perto de `_draw_menu`.
- Criar/ajustar helper para desenhar uma faixa inferior consistente tanto para touch quanto desktop.
- No desktop, usar texto curto como "Escolha uma opcao no painel".
- Garantir que a faixa nao esconda botoes nem informacoes do painel.

### 3. Persistencia Web: Teste Real E Ajustes

O save web ja foi implementado, mas precisa ser validado na pratica.

Comportamento esperado:

- Em ambiente web, concluir a fase 1 deve salvar progresso em `localStorage`.
- Ao recarregar a pagina, o menu/linha do tempo deve manter a fase 2 liberada.
- A colecao deve persistir entradas descobertas.
- Se `localStorage` falhar, o jogo deve continuar sem quebrar.
- A nova jornada temporaria com `N` nao deve gravar progresso permanente.

Sugestao tecnica:

- Revisar `src/progress.py` sem mudar formato de save.
- Se necessario, ajustar a deteccao de web/localStorage.
- Evitar qualquer dependencia nova.
- Criar teste automatizado local para `ProgressStore` ja existe; amplie somente se encontrar lacuna.

Teste publicado recomendado:

- Usar Chrome/Selenium apenas como ferramenta local de teste, sem versionar dependencia:
  - instalar com `.\.venv_brasil\Scripts\python.exe -m pip install selenium` se necessario;
  - nao alterar `requirements.txt`;
  - usar perfil temporario em `build/`.
- Abrir `https://msimoes38.github.io/caminhos_brasil/?v=<numero>` para evitar cache.
- Concluir fase 1 manualmente ou automatizar o minimo possivel.
- Recarregar e inspecionar `localStorage["caminhos_brasil_save_v1"]`.

### 4. Polimento Leve Da Fase 1 E Feedbacks

Problema observado:

- A abertura e muito rica visualmente, mas o gameplay da fase 1 ainda parece simples em comparacao.

Comportamento esperado:

- A fase 1 deve continuar leve e legivel, mas com mais vida visual.
- Nao aumentar dificuldade.
- Nao mover pilulas, checkpoints, areas de cuidado ou plataformas sem necessidade.
- Nao atrapalhar HUD, mensagens historicas nem controles touch.

Ideias seguras:

- Mais detalhes no litoral em `src/backgrounds.py`: ondas discretas, aves, marco costeiro, vegetacao baixa ou brilho no mar.
- Pequena animacao/efeito visual no portal quando liberado.
- Melhor destaque visual para a primeira pilula sem mudar sua posicao.
- Feedback mais claro quando todas as pilulas ativas foram coletadas.

Valide com:

- `python -m compileall main.py src`
- smoke tests;
- screenshot ou teste visual da fase 1.

### 5. Acessibilidade E Instrucoes Fora Do Canvas

Problema:

- O jogo roda em canvas; leitores de tela e verificadores HTML veem pouco conteudo util.

Comportamento esperado:

- Sem mudar a experiencia visual principal, a pagina publicada deve expor uma orientacao simples fora do canvas.
- Isso pode ficar no `index.html` gerado pelo build limpo, em texto visualmente discreto ou `noscript`.
- Deve explicar objetivo e controles basicos.
- Nao atrapalhar canvas, tela de carregamento, fullscreen nem Pygbag.

Sugestao tecnica:

- Atualizar `scripts/build_pygbag_clean.py` para injetar uma pequena area HTML acessivel.
- Pode ser uma `div` com classe visualmente oculta, usando CSS seguro.
- Incluir textos curtos:
  - "Caminhos do Brasil e um jogo educativo de plataforma."
  - "Use teclado ou toque para mover Mig, coletar pilulas historicas e responder ao Guardiao do Portal."
- Preservar manifest/metadados atuais.

## Cuidados Historicos E De Produto

- Use linguagem simples.
- Evite descricoes fortes, violentas ou graficas.
- Trate povos indigenas, pessoas escravizadas e temas sensiveis com respeito.
- Nao glorifique processos controversos.
- Valorize memoria, diversidade, cidadania e curiosidade.
- O publico de referencia e crianca por volta de 8 anos.

## Restricoes Tecnicas

- Nao substituir Python, Pygame-CE ou Pygbag.
- Nao quebrar `main.py` com loop `async`.
- Nao adicionar dependencias novas ao projeto.
- Nao adicionar Selenium ao projeto; use apenas para teste local se necessario.
- Nao empacotar `.venv_brasil`, saves locais ou artefatos de teste.
- Preservar `--ume_block=0` no build web.
- Preservar tela de carregamento HTML e seus fallbacks.
- Preservar helper de tela cheia e manifest.
- Preservar controles de teclado e toque.
- Preservar nova jornada temporaria com `N`.
- Preservar save web/local e tolerancia a falhas.
- Preservar checkpoints, respawns e pilulas em posicoes seguras.

## Validacoes Obrigatorias

Rode:

```powershell
python -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall scripts
.\.venv_brasil\Scripts\python.exe scripts\smoke_tests.py
```

Se alterar build web, persistencia web ou HTML publicado, rode tambem:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Se o Python global nao tiver `pygame-ce`, mencione isso e use a venv local.

## Teste Visual/Publicacao Recomendado

Local:

1. Abrir o jogo localmente.
2. Conferir menu desktop.
3. Simular ou forcar contexto touch e conferir menu touch.
4. Iniciar fase 1.
5. Mover, pular e conferir se botoes touch nao cobrem Mig.
6. Abrir colecao.
7. Abrir linha do tempo.
8. Abrir ajuda.

Publicado:

1. Abrir `https://msimoes38.github.io/caminhos_brasil/?v=<numero>`.
2. Confirmar tela de carregamento e menu.
3. Testar desktop.
4. Testar em celular real, se possivel.
5. Em celular, usar modo paisagem.
6. Conferir que o menu inicial ja aparece em modo touch.
7. Concluir fase 1, recarregar e verificar persistencia.

Selenium opcional apenas para teste:

- Pode instalar Selenium na venv local, sem alterar dependencias do projeto.
- Use perfil temporario dentro de `build/`.
- Capture screenshots em `build/`, que nao devem ser commitados.
- Se o Chrome headless falhar, tente `--user-data-dir` temporario, `--no-sandbox`, `--disable-extensions` e `--headless`.

## Criterios De Aceitacao

A rodada esta pronta quando:

- Mobile/touch publicado abre no layout touch quando o navegador indica toque.
- Menu inicial nao mostra orientacoes redundantes/confusas.
- Save web continua usando `localStorage` e passa em teste real ou simulado robusto.
- Fase 1 tem leve melhoria visual sem perder clareza.
- Build limpo continua funcionando.
- Smoke tests passam.
- Documentacao reflete as mudancas.
- Nenhuma dependencia de teste foi adicionada ao projeto.

## Entrega Esperada

Ao finalizar, diga de forma curta:

- o que mudou;
- arquivos principais alterados;
- como testar;
- validacoes que passaram;
- qualquer limitacao restante, especialmente se nao foi possivel testar em celular real ou navegador publicado.
