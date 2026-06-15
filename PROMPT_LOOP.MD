# PROMPT LOOP - Caminhos Do Brasil Mais Vivo

Voce e um agente de IA trabalhando em ciclos sucessivos no projeto `caminhos_brasil`, um jogo educativo 2D em Python/Pygame-CE sobre a historia do Brasil para criancas. Sua missao e deixar o jogo mais atraente, divertido, bonito, expressivo e educativo para criancas e familias, sem perder a simplicidade tecnica que permite rodar no navegador via Pygbag e GitHub Pages.

Trabalhe em loop: escolha uma melhoria pequena, implemente, valide, documente quando necessario e avance para a proxima melhoria de maior impacto. Cada ciclo deve deixar o jogo mais agradavel de jogar, mais facil de entender ou mais memoravel.

## Norte Criativo

Transforme `Caminhos do Brasil` em uma aventura historica acolhedora, com sensacao de descoberta. A crianca deve entender rapido o que fazer, sentir vontade de explorar e receber pequenas recompensas por aprender.

A experiencia ideal:

- Mig parece estar viajando por mundos historicos vivos.
- Cada fase tem identidade visual clara e pequenos detalhes que convidam a olhar.
- Coletar pilulas historicas da prazer, brilho, som e sentido.
- O Guardiao do Portal parece um guia simpatico, nao uma prova escolar.
- A colecao e a linha do tempo dão vontade de completar a jornada.
- O jogo continua leve, simples e confiavel no celular.

## Contexto Obrigatorio

Antes de alterar codigo, leia:

- `AGENTS.md`
- `README.md`
- `SPEC.MD`
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

Preserve as regras desses arquivos. Se houver conflito, siga `AGENTS.md` primeiro.

## Regras Fortes

- Preserve Python, Pygame-CE, Pygbag e o loop `async` de `main.py`.
- Nao adicione dependencias novas sem necessidade clara.
- Nao adicione Selenium ao `requirements.txt`; use o Selenium ja instalado na venv para testes de navegador.
- Nao torne o jogo pesado para web.
- Nao remova funcionalidades existentes sem motivo claro.
- Nao quebre teclado, mouse, toque, save local, save web ou nova jornada temporaria com `N`.
- Preserve o build limpo com `--ume_block=0`, tela de carregamento HTML, manifest, ponte JS de touch/save e helper de tela cheia.
- Preserve a linguagem historica simples, curta, respeitosa e adequada para criancas.
- Nao glorifique processos historicos controversos.
- Nao use descricoes violentas, graficas ou pesadas.
- Nao coloque pilulas, missoes extras, checkpoints ou respawns em lugares injustos.
- Nao cubra Mig, HUD, mensagens historicas ou botoes touch.

## Grande Proposta De Melhoria

Crie, ao longo de varias rodadas pequenas, a sensacao de uma **Jornada De Descobertas**.

Essa melhoria geral combina jogabilidade, graficos, colecao, feedback e aprendizado:

- Cada fase ganha um pequeno elemento especial observavel, como mapa, marco, placa, carta, radio, livro, arvore, estrela, memoria ou simbolo civico.
- A crianca pode tocar/coletar/observar esse elemento como uma missao opcional simples.
- Ao observar, o jogo mostra uma frase curta e positiva, com particulas leves e som suave.
- A colecao passa a valorizar essas observacoes como "lembrancas da viagem".
- A tela final celebra pilulas, fases, selos e lembrancas encontradas.
- O visual das fases reforca o tema, mas sem aumentar a dificuldade.

Nao implemente tudo de uma vez. Use isso como direcao de produto. Em cada ciclo, escolha uma fatia pequena e completa.

## Modo De Trabalho Em Loop

Em cada ciclo:

1. Diagnostique o estado atual.
2. Escolha uma meta pequena e visivel.
3. Planeje brevemente arquivos e validacoes.
4. Implemente a menor versao funcional.
5. Rode validacoes proporcionais.
6. Atualize docs/testes se comportamento mudou.
7. Entregue resumo curto e sugira a proxima melhoria.

Uma boa meta cabe em uma frase:

- "Melhorar a celebracao de conclusao da fase."
- "Adicionar mais vida visual a fase 1 sem mudar plataformas."
- "Criar fala curta do Guardiao antes da pergunta."
- "Mostrar uma lembranca da viagem na colecao."
- "Deixar a linha do tempo mais gostosa para crianca escolher a proxima aventura."

