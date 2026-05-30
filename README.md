# Caminhos do Brasil

Jogo de plataforma 2D educativo sobre a historia do Brasil, feito em Python com Pygame-CE e pensado para futura publicacao web com Pygbag.

O jogador controla Mig, um menino ficticio nascido em 2018, que viaja por diferentes periodos historicos do Brasil. A proposta e ensinar historia de forma leve, visual, respeitosa e adequada para criancas.

## Estado Atual

O projeto possui uma versao jogavel e mais polida para primeiro teste publico, com jornada cronologica completa, do ano de 1500 ao Brasil contemporaneo.

Principais recursos:

- Tela inicial com imagem `abertura.png`.
- Menu com continuar jornada, nova sessao temporaria, linha do tempo, colecao e ajuda rapida.
- Linha do tempo com fases bloqueadas, liberadas, proximas e concluidas.
- Dezesseis fases historicas jogaveis.
- Progresso salvo localmente quando possivel.
- Opcao de nova jornada temporaria com `N`, sem apagar o save.
- Movimento lateral, pulo, gravidade, colisao, coyote time e buffer curto de pulo.
- Camera horizontal.
- HUD com ajuste discreto para manter titulos longos dentro do painel.
- Controles por toque para jogar no celular em modo paisagem no navegador.
- Fragmentos historicos coletaveis com brilho, flutuacao e mensagem "Voce sabia?".
- Mensagens historicas fixas no topo; se Mig passar por tras, o painel fica temporariamente translucido.
- Colecao historica com aparencia de album e progresso por fase.
- Introducao narrativa por fase.
- Nota historica e pergunta curta ao concluir fase.
- Portal final liberado apenas apos coletar todos os fragmentos da fase.
- Checkpoints seguros com bandeira animada.
- Areas de cuidado mais visiveis, com aviso antes do contato.
- Tela de pausa.
- Tela final com resumo de fases e fragmentos.
- Cenarios por tema desenhados com Pygame.
- Sprite animado do Mig usando `assets/images/personagem.png`.
- Sons leves gerados por codigo.
- Smoke tests permanentes em `scripts/smoke_tests.py`.
- Script de build web limpo em `scripts/build_pygbag_clean.py`, com tela de carregamento propria e ajuste para evitar travamento na tela "Ready to start !" em celulares.

## Fases Implementadas

1. `1500 - Chegada dos portugueses`
2. `Seculo XVI - Ciclo do acucar`
3. `Seculos XVII e XVIII - Interiorizacao do territorio`
4. `Seculo XVIII - Ciclo do ouro`
5. `1789 - Inconfidencia Mineira`
6. `1808 - Vinda da familia real`
7. `1822 - Independencia`
8. `1822 a 1889 - Imperio`
9. `1888 - Abolicao da escravidao`
10. `1889 - Proclamacao da Republica`
11. `1889 a 1930 - Primeira Republica`
12. `1930 a 1945 - Era Vargas`
13. `1946 a 1964 - Experiencia democratica`
14. `1964 a 1985 - Ditadura militar`
15. `1985 a 1988 - Redemocratizacao`
16. `1988 ate hoje - Brasil contemporaneo`

Cada fase tem:

- introducao curta;
- missao;
- nota historica de conclusao;
- pergunta curta para pensar;
- pelo menos 3 fragmentos;
- pelo menos 1 checkpoint;
- pelo menos 1 area de cuidado;
- objetivo final em forma de portal.

## Como Executar

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
- R: reiniciar a fase.
- M: voltar ao menu em telas internas.
- Esc: sair.

Celular ou tela de toque:

- Use o aparelho deitado, em modo paisagem.
- Toque nas opcoes do menu para continuar, iniciar nova sessao, abrir linha do tempo, colecao ou ajuda.
- Durante a fase, use os botoes virtuais `<`, `>` e `Pular`.
- Toque em `P` para pausar e em `C` para abrir a colecao.
- Na linha do tempo e na colecao, toque nas opcoes ou arraste para rolar.

## Progresso E Salvamento

O jogo salva progresso local em `caminhos_brasil_save.json`.

O save guarda:

- maior fase desbloqueada;
- fases concluidas;
- fragmentos ja coletados na colecao.

No menu:

- `Enter` continua usando o progresso salvo.
- `N` inicia uma nova jornada apenas na sessao atual.

Ao iniciar uma nova jornada temporaria, as fases voltam a comecar bloqueadas e a colecao fica vazia, mas o arquivo de save anterior nao e apagado nem sobrescrito.

Se o save nao puder ser lido ou escrito, o jogo continua funcionando com progresso apenas em memoria.

## Como Testar

Validacao tecnica:

```powershell
python -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
```

Smoke test permanente:

```powershell
python scripts\smoke_tests.py
.\.venv_brasil\Scripts\python.exe scripts\smoke_tests.py
```

Use o segundo comando quando o Python global nao tiver `pygame-ce` instalado.

O smoke test confere:

- existem 16 fases;
- cada fase tem fragmentos, checkpoint e area de cuidado;
- inicio, checkpoints e respawns nao caem em areas de cuidado;
- fragmentos ficam apoiados em plataformas proximas e alcancaveis por criterio conservador;
- `Game` inicializa em modo dummy;
- `abertura.png` e `assets/images/personagem.png` carregam;
- fluxo basico de menu, nova sessao temporaria, colecao, checkpoint, area de cuidado, conclusao e final passa sem alterar o save.
- fluxo basico por toque cobre menu, fase, movimento, pulo, colecao e linha do tempo;
- mensagens historicas permanecem em posicao estavel e ficam translucidas quando Mig passa por tras.

Teste manual recomendado:

1. Abrir com `python main.py`.
2. Verificar se `abertura.png` aparece na tela inicial.
3. Pressionar `Enter` e iniciar a fase liberada.
4. Voltar ao menu.
5. Testar `H` para abrir ajuda rapida.
6. Testar `N` no menu e confirmar que a jornada temporaria comeca na fase 1.
7. Mover, pular e cair em plataformas.
8. Coletar fragmentos.
9. Abrir a colecao com `C`.
10. Ativar checkpoint.
11. Tocar em area de cuidado e confirmar retorno seguro.
12. Reiniciar fase com `R`.
13. Pausar e continuar com `P`.
14. Concluir fase.
15. Confirmar desbloqueio da fase seguinte.
16. Entrar pela linha do tempo com `S`.
17. Testar a fase 2, especialmente fragmentos e checkpoints.
18. Testar uma fase intermediaria.
19. Testar a ultima fase.
20. Ver tela final.
21. Fechar e abrir novamente para confirmar save.

Teste mobile recomendado apos publicar:

1. Abrir `https://msimoes38.github.io/caminhos_brasil/` no celular.
2. Virar o aparelho para modo paisagem.
3. Confirmar que a tela de carregamento mostra mensagem e depois libera o menu.
4. Tocar em continuar e iniciar uma fase.
5. Usar `<`, `>` e `Pular` para mover Mig.
6. Coletar um fragmento.
7. Abrir colecao com `C`.
8. Pausar com `P` e voltar.
9. Abrir a linha do tempo pelo menu.

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
- `src/level_data.py`: contem dados das 16 fases e geradores simples de layout.
- `src/levels.py`: converte dados das fases em objetos `pygame.Rect`.
- `src/backgrounds.py`: desenha cenarios por tema.
- `src/progress.py`: salva e carrega progresso local em JSON.
- `src/sounds.py`: gera sons simples por codigo.
- `src/settings.py`: constantes gerais.
- `scripts/smoke_tests.py`: validacao automatica leve.
- `scripts/build_pygbag_clean.py`: cria uma copia minima e roda build Pygbag sem empacotar venv ou save local.

## Diretriz De Conteudo

Como o jogo e voltado para criancas:

- usar linguagem simples;
- evitar descricoes fortes, violentas ou graficas;
- tratar temas sensiveis com respeito;
- nao glorificar processos historicos controversos;
- valorizar memoria, cidadania, diversidade e curiosidade;
- manter frases curtas nos fragmentos historicos.

## Publicacao Web Futura

A entrada principal ja usa loop `async`, e o projeto evita dependencias alem de Pygame-CE e Pygbag.

O comando direto abaixo foi testado:

```powershell
pygbag .
```

Resultado: o comando iniciou e gerou build, mas na raiz do projeto ele tambem tentou empacotar `.venv_brasil` e `caminhos_brasil_save.json`. Por isso, para publicacao, use o build limpo:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Resultado validado: o build limpo empacotou somente 13 arquivos do jogo (`main.py`, `requirements.txt`, `abertura.png`, `assets/images/personagem.png` e arquivos de `src/`). Ele tambem adiciona uma tela de carregamento propria, que pode ser liberada por toque ou automaticamente apos alguns segundos, e usa `--ume_block=0` para evitar que celulares fiquem presos na tela "Ready to start !" antes do jogo iniciar. A saida fica em:

```text
build/pygbag_app/build/web
```

Pontos ainda a validar antes de publicar:

- abrir o `index.html` gerado em navegador real;
- conferir se a tela inicial de carregamento aparece com mensagem no celular;
- confirmar no celular que a tela "Ready to start !" nao fica travada;
- testar audio no navegador;
- avaliar armazenamento web para substituir ou complementar o save local em arquivo JSON.

## Limites Conhecidos

- As fases compartilham gerador simples de layout.
- O salvamento atual e local por arquivo JSON; no navegador, pode precisar de adaptacao.
- A interface esta otimizada para 960x540.
- A experiencia mobile foi pensada para celular deitado; modo retrato nao possui layout dedicado.
- As mensagens historicas usam painel fixo e translucidez para nao disputar espaco com o pulo do Mig.
- `src/game.py` concentra muitas responsabilidades e pode ser dividido futuramente.
- A build Pygbag limpa passa, mas ainda falta rodada manual em navegador real.

## Proximas Melhorias Recomendadas

1. Fazer teste publico curto com criancas ou familiares observando dificuldade e leitura.
2. Testar o build Pygbag em navegador real.
3. Adaptar `src/progress.py` para armazenamento web quando a publicacao for prioridade.
4. Polir mais layouts especificos de algumas fases sem aumentar complexidade.
5. Separar telas de `src/game.py` se o arquivo crescer mais.
