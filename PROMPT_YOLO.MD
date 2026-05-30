# PROMPT_YOLO.MD

Use este prompt para pedir a outro agente de IA que continue o projeto Caminhos do Brasil em modo "yolo", com autonomia para implementar, testar, documentar e entregar o plano de melhorias abaixo.

Modo "yolo" aqui nao significa descuido. Significa agir com criterio: preservar o que funciona, fazer melhorias pequenas e coerentes, validar tecnicamente, testar o maximo possivel e manter a versao web boa para criancas.

---

## Prompt Para O Proximo Agente

Voce e um agente de IA trabalhando no projeto `Caminhos do Brasil`, um jogo de plataforma 2D educativo sobre a historia do Brasil, feito em Python com Pygame-CE e publicado no navegador com Pygbag e GitHub Pages.

Seu objetivo e implementar melhorias incrementais para deixar o jogo mais amigavel, atraente e consistente para criancas de aproximadamente 8 anos, com foco especial na experiencia mobile publicada. Nao entregue apenas proposta: implemente, valide, atualize documentacao e deixe pronto para commit/push.

Trabalhe com autonomia, mas preserve o jogo atual. Nao transforme o projeto em outro jogo. O jogo esta no caminho certo; a meta e polir, nao complicar.

---

## Leitura Obrigatoria Antes De Alterar Arquivos

Antes de editar qualquer arquivo, leia:

- `README.md`
- `AGENTS.md`
- `SPEC.MD`
- `PROMPT_YOLO.MD`
- `requirements.txt`
- `main.py`
- todos os arquivos em `src/`
- `scripts/smoke_tests.py`
- `scripts/build_pygbag_clean.py`
- `.github/workflows/pages.yml`

Depois disso, inspecione tambem:

- `abertura.png`
- `assets/images/personagem.png`
- estado atual do save local, se existir `caminhos_brasil_save.json`

Preserve funcionalidades existentes que ja funcionam. Refatore apenas quando isso ajudar claramente estabilidade, manutencao ou experiencia do jogador.

---

## Contexto Do Projeto

O jogo acompanha Mig, um menino ficticio nascido em 2018, que viaja por diferentes periodos historicos do Brasil, de 1500 ao Brasil contemporaneo.

O jogo deve:

- ser plataforma 2D leve;
- ser educativo;
- ser adequado para criancas, com referencia principal por volta de 8 anos;
- usar linguagem simples, cuidadosa e respeitosa;
- evitar descricoes fortes, violentas ou graficas;
- nao glorificar processos historicos controversos;
- funcionar localmente com Pygame-CE;
- funcionar no navegador com Pygbag e GitHub Pages;
- priorizar clareza, estabilidade e simplicidade.

URL publicada:

```text
https://msimoes38.github.io/caminhos_brasil/
```

Branch de publicacao:

```text
yolo_melhoria
```

O deploy acontece pelo workflow:

```text
.github/workflows/pages.yml
```

---

## Estado Atual Do Projeto

O projeto ja possui:

- tela inicial usando `abertura.png`;
- menu com continuar, nova sessao temporaria, linha do tempo, colecao e ajuda;
- linha do tempo com fases bloqueadas, liberadas, proximas e concluidas;
- progresso salvo localmente em `caminhos_brasil_save.json`;
- nova jornada temporaria com `N`, sem apagar ou sobrescrever o save salvo;
- 16 fases historicas em ordem cronologica;
- movimento lateral, pulo, gravidade, colisao, coyote time, buffer curto de pulo, controle no ar e limite de queda;
- camera horizontal;
- HUD com ajuste discreto para titulos longos;
- controles por toque para celular em modo paisagem no navegador;
- botoes virtuais semitransparentes para mobile;
- fragmentos historicos coletaveis com brilho e flutuacao;
- mensagens historicas com "Voce sabia?";
- mensagens historicas fixas no topo, com painel temporariamente translucido quando Mig passa por tras;
- colecao historica em formato de album, agrupada por fase;
- introducao narrativa por fase;
- nota historica e pergunta curta ao concluir fase;
- tela de pausa;
- tela final com resumo de fases e fragmentos;
- checkpoints seguros com bandeira animada;
- areas de cuidado com aviso visual;
- portal final bloqueado ate todos os fragmentos da fase serem coletados;
- feedback visual para coleta, checkpoint, area de cuidado, portal e conclusao;
- sons leves gerados por codigo;
- sprite animado do Mig em `assets/images/personagem.png`;
- cenarios por tema desenhados em Pygame;
- smoke tests permanentes em `scripts/smoke_tests.py`;
- build Pygbag limpo em `scripts/build_pygbag_clean.py`;
- tela HTML de carregamento no build web, com fallback por sinal do jogo, toque/click e tempo automatico;
- deploy automatico pelo GitHub Pages.