Evite metas grandes:

- "Refazer o jogo inteiro."
- "Criar novo motor de fisica."
- "Reescrever toda a interface."
- "Adicionar inventario complexo."
- "Adicionar ranking online, conta, loja ou multiplayer."

## Prioridade 0 - Confiabilidade Antes Do Encanto

Antes de polir visual ou gameplay, corrija qualquer problema que quebre:

- abrir o jogo;
- jogar no celular em modo paisagem;
- salvar e carregar progresso;
- iniciar fase;
- tocar botoes virtuais;
- coletar pilulas;
- responder o Guardiao;
- gerar build web limpo.

Se tocar web/mobile, use Selenium instalado na venv quando fizer teste de navegador. Nao instale nem versione Selenium no projeto.

## Prioridade 1 - Primeiro Minuto Encantador

O primeiro minuto precisa dizer para a crianca: "eu sei o que fazer e quero continuar".

Ideias:

- Menu com chamada curta e clara, sem parecer manual.
- Botoes touch grandes e simpaticos.
- Tutorial da fase 1 com dicas que aparecem uma por vez.
- Primeira pilula com brilho especial e feedback mais alegre.
- Portal bloqueado com dica visual clara.
- Portal liberado com brilho, som e frase curta.
- Guardiao com primeira fala acolhedora.

Regra: nenhuma dica deve cobrir Mig, controles touch, HUD ou mensagens historicas.

## Prioridade 2 - Fases Com Identidade Visual

Melhore poucas fases por vez. Priorize fase 1, fase 2, ultima fase e fases sensiveis.

Ideias por tema:

- Litoral: ondas, espuma, conchas discretas, passaros, vegetacao baixa, barco distante, brilho do mar.
- Acucar: canavial, engenho estilizado, roda d'agua, feixes de cana, caminho de terra, sombras de folhas.
- Interiorizacao: rios, trilhas, placas de mapa, morros, arvores, pegadas, pequenas pontes.
- Ouro: montanhas, lanternas, trilhos, pedras brilhantes discretas, vilas ao fundo.
- Cidades coloniais: ruas de pedra, janelas coloridas, lampioes, praca, igreja ao fundo.
- Independencia/Imperio: cartas, livros, jardins, pracas, bandeiras discretas, bancos de praca.
- Republica/Vargas/Democracia: radio, jornais, cartazes civicos, predios, praca de encontro.
- Ditadura/Redemocratizacao: memoria, direitos, luz suave, cartazes por democracia, livros e velas sem tom pesado.
- Brasil contemporaneo: escola, tecnologia, natureza, conexoes, diversidade, meio ambiente.

Use formas simples de Pygame antes de criar assets. Assets novos devem ser leves.

## Prioridade 3 - Jogabilidade Mais Gostosa

Melhore a sensacao de jogo com cuidado:

- pulo responsivo, sem ficar dificil;
- controles touch mais tolerantes;
- plataformas com ritmo levemente variado;
- areas de cuidado bem sinalizadas;
- checkpoints em lugares naturais;
- pequenas subidas e descidas;
- recompensas opcionais sem bloquear a fase.

Nao use inimigos violentos. Para obstaculos, prefira elementos abstratos e seguros:

- poco de cuidado;
- neblina;
- pedra;
- buraco sinalizado;
- caixa;
- cerca baixa;
- vento leve;
- ponte curta;
- plataforma estreita mas justa.

Toda mudanca em fase/player precisa preservar smoke tests de alcance e seguranca.

## Prioridade 4 - Recompensas Que Motivam

Crie motivos para completar a jornada:

- selos por blocos historicos;
- medalha simples por fase concluida;
- celebracao quando uma fase chega a 10/10 descobertas;
- destaque de descoberta recente;
- contador de descobertas da sessao;
- lembrancas da viagem por missoes opcionais;
- tela final com resumo alegre;
- linha do tempo mostrando "proxima aventura".

Comece visualmente simples. Uma medalha desenhada com circulo, faixa e brilho ja pode funcionar.

## Prioridade 5 - Guardiao Mais Vivo

O Guardiao deve parecer um guia da aventura.

Melhorias possiveis:

- fala curta antes da pergunta;
- comentario diferente por bloco historico;
- dica acolhedora apos erro;
- celebracao curta apos acerto;
- frase que conecta a pilula com a fase;
- efeito visual quando o portal abre.

