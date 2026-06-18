# PROMPT LOOP 3 - Transformar Caminhos do Brasil Em Um Jogo De Verdade

Você é um agente de IA trabalhando no projeto `caminhos_brasil`, um jogo de plataforma 2D educativo sobre a história do Brasil, feito em Python com Pygame-CE e publicado no navegador com Pygbag.

Sua missão é trabalhar em ciclos sucessivos de análise, criação, implementação e teste para transformar o jogo em uma experiência muito mais divertida, atraente, variada e memorável para crianças de 8 a 10 anos.

Não trate este trabalho como uma lista de pequenos retoques cosméticos. O projeto já possui muitos sistemas, mas ainda pode parecer um protótipo porque:

- as fases podem transmitir sensações muito parecidas;
- a maior parte da ação ainda se resume a andar, pular e coletar;
- textos, falas e artefatos podem soar padronizados ou intercambiáveis;
- recompensas podem não gerar desejo de continuar ou revisitar;
- efeitos visuais e sonoros podem informar, mas ainda não empolgar;
- a criança pode aprender algo sem sentir que viveu uma aventura;
- sistemas existentes podem estar presentes, mas pouco conectados à jogabilidade.

O objetivo principal é mudar a experiência percebida pela criança. Cada ciclo deve deixar o jogo mais gostoso de jogar, não apenas mais completo no papel.

## Regra Principal Do Modo Looping

Trabalhe continuamente em ciclos de melhoria.

Em cada ciclo:

1. analise o estado atual do projeto;
2. identifique o maior gargalo de atratividade naquele momento;
3. proponha de 3 a 5 melhorias concretas;
4. avalie impacto, simplicidade, risco e valor para crianças;
5. escolha autonomamente a melhoria com melhor relação entre impacto e simplicidade;
6. implemente uma fatia funcional;
7. teste compatibilidade técnica e comportamento;
8. confira visualmente ou jogue a parte alterada quando necessário;
9. explique brevemente o que mudou e como testar;
10. indique o próximo gargalo;
11. inicie imediatamente o ciclo seguinte.

Não espere o usuário escolher entre as propostas. Não pare depois de apresentar um plano. Não encerre o trabalho apenas porque um ciclo foi concluído.

Continue os ciclos enquanto houver tempo e capacidade de execução. Pare apenas quando:

- o usuário pedir para parar;
- existir um bloqueio externo real que exija ação do usuário;
- uma ação irreversível ou arriscada exigir aprovação;
- o ambiente encerrar a execução.

Se o contexto for compactado ou a execução for retomada, releia os documentos, confira `git status`, identifique o último ciclo concluído e continue do ponto seguinte. Não reinicie o projeto nem repita melhorias já entregues.

## Público-Alvo

O jogo deve funcionar simultaneamente para:

- crianças de 8 anos, que precisam entender objetivos e controles rapidamente;
- crianças de 9 anos, que já percebem repetição e querem variedade;
- crianças de 10 anos, que podem buscar segredos, domínio e conclusão completa;
- pais e professores, que devem reconhecer valor histórico, respeito e oportunidades de conversa.

Use esta régua:

### Para 8 anos

- objetivo compreensível em poucos segundos;
- controles tolerantes;
- erros com recuperação rápida;
- textos curtos;
- pistas visuais claras;
- ausência de punições frustrantes.

### Para 9 anos

- fases com identidade própria;
- pequenas surpresas;
- desafios variados;
- recompensas visíveis;
- sensação de avanço frequente.

### Para 10 anos

- objetivos opcionais;
- exploração;
- rotas alternativas;
- domínio de movimento;
- coleção e conquistas;
- vontade de melhorar o resultado ou completar tudo.

### Para adultos acompanhantes

- conteúdo respeitoso e historicamente cuidadoso;
- informação compreensível;
- oportunidades de conversa;
- nenhuma glorificação de processos históricos controversos;
- nenhum excesso de texto obrigatório.

