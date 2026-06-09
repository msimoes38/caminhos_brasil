# LOOP PROMPT - Caminhos do Brasil

Voce e um agente de IA trabalhando em loop no projeto `caminhos_brasil`, um jogo educativo 2D em Python/Pygame-CE sobre a historia do Brasil para criancas. Sua missao e conduzir ciclos sucessivos de melhoria para tornar o jogo mais atrativo, completo, confiavel no navegador e agradavel para criancas e familias, sem perder a simplicidade tecnica que permite publicar via Pygbag no GitHub Pages.

Trabalhe de forma autonoma, incremental e pragmatica. Em cada ciclo, escolha uma meta concreta, implemente, valide, documente e avance para o proximo ponto mais importante. Priorize uma versao funcional e testavel em todas as etapas.

## Meta Ambiciosa

Transformar `Caminhos do Brasil` de uma versao jogavel inicial em uma experiencia educativa mais polida e envolvente, com:

- web/mobile confiavel em celulares reais;
- save web funcionando de ponta a ponta;
- primeira impressao forte e clara;
- gameplay mais gostoso, responsivo e legivel;
- fases com mais identidade visual e pequenas variacoes de desafio;
- colecao e linha do tempo mais motivadoras;
- feedbacks visuais/sonoros mais ricos, ainda leves para web;
- linguagem historica simples, cuidadosa e adequada para criancas;
- testes automatizados e manuais suficientes para sustentar evolucoes futuras.

## Contexto Obrigatorio

Antes de alterar codigo, leia:

- `AGENTS.md`
- `README.md`
- `SPEC.MD`
- `PROMPT_YOLO.MD`
- `requirements.txt`
- `main.py`
- `src/game.py`
- `src/player.py`
- `src/progress.py`
- `src/backgrounds.py`
- `src/level_data.py`
- `src/levels.py`
- `src/settings.py`
- `src/sounds.py`
- `scripts/smoke_tests.py`
- `scripts/build_pygbag_clean.py`
- `.github/workflows/pages.yml`

Preserve as instrucoes desses arquivos. Se houver conflito, siga primeiro `AGENTS.md` e as restricoes tecnicas deste prompt.

## Estado Atual Resumido

O jogo ja possui:

- 16 fases historicas em ordem cronologica;
- tela inicial com `abertura.png`;
- menu, linha do tempo, colecao, ajuda, pausa, introducao, quiz e final;
- controles por teclado, mouse e toque;
- pulo com coyote time e jump buffer;
- checkpoints, areas de cuidado, camera horizontal e respawn seguro;
- banco com 10 pilulas por fase e selecao ativa por sessao;
- Guardiao do Portal com pergunta sobre pilula ativa;
- save local em JSON e tentativa de save web via `localStorage`;
- build Pygbag limpo com `--ume_block=0`, tela de carregamento, manifest e helper de fullscreen;
- smoke tests permanentes.

Achados recentes de Selenium na URL publicada:

- desktop/headless carregou bem, com canvas `960x540`, metadados, manifest e bloco HTML acessivel;
- teclado abriu intro, fase, ajuda, colecao e linha do tempo;
- emulacao mobile/touch reportou `maxTouchPoints = 1`, `pointer: coarse = true` e `hover: none = true`, mas o menu publicado ainda abriu no layout de teclado;
- o pacote publicado contem a deteccao touch robusta, entao o problema pode estar no acesso Python/Pygbag as APIs JS ou no momento da deteccao;
- um save valido gravado manualmente em `localStorage["caminhos_brasil_save_v1"]` nao foi refletido no menu apos reload, que continuou mostrando `Fases liberadas: 1/16`;
- portanto, web/mobile e save web sao prioridades maximas antes de grandes polimentos.

## Restricoes Fortes

- Nao substituir Python, Pygame-CE ou Pygbag.
- Nao quebrar o loop `async` de `main.py`.
- Nao adicionar dependencias novas ao projeto sem necessidade clara e justificativa curta.
- Nao adicionar Selenium ao `requirements.txt`; se usar Selenium, use apenas a venv local para testes.
- Nao empacotar `.venv_brasil`, saves locais ou artefatos de teste no build web.
- Preservar `--ume_block=0` no build limpo.
- Preservar tela HTML de carregamento, fallbacks, manifest e helper de fullscreen.
- Preservar nova jornada temporaria com `N`, sem sobrescrever save permanente.
- Preservar linguagem historica infantil, respeitosa e cuidadosa.
- Nao tornar o jogo pesado para web.
- Nao fazer grandes refatoracoes antes de ter testes cobrindo o comportamento afetado.
- Nao remover funcionalidades existentes sem motivo claro.
- Nao fazer commit/push/deploy a menos que o usuario peca explicitamente.

## Modo De Trabalho Em Loop

Repita este ciclo enquanto houver tempo e progresso util:

1. **Diagnosticar**
   - Leia o contexto relevante.
   - Rode ou consulte os testes existentes quando fizer sentido.
   - Identifique o maior gargalo atual para tornar o jogo mais atrativo e completo.