Evite perguntas longas. A crianca deve ler sem cansar.

## Prioridade 6 - Aprendizado Leve E Respeitoso

O jogo ensina melhor quando cada texto tem uma ideia clara.

Boas praticas:

- uma ideia por pilula;
- frases curtas;
- termos simples;
- perguntas de quiz diretas;
- dicas que ensinam sem punir;
- conclusoes que conectam passado e presente;
- temas sensiveis tratados com dignidade e cuidado.

Ao mencionar povos indigenas, pessoas escravizadas, censura, desigualdade ou grupos afetados, use linguagem respeitosa. Valorize memoria, diversidade, cidadania e curiosidade.

## Prioridade 7 - Som, Particulas E Movimento

Use polimento leve para dar vida:

- particulas ao coletar pilula;
- brilho no checkpoint;
- pequena ondulacao no portal;
- pulso suave no marcador de missao extra;
- som de acerto mais feliz;
- som de erro gentil, nao punitivo;
- microanimacao em medalhas e selos;
- fundo com detalhes em parallax simples.

Tudo deve continuar barato para web. Poucos objetos, poucos calculos, sem arquivos grandes.

## Prioridade 8 - Mobile E Acessibilidade

Sempre pense no celular:

- botoes grandes;
- toque tolerante;
- textos curtos;
- quiz facil de tocar;
- menu e pausa escaneaveis;
- Mig visivel no inicio;
- painel historico fixo e translucido quando necessario;
- nada importante atras dos controles.

Para acessibilidade:

- preserve orientacao HTML fora do canvas;
- mantenha contraste bom;
- evite texto pequeno;
- preserve atalhos de teclado;
- nao dependa apenas de cor para informar estado.

## Ideias De Ciclos Criativos

Escolha uma por rodada.

### Ciclo A - Fase 1 Inesquecivel

Dar ao litoral inicial mais vida: ondas em camadas, brilho do sol no mar, conchas discretas, passaros e uma primeira pilula com destaque especial. Nao mudar dificuldade.

Estado atual: primeira versao implementada com ondas em camadas, brilho no mar, conchas discretas, mais passaros e destaque visual na primeira pilula. Proximas rodadas podem polir vegetacao e profundidade sem mexer nas plataformas.

### Ciclo B - Guardiao Guia

Adicionar uma fala curta do Guardiao antes da pergunta e uma fala de celebracao apos acerto. Manter quiz simples e legivel.

Estado atual: primeira versao implementada com fala acolhedora por bloco historico, foco curto na pilula usada pela pergunta, som de portal e celebracao apos acerto. Proximas rodadas podem variar mais as falas.

### Ciclo C - Lembrancas Da Viagem

Transformar missoes extras em "lembrancas" simples mostradas na colecao ou tela final. Comecar com contador e destaque textual.

Estado atual: a colecao e a tela final ja mostram as missoes extras observadas como lembrancas da viagem da sessao, com cards proprios na colecao. Proximas rodadas podem avaliar persistencia no save.

### Ciclo D - Colecao Album Vivo

Melhorar a colecao com mini-selos, descoberta favorita, progresso por bloco e celebracao 10/10 mais clara.

Estado atual: primeira versao implementada com descoberta recente destacada, cards de lembrancas, progresso por fase, celebracao 10/10 e selos por blocos historicos. Proximas rodadas podem adicionar microanimacao aos selos.

### Ciclo E - Linha Do Tempo Como Mapa

Fazer a linha do tempo parecer um mapa de aventuras, com marcador da proxima fase, icones por bloco e uma frase curta por periodo.

Estado atual: primeira versao implementada com caminho pontilhado, bussola simples, marcadores de proxima aventura, icones e frases por bloco historico. Proximas rodadas podem polir o desenho sem reduzir legibilidade.

### Ciclo F - Final De Jornada

Deixar a tela final mais emocionante: selos conquistados, descobertas da sessao, lembrancas, mensagem final e convite para revisitar fases.

Estado atual: primeira versao implementada com medalha visual, selos, descobertas da sessao, lembrancas da viagem, mensagem final e convite para revisitar. Proximas rodadas podem melhorar celebracao visual.

### Ciclo G - Fase 2 Mais Clara

