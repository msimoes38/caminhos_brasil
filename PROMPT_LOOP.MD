# PROMPT LOOP 2 - Grande Salto Emocional De Caminhos Do Brasil

Voce e um agente de IA trabalhando no projeto `caminhos_brasil`, um jogo educativo 2D em Python/Pygame-CE sobre a historia do Brasil para criancas. Sua missao agora nao e apenas polir detalhes: e conduzir uma evolucao criativa que faca o jogo parecer mais vivo, emocionante, memoravel e gostoso de revisitar, mantendo a leveza tecnica necessaria para rodar no navegador via Pygbag e GitHub Pages.

Este prompt substitui o ciclo anterior. O jogo ja tem uma base funcional forte: 16 fases, pilulas historicas, Guardiao do Portal, colecao, linha do tempo, lembrancas da viagem, selos, momentos observaveis, toque/mobile, save local/web, sons por codigo e build limpo. A partir daqui, pense como diretor de experiencia, designer de jogo educativo e engenheiro cuidadoso ao mesmo tempo.

## Estado Apos Esta Rodada

- Ciclo B/G iniciou: a primeira pilula inedita de uma jornada limpa na fase 1 ganhou ritual de Caderno de Viagem, particulas e som leve.
- O primeiro portal da fase 1 ganhou fala especial do Guardiao e brilho extra.
- O Guardiao agora tem retrato simples animado por formas no quiz, com estado visual para ritual e dica.
- Ciclo I avancou para todas as 16 fases: microeventos textuais viraram `StageMoment`, objetos observaveis no cenario com mensagem, particulas e registro no Caderno.
- O Caderno agora trata momentos observaveis como lembrancas da viagem e pode destaca-los como descoberta recente com texto legivel.
- A tela final ganhou uma mini-retrospectiva de lembrancas marcantes guardadas no Caderno.
- `scripts/smoke_tests.py` cobre o ritual da primeira descoberta, o primeiro portal, momentos observaveis, Caderno e retrospectiva final sem alterar o save local.
- Proxima rodada recomendada: polir uma fase ancora com arte/cenario mais memoravel ou evoluir o Caderno com postais visuais, sem reimplementar o ritual inicial nem os `StageMoment`.

## Visao De Produto

Transforme `Caminhos do Brasil` em uma pequena aventura historica com clima de jornada: Mig nao deve apenas atravessar plataformas; ele deve sentir que esta visitando lugares, lembrando descobertas, montando um caderno de viagem e chegando ao final com uma sensacao de conquista.

A experiencia-alvo:

- A crianca entende rapido o que fazer e sente vontade de continuar.
- Cada fase tem pelo menos um momento visual ou interativo que a torna lembravel.
- O Guardiao do Portal parece um companheiro-guia, nao uma prova escolar.
- A colecao parece um "Caderno de Viagem" vivo, nao apenas uma lista.
- A linha do tempo parece um mapa de aventura historica.
- O final relembra a jornada com carinho e da vontade de revisitar fases.
- O jogo continua simples, respeitoso, leve, estavel e jogavel no celular.

## Leitura Obrigatoria

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

Se houver conflito entre este prompt e `AGENTS.md`, siga `AGENTS.md`.

## Regras Inegociaveis

- Preserve Python, Pygame-CE, Pygbag e o loop `async` de `main.py`.
- Nao troque de engine.
- Nao adicione dependencias novas sem necessidade muito clara.
- Nao adicione Selenium ao `requirements.txt`; use o Selenium ja instalado na venv apenas para teste de navegador quando fizer sentido.
- Nao torne o build web pesado.
- Nao quebre teclado, mouse, toque, save local, save web, nova jornada temporaria com `N`, colecao ou linha do tempo.
- Preserve `scripts/build_pygbag_clean.py`, `--ume_block=0`, loading HTML, manifest, ponte JS de touch/save e helper de tela cheia.
- Nao use caminhos absolutos para assets.
- Nao use linguagem historica pesada, grafica, violenta ou inadequada para criancas.
- Nao glorifique processos historicos controversos.
- Ao tratar povos indigenas, pessoas escravizadas, memoria, democracia, direitos, desigualdade ou grupos afetados, use linguagem cuidadosa, curta e respeitosa.
- Nao coloque pilulas, missoes, checkpoints, respawns ou elementos obrigatorios em locais injustos.
- Nao cubra Mig, HUD, mensagens historicas ou botoes touch.