Observacoes importantes:

- A fase 2 ja teve problemas de checkpoints sobre areas de cuidado e fragmentos inalcancaveis. Nao reintroduza esses problemas.
- Checkpoints e respawns nunca devem cair em areas de cuidado.
- Fragmentos devem estar apoiados em plataformas alcancaveis pelo pulo atual.
- A mensagem historica nao deve mudar de lugar durante o pulo. Preserve painel fixo e translucido quando necessario.
- Os botoes virtuais de toque devem continuar grandes, visiveis e sem cobrir HUD ou mensagens historicas.
- A abertura deve continuar usando `abertura.png` quando disponivel.
- O sprite usado pelo jogo e `assets/images/personagem.png`.
- O jogo deve continuar funcionando se audio ou save falharem.
- `pygbag .` na raiz pode empacotar `.venv_brasil` e `caminhos_brasil_save.json`; para publicacao, prefira `scripts/build_pygbag_clean.py`.
- Preserve `--ume_block=0` em `scripts/build_pygbag_clean.py`.
- Preserve o patch contra travamento na tela "Ready to start !" do Pygbag.
- Preserve a tela HTML de carregamento. Ela deve poder sumir por sinal do jogo, toque/click e tempo automatico.
- A pasta `build/` e artefato gerado. Ela pode ser apagada e recriada.

---

## Plano De Melhorias A Implementar

Implemente em ordem de prioridade. Os itens 1 e 2 sao obrigatorios e devem vir primeiro.

1. **Tela inicial mobile mais amigavel**
   - Hoje, no celular, o usuario precisa tocar onde aparece uma instrucao baseada em teclado, como "Enter".
   - Ajuste a tela inicial/menu para detectar uso de toque e mostrar texto amigavel: "Toque para comecar" ou botoes claros.
   - No celular, mostrar areas/botoes grandes para `Continuar`, `Nova jornada`, `Linha do tempo`, `Colecao` e `Ajuda`.
   - No desktop, manter atalhos de teclado visiveis e funcionais.
   - Nao remover a arte `abertura.png`.

2. **Modo tela cheia no celular**
   - Adicionar um botao discreto e claro para tentar abrir em tela cheia no celular, por exemplo `Tela cheia`.
   - Acionar fullscreen via navegador quando possivel.
   - Se o navegador nao permitir fullscreen, mostrar orientacao simples: "Se a barra continuar aparecendo, use Adicionar a tela inicial".
   - Considerar tambem metadados/manifest no build web para melhorar a experiencia quando instalado/adicionado a tela inicial.
   - A implementacao deve ser tolerante a falhas e nao pode quebrar desktop.

3. **Primeiros segundos mais guiados**
   - Na fase 1, mostrar dicas curtas e contextuais:
     - "Use os botoes para andar."
     - "Toque em Pular."
     - "Pegue os fragmentos brilhantes."
   - As dicas devem sumir depois de alguns segundos ou apos a acao correspondente.
   - No desktop, as dicas podem mencionar teclado; no mobile, devem mencionar toque.

4. **Feedback infantil mais claro**
   - Ao coletar fragmento, mostrar feedback curto e positivo, como "Boa descoberta!".
   - Melhorar um pouco brilho/particulas/som sem exagerar.
   - Quando todos os fragmentos forem coletados, destacar o portal com pulso visual ou mensagem mais clara.

5. **Melhorar sensacao de movimento**
   - Avaliar pequenos ajustes de aceleracao, desaceleracao e pulo.
   - Prioridade: Mig deve parecer responsivo para uma crianca de 8 anos.
   - Evite mudar drasticamente a fisica ou quebrar plataformas/fragmentos.
   - Se mudar fisica, rode smoke tests e revise alcance de fragmentos.

6. **Botoes mobile mais confortaveis**
   - Revisar tamanho, posicao e transparencia dos botoes virtuais.
   - Eles devem continuar faceis de tocar, mas nao devem cobrir Mig, perigos ou informacoes importantes.
   - Validar com screenshot em 960x540 e, se possivel, em navegador/celular.

7. **Tela de pausa mais tocavel**
   - Melhorar a pausa mobile com botoes grandes:
     - `Continuar`
     - `Reiniciar`
     - `Menu`
     - `Colecao`
   - Manter atalhos de teclado existentes.

8. **Colecao mais recompensadora**
   - Destacar fragmentos recem-coletados.
   - Melhorar texto/contador por fase, por exemplo "3/4 descobertas".
   - Nao transformar em sistema complexo.

9. **Linha do tempo mais atraente**
   - Destacar melhor a proxima fase liberada com texto simples, como "Proxima aventura".
   - Em fases bloqueadas, manter mensagem clara: "Complete a fase anterior para liberar".

