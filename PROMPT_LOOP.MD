# PROMPT YOLO - Evolucao Criativa Do Caminhos Do Brasil

Voce e um agente de IA trabalhando em loop no projeto `caminhos_brasil`, um jogo educativo 2D em Python/Pygame-CE sobre a historia do Brasil para criancas. Sua missao e tornar o jogo mais bonito, divertido, expressivo e educativo, com mais funcionalidades e pequenos desafios, sem perder leveza, clareza e compatibilidade com Pygbag/GitHub Pages.

Trabalhe de forma autonoma, incremental e muito cuidadosa. Cada rodada deve deixar o jogo melhor de um jeito visivel ou pedagogicamente util, com validacao proporcional. Prefira ciclos pequenos, completos e testaveis a grandes promessas.

## Visao De Produto

O jogo deve parecer uma aventura historica acolhedora: Mig viaja por periodos do Brasil, coleta descobertas, supera desafios simples e conversa com o Guardiao do Portal. A crianca deve sentir curiosidade, alegria de explorar e vontade de completar a colecao, enquanto aprende historia com frases curtas, respeitosas e memoraveis.

Meta de longo prazo:

- Fases mais vivas, bonitas e diferentes entre si.
- Mais motivos para explorar, revisar e completar a jornada.
- Desafios leves, justos e variados, adequados a criancas por volta de 8 anos.
- Conteudo historico simples, respeitoso e efetivo.
- Feedbacks visuais e sonoros mais encantadores.
- Mobile/web confiavel e facil de usar.
- Codigo ainda simples, leve e sustentavel.

## Contexto Obrigatorio

Antes de alterar codigo, leia:

- `AGENTS.md`
- `README.md`
- `SPEC.MD`
- `LOOP_PROMPT.MD`
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

Preserve Python, Pygame-CE, Pygbag, o loop `async` de `main.py`, o build limpo com `--ume_block=0`, os controles de teclado/toque, a nova jornada temporaria com `N`, o save tolerante a falhas e o tom historico infantil e respeitoso.

## Regras De Ouro

- Nao adicione dependencias novas sem necessidade muito clara.
- Nao adicione Selenium ao `requirements.txt`; use apenas a venv local se precisar testar web.
- Nao torne o jogo pesado para navegador.
- Nao remova funcionalidades existentes sem motivo forte.
- Nao crie sistemas enormes antes de ter uma versao simples funcionando.
- Nao use linguagem historica pesada, grafica ou inadequada para criancas.
- Nao glorifique processos historicos controversos.
- Nao deixe pilulas, checkpoints ou respawns em posicoes injustas.
- Nao cubra Mig, HUD, mensagens historicas ou botoes touch com novos elementos.
- Atualize smoke tests quando mudar regras de fase, fluxo, save, touch, player ou progresso.
- Atualize documentacao quando mudar comportamento, controles, arquitetura, publicacao ou processo.

## Como Trabalhar Em Loop

Em cada ciclo:

1. Leia o contexto relevante.
2. Escolha uma meta pequena e de alto impacto.
3. Implemente uma melhoria completa.
4. Valide.
5. Atualize documentacao/testes quando necessario.
6. Entregue resumo curto com proximas sugestoes.

Escolha sempre a menor fatia que gere valor real. Exemplos de boas metas:

- "Adicionar medalhas simples por blocos de fases."
- "Dar mais identidade visual a fase 2."
- "Criar feedback especial ao completar todas as pilulas de uma fase."
- "Melhorar o Guardiao com uma fala curta antes da pergunta."
- "Adicionar uma missao secundaria simples na fase 1."

Evite metas grandes demais:

- "Refazer todas as fases."
- "Criar novo motor de fisica."
- "Adicionar sistema completo de inventario."
- "Reescrever toda a UI."

## Prioridade 1 - Diversao Educativa Imediata

Priorize melhorias que uma crianca perceba em menos de 1 minuto:

- Dicas iniciais mais claras e simpaticas.
- Celebracao visual ao coletar pilula.
- Portal com estado bloqueado/liberado mais expressivo.
- Pequena fala do Guardiao antes do quiz.
- Mensagem positiva apos erro no quiz, com dica curta e acolhedora.
- Tela de conclusao com medalha, carimbo ou selo da fase.
- Linha do tempo mostrando "proxima aventura" de forma mais chamativa.
- Colecao destacando conquistas recentes.

## Prioridade 2 - Fases Mais Vivas E Memoraveis

Melhore poucas fases por vez. Comece por fase 1, fase 2, ultima fase e fases sensiveis.

Ideias visuais por tema:

- Litoral: ondas, espuma, passaros, vegetacao baixa, brilho do mar, pequenos barcos ao fundo.
- Acucar: canavial, engenho estilizado, rodas d'agua, feixes de cana, caminho de terra.
- Interiorizacao: rios, trilhas, placas de mapa, arvores, morros e pequenas marcas de caminho.
- Ouro: montanhas, trilhos, lanternas, pedras brilhantes discretas, vilas ao fundo.
- Cidades coloniais: igrejas, ruas de pedra, lampioes, janelas coloridas.
- Independencia/Imperio: praca, jardins, bandeiras discretas, livros e cartas.
- Republica/Vargas/Democracia: pracas civicas, radios, cartazes, predios e simbolos de participacao.
- Ditadura/Redemocratizacao: visual cuidadoso, memoria, direitos, luzes suaves, cartazes por democracia, sem imagens pesadas.
- Brasil contemporaneo: cidades, natureza, conexoes, diversidade, escola, tecnologia e meio ambiente.

Regra: detalhes devem enriquecer a leitura sem atrapalhar plataformas, pilulas, perigos, HUD ou toque.

## Prioridade 3 - Desafios Leves E Justos

Crie variedade sem frustrar:

- Plataformas com ritmo um pouco diferente por tema.
- Pequenas sequencias de pulo com checkpoint perto.
- Areas de cuidado bem sinalizadas antes do contato.
- Miniobjetivos opcionais, como observar um marco, ativar uma placa ou coletar um simbolo de memoria.
- "Missao secundaria" simples por fase, sem bloquear progresso principal.
- Recompensa extra por concluir fase com todas as pilulas ativas.

Nao use inimigos violentos. Se criar obstaculos, prefira elementos abstratos e seguros: poças de cuidado, neblina, pedras, buracos sinalizados, caixas, cercas baixas, vento ou plataformas estreitas.

## Prioridade 4 - Funcionalidades Que Aumentam Vontade De Jogar

Implemente em versoes pequenas:

- Medalhas por fase concluida.
- Selos por bloco historico completado, por exemplo:
  - Primeiros Contatos
  - Brasil Colonial
  - Independencia E Imperio
  - Republica E Democracia
  - Brasil De Hoje
- Colecao com progresso por bloco historico.
- Tela final mais celebrativa, com resumo da jornada e selos conquistados.
- "Descoberta favorita" ou destaque aleatorio de uma pilula ja coletada.
- Pequeno contador de "descobertas da sessao".
- Botao/atalho para revisitar a proxima fase incompleta.
- Ajuda visual com icones simples desenhados por Pygame.

Evite sistemas complexos de economia, loja, ranking online, contas ou multiplayer.

## Prioridade 5 - Aprendizagem Historica Efetiva

Cada melhoria deve ajudar a aprender melhor, nao apenas decorar.

Boas praticas:

- Frases curtas.
- Uma ideia por pilula.
- Perguntas simples, mas nao bobas.
- Dicas que ensinam sem punir.
- Conclusoes que conectam passado e presente.
- Conteudo sensivel tratado com respeito, cuidado e memoria.
- Povos indigenas, pessoas escravizadas e grupos afetados sempre descritos com dignidade.

Ideias didaticas:

- Guardiao pergunta sobre uma pilula ja vista.
- A conclusao da fase pode fazer uma pergunta de reflexao curta.
- A colecao pode agrupar descobertas por tema.
- A linha do tempo pode mostrar "o que mudou" em uma frase.
- Fases sensiveis podem ter notas de cuidado com linguagem simples.

Evite:

- textos longos;
- humor sobre sofrimento;
- glorificacao de conquista, escravizacao, censura ou violencia;
- descricoes graficas;
- alternativas de quiz humilhantes ou agressivas.

## Prioridade 6 - Beleza E Feedback

Melhore o sentimento de recompensa:

- Particulas leves ao coletar pilula.
- Pequeno brilho no checkpoint ativado.
- Portal mais luminoso quando liberado.
- Medalha animada na conclusao.
- Som curto e suave para coleta, checkpoint, acerto, bloqueio e conclusao.
- Cores de feedback consistentes.
- Textos positivos como "Boa descoberta!", "Voce lembrou bem!" e "Mais uma parte da historia no album!".

Tudo deve ser leve: poucos objetos, poucos calculos, sem assets grandes.

## Prioridade 7 - Mobile, Acessibilidade E Clareza

Sempre pense no celular em modo paisagem:

- Botoes touch grandes.
- Nenhum texto importante atras dos botoes.
- Mig visivel no inicio da fase.
- Mensagens historicas fixas e translucidas quando necessario.
- Menu e pausa com areas tocaveis claras.
- Quiz facil de tocar.
- Tela cheia com falha segura.

Para acessibilidade:

- Manter orientacao HTML fora do canvas.
- Garantir contraste bom.
- Evitar textos pequenos demais.
- Evitar excesso de informacao na tela.
- Preservar atalhos de teclado.

## Ideias De Ciclos Criativos

Use esta lista como fonte de inspiracao. Escolha uma por ciclo.

### Ciclo A - Selos Da Jornada

Adicionar selos por blocos historicos. Ao concluir todas as fases de um bloco, mostrar um selo na tela final e na colecao. Comece com visual simples desenhado por Pygame.

### Ciclo B - Missao Secundaria Simples

Adicionar uma pequena missao opcional por fase, como "observe o marco", "encontre o mapa" ou "ative a placa de memoria". A recompensa pode ser um feedback e um selo simples, sem bloquear conclusao.

### Ciclo C - Guardiao Mais Vivo

Antes da pergunta, o Guardiao pode dizer uma frase curta relacionada a fase. Apos erro, ele ensina com delicadeza. Apos acerto, ele celebra e abre o portal.

### Ciclo D - Fases Com Identidade

Escolher 2 ou 3 temas e adicionar detalhes visuais especificos em `src/backgrounds.py`. Validar que nada atrapalha gameplay.

### Ciclo E - Colecao Mais Motivadora

Adicionar destaque de progresso por bloco historico, descoberta recente mais clara e pequena celebracao quando uma fase chega a 10/10 descobertas no album.

### Ciclo F - Linha Do Tempo Viva

Melhorar a linha do tempo com icones simples, marcador da proxima aventura e uma frase curta por bloco historico.

### Ciclo G - Tela Final Celebrativa

Transformar a tela final em um resumo da jornada com medalhas, selos, quantidade de descobertas e mensagem final sobre aprender historia com respeito.

### Ciclo H - Sensacao De Plataforma

Ajustar movimento/pulo de forma conservadora, melhorar resposta dos controles touch e criar teste manual especifico para fase 1 e fase 2.

### Ciclo I - Audio Mais Carinhoso

Melhorar sons gerados por codigo com variacoes suaves por evento, mantendo fallback silencioso se mixer falhar.

### Ciclo J - Tutorial Jogavel

Melhorar os primeiros segundos da fase 1 com dicas contextuais que aparecem uma por vez e somem quando a crianca executa a acao.

## Validacoes Obrigatorias

Para qualquer alteracao de codigo, rode:

```powershell
python -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall scripts
.\.venv_brasil\Scripts\python.exe scripts\smoke_tests.py
```

Se alterar build web, HTML, touch, save web, carregamento ou publicacao, rode tambem:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Se alterar UI/visual, faca pelo menos uma checagem visual:

- screenshot em SDL dummy;
- execucao local;
- ou Selenium/headless quando for web.

Se alterar fases, player, plataformas, checkpoints, perigos ou pilulas, atualize smoke tests quando necessario.

## Teste Manual Minimo Para Mudancas Visuais Ou De Gameplay

- Abrir o jogo local.
- Confirmar abertura/menu.
- Iniciar fase 1.
- Mover e pular.
- Coletar uma pilula.
- Verificar feedback.
- Abrir colecao.
- Pausar e continuar.
- Encostar no portal bloqueado e liberado.
- Responder o Guardiao.
- Conferir fase 2 se houve alteracao de layout ou player.
- Em modo touch ou emulacao, conferir botoes `<`, `>`, `Pular`, `P` e `C`.

## Como Escolher A Proxima Tarefa

Use esta ordem:

1. Se algo quebra mobile/web/save, corrija primeiro.
2. Se o primeiro minuto do jogo esta confuso, melhore onboarding.
3. Se a fase 1 esta pouco atrativa, embeleze e clarifique.
4. Se a jornada precisa de motivacao, adicione recompensas simples.
5. Se uma fase esta generica, de identidade visual a ela.
6. Se a aprendizagem esta rasa, melhore quiz, colecao ou reflexoes.
7. Se o arquivo `src/game.py` estiver impedindo progresso, refatore uma parte pequena com testes.

## Formato De Entrega

Ao final de cada rodada, diga:

- o que mudou;
- por que isso deixa o jogo mais atrativo ou educativo;
- arquivos alterados;
- como testar;
- validacoes executadas;
- limitacoes restantes;
- proxima sugestao de melhoria.

## Norte Criativo

Pense como alguem construindo uma aventura carinhosa de historia para criancas. O jogo deve convidar a explorar, recompensar curiosidade e ensinar sem ficar pesado. Cada detalhe deve responder a uma pergunta simples: "isso ajuda a crianca a se divertir, entender melhor ou querer continuar?" Se sim, implemente uma versao pequena, bonita e segura. Se nao, deixe para depois.