O jogo deve ser simples o bastante para uma criança de 8 anos e interessante o bastante para não parecer bobo a uma criança de 10 anos.

## Visão De Produto

Mig deve parecer um explorador viajando por lugares e períodos diferentes, não apenas o mesmo personagem atravessando plataformas com textos trocados.

A experiência desejada deve ter:

- controles agradáveis;
- ritmo claro;
- descoberta frequente;
- fases reconhecíveis;
- objetivos curtos e variados;
- recompensas que a criança queira conquistar;
- feedback imediato;
- humor leve quando apropriado;
- conteúdo histórico integrado à ação;
- progressão visível;
- motivos para revisitar fases.

A criança deve pensar:

```text
Quero tentar de novo.
Quero descobrir o que tem ali.
Quero ganhar essa estrela.
Quero ver a próxima fase.
```

## Leitura Obrigatória Antes Do Primeiro Ciclo

Leia completamente:

- `AGENTS.md`
- `README.md`
- `SPEC.MD`
- `PROMPT_LOOP.MD`
- `requirements.txt`
- `main.py`
- todos os arquivos relevantes de `src/`
- `scripts/smoke_tests.py`
- `scripts/build_pygbag_clean.py`
- `.github/workflows/pages.yml` quando a mudança tocar publicação

Entenda a arquitetura existente antes de alterar código.

Se houver conflito entre este prompt e `AGENTS.md`, siga `AGENTS.md`.

Confira também:

- `git status`;
- alterações locais existentes;
- sistemas já implementados;
- testes disponíveis;
- ambientes virtuais disponíveis;
- estado das fases afetadas.

Nunca reverta alterações do usuário ou de ciclos anteriores sem pedido explícito.

## Diagnóstico Inicial Obrigatório

Antes de escolher a primeira melhoria de uma nova execução:

1. abra ou renderize o jogo;
2. jogue ou simule pelo menos a fase 1;
3. examine também uma fase inicial, uma intermediária e uma final;
4. confira menu, linha do tempo, Caderno/Coleção, Guardião e tela final;
5. procure textos repetidos ou muito parecidos;
6. observe o ritmo entre ações, mensagens e recompensas;
7. identifique onde a criança ficaria entediada, confusa ou indiferente;
8. confirme que sistemas existentes realmente influenciam a experiência.

Não presuma que uma funcionalidade é divertida apenas porque está implementada.

## Perguntas Para Encontrar O Maior Gargalo

Em cada ciclo, pergunte:

- O que uma criança faz durante a maior parte do tempo?
- Há decisões ou apenas deslocamento?
- A fase tem começo, desenvolvimento e clímax?
- Existe algo surpreendente nos primeiros 30 segundos?
- A criança entende o próximo objetivo sem ler um parágrafo?
- O erro ensina ou apenas interrompe?
- A recompensa parece valiosa?
- Esta fase poderia trocar de texto e continuar parecendo a mesma?
- Há razão para explorar?
- Há razão para jogar novamente?
- Os fatos históricos aparecem através da aventura ou interrompem a aventura?
- O som e a animação tornam a ação mais satisfatória?
- Um jogador de 10 anos encontraria algo para dominar?

Escolha o problema que mais reduz a diversão naquele momento.

## Avaliação Das Propostas

Para cada uma das 3 a 5 propostas do ciclo, avalie de 0 a 5:

- diversão imediata;
- impacto na jogabilidade;
- diferenciação entre fases;
- sensação de recompensa;
- potencial de revisita;
- adequação para 8 a 10 anos;
- integração educativa;
- simplicidade de implementação;
- risco técnico;
- custo para web/mobile.

Prefira a proposta que:

- muda algo que a criança sente ou faz;
- pode ser entregue funcionalmente no ciclo atual;
- usa bem a arquitetura existente;
- não exige dependências novas;
- tem risco controlado;
- pode ser testada de forma objetiva.

Uma melhoria pequena de alto impacto é melhor que um sistema enorme incompleto.

## Regra Contra Ciclos Rasos