2. **Escolher Uma Meta Do Ciclo**
   - Escolha uma meta pequena, verificavel e de alto impacto.
   - Prefira corrigir riscos de publicacao/mobile/save antes de polir conteudo.
   - Evite tocar muitos subsistemas no mesmo ciclo.

3. **Planejar Brevemente**
   - Descreva a mudanca em poucas linhas.
   - Liste arquivos provaveis.
   - Defina como validar.

4. **Implementar Incrementalmente**
   - Faca a menor alteracao coerente com a meta.
   - Siga padroes existentes do projeto.
   - Adicione helpers pequenos quando reduzirem complexidade real.
   - Atualize smoke tests quando mudar regra de fluxo, save, touch, fases, player ou build.

5. **Validar**
   - Sempre rode:

```powershell
python -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall scripts
.\.venv_brasil\Scripts\python.exe scripts\smoke_tests.py
```

   - Se mudar build web, HTML, save web, touch web ou publicacao, rode:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

   - Se mudar interface ou visual, gere screenshot local/dummy ou abra o jogo para conferir.
   - Se mudar web/mobile, use Selenium na venv local quando possivel.

6. **Documentar**
   - Atualize `README.md`, `SPEC.MD` e `AGENTS.md` quando mudar comportamento, arquitetura, publicacao, controles ou processo.
   - Atualize `PROMPT_YOLO.MD` ou este `LOOP_PROMPT.MD` quando prioridades ou estado geral mudarem.

7. **Resumo Do Ciclo**
   - Informe o que mudou.
   - Diga como testar.
   - Liste validacoes feitas.
   - Aponte limitacoes restantes.
   - Proponha a proxima meta mais importante.

## Prioridades Do Loop

### P0 - Confiabilidade Web/Mobile

Resolva antes de grandes melhorias visuais.

1. **Deteccao touch publicada**
   - Se `navigator.maxTouchPoints`, `matchMedia("(pointer: coarse)")` ou `matchMedia("(hover: none)")` indicarem toque, o menu inicial deve abrir no layout touch.
   - Como o acesso Python/Pygbag pode falhar, injete no `index.html` uma flag JS simples, por exemplo `window.caminhosTouchContext`, calculada antes do jogo iniciar.
   - Em Python, `_detect_touch_context()` deve consultar essa flag primeiro.
   - Tambem faca uma rechecagem tardia no menu se nenhum teclado foi usado ainda.
   - Valide com smoke test simulado e Selenium mobile emulado.

2. **Save web real**
   - Garanta que um save valido em `localStorage["caminhos_brasil_save_v1"]` seja lido apos reload.
   - Se acesso direto a `platform.window.localStorage` for instavel, injete helpers JS no build, por exemplo:
     - `window.caminhosReadSave()`
     - `window.caminhosWriteSave(data)`
     - `window.caminhosClearSave()` se necessario para teste
   - `ProgressStore` deve usar esses helpers como caminho principal ou fallback.
   - Validar com Selenium: gravar save, recarregar, confirmar menu `2/16`, abrir fase 2, concluir fase e recarregar.

3. **Teste Selenium permanente opcional**
   - Criar script de teste web em `scripts/` somente se nao exigir nova dependencia versionada.
   - Se Selenium nao estiver garantido, documentar como teste manual/opcional.
   - Nao adicionar Selenium a `requirements.txt`.

### P1 - Primeiro Contato E Onboarding

1. Tornar o menu inicial mais claro em desktop e touch.
2. Garantir que criancas entendam rapidamente: andar, pular, coletar pilulas, responder o Guardiao.
3. Melhorar dicas iniciais sem cobrir Mig, botoes touch, HUD ou pilulas.
4. Criar feedback mais claro quando o portal ainda esta bloqueado e quando fica liberado.
5. Melhorar ajuda rapida com texto curto e legivel, sem virar manual longo.

### P2 - Sensacao De Jogo

1. Ajustar movimento, aceleracao, desaceleracao e pulo com cuidado.
2. Melhorar animacao do Mig se possivel usando a folha existente.
3. Dar mais clareza visual a plataformas, areas de cuidado, checkpoints, pilulas e portal.
4. Variar levemente desafios sem aumentar dificuldade para criancas:
   - plataformas com espaçamentos mais interessantes;
   - pequenas subidas/descidas;
   - checkpoints em pontos naturais;
   - perigos bem sinalizados, nunca punitivos demais.
5. Preservar smoke tests de alcance de pilulas e seguranca de respawn.

### P3 - Fases Mais Memoraveis

1. Dar identidade visual mais forte a cada tema em `src/backgrounds.py`.
2. Polir algumas fases por vez, nao todas de uma vez.
3. Priorizar fases:
   - fase 1, por ser o primeiro contato;
   - fase 2, por historico de problemas de alcance/checkpoint;
   - fases sensiveis, com linguagem e simbolos cuidadosos;
   - ultima fase, por fechar a experiencia.
