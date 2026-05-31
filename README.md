# Caminhos do Brasil

Jogo de plataforma 2D educativo sobre a história do Brasil, feito em Python com Pygame-CE e publicado no navegador com Pygbag e GitHub Pages.

O jogador controla Mig, um menino fictício nascido em 2018, que viaja por diferentes períodos históricos do Brasil. A proposta é ensinar história de forma leve, visual, respeitosa e adequada para crianças.

## Estado Atual

O projeto possui uma versão jogável para teste público, com jornada cronológica completa, do ano de 1500 ao Brasil contemporâneo.

Versao publicada:

```text
https://msimoes38.github.io/caminhos_brasil/
```

Principais recursos:

- Tela inicial com imagem `abertura.png`.
- Menu com continuar jornada, nova sessão temporária, linha do tempo, coleção, ajuda rápida e botão mobile de tela cheia.
- Menu mobile com botões grandes, faixa de orientação por toque e botão de tela cheia.
- Linha do tempo com fases bloqueadas, liberadas, próximas e concluídas.
- Dezesseis fases históricas jogáveis.
- Progresso salvo em JSON no desktop e em `localStorage` no navegador quando possível.
- Opção de nova jornada temporária com `N`, sem apagar o save.
- Movimento lateral, pulo, gravidade, colisao, coyote time e buffer curto de pulo.
- Câmera horizontal.
- HUD com ajuste discreto para manter títulos longos dentro do painel.
- Controles por toque para jogar no celular em modo paisagem no navegador, posicionados para não cobrir Mig no início.
- Dicas curtas nos primeiros segundos da fase 1, com texto adequado para teclado ou toque.
- Banco com 10 pílulas de conhecimento por fase.
- Seleção por sessão: 4 pílulas ativas na fase 1 e 5 pílulas ativas nas demais.
- Pílulas históricas coletáveis com brilho, flutuação e mensagem "Você sabia?".
- Feedback positivo de coleta, como "Boa descoberta!", e destaque do portal quando todas as pílulas da jogada são encontradas.
- Mensagens históricas fixas no topo; se Mig passar por trás, o painel fica temporariamente translúcido.
- Coleção histórica acumulativa com aparência de álbum, destaque da descoberta recente e progresso por fase no formato `7/10 descobertas`.
- Introdução narrativa por fase.
- Nota histórica e pergunta curta ao concluir fase.
- Portal final liberado apenas após coletar todas as pílulas ativas da fase.
- Guardião do Portal com pergunta sorteada apenas entre as pílulas que apareceram na jogada.
- Checkpoints seguros com bandeira animada.
- Áreas de cuidado mais visíveis, com aviso antes do contato.
- Tela de pausa com botões grandes para continuar, reiniciar, voltar ao menu e abrir a coleção.
- Tela final com resumo de fases e pílulas descobertas.
- Cenários por tema desenhados com Pygame, com detalhes visuais próprios de cada período.
- Sprite animado do Mig usando `assets/images/personagem.png`.
- Sons leves gerados por codigo.
- Smoke tests permanentes em `scripts/smoke_tests.py`.
- Script de build web limpo em `scripts/build_pygbag_clean.py`, com tela de carregamento propria, metadados de app/manifest e ajuste para evitar travamento na tela "Ready to start !" em celulares.

## Fases Implementadas

1. `1500 - Chegada dos portugueses`
2. `Século XVI - Ciclo do açúcar`
3. `Séculos XVII e XVIII - Interiorização do território`
4. `Século XVIII - Ciclo do ouro`
5. `1789 - Inconfidência Mineira`
6. `1808 - Vinda da família real`
7. `1822 - Independência`
8. `1822 a 1889 - Império`
9. `1888 - Abolição da escravidão`
10. `1889 - Proclamação da República`
11. `1889 a 1930 - Primeira Republica`
12. `1930 a 1945 - Era Vargas`
13. `1946 a 1964 - Experiência democrática`
14. `1964 a 1985 - Ditadura militar`
15. `1985 a 1988 - Redemocratização`
16. `1988 até hoje - Brasil contemporâneo`