Um ciclo não conta como melhoria principal se apenas:

- alterar documentação;
- renomear elementos;
- trocar cores;
- adicionar mais texto;
- adicionar partículas genéricas;
- copiar o mesmo diálogo para todas as fases;
- criar um contador sem recompensa associada;
- adicionar conteúdo que não muda decisões, ritmo ou emoção;
- criar mais uma tela explicativa.

Testes e documentação são obrigatórios, mas não substituem a melhoria jogável.

Em cada grupo de 3 ciclos:

- pelo menos 2 ciclos devem melhorar jogabilidade, fase, desafio, exploração ou recompensa;
- no máximo 1 ciclo pode ser dedicado principalmente a menu, texto ou organização visual;
- pelo menos 1 ciclo deve ser testado manualmente em uma fase real.

## Ordem Geral De Prioridade

Use esta ordem como orientação, não como sequência rígida:

1. sensação de movimento e controle;
2. ritmo e variedade das fases;
3. objetivos e desafios interessantes;
4. recompensas e progressão;
5. identidade própria de cada fase;
6. feedback visual e sonoro;
7. exploração e segredos;
8. Caderno, mapa e telas de progresso;
9. variedade textual e narrativa;
10. arquitetura necessária para continuar evoluindo.

Se a jogabilidade básica não for prazerosa, não esconda o problema atrás de mais interface.

## Frente 1 - Movimento Gostoso

Avalie e melhore com cuidado:

- aceleração e desaceleração;
- controle no ar;
- altura e arco do pulo;
- coyote time;
- jump buffer;
- resposta do toque;
- pouso;
- mudança de direção;
- câmera;
- leitura de colisões;
- respawn;
- sensação de velocidade;
- clareza do alcance do pulo.

Possíveis melhorias:

- poeira ou pequeno impacto ao pousar;
- animação curta de preparação ou aterrissagem;
- variação visual ao correr;
- câmera com antecipação horizontal suave;
- pequena tolerância ao encostar em bordas;
- resposta mais clara quando um pulo falha;
- checkpoints mais próximos após trechos difíceis;
- opção de assistência simples, se realmente necessária.

Não altere física em massa. Faça ajustes pequenos, compare antes/depois e teste as fases 1 e 2, além de uma fase intermediária.

## Frente 2 - Fases Com Identidade Própria

Cada fase deve ter pelo menos um gancho jogável reconhecível.

Não basta mudar:

- cor do céu;
- nome da fase;
- texto da pílula;
- decoração de fundo.

Exemplos de ganchos simples:

- seguir uma sequência de pistas;
- ativar três marcos;
- escolher entre rota segura e rota de exploração;
- transportar um item por um trecho curto;
- encontrar um personagem;
- acompanhar um objeto em movimento;
- atravessar uma área com ritmo próprio;
- localizar uma lembrança escondida;
- completar um desafio de movimento opcional;
- montar uma pequena sequência histórica;
- observar o cenário para descobrir o caminho;
- liberar um atalho;
- escolher qual objetivo secundário tentar.

Estrutura recomendada para uma fase:

1. apresentação rápida do lugar e do objetivo;
2. trecho curto para aprender o gancho;
3. variação simples;
4. recompensa ou descoberta opcional;
5. pequeno clímax antes do portal;
6. fechamento curto com o Guardião.

Introduza no máximo uma mecânica nova importante por fase. Ensine pela ação, não por texto longo.

## Frente 3 - Miniobjetivos E Desafios Opcionais

Use objetivos secundários para criar domínio sem bloquear crianças menores.

Possibilidades:

- encontrar uma lembrança escondida;
- concluir a missão Extra;
- alcançar uma área alta;
- ativar todos os marcos;
- completar um trecho sem cair;
- encontrar uma rota alternativa;
- responder ao Guardião sem usar dica;
- coletar todas as pílulas disponíveis;
- descobrir um personagem ou objeto raro;
- concluir um pequeno desafio de movimento;
- terminar com um item especial.

Regras:

- objetivos opcionais não impedem a conclusão;
- devem ser explicados visualmente;
- devem dar recompensa real;
- não devem punir respostas erradas;
- não devem exigir precisão excessiva;
- devem ser diferentes entre fases quando possível.

## Frente 4 - Recompensas E Progressão

Crie recompensas que comuniquem conquista.

Possíveis sistemas leves:

- até 3 estrelas por fase;
- medalhas por exploração;
- selos por bloco histórico;
- lembranças especiais;
- conquistas locais;
- pontuação simples;
- melhor resultado por fase;
- porcentagem de conclusão;
- cosméticos visuais simples;
- novos postais no Caderno;
- brilho ou moldura especial na linha do tempo;
- pequenas celebrações por completar objetivos.

Exemplo de 3 estrelas sem punição:

- estrela de jornada: concluir a fase;
- estrela de descoberta: cumprir o objetivo opcional;
- estrela de curiosidade: encontrar todas as descobertas da sessão.

Não use cronômetro obrigatório como padrão. Evite transformar aprendizado em competição ansiosa.

Se alterar o save:

- preserve compatibilidade com saves antigos;
- use valores padrão seguros;
- mantenha fallback tolerante;
- teste desktop e simulação web;
- documente a mudança.

Ranking, se houver, deve ser local e simples. Não crie contas, servidor ou ranking online.

## Frente 5 - Feedback Visual E Sonoro

Toda ação importante deve responder de forma clara e agradável:

- pular;
- pousar;
- coletar;
- encontrar segredo;
- cumprir miniobjetivo;
- ativar checkpoint;
- liberar portal;
- errar;
- acertar;
- concluir fase;
- ganhar estrela, medalha ou selo.

Use com moderação:

- partículas leves;
- pulsos;
- brilho;
- pequena mudança de escala;
- animação curta;
- pausa visual muito breve;
- som gerado por código;
- variações de tom;
- rastro sutil;
- movimento de câmera muito pequeno.

Evite:

- excesso de flashes;
- tremor forte;
- sons repetitivos ou estridentes;
- efeitos que escondem plataformas;
- partículas pesadas;
- efeitos que atrapalham mobile.

Feedback deve comunicar causa e recompensa, não apenas decorar.

## Frente 6 - Exploração E Segredos

Crie curiosidade com:

- caminhos parcialmente visíveis;
- pistas no cenário;
- plataformas opcionais;
- pequenos atalhos;
- objetos que reagem à proximidade;
- personagens escondidos;
- itens raros;
- áreas de observação;
- rotas alta e baixa;
- recompensas visuais fora do caminho principal.

Segredos devem:

- ser opcionais;
- ter pistas justas;
- não exigir salto além da física atual;
- não ficar em áreas de cuidado;
- ser registrados no Caderno ou na pontuação;
- variar entre fases.

## Frente 7 - Personagens E Narrativa Curta

Personagens secundários podem dar identidade às fases.

Use:

- falas de uma ou duas frases;
- pedidos simples;
- humor leve;
- reações à ação de Mig;
- dicas contextuais;
- comentários sobre o lugar;
- pequenas despedidas.

Evite:

- caixas longas;
- personagens que apenas despejam fatos;
- falas genéricas reutilizadas;
- estereótipos;
- linguagem infantilizada demais;
- interromper o movimento constantemente.

Um personagem deve ter função jogável ou emocional clara.

## Frente 8 - Textos Menos Padronizados

Faça uma auditoria periódica de textos semelhantes em:

- introduções;
- missões;
- pílulas;
- objetos observáveis;
- missões Extras;
- falas do Guardião;
- mensagens de checkpoint;
- conclusões;
- Caderno;
- artefatos e lembranças.

Não use a mesma estrutura de frase em todas as fases.

Varie formatos:

- descoberta surpreendente;
- pergunta curta;
- comparação com o presente;
- fala de personagem;
- pista;
- observação do cenário;
- pequeno desafio;
- frase de memória;
- convite à exploração;
- relação de causa e consequência.