## O Que Significa "Grande Salto"

Um grande salto nao e um sistema enorme. E um conjunto de melhorias verticais que mudam a sensacao do jogo:

1. **Cenas memoraveis**: cada bloco historico ganha momentos visuais/interativos que a crianca reconhece.
2. **Ritual de descoberta**: coletar pilulas, observar extras e abrir portal ganha mais brilho, som, movimento e sentido.
3. **Caderno de Viagem**: a colecao vira um album afetivo, com paginas, postais, selos, lembrancas e progresso claro.
4. **Guardiao-personagem**: o Guardiao recebe voz, presenca, reacoes e pequenas falas por bloco/fase.
5. **Mapa de aventura**: a linha do tempo parece um percurso vivo, com caminhos, marcos, proxima parada e selos.
6. **Final retrospectivo**: a tela final mostra uma celebracao da jornada, com resumo visual e convite para revisitar.
7. **Polimento sensorial**: particulas, camera sutil, sons leves, pequenas animacoes e feedback instantaneo.

Implemente em fatias. Cada ciclo deve terminar com o jogo funcionando melhor do que antes.

## Estrategia Recomendada

Trabalhe em "fatias verticais": escolha uma melhoria que atravesse dados, visual, feedback e teste, mas com escopo pequeno.

Uma fatia boa:

- adiciona uma cena especial a 1 ou 2 fases;
- melhora uma tela importante;
- acrescenta uma recompensa visual;
- deixa um fluxo mais emocionante;
- atualiza smoke tests e docs quando comportamento muda.

Uma fatia ruim:

- reescreve todo `src/game.py` de uma vez;
- cria um motor novo;
- muda todas as fases sem validar;
- adiciona assets pesados;
- altera fisica sem teste manual;
- cria UI complexa demais para celular.

## Arquitetura Leve Sugerida

Se precisar criar estruturas novas, prefira modelos simples:

- dados em Python em `src/level_data.py` ou `src/levels.py`;
- helpers de desenho em `src/backgrounds.py` ou funcoes pequenas em `src/game.py`;
- sons gerados em `src/sounds.py`;
- constantes em `src/settings.py`;
- testes em `scripts/smoke_tests.py`.

Possiveis estruturas leves:

- `StageMoment`: pequeno momento observavel por fase, com titulo, texto curto, posicao, cor e icone.
- `TravelPostcard`: item visual do Caderno de Viagem gerado a partir de fase, pilula, missao extra ou selo.
- `GuardianLine`: falas do Guardiao por bloco, fase, erro, acerto e final.
- `CelebrationBurst`: configuracao simples para particulas/sons em coleta, portal, selo e album completo.

Crie novas abstrações apenas se reduzirem complexidade real. Se um helper local resolver, use helper local.

## Prioridade 0 - Confiabilidade Antes Da Magia

Antes de qualquer encanto, corrija o que quebrar:

- abrir o jogo;
- iniciar fase;
- mover e pular;
- coletar pilulas;
- responder Guardiao;
- abrir colecao;
- abrir linha do tempo;
- usar toque em celular paisagem;
- salvar/carregar progresso;
- gerar build web limpo.

Se uma melhoria ameaçar estabilidade, simplifique a ideia.

## Prioridade 1 - Primeiro Minuto Mais Emocionante

O primeiro minuto deve dizer: "vem comigo, isso aqui e uma aventura".

Ideias:

- menu com microanimacoes discretas na arte, botoes e caminho historico;
- chamada curta de aventura, sem virar tela de marketing;
- transicao suave do menu para a primeira fase;
- tutorial da fase 1 com pequenos marcos visuais, nao apenas texto;
- primeira pilula com celebracao especial;
- primeiro portal com ritual claro: brilho, som, fala do Guardiao e recompensa.

Valide em desktop e em toque. Nada pode ficar pequeno demais no celular.

## Prioridade 2 - Fases Ancora Cinematograficas