4. Evitar assets pesados; preferir desenho por codigo ou assets pequenos.

### P4 - Aprendizado E Motivacao

1. Tornar a colecao mais recompensadora:
   - destacar descobertas recentes;
   - mostrar progresso por periodo;
   - talvez criar pequenas medalhas por blocos de fases.
2. Melhorar linha do tempo:
   - leitura mais facil em mobile;
   - estados de fase mais claros;
   - indicacao do proximo objetivo.
3. Melhorar o Guardiao:
   - dicas mais acolhedoras;
   - feedback positivo apos acerto;
   - evitar repeticao cansativa.
4. Revisar pilulas historicas para frases curtas, respeitosas e memoraveis.

### P5 - Audio, Acessibilidade E Polimento

1. Melhorar sons gerados por codigo sem depender de arquivos grandes.
2. Garantir que o jogo siga silencioso se audio falhar.
3. Fortalecer orientacao HTML fora do canvas para leitores de tela.
4. Checar contraste e tamanho de textos em menu, HUD, colecao e quiz.
5. Evitar sobreposicoes em 960x540 e em canvas escalado no navegador.

### P6 - Arquitetura Com Cuidado

1. Separar `src/game.py` apenas quando houver dor real.
2. Se separar, prefira modulos pequenos:
   - `ui.py` para desenho de componentes comuns;
   - `screens.py` para telas;
   - `input.py` se entrada ficar complexa;
   - `web.py` para ponte JS/Pygbag.
3. Toda separacao deve preservar comportamento e ter testes antes/depois.

## Ideias Concretas Para Primeiros Ciclos

Comece por estas metas, nesta ordem, salvo se o estado local ja tiver resolvido alguma:

1. Corrigir touch inicial no publicado com flag JS `window.caminhosTouchContext`.
2. Corrigir leitura/escrita web real com helpers JS para `localStorage`.
3. Criar teste Selenium opcional que valide menu touch e save injetado.
4. Melhorar feedback do portal bloqueado/liberado e tutorial inicial.
5. Polir visual das fases 1 e 2 sem mudar dificuldade.
6. Melhorar album da colecao com pequenas recompensas visuais.
7. Ajustar sensacao de movimento/pulo com teste manual e smoke.
8. Criar uma matriz curta de QA web/mobile documentada.

## Validacao Web Com Selenium

Quando testar a URL publicada:

- use `https://msimoes38.github.io/caminhos_brasil/?v=<numero>` para evitar cache;
- teste tambem a URL sem query, pois usuarios entram por ela;
- em desktop, verificar:
  - titulo da aba;
  - canvas `960x540`;
  - carregamento some;
  - Enter abre intro;
  - Enter inicia fase;
  - `H`, `C`, `S`, `P`, `R`, `M` respondem;
- em mobile emulado, verificar:
  - `maxTouchPoints > 0`;
  - `pointer: coarse`;
  - menu inicial em layout touch;
  - botao `Tela cheia` visivel;
  - tocar em continuar abre intro;
  - tocar na intro inicia fase;
  - botoes `<`, `>`, `Pular`, `P`, `C` aparecem e nao cobrem Mig;
- para save:
  - limpar `localStorage`;
  - injetar save valido com fase 2 liberada;
  - recarregar;
  - confirmar menu `2/16`;
  - pressionar/tocar continuar e confirmar fase 2;
  - concluir fase 1 quando possivel e confirmar persistencia apos reload.

## Checklist De Qualidade Para Cada Mudanca

Antes de encerrar um ciclo, confira:

- O jogo ainda abre localmente?
- O build web limpo ainda funciona?
- O save local nao foi corrompido?
- Nova jornada temporaria com `N` continua sem gravar save permanente?
- Mobile/touch continua com botoes grandes?
- Mig nao nasce coberto por botoes touch?
- Mensagem historica continua fixa e translucida quando Mig passa por tras?
- Checkpoints e respawns continuam fora de areas de cuidado?
- Pilulas continuam alcançaveis?
- O tom historico continua adequado para criancas?
- Documentacao e testes foram atualizados quando necessario?

## Formato De Entrega Ao Usuario

Ao final de cada rodada, responda de forma curta:

- o que mudou;
- arquivos principais alterados;
- como testar;
- validacoes que passaram;
- o que nao foi possivel validar;
- proxima melhoria recomendada.

Se algum ponto bloquear por tres tentativas consecutivas, explique o bloqueio com clareza, proponha alternativas e pare para pedir decisao do usuario.

## Norte De Produto

O jogo deve parecer simples, vivo e cuidadoso. Criancas devem entender o que fazer sem ler muito, familias devem perceber valor educativo, e o projeto deve continuar leve o suficiente para rodar no navegador. Prefira progresso consistente a grandes promessas: um ciclo bom deixa o jogo mais confiavel, mais bonito ou mais claro sem quebrar o que ja funciona.
