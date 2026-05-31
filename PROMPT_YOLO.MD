# PROMPT YOLO - Caminhos do Brasil

Voce é um agente de IA trabalhando no projeto `caminhos_brasil`, um jogo educativo 2D em Python/Pygame-CE sobre a história do Brasil para crianças. Trabalhe em modo autônomo, incremental e pragmático: preserve o que ja foi implementado, escolha novas melhorias pequenas quando solicitado, valide, atualize documentação e entregue um resumo claro.

Atualizacao desta rodada: as melhorias de persistencia web, menu/controles touch, linha do tempo, colecao em album e variedade visual foram implementadas. Em proximas rodadas, use este arquivo como registro do que preservar e priorize validacao em navegadores reais, polimento de fases especificas e separacao gradual de telas se `src/game.py` crescer mais.

## Contexto Obrigatório

Antes de alterar código, leia:

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

- O jogo já tem 16 fases históricas, controles por teclado/toque, build Pygbag limpo e smoke tests.
- Cada fase tem banco com 10 pílulas de conhecimento.
- Em cada sessão, a fase 1 sorteia 4 pílulas ativas e as fases 2 a 16 sorteiam 5.
- O Guardião do Portal pergunta apenas sobre uma pílula ativa/coletada na jogada.
- A coleção histórica é acumulativa e mostra progresso do banco completo por fase.
- O save web usa `localStorage` com a chave `caminhos_brasil_save_v1`, mantendo JSON local no desktop.
- O menu touch cobre o rodape confuso da abertura e os controles virtuais nao cobrem Mig no inicio.
- A linha do tempo reserva coluna de status, e a colecao tem visual de album com cards.
- A versão web usa Pygbag e GitHub Pages.
- Não adicione dependências novas.
- Preserve o loop `async` de `main.py`.
- Preserve `--ume_block=0`, a tela HTML de carregamento e o helper de tela cheia em `scripts/build_pygbag_clean.py`.
- Preserve linguagem infantil, acolhedora e respeitosa.

## Objetivo Da Rodada Implementada

Melhorar a versão web/mobile para teste público leve, com foco em persistência, usabilidade touch, limpeza visual e sensação de variedade entre fases.

Esta rodada implementou, nesta ordem de prioridade:

1. Persistência no navegador usando armazenamento web.
2. Ajustes de menu e controles touch.
3. Limpeza da linha do tempo.
4. Coleção histórica com aparência mais forte de álbum.
5. Mais variedade visual por período histórico.

Faça mudanças pequenas, funcionais e coerentes com o estilo existente.

## Melhorias Implementadas

As listas abaixo registram o comportamento que deve ser preservado em futuras rodadas.

### 1. Persistência No Navegador

Adapte `src/progress.py` para salvar e carregar progresso no navegador via `localStorage` quando o jogo estiver rodando em Pygbag.

Comportamento esperado:

- Em ambiente web, usar uma chave estável, por exemplo `caminhos_brasil_save_v1`.
- Em ambiente local/desktop, manter o arquivo `caminhos_brasil_save.json`.
- Se `localStorage` falhar ou não existir, cair para o comportamento atual sem quebrar o jogo.
- `load()` e `save()` devem continuar tolerantes a erro.
- Manter compatibilidade com o formato atual:
  - `highest_unlocked_level`
  - `completed_levels`
  - `collection_entries`
- Normalizar entradas inválidas como hoje.
- Não perder saves antigos em arquivo local.
- Não salvar nada durante nova jornada temporária, pois isso já é controlado em `src/game.py`.

Sugestão técnica:

- Criar helpers privados em `ProgressStore`, como `_get_web_storage()`, `_load_from_web()`, `_save_to_web()`, `_load_from_file()` e `_save_to_file()`.
- Para detectar web, usar `import platform` dentro de `try` e procurar `platform.window.localStorage`.
- Não importar módulos que quebrem desktop.
- Atualizar `scripts/smoke_tests.py` para cobrir pelo menos:
  - formato salvo/carregado continua válido;
  - entradas duplicadas/ruins continuam sendo ignoradas;
  - se armazenamento web simulado falha, o store não quebra.

### 2. Menu E Controles Touch

Corrija dois incômodos da experiência mobile:

- No menu touch, esconder ou substituir qualquer rodapé visual do tipo "PRESSIONE ENTER..." que apareça atrás/parcialmente atrás do painel mobile. Se esse texto vier da imagem `abertura.png`, cubra a faixa inferior com um painel discreto e escreva uma orientação própria para toque, como "Toque em uma opção para começar".
- O botão virtual esquerdo cobre o Mig no começo da fase. Ajuste sem prejudicar jogadores:
  - preferencialmente reposicione os botões virtuais um pouco mais para baixo/lados, mantendo tamanho confortável;
  - se necessário, desloque o `START_POSITION` um pouco para a direita, mas sem quebrar câmera, tutorial, colisão ou fase 1;
  - garanta que os botões não cubram HUD, mensagens históricas nem pílulas iniciais.

Atualize smoke tests para validar que:

- em modo touch, o botão esquerdo não intersecta o retângulo inicial do jogador;
- controles de toque continuam funcionando para esquerda, direita, pular, pausa e coleção.

### 3. Linha Do Tempo Mais Limpa

Melhore a tela de linha do tempo em `src/game.py` para evitar texto/status encostando nos botões de rolagem.

Comportamento esperado:

- Reservar uma coluna fixa à direita para status/medalha.
- Reduzir a largura disponível do título da fase de forma consistente.
- Manter textos longos cabendo com `_render_fitting_text`.
- Manter toque nas linhas funcionando.
- Manter botões de rolagem visíveis quando houver scroll.