Escolha poucas fases para elevar bastante primeiro:

1. Fase 1: chegada/litoral, inicio da jornada.
2. Fase 2: engenho/acucar, clareza visual e cuidado historico.
3. Fase 9: abolicao, memoria e respeito.
4. Fase 14: ditadura, direitos e memoria sem peso grafico.
5. Fase 16: Brasil contemporaneo, chegada ao presente.

Para cada fase ancora:

- adicione profundidade visual com formas simples;
- crie um momento observavel;
- use uma frase curta e respeitosa;
- melhore portal/checkpoint/pilulas sem alterar dificuldade injustamente;
- garanta que os elementos nao cobrem controles ou HUD.

Depois de validar as fases ancora, espalhe o padrao para outras fases.

## Prioridade 3 - Caderno De Viagem Vivo

Evolua a colecao para parecer um caderno/album que Mig esta construindo.

Ideias:

- abas por bloco historico;
- pagina "Hoje descobri..." com descoberta recente;
- postais por fase com mini-cenario desenhado por Pygame;
- lembrancas de missoes extras com icones e frase curta;
- selo de album completo com brilho ou pequena animacao;
- progresso por bloco com linguagem de aventura;
- tela vazia acolhedora quando ainda ha poucas descobertas;
- opcao de revisitar fase a partir da colecao, se couber sem complicar.

Nao transforme a colecao em sistema pesado. O objetivo e dar vontade de completar.

## Prioridade 4 - Guardiao Como Personagem

O Guardiao deve ter presenca carismatica e educativa.

Ideias:

- retrato simples animado por formas;
- falas por bloco historico;
- reacao gentil quando a crianca erra;
- celebracao quando acerta;
- conexao clara com a pilula perguntada;
- "memoria do portal": uma frase que resume a descoberta antes de liberar;
- efeito visual no portal quando todas as pilulas sao coletadas;
- som proprio do Guardiao.

Evite longos dialogos. Uma ou duas frases curtas bastam.

## Prioridade 5 - Mapa Da Jornada

A linha do tempo deve virar um mapa que a crianca entende e quer completar.

Ideias:

- caminho com curvas e pontos de parada;
- mini-icones por fase ou bloco;
- marcador "voce esta aqui";
- pre-visualizacao curta da proxima fase;
- selos conquistados integrados ao mapa;
- estados bloqueado/liberado/concluido que nao dependem so de cor;
- animacao discreta no proximo destino.

Preserve navegacao por teclado, mouse e toque.

## Prioridade 6 - Momentos De Descoberta Por Fase

Transforme microeventos em momentos observaveis de verdade.

Ideia de formato:

- um objeto simples no cenario: placa, livro, radio, arvore, mapa, marco, luz, ponte, carta, escola, estrela;
- ao se aproximar ou tocar, aparece frase curta;
- gera particulas leves e som suave;
- entra no Caderno de Viagem como lembranca;
- nao e obrigatorio para concluir fase;
- nao aumenta dificuldade.

Comece com 3 fases. Depois generalize.

## Prioridade 7 - Feedback Sensorial

O jogo deve responder com alegria ao aprendizado.

Melhore:

- coleta de pilula;
- checkpoint;
- missao extra;
- album completo;
- selo de bloco;
- portal bloqueado/liberado;
- resposta correta/errada;
- final da fase;
- final do jogo.

Use:

- particulas pequenas;
- pulsos de brilho;
- sons gerados por codigo;
- pequenos deslocamentos ou escalas visuais;
- camera muito sutil, sem enjoo e sem atrapalhar pulo.

Tudo deve continuar barato para web.

## Prioridade 8 - Final Que Da Arrepio Bom

A tela final deve parecer uma chegada, nao apenas um placar.

Ideias:

- retrospectiva visual dos blocos historicos;
- selos conquistados com brilho;
- contagem de pilulas, lembrancas e fases;
- frase final sobre aprender historia com curiosidade e respeito;
- convite para revisitar fases incompletas;
- mini-mapa completo;
- destaque para "Caderno de Viagem";
- som final leve e alegre.

Nao use texto longo. A emocao deve vir da composicao, dos selos e da memoria da jornada.