Cada texto deve responder a pelo menos uma pergunta:

- O que torna esta fase diferente?
- O que a criança acabou de fazer?
- Que curiosidade vale lembrar?
- Como isso se conecta ao cenário?
- Por que esta informação importa?

Prefira mensagens de uma ou duas linhas. Textos obrigatórios devem ser ainda menores.

Não espalhe a mesma frase genérica por todas as fases. Evite fórmulas como:

```text
Esse período trouxe mudanças importantes.
Observe este objeto.
Boa descoberta.
Continue aprendendo.
```

Essas frases podem aparecer pontualmente, mas não devem ser o molde dominante.

O conteúdo deve ser:

- simples;
- curioso;
- narrativo;
- correto;
- adequado para crianças;
- respeitoso;
- sem descrições gráficas;
- sem glorificação de processos controversos;
- sério quando o tema exigir;
- nunca bobo ou condescendente.

Ensine por aventura, exploração, consequência e descoberta. Não transforme o jogo em uma sequência de aulas ou questionários.

## Frente 9 - Linha Do Tempo, Caderno E Menus

Essas telas devem reforçar desejo de continuar.

Linha do tempo:

- mostrar claramente onde Mig está;
- destacar próxima aventura;
- exibir estrelas, medalhas ou segredos;
- permitir comparar conclusão;
- ter leitura clara sem depender apenas de cor;
- parecer um mapa, não uma tabela administrativa.

Caderno/Coleção:

- mostrar descobertas visualmente;
- diferenciar fases;
- destacar itens raros;
- permitir perceber o que falta;
- valorizar personagens, lembranças e postais;
- celebrar conjuntos completos;
- convidar à revisita.

Menu:

- comunicar aventura rapidamente;
- permitir começar sem fricção;
- manter botões claros em toque;
- mostrar progresso atual;
- evitar aparência de tela provisória.

Ajuda e tutorial:

- usar demonstração visual e ação;
- mostrar apenas o necessário naquele momento;
- não listar tudo antes da criança jogar;
- adaptar texto para teclado ou toque.

## Frente 10 - Dificuldade E Acessibilidade

O caminho principal deve ser acessível para 8 anos. A profundidade deve vir de objetivos opcionais.

Considere:

- áreas de aterrissagem generosas;
- recuperação rápida;
- checkpoints bem posicionados;
- dicas após repetidos erros;
- sinais antes de perigos;
- contraste;
- textos legíveis;
- controles grandes no touch;
- status que não dependem apenas de cor;
- modo de assistência simples;
- desafio opcional para jogadores mais experientes.

Se criar modos de dificuldade, mantenha-os simples. Exemplo:

- Aventura: padrão, tolerante;
- Explorador: mesmos conteúdos, desafios opcionais mais exigentes.

Não crie menus complexos ou dezenas de configurações.

## Sistemas Existentes Que Devem Ser Aproveitados

O projeto já possui, entre outros:

- 16 fases;
- movimento, pulo, coyote time e jump buffer;
- controles por teclado e toque;
- pílulas históricas;
- missões Extras;
- momentos observáveis;
- Guardião do Portal;
- Caderno/Coleção;
- linha do tempo;
- selos por blocos;
- save local e web;
- checkpoints;
- áreas de cuidado;
- sons gerados por código;
- efeitos de partículas;
- build web limpo;
- smoke tests.

Antes de criar um sistema paralelo, tente aprofundar e conectar o que já existe.

Exemplos:

- missões Extras podem conceder estrelas;
- momentos observáveis podem liberar postais;
- o Guardião pode comentar objetivos concluídos;
- a linha do tempo pode mostrar desempenho;
- o Caderno pode indicar segredos ainda não encontrados;
- checkpoints podem marcar trechos de uma missão;
- pílulas podem funcionar como pistas, não apenas caixas de texto.

Não reimplemente sistemas existentes com nomes diferentes.

## Limites Obrigatórios

Não:

- troque Pygame-CE por outra engine;
- remova funcionalidades sem motivo claro;
- abandone Pygbag;
- quebre o loop `async` de `main.py`;
- use caminhos absolutos para assets;
- adicione dependências sem necessidade forte;
- torne o download pesado;
- crie sistemas online;
- crie mecânicas complexas demais;
- faça mudanças gigantescas sem organizar o código;
- reescreva `src/game.py` inteiro em um ciclo;
- altere muitas fases de uma vez sem piloto;
- deixe código experimental sem teste;
- bloqueie a progressão por desafio opcional;
- torne respostas erradas punitivas;
- adicione longos textos obrigatórios;
- comprometa teclado, mouse ou touch;
- quebre save local ou web;
- remova `--ume_block=0`;
- remova loading HTML, manifest, touch/save bridge ou fullscreen helper do build limpo;
- empacote venv ou save local no build web.

## Estratégia De Implementação

Trabalhe em fatias verticais.

Uma boa fatia:

- escolhe um gargalo claro;
- toca poucos arquivos;
- muda a experiência do jogador;
- inclui dados, comportamento, feedback e teste;
- pode ser validada em uma fase;
- deixa base reutilizável para ciclos futuros.

Exemplo:

```text
Gargalo: fases não dão motivo para explorar.
Piloto: fase 1.
Melhoria: rota opcional com lembrança rara e estrela de exploração.
Implementação: dado da fase + posicionamento seguro + feedback + Caderno + resumo.
Validação: alcance, colisão, touch, smoke e screenshot.
Próximo ciclo: testar o padrão na fase 2 com objetivo diferente.
```

Quando a ideia for compartilhada por várias fases:

1. implemente em 1 ou 2 fases;
2. valide diversão e estabilidade;
3. corrija o modelo;
4. expanda em ciclos posteriores;
5. preserve diferenças entre fases.

Não copie a mesma atividade para todas as 16 fases.

## Organização De Código

Siga os padrões existentes.

Prefira:

- dados de fase em `src/level_data.py` ou `src/levels.py`;
- física e movimento em `src/player.py`;
- fluxo e estados em `src/game.py`;
- fundos em `src/backgrounds.py`;
- sons em `src/sounds.py`;
- constantes em `src/settings.py`;
- persistência em `src/progress.py`;
- testes em `scripts/smoke_tests.py`.

Se `src/game.py` estiver impedindo uma melhoria:

- extraia apenas uma área coesa;
- preserve comportamento;
- evite abstrações genéricas prematuras;
- adicione ou adapte testes;
- não transforme refatoração em objetivo principal do ciclo.

## Assets

Assets novos devem:

- ser leves;
- usar formatos comuns;
- ficar preferencialmente em `assets/images/` ou `assets/audio/`;
- ter tamanho adequado para web;
- ter função visual clara;
- combinar com o estilo do jogo.

Prefira desenho por Pygame, sprites pequenos e sons gerados por código quando isso for suficiente.

Não adicione imagens grandes apenas como decoração.

## Validação Técnica Obrigatória

Após qualquer alteração de código, rode:

```powershell
python -m compileall main.py src
```

Se existir a venv local, rode também:

```powershell
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall scripts
.\.venv_brasil\Scripts\python.exe scripts\smoke_tests.py
```

Se o Python global não tiver `pygame-ce`, registre a limitação e use a venv.

Quando a mudança tocar fases, física, player, save, assets, controles, recompensas, progressão ou fluxo:

- atualize `scripts/smoke_tests.py`;
- rode o smoke test;
- teste manualmente a fase afetada.

Quando tocar interface, menus, HUD, Caderno, linha do tempo, quiz ou final:

- renderize ou abra o jogo;
- gere screenshot quando possível;
- confira texto, contraste e sobreposição;
- teste em 960x540;
- confira layout touch se afetado.

Quando tocar build web, HTML, save web, touch, fullscreen, loading ou publicação:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Preserve `--ume_block=0` e todos os patches do build limpo.

## Teste Manual Obrigatório Por Ciclo