Cada fase tem:

- introducao curta;
- missao;
- nota historica de conclusao;
- pergunta curta para pensar;
- banco com 10 pílulas de conhecimento;
- seleção ativa de 4 pílulas na fase 1 e 5 pílulas nas demais;
- pergunta do Guardião do Portal com 3 alternativas, ligada a uma pílula ativa;
- pelo menos 1 checkpoint;
- pelo menos 1 área de cuidado;
- objetivo final em forma de portal.

## Como Executar

No navegador:

```text
https://msimoes38.github.io/caminhos_brasil/
```

Localmente:

```powershell
python -m venv .venv_brasil
.\.venv_brasil\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Controles

Teclado:

- Setas esquerda/direita ou A/D: mover.
- Espaco, seta para cima ou W: pular.
- Enter: confirmar, iniciar fase ou avancar.
- N: iniciar nova jornada temporaria sem apagar o progresso salvo.
- S: abrir linha do tempo no menu.
- H: abrir ajuda rapida no menu ou durante o jogo.
- Setas ou W/S: navegar na linha do tempo e na colecao.
- P: pausar ou continuar durante a fase.
- C: abrir ou fechar a colecao historica.
- No Guardiao do Portal, setas ou W/S escolhem e Enter confirma a resposta.
- R: reiniciar a fase.
- M: voltar ao menu em telas internas.
- Esc: reiniciar a tentativa atual e voltar para a tela inicial.

Celular ou tela de toque:

- Use o aparelho deitado, em modo paisagem.
- Toque nas opcoes do menu para continuar, iniciar nova sessao, abrir linha do tempo, colecao ou ajuda.
- Toque em `Tela cheia` no menu para tentar esconder a barra do navegador.
- Durante a fase, use os botoes virtuais `<`, `>` e `Pular`.
- Toque em `P` para pausar e em `C` para abrir a colecao.
- No Guardiao do Portal, toque em uma alternativa para responder.
- Na pausa, toque em `Continuar`, `Reiniciar`, `Menu` ou `Colecao`.
- Na linha do tempo e na colecao, toque nas opcoes ou arraste para rolar.

## Progresso E Salvamento

No desktop, o jogo salva progresso local em `caminhos_brasil_save.json`.

No navegador via Pygbag, o jogo tenta usar `localStorage` com a chave `caminhos_brasil_save_v1`.

O save guarda:

- maior fase desbloqueada;
- fases concluidas;
- pílulas já descobertas na coleção.

No menu:

- `Enter` continua usando o progresso salvo.
- `N` inicia uma nova jornada apenas na sessao atual.

Ao iniciar uma nova jornada temporária, as fases voltam a começar bloqueadas e a seleção de pílulas é sorteada novamente. A coleção acumulativa permanece disponível na sessão, e o arquivo de save anterior não é apagado nem sobrescrito.

Se o save nao puder ser lido ou escrito, o jogo continua funcionando com progresso apenas em memoria.

## Como Testar

Validacao tecnica:

```powershell
python -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall scripts
```

Smoke test permanente:

```powershell
python scripts\smoke_tests.py
.\.venv_brasil\Scripts\python.exe scripts\smoke_tests.py
```

Use o segundo comando quando o Python global nao tiver `pygame-ce` instalado.

O smoke test confere:

- existem 16 fases;
- cada fase tem banco com 10 pílulas, checkpoint e área de cuidado;
- a fase 1 ativa 4 pílulas por sessão, e as demais ativam 5;
- inicio, checkpoints e respawns nao caem em areas de cuidado;
- pílulas ficam apoiadas em plataformas próximas e alcançáveis por critério conservador;
- `Game` inicializa em modo dummy;
- `abertura.png` e `assets/images/personagem.png` carregam;
- Guardião do Portal pergunta apenas sobre uma pílula ativa da jogada e exige resposta correta para concluir;
- coleção histórica acumula descobertas sem duplicar entradas;
- progresso salva/carrega em arquivo local e em `localStorage` simulado, com fallback seguro;
- fluxo basico de menu, nova sessao temporaria, colecao, checkpoint, area de cuidado, conclusao e final passa sem alterar o save.
- fluxo basico por toque cobre menu, fase, movimento, pulo, colecao e linha do tempo;
- botão virtual esquerdo não cobre Mig no início da fase;
- mensagens historicas permanecem em posicao estavel e ficam translucidas quando Mig passa por tras.

Teste manual recomendado:

1. Abrir com `python main.py`.
2. Verificar se `abertura.png` aparece na tela inicial.
3. Pressionar `Enter` e iniciar a fase liberada.
4. Voltar ao menu.
5. Testar `H` para abrir ajuda rapida.
6. Testar `N` no menu e confirmar que a jornada temporaria comeca na fase 1.
7. Mover, pular e conferir as dicas iniciais da fase 1.
8. Coletar pílulas e observar o feedback positivo.
9. Abrir a coleção com `C` e conferir o visual de álbum e o contador de descobertas.
10. Ativar checkpoint.
11. Tocar em area de cuidado e confirmar retorno seguro.
12. Reiniciar fase com `R`.
13. Pausar e continuar com `P`; em toque, conferir os botoes grandes.
14. Tocar no portal liberado e responder ao Guardiao do Portal.
15. Errar uma alternativa de proposito e conferir dica sem punicao.
16. Acertar a resposta e concluir a fase.
17. Confirmar desbloqueio da fase seguinte.
18. Entrar pela linha do tempo com `S` e conferir status sem encostar nos botões de rolagem.
19. Testar a fase 2, especialmente pílulas, checkpoints e quiz.
20. Testar uma fase intermediaria.
21. Testar a ultima fase.
22. Ver tela final.
23. Fechar e abrir novamente para confirmar save.

Teste mobile recomendado apos publicar:

1. Abrir `https://msimoes38.github.io/caminhos_brasil/` no celular.
2. Virar o aparelho para modo paisagem.
3. Confirmar que a tela de carregamento mostra mensagem e depois libera o menu.
4. Confirmar menu com convite para tocar e botao `Tela cheia`.
5. Tocar em continuar e iniciar uma fase.
6. Usar `<`, `>` e `Pular` para mover Mig.
7. Coletar uma pílula.
8. Abrir colecao com `C`.
9. Pausar com `P` e voltar usando os botoes grandes.
10. Responder ao Guardiao do Portal tocando em uma alternativa.
11. Abrir a linha do tempo pelo menu.