## Prioridade 9 - Mobile E Acessibilidade

Cada salto visual precisa funcionar em celular paisagem.

Cuidados:

- botoes grandes;
- toque tolerante;
- textos curtos;
- contraste forte;
- nada importante atras dos controles;
- HUD e mensagem historica sempre legiveis;
- quiz com alternativas grandes;
- colecao e linha do tempo rolaveis;
- evitar elementos pequenos demais;
- preservar orientacao HTML acessivel fora do canvas.

Nao dependa apenas de cor para status. Use texto, icone, forma ou padrao.

## Ciclos Criativos De Alto Impacto

Escolha um ciclo por rodada, implemente e valide. Se o usuario pedir "todos", faca em lotes coerentes, sempre mantendo o jogo funcional.

### Ciclo A - Abertura De Aventura

Transformar menu e entrada na fase 1 em um convite emocional: caminho animado, brilho discreto, chamada curta, botoes mais vivos, transicao suave para introducao.

### Ciclo B - Ritual Da Primeira Descoberta

Criar celebracao especial para a primeira pilula da fase 1 e para o primeiro portal: particulas, som, fala curta do Guardiao e feedback visual claro.

### Ciclo C - Caderno De Viagem 1.0

Reorganizar a colecao para parecer um caderno: capa, abas simples, descoberta recente, lembrancas, selos e progresso por bloco em composicao mais bonita.

### Ciclo D - Fase Ancora: Litoral Memoravel

Elevar a fase 1 com profundidade visual, objetos observaveis, momento de descoberta opcional e melhorias de feedback sem mudar plataformas.

### Ciclo E - Fase Ancora: Engenho Com Cuidado

Polir fase 2 com visual mais claro, areas de cuidado mais compreensiveis, objeto observavel e linguagem historica respeitosa.

### Ciclo F - Fase Ancora: Memoria E Direitos

Polir fases sensiveis, especialmente abolicao, ditadura e redemocratizacao, com luz suave, memoria, livros, cartazes civicos e textos cuidadosos.

### Ciclo G - Guardiao Vivo

Dar mais presenca ao Guardiao: retrato simples, falas por bloco, reacao de erro/acerto, som proprio e portal mais expressivo.

### Ciclo H - Mapa Da Jornada

Melhorar linha do tempo como mapa: caminho mais visual, voce-esta-aqui, proxima parada, selos por bloco e pre-visualizacao curta.

### Ciclo I - Momentos Observaveis

Consolidado: os microeventos textuais ja foram substituidos por objetos observaveis nas 16 fases, com registro no Caderno de Viagem. Proximas melhorias devem polir visual, icones, postais ou interacoes desses momentos, nao recriar o sistema.

### Ciclo J - Final Retrospectivo

Criar final mais emocionante com mini-retrospectiva, selos, lembrancas, resumo visual e convite para revisitar.

### Ciclo K - Juiciness Seguro

Adicionar mais vida a coleta, checkpoint, portal, album completo e selos com particulas, pulso, sons e animacoes discretas.

### Ciclo L - Mobile Premium

Revisar toque, legibilidade, colecao, linha do tempo e quiz em layout mobile. Melhorar alvos de toque e reduzir qualquer sobreposicao.

### Ciclo M - Arquitetura Para Crescer

Se `src/game.py` estiver dificultando progresso, extraia apenas uma parte pequena e segura, como desenho da colecao, linha do tempo ou final. Preserve comportamento e testes.

## Banco De Ideias Por Bloco Historico

Use como inspiracao visual, nao como checklist obrigatorio.

### Primeiros Contatos

- mar com brilho;
- vento em folhas;
- conchas;
- barco distante;
- marco de memoria;
- frase sobre muitos povos ja viverem aqui.

### Brasil Colonial

- canavial;
- roda d'agua;
- caminhos de terra;
- mapas;
- vilas;
- pedras brilhantes discretas;
- frase sobre trabalho, encontros, mudancas e cuidado.

### Independencia E Imperio

- cartas;
- livros;
- jardins;
- bancos de praca;
- lampioes;
- bandeiras discretas;
- frase sobre escolhas, mudancas e perguntas.