Explique passos exatos, não apenas “teste o jogo”.

Formato:

```text
1. Execute ...
2. Entre na fase ...
3. Faça ...
4. Observe ...
5. Repita com ...
6. Resultado esperado ...
```

Se mexer em jogabilidade geral, teste pelo menos:

1. fase 1;
2. fase 2;
3. uma fase intermediária;
4. teclado;
5. toque ou simulação touch;
6. queda e respawn;
7. checkpoint;
8. portal e Guardião.

Se mexer em recompensa ou progressão:

1. conquistar;
2. falhar ou ignorar;
3. reiniciar fase;
4. revisitar fase;
5. fechar e carregar save quando persistente;
6. conferir linha do tempo;
7. conferir Caderno;
8. conferir resumo de fase ou final.

## Critérios De Aceite De Cada Ciclo

Um ciclo só está concluído quando:

- existe melhoria perceptível para a criança;
- o recurso principal funciona;
- a fase continua possível de concluir;
- teclado continua funcionando;
- touch não foi prejudicado;
- textos cabem;
- feedback não cobre elementos importantes;
- o conteúdo histórico permanece respeitoso;
- compilação passa;
- smoke test relevante passa;
- teste manual é descrito;
- documentação necessária é atualizada;
- próximo gargalo é identificado.

Se a melhoria não ficou divertida, simplifique ou ajuste antes de expandir.

## Atualização Obrigatória Da Documentação

Quando comportamento, controles, arquitetura, save, publicação ou processo mudar:

- atualize `README.md`;
- atualize `SPEC.MD`;
- atualize `AGENTS.md`;
- atualize `PROMPT_LOOP.MD` apenas na seção de estado do loop e prioridades futuras.

Não descreva como pronto algo que ainda é apenas ideia.

## Comunicação Durante O Loop

No início de cada ciclo, informe de forma curta:

```text
Ciclo N
Maior gargalo observado:
3 a 5 opções:
Escolha:
Por que esta opção:
```

Depois implemente sem pedir confirmação.

Ao concluir o ciclo, informe:

```text
O que mudou:
Por que ficou mais divertido:
Arquivos alterados:
Validações:
Como testar manualmente:
Riscos ou limitações:
Próximo gargalo:
```

Em seguida, comece o próximo ciclo.

Não transforme as atualizações em relatórios longos. Use a maior parte do esforço para implementar e testar.

## Memória Entre Ciclos

Ao final de cada ciclo:

- registre sucintamente o que foi concluído;
- não repita a mesma melhoria;
- preserve decisões que funcionaram;
- anote limitações encontradas;
- mantenha o próximo ciclo concreto;
- confira o estado atual do código antes de continuar.

Use a seção `Estado Atual Do Loop` no final deste arquivo para continuidade. Atualize apenas essa seção, preservando as instruções acima.

## Estado Atual Do Loop

Este bloco deve ser atualizado pelo agente ao final de cada ciclo.

- Situação inicial: jogo funcional, mas ainda pouco empolgante e com sensação de protótipo.
- Problemas percebidos pelo usuário: baixa diversão, pouca variedade, recompensas fracas e textos muito padronizados.
- Prioridade inicial recomendada: diagnosticar a sensação de movimento e o ritmo real das fases antes de adicionar novos sistemas.
- Último ciclo concluído: nenhum ciclo deste novo prompt.
- Próximo ciclo: executar diagnóstico jogável e escolher a primeira melhoria de alto impacto.

## Comando Final

Comece agora.

Leia o projeto, execute o diagnóstico inicial, apresente de 3 a 5 propostas, escolha a melhor, implemente, teste, documente e continue para o ciclo seguinte sem esperar confirmação.

Seu objetivo não é apenas adicionar funcionalidades. Seu objetivo é fazer `Caminhos do Brasil` deixar de parecer um protótipo educativo e passar a parecer uma aventura de plataforma que crianças de 8 a 10 anos realmente queiram jogar, completar e revisitar.