Atualize smoke tests se necessário para garantir que as linhas continuam tocáveis e que a seleção por toque ainda abre fase liberada.

### 4. Coleção Histórica Mais Parecida Com Álbum

A coleção atual é funcional, mas densa. Refaça a apresentação para parecer mais um álbum de descobertas.

Comportamento esperado:

- Manter agrupamento por fase e progresso `x/10 descobertas`.
- Mostrar pílulas em cards menores, com borda e destaque para descoberta recente.
- Reduzir densidade por tela sem perder legibilidade.
- Continuar com rolagem por setas/W/S e arraste no touch.
- Manter botão Voltar.
- Não criar cards dentro de cards; use a superfície principal do álbum e cards individuais de pílulas.
- Se a fase não tiver descobertas, mostrar uma mensagem curta e acolhedora.

Critério visual:

- Deve parecer um álbum/caderno de descobertas, não uma tabela.
- Texto não deve ultrapassar o card.
- Em mobile, nada deve encostar nos botões de navegação.

Atualize smoke tests para garantir que:

- a coleção abre e fecha;
- rolagem ainda funciona;
- coleção não duplica entradas;
- contadores continuam usando o banco completo da fase.

### 5. Variedade Visual Das Fases

Adicione 1 ou 2 elementos visuais específicos por período/família de fase em `src/backgrounds.py`, sem aumentar peso do jogo e sem novos assets obrigatórios.

Direção:

- Use formas simples desenhadas por Pygame, coerentes com o estilo atual.
- Evite poluição visual e contraste excessivo.
- Não atrapalhe plataformas, pílulas, HUD, mensagens históricas ou controles touch.
- Mantenha desempenho leve no navegador.

Sugestões:

- `coast`: mais sinais de litoral/navegação, como aves simples, ondas ou marco costeiro.
- `sugar`: moenda/cana mais reconhecível ou pilhas de cana.
- `interior`: rios/trilhas mais claros.
- `mines`: carrinho de mina, trilhos ou lampião.
- `colonial_city`: igrejas/janelas coloniais discretas.
- `court`: palácio mais distinto.
- `independence`: bandeiras/símbolos cívicos discretos.
- `empire`: jardins, postes ou edifícios imperiais.
- `republic`: praça/coreto ou bandeiras.
- `rural_republic`: trilhos/café mais explícitos.
- `vargas`: fábrica/rádio/engrenagens.
- `democracy`: praça cívica/cartazes.
- `dictatorship`: muro de memória discreto, tom sóbrio.
- `redemocratization`: cartazes/assembleia/Constituição.
- `contemporary`: cidade, árvores, conectividade, diversidade.

Não precisa fazer uma obra de arte nova para cada fase; foque em variedade perceptível e segura.

## Documentação

Atualize `README.md`, `SPEC.MD` e `AGENTS.md` se mudar comportamento, arquitetura, salvamento web, UI touch, coleção, testes ou build.

Não deixe a documentação dizer que o save web ainda é apenas um limite conhecido se você implementar `localStorage`.

Atualize `PROMPT_YOLO.MD` apenas se quiser deixar novas prioridades para uma rodada futura.

## Validações Obrigatórias

Rode:

```powershell
python -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall scripts
.\.venv_brasil\Scripts\python.exe scripts\smoke_tests.py
```

Se alterar build web ou persistência web, rode também:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Se o Python global não tiver `pygame-ce`, mencione isso e use a venv local.

## Teste Manual Recomendado

Faça pelo menos um teste manual/local ou visual quando possível:

- Abrir menu desktop e menu touch.
- Confirmar que o menu touch não mostra rodapé confuso atrás do painel.
- Confirmar que o botão esquerdo touch não cobre Mig no início.
- Iniciar fase 1, andar, pular e coletar uma pílula.
- Abrir coleção com `C` e conferir visual de álbum.
- Abrir linha do tempo e conferir status/scroll sem sobreposição.
- Tocar no portal após coletar pílulas e responder ao Guardião.
- Reiniciar/recarregar e verificar persistência quando em ambiente web.

## Critérios De Aceitação

A rodada estará pronta quando:

- Save local continua funcionando no desktop.
- Save web usa `localStorage` no Pygbag e não quebra se indisponível.
- Menu touch está visualmente limpo.
- Controles touch continuam grandes e não cobrem o Mig no início.
- Linha do tempo não tem status encostado nos botões de rolagem.
- Coleção parece mais um álbum e continua legível.
- Fases têm mais variedade visual sem pesar o jogo.
- Smoke tests passam.
- Build Pygbag limpo continua preservando `--ume_block=0`, tela de carregamento, manifest e fullscreen helper.
- README/SPEC/AGENTS refletem o estado final.

## Cuidados Finais

- Não remova funcionalidades existentes.
- Não altere Python, Pygame-CE ou Pygbag.
- Não adicione dependências.
- Não torne o jogo mais difícil.
- Não coloque pílulas em lugares arriscados.
- Não use linguagem histórica pesada.
- Preserve o tom infantil, acolhedor e respeitoso.
- Preserve compatibilidade com saves antigos.
- Ao terminar, explique de forma curta o que mudou, quais arquivos principais foram alterados e quais validações passaram.

## Proximas Prioridades Sugeridas

1. Testar save web, audio e tela cheia em celulares e navegadores reais.
2. Polir layouts de fases especificas sem aumentar a complexidade do gerador.
3. Melhorar feedback visual de portal, checkpoint e pílulas se os testes com jogadores mostrarem necessidade.
4. Separar telas de `src/game.py` apenas quando houver ganho claro de manutencao.