### Republica E Democracia

- jornais;
- radio;
- trilhos;
- cartazes civicos;
- praca de conversa;
- escola;
- frase sobre participacao, direitos e memoria.

### Brasil De Hoje

- escola;
- tecnologia;
- natureza;
- conexoes;
- diversidade;
- ambiente urbano e verde;
- frase sobre o presente tambem fazer parte da historia.

## Validacoes Obrigatorias

Para qualquer alteracao de codigo:

```powershell
python -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall scripts
.\.venv_brasil\Scripts\python.exe scripts\smoke_tests.py
```

Se o Python global nao tiver `pygame-ce`, registre isso e use a venv.

Se alterar build web, HTML, save web, touch, carregamento, fullscreen ou publicacao:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Se alterar interface, visual, fases, mobile ou telas:

- gere screenshot local ou faca teste manual;
- confira fase 1 e fase afetada;
- confira menu, colecao, linha do tempo, quiz e final se tocados;
- em navegador, use Selenium ja instalado na venv quando fizer sentido;
- nao adicione Selenium ao projeto.

## Smoke Tests Devem Evoluir

Atualize `scripts/smoke_tests.py` quando adicionar:

- novo dado obrigatorio por fase;
- novo tipo de objeto observavel;
- nova regra de colecao;
- nova regra de save;
- nova regra de touch;
- novo requisito de quiz/Guardiao;
- nova regra de posicionamento de item;
- nova tela ou fluxo importante.

Smoke test nao substitui teste visual. Use os dois quando mexer em interface.

## Teste Manual Minimo

Quando mexer em visual, gameplay ou fluxo:

1. Abrir o jogo.
2. Confirmar tela inicial.
3. Entrar na fase 1.
4. Mover e pular.
5. Coletar uma pilula.
6. Observar feedback de coleta.
7. Acionar um momento observavel ou missao extra.
8. Abrir Caderno/Colecao.
9. Pausar e continuar.
10. Tocar no portal bloqueado.
11. Coletar tudo e liberar portal.
12. Responder o Guardiao com erro e acerto.
13. Confirmar conclusao de fase.
14. Abrir linha do tempo.
15. Conferir toque se a mudanca afetar mobile.
16. Conferir fase 2 se mexer em fisica, layout, HUD ou feedback geral.
17. Conferir tela final se mexer em recompensas ou progresso.

## Como Escolher O Proximo Passo

Use esta ordem de decisao:

1. Se algo quebra web/mobile/save, corrija.
2. Se o primeiro minuto ainda nao encanta, melhore entrada e fase 1.
3. Se a colecao nao da vontade de completar, evolua Caderno de Viagem.
4. Se o Guardiao parece seco, de mais presenca a ele.
5. Se as fases parecem parecidas, escolha uma fase ancora e torne memoravel.
6. Se falta emocao no progresso, melhore linha do tempo, selos e final.
7. Se a jogabilidade incomoda, ajuste controle com cuidado e teste manual.
8. Se `src/game.py` travar evolucao, extraia uma parte pequena com testes.

## Criterios De Aceite Para Um Grande Salto

Considere que uma rodada grande foi bem sucedida quando:

- o jogo continua abrindo e passando smoke tests;
- pelo menos uma tela ou fase ficou visivelmente mais memoravel;
- a crianca recebe feedback mais claro e alegre;
- a linguagem historica continua respeitosa;
- mobile continua jogavel;
- o save nao quebra;
- o build web limpo continua preservado;
- docs e testes refletem o novo comportamento.

## Formato De Entrega Para O Agente

Ao final, responda de forma curta:

- o que mudou;
- qual sensacao nova isso traz para a crianca;
- quais arquivos foram alterados;
- como testar;
- validacoes executadas;
- o que nao foi possivel validar;
- proxima melhoria recomendada.

## Ultima Direcao Criativa

O jogo deve crescer como um caderno de memorias: cada fase deixa uma imagem, uma frase, um som e uma pequena conquista. Busque encanto sem exagero, emocao sem peso, aprendizado sem sermão e beleza sem quebrar a web. O melhor salto sera aquele que fizer uma crianca pensar: "quero ver a proxima parte da historia".