Build web local:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Saida esperada:

```text
build/pygbag_app/build/web
```

## Estrutura De Arquivos

```text
main.py
requirements.txt
README.md
AGENTS.md
SPEC.MD
PROMPT_YOLO.MD
abertura.png
caminhos_brasil_save.json       # gerado em execucao local
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

## Arquitetura Resumida

- `main.py`: ponto de entrada com loop `async`, importante para Pygbag.
- `src/game.py`: controla estados, telas, HUD, progresso, colecao, ajuda, efeitos visuais, abertura e loop principal.
- `src/player.py`: controla Mig, movimento, colisao, coyote time, buffer de pulo e animacao.
- `src/level_data.py`: contém dados das 16 fases, bancos de pílulas históricas e geradores simples de layout.
- `src/levels.py`: converte dados das fases em objetos `pygame.Rect`.
- `src/backgrounds.py`: desenha cenarios por tema, com pequenos detalhes visuais por período.
- `src/progress.py`: salva e carrega progresso em JSON no desktop e em `localStorage` no navegador quando disponível.
- `src/sounds.py`: gera sons simples por codigo.
- `src/settings.py`: constantes gerais.
- `scripts/smoke_tests.py`: validacao automatica leve.
- `scripts/build_pygbag_clean.py`: cria uma copia minima, roda build Pygbag sem empacotar venv/save local e injeta ajustes mobile no `index.html`.

## Diretriz De Conteudo

Como o jogo e voltado para criancas:

- usar linguagem simples;
- evitar descricoes fortes, violentas ou graficas;
- tratar temas sensiveis com respeito;
- nao glorificar processos historicos controversos;
- valorizar memoria, cidadania, diversidade e curiosidade;
- manter frases curtas nas pílulas históricas.

## Publicacao Web

A entrada principal usa loop `async`, e o projeto evita dependencias alem de Pygame-CE e Pygbag.

A publicacao ocorre via GitHub Actions em `.github/workflows/pages.yml` quando ha push na branch:

```text
yolo_melhoria
```

O workflow instala as dependencias, roda `scripts/build_pygbag_clean.py` e publica a pasta:

```text
build/pygbag_app/build/web
```

O comando direto abaixo foi testado:

```powershell
pygbag .
```

Resultado: o comando iniciou e gerou build, mas na raiz do projeto ele tambem tentou empacotar `.venv_brasil` e `caminhos_brasil_save.json`. Por isso, para publicacao, use o build limpo:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Resultado validado: o build limpo empacota somente os arquivos necessarios do jogo (`main.py`, `requirements.txt`, `abertura.png`, `assets/images/personagem.png` e arquivos de `src/`). Ele tambem adiciona uma tela de carregamento propria, manifest basico, titulo/descricao da aba, helper de tela cheia e usa `--ume_block=0` para evitar que celulares fiquem presos na tela "Ready to start !" antes do jogo iniciar. A tela de carregamento pode ser liberada por sinal do jogo, toque/click ou automaticamente apos alguns segundos. A saida fica em:

```text
build/pygbag_app/build/web
```

Checklist apos deploy:

- abrir a URL publicada em desktop e celular;
- conferir se a tela de carregamento aparece com mensagem e nao fica travada;
- usar celular em modo paisagem;
- testar botao `Tela cheia` e, se o navegador nao permitir, orientar uso de "Adicionar a tela inicial";
- iniciar fase, andar, pular, coletar pílula, pausar, abrir coleção e linha do tempo;
- responder ao Guardiao do Portal antes de concluir a fase;
- recarregar a pagina e confirmar que o jogo volta ao menu sem ficar preso no carregamento;
- concluir uma fase, recarregar e confirmar que o progresso web foi mantido no navegador;
- testar audio no navegador;
- conferir se o navegador permite `localStorage`; se nao permitir, o jogo deve seguir sem quebrar.

Checklist curto de publicacao:

- desktop: abrir, iniciar fase, andar, pular, coletar, quiz, pausar, colecao e linha do tempo;
- celular paisagem: carregamento, menu por toque, tela cheia, fase, botoes `<`, `>`, `Pular`, `P`, `C` e quiz por toque;
- progresso: concluir fase, voltar ao menu, abrir linha do tempo e recarregar pagina;
- web: confirmar titulo da aba, manifest basico e ausencia de bloqueio na tela de carregamento.

## Limites Conhecidos

- As fases compartilham gerador simples de layout.
- O salvamento web depende de `localStorage`; se o navegador bloquear esse recurso, o jogo continua sem quebrar, mas pode nao persistir.
- A interface esta otimizada para 960x540.
- A experiencia mobile foi pensada para celular deitado; modo retrato nao possui layout dedicado.
- As mensagens historicas usam painel fixo e translucidez para nao disputar espaco com o pulo do Mig.
- `src/game.py` concentra muitas responsabilidades e pode ser dividido futuramente.
- A experiencia web depende do comportamento do navegador, especialmente em celular; sempre testar apos deploy.

## Proximas Melhorias Recomendadas

1. Fazer teste publico curto com criancas ou familiares observando dificuldade e leitura.
2. Testar persistencia web em celulares e navegadores reais.
3. Melhorar a tela de carregamento com progresso real se o Pygbag expuser um sinal confiavel.
4. Polir mais layouts especificos de algumas fases sem aumentar complexidade.
5. Separar telas de `src/game.py` se o arquivo crescer mais.