Polir visual e legibilidade da fase 2, revisando checkpoints, pilulas e areas de cuidado com smoke tests.

Estado atual: primeira versao implementada com canavial mais visivel, detalhes de engenho, placas de cuidado e smoke test especifico para checkpoints da fase 2. Proximas rodadas podem revisar ritmo visual sem alterar dificuldade.

### Ciclo H - Controles Mais Macios

Ajustar sensacao de movimento e pulo de forma conservadora, com teste manual em fase 1 e 2. Evitar deixar dificil.

Estado atual: primeira versao implementada com pulo levemente mais alto, coyote time/buffer um pouco maiores, resposta touch no ar mais viva e margem extra nos botoes virtuais. Proximas rodadas devem ajustar so com teste manual.

### Ciclo I - Sons De Descoberta

Melhorar sons gerados por codigo para coleta, checkpoint, portal, acerto e selo. O jogo deve seguir silencioso se audio falhar.

Estado atual: primeira versao implementada com sinais mais ricos para coleta, checkpoint e acerto, alem de novos sons para portal e dica do Guardiao. O jogo continua tolerante a falha de audio.

### Ciclo J - Microeventos De Fase

Criar pequenos acontecimentos nao perigosos: uma placa que aparece, um brilho no marco, uma onda mais forte, uma luz no portal, uma frase curta ao observar algo.

Estado atual: primeira versao implementada com um microevento contextual por fase, disparado uma vez por visita, com mensagem curta e particulas leves. Proximas rodadas podem trocar eventos por objetos observaveis dedicados.

## Validacoes Obrigatorias

Para qualquer alteracao de codigo:

```powershell
python -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall scripts
.\.venv_brasil\Scripts\python.exe scripts\smoke_tests.py
```

Se alterar build web, HTML, save web, touch, carregamento, fullscreen ou publicacao:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Se alterar interface, visual ou mobile:

- faca checagem visual local, screenshot ou teste manual;
- para navegador, use Selenium instalado na venv;
- nao adicione Selenium ao `requirements.txt`.

Teste Selenium recomendado para web:

- abrir build local ou URL publicada;
- confirmar titulo da aba;
- confirmar canvas;
- confirmar loading HTML;
- confirmar manifest;
- confirmar `window.caminhosTouchContext` em mobile emulado;
- confirmar helpers `window.caminhosReadSave()` e `window.caminhosWriteSave(data)`;
- confirmar que `abertura.png` do manifest responde 200 no build final.

## Teste Manual Minimo

Quando a mudanca tocar visual, fase ou gameplay:

1. Abrir o jogo local.
2. Confirmar menu e abertura.
3. Iniciar fase 1.
4. Mover e pular.
5. Coletar uma pilula.
6. Observar feedback.
7. Tocar no marcador extra, se existir.
8. Abrir colecao.
9. Pausar e continuar.
10. Encostar no portal bloqueado.
11. Liberar portal e responder o Guardiao.
12. Conferir fase 2 se mudou layout, player ou dificuldade.
13. Em touch/emulacao, conferir `<`, `>`, `Pular`, `P` e `C`.

## Como Decidir A Proxima Melhoria

Use esta ordem:

1. Se algo quebra web/mobile/save, corrija.
2. Se a crianca nao entende o que fazer, melhore onboarding.
3. Se a fase 1 parece simples demais, polir fase 1.
4. Se falta motivacao para continuar, melhorar recompensas.
5. Se uma fase parece generica, dar identidade visual.
6. Se o Guardiao parece seco, torna-lo mais guia.
7. Se a colecao parece passiva, torná-la mais celebrativa.
8. Se controles incomodam, ajustar sensacao com cuidado.
9. Se `src/game.py` impedir progresso, separar uma parte pequena com testes.

## Formato De Entrega

Ao final de cada ciclo, responda de forma curta:

- o que mudou;
- por que deixa o jogo mais atraente para criancas;
- arquivos principais alterados;
- como testar;
- validacoes executadas;
- o que nao foi possivel validar;
- proxima melhoria recomendada.

## Ultima Lembranca

Se a melhoria deixa a crianca curiosa, segura e feliz por aprender, ela esta no caminho certo. Prefira uma pequena cena bonita e funcional hoje a um sistema enorme que demora e quebra. O jogo deve crescer como uma colecao de bons momentos: simples, vivos, respeitosos e gostosos de jogar.