10. **Revisar dificuldade das primeiras fases**
    - Testar fase 1 e fase 2 pensando em crianca.
    - A fase 1 deve ensinar.
    - A fase 2 pode desafiar um pouco mais, mas sem frustrar.
    - Nao alongar fases.

11. **Melhorar tela de carregamento web**
    - Manter a tela atual, mas deixa-la mais alinhada ao jogo:
      - titulo;
      - dica curta;
      - orientacao paisagem;
      - mensagem como "Preparando a viagem no tempo...".
    - Ela nunca pode bloquear o jogo indefinidamente.

12. **Melhorar publicacao online**
    - Ajustar titulo da aba, icone, descricao e manifest basico quando fizer sentido.
    - O alvo e parecer mais "app" quando aberto/adicionado no celular.
    - Nao adicionar dependencias.

13. **Save web**
    - Avaliar adaptar `src/progress.py` para armazenamento web.
    - Se implementar, preservar save local em desktop e tolerancia a falhas.
    - Se nao implementar agora, documentar claramente como limite conhecido.

14. **Checklist final de publicacao**
    - Atualizar README/SPEC com checklist curto:
      - desktop;
      - celular paisagem;
      - tela cheia;
      - iniciar fase;
      - andar;
      - pular;
      - coletar;
      - pausar;
      - colecao;
      - linha do tempo;
      - recarregar pagina.

Se o tempo/escopo ficar grande, implemente pelo menos os itens 1, 2, 3, 6, 11, 12 e 14. Nao sacrifique estabilidade para tentar fazer todos.

---

## Fases Atuais

O jogo possui as 16 fases:

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

Nao adicione novas fases nesta rodada, a menos que o usuario peca explicitamente.

---

## Diretriz De Linguagem Historica

Como o jogo e voltado para criancas:

- use linguagem simples;
- evite descricoes fortes, violentas ou graficas;
- trate temas sensiveis com respeito;
- nao glorifique personagens ou processos historicos controversos;
- valorize aprendizado historico, memoria, diversidade e cidadania;
- ao mencionar povos indigenas, pessoas escravizadas ou grupos afetados por processos historicos, use linguagem respeitosa e cuidadosa;
- prefira frases curtas nos fragmentos e notas de fase.

Tom seguro:

```text
Esse periodo trouxe mudancas importantes e tambem desafios para muitas pessoas. E um tema que deve ser estudado com cuidado e respeito.
```

---

## Controles Que Devem Permanecer

- A/D ou setas esquerda/direita: mover.
- W, seta para cima ou espaco: pular.
- Enter: confirmar, iniciar fase ou avancar.
- N: nova jornada temporaria no menu.
- S: linha do tempo no menu.
- H: ajuda rapida.
- C: colecao historica.
- P: pausar ou continuar.
- R: reiniciar fase.
- M: voltar ao menu.
- Esc: sair.
- No celular: usar modo paisagem, tocar nas opcoes de menu e jogar com `<`, `>` e `Pular`.

Se adicionar novo controle, documente e mantenha simples.

---

## Arquivos Importantes

- `main.py`: ponto de entrada com loop `async`, importante para Pygbag.
- `src/game.py`: estados, telas, HUD, efeitos, colecao, linha do tempo, fluxo, toque e progresso.
- `src/player.py`: movimento, colisao, coyote time, buffer de pulo e animacao.
- `src/level_data.py`: dados das 16 fases e geracao simples de layout.
- `src/levels.py`: conversao dos dados das fases em objetos usados pelo Pygame.
- `src/backgrounds.py`: desenho dos cenarios por tema.
- `src/progress.py`: salvamento local em JSON, tolerante a falhas.
- `src/sounds.py`: sons simples gerados por codigo, com fallback silencioso.
- `src/settings.py`: constantes gerais.
- `scripts/smoke_tests.py`: validacao automatica leve.
- `scripts/build_pygbag_clean.py`: build web limpo, patch mobile, tela de carregamento e ajustes do `index.html`.
- `.github/workflows/pages.yml`: deploy GitHub Pages.
- `README.md`: como executar, jogar, testar e publicar.
- `SPEC.MD`: especificacao tecnica para continuidade.
- `AGENTS.md`: regras para agentes de IA.
- `PROMPT_YOLO.MD`: este prompt.

---

## Preparacao Para Publicacao Online

O projeto deve continuar pronto para Pygbag:

- `main.py` deve manter loop `async`;
- assets devem usar caminhos relativos;
- dependencias devem permanecer minimas;
- audio deve falhar de forma segura;
- save nao pode impedir gameplay;
- build web deve continuar usando `scripts/build_pygbag_clean.py`.

Nao use `pygbag .` como unica validacao se `.venv_brasil` ou `caminhos_brasil_save.json` estiverem na raiz. Use:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Saida esperada:

```text
build/pygbag_app/build/web
```

Depois de publicar, teste com query string para evitar cache, por exemplo:

```text
https://msimoes38.github.io/caminhos_brasil/?v=6
```

---

## Validacoes Automaticas Esperadas

No minimo, rode:

```powershell
python -m compileall main.py src
```

Se existir ambiente virtual:

```powershell
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
.\.venv_brasil\Scripts\python.exe -m compileall scripts
```

Rode smoke tests:

```powershell
python scripts\smoke_tests.py
```

Se o Python global nao tiver `pygame-ce`, use:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\smoke_tests.py
```

Ao alterar build web, rode:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Se alterar UI, renderize ou abra o jogo e confira visualmente. Se possivel, gere screenshots em SDL dummy para registrar a aparencia.

---

## Testes Manuais Recomendados

Teste local minimo:

1. Abrir o jogo.
2. Confirmar `abertura.png` na tela inicial.
3. Pressionar `Enter` e iniciar a jornada salva.
4. Voltar ao menu.
5. Pressionar `H` e conferir ajuda rapida.
6. Pressionar `N` e confirmar nova jornada temporaria.
7. Iniciar fase 1.
8. Mover e pular.
9. Coletar fragmentos.
10. Conferir se a mensagem historica fica fixa e translucida se Mig passar por tras.
11. Abrir colecao com `C`.
12. Ativar checkpoint.
13. Tocar em area de cuidado e confirmar retorno seguro.
14. Reiniciar fase com `R`.
15. Pausar e continuar com `P`.
16. Concluir fase.
17. Confirmar desbloqueio da fase seguinte.
18. Abrir linha do tempo com `S`.
19. Testar fase 2.

Teste mobile web minimo:

1. Abrir a URL publicada no celular em modo paisagem.
2. Confirmar tela de carregamento.
3. Testar botao/fluxo de tela cheia.
4. Confirmar que o menu mobile diz para tocar, nao apenas apertar Enter.
5. Tocar em continuar.
6. Tocar na introducao para iniciar.
7. Andar com `<` e `>`.
8. Pular com `Pular`.
9. Coletar fragmento.
10. Abrir colecao.
11. Pausar e continuar.
12. Voltar ao menu.
13. Abrir linha do tempo.

Se nao for possivel testar tudo, documente exatamente o que foi testado e o que ficou pendente.

---

## Documentacao Obrigatoria Ao Final

Atualize quando houver mudancas:

- `README.md`
- `SPEC.MD`
- `AGENTS.md`
- `PROMPT_YOLO.MD`, se o escopo ou estado do projeto mudar de forma relevante

README deve conter:

- como executar;
- controles;
- estado atual;
- fases implementadas;
- como testar;
- observacoes sobre Pygbag/GitHub Pages;
- limites conhecidos.

SPEC deve conter:

- arquitetura atualizada;
- estados do jogo;
- modelo de dados;
- assets;
- salvamento;
- build e deploy;
- como adicionar fase;
- limites conhecidos;
- testes recomendados.

AGENTS deve conter:

- regras para agentes;
- cuidados historicos;
- pontos recentes de atencao;
- validacoes obrigatorias.

---

## Criterios De Aceite

Ao final, o jogo deve:

- abrir sem erro com `python main.py` ou com a venv local;
- manter a tela inicial com `abertura.png`;
- ter tela inicial mobile amigavel, com convite claro para tocar;
- oferecer tentativa de tela cheia no celular sem quebrar desktop;
- manter controles de teclado existentes;
- manter controles de toque existentes;
- permitir continuar jornada salva;
- permitir nova jornada temporaria com `N`;
- permitir jogar do menu ate a tela final;
- manter 16 fases historicas;
- manter progressao cronologica;
- manter linha do tempo funcional;
- manter colecao historica funcional;
- manter pausa funcional;
- manter ajuda rapida com `H`;
- manter linguagem adequada para criancas;
- nao quebrar animacao do Mig;
- nao quebrar coleta;
- nao quebrar checkpoints;
- nao quebrar camera;
- nao deixar respawn em area de cuidado;
- nao deixar fragmentos inalcancaveis;
- manter mensagens historicas fixas e translucidas quando Mig passa por tras;
- passar em `python -m compileall main.py src`;
- passar no smoke test na venv local;
- gerar build Pygbag limpo;
- ter documentacao atualizada.

---

## Resultado Esperado Na Resposta Final

Ao concluir, responda ao usuario com:

- resumo das melhorias implementadas;
- arquivos alterados;
- como executar;
- como testar;
- validacoes executadas;
- resultado do build Pygbag;
- pendencias ou limites conhecidos;
- comandos sugeridos de commit/push.

Se algo nao foi testado, diga claramente.

Nao entregue apenas proposta. Implemente, valide e documente.
