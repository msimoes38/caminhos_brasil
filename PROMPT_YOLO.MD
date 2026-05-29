# PROMPT_YOLO.MD

Use este prompt para pedir a outro agente de IA que continue o projeto Caminhos do Brasil em modo "yolo": com autonomia para implementar, testar, documentar e entregar uma versao mais completa, sem depender de aprovacoes pequenas a cada passo.

O modo "yolo" aqui nao significa descuido. Significa executar com criterio, preservar o que ja funciona, validar tecnicamente e priorizar uma experiencia jogavel, bonita, leve e adequada para criancas.

---

## Prompt Para O Agente

Voce e um agente de IA trabalhando no projeto `Caminhos do Brasil`, um jogo de plataforma 2D educativo sobre a historia do Brasil, feito em Python com Pygame-CE e pensado para futura publicacao web com Pygbag.

Seu objetivo e prosseguir com autonomia e entregar uma versao mais polida, consistente e pronta para primeiro teste publico, melhorando jogabilidade, atratividade para criancas de cerca de 8 anos e preparacao operacional para publicacao online.

Nao entregue apenas proposta. Implemente, valide e documente.

---

## Leitura Obrigatoria Antes De Alterar Arquivos

Antes de editar qualquer arquivo, leia:

- `README.md`
- `AGENTS.md`
- `SPEC.MD`
- `requirements.txt`
- `main.py`
- todos os arquivos em `src/`

Depois disso, inspecione tambem:

- `abertura.png`
- `assets/images/personagem.png`
- estado atual do save local, se existir `caminhos_brasil_save.json`

Preserve funcionalidades existentes que ja funcionam. Refatore apenas quando isso ajudar claramente a melhorar estabilidade, manutencao ou experiencia do jogador.

---

## Contexto Do Projeto

O jogo acompanha Mig, um menino ficticio nascido em 2018, que viaja por periodos historicos do Brasil.

O jogo deve:

- ser plataforma 2D leve;
- ser educativo;
- ser adequado para criancas;
- usar linguagem simples, cuidadosa e respeitosa;
- evitar descricoes fortes, violentas ou graficas;
- nao glorificar processos historicos controversos;
- funcionar localmente com Pygame-CE;
- ser pensado para futura execucao no navegador com Pygbag;
- priorizar clareza e simplicidade em vez de sistemas complexos.

---

## Estado Atual Do Projeto

O projeto ja possui:

- tela inicial usando `abertura.png`;
- menu com `Enter` para continuar, `N` para nova sessao temporaria, `S` para linha do tempo e `C` para colecao;
- linha do tempo com fases bloqueadas, liberadas e concluidas;
- progresso salvo localmente em `caminhos_brasil_save.json`;
- nova jornada temporaria com `N`, sem apagar ou sobrescrever o save salvo;
- 16 fases historicas em ordem cronologica;
- movimento lateral, pulo, gravidade e colisao;
- camera horizontal;
- fragmentos historicos coletaveis;
- colecao historica agrupada por fase;
- introducao narrativa por fase;
- nota historica ao concluir fase;
- tela de pausa;
- tela final com creditos simples;
- checkpoints;
- areas de cuidado;
- sons leves gerados por codigo;
- sprite animado do Mig em `assets/images/personagem.png`;
- cenarios por tema desenhados em Pygame;
- documentacao atualizada em `README.md`, `AGENTS.md` e `SPEC.MD`.

Observacoes importantes:

- A fase 2 ja teve problemas de checkpoints sobre areas de cuidado e fragmentos inalcanccaveis. Nao reintroduza esses problemas.
- Checkpoints e respawns nunca devem cair em areas de cuidado.
- Fragmentos devem estar em plataformas alcancaveis pelo pulo atual.
- A abertura deve continuar usando `abertura.png` quando disponivel.
- O jogo deve continuar funcionando se audio ou save falharem.

---

## Fases Atuais

O jogo ja possui as 16 fases:

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

Nao e prioridade adicionar mais fases. A prioridade agora e deixar as fases existentes mais gostosas, claras, bonitas, seguras e publicaveis.

---

## Objetivo Principal Do Modo YOLO

Transformar o estado atual em uma versao mais finalizada para criancas, com:

- controles mais confortaveis;
- fases mais justas;
- feedback visual mais claro;
- elementos mais atrativos;
- colecao e linha do tempo mais agradaveis;
- audio leve melhor polido;
- validacoes automaticas simples;
- documentacao pronta para continuidade e publicacao;
- tentativa real de teste com Pygbag, ou documentacao clara do que faltou validar.

Nao complique demais. O jogo esta no caminho certo. Melhore a experiencia sem transformar o projeto em outro jogo.

---

## Prioridades De Implementacao

Siga esta ordem:

1. Estabilidade e jogabilidade.
2. Fases justas e alcancaveis.
3. Feedback visual claro.
4. Atratividade para crianca de 8 anos.
5. Colecao e linha do tempo mais motivadoras.
6. Audio leve.
7. Preparacao para publicacao web.
8. Documentacao final.
9. Testes finais.

Se houver conflito entre polimento e estabilidade, escolha estabilidade.

---

## Melhorias De Jogabilidade

Implemente melhorias simples no "sentir" do personagem:

- pulo um pouco mais confortavel;
- queda menos brusca, se necessario;
- controle no ar mais suave;
- margem de perdao para pulo depois de sair da plataforma, conhecida como "coyote time";
- opcionalmente buffer de pulo por poucos milissegundos, para aceitar pulo apertado um pouco antes de tocar no chao;
- evitar qualquer mudanca que torne fases existentes impossiveis.

Depois de mudar fisica:

- revisar fase 1;
- revisar fase 2;
- revisar uma fase intermediaria;
- revisar a fase 16;
- garantir que fragmentos continuam alcancaveis.

---

## Melhorias Nas Fases

Melhore as fases sem reescrever tudo:

- reduzir trechos vazios;
- deixar o ritmo mais direto;
- manter fases curtas o suficiente para crianca;
- criar caminhos mais guiados para os fragmentos;
- tornar areas de cuidado mais legiveis;
- diferenciar alguns desafios entre fases, sem complexidade excessiva.

Ideias simples permitidas:

- pequenas plataformas moveis em poucas fases, se implementadas com seguranca;
- rotas alternativas faceis para fragmentos;
- degraus historicos ou plataformas de apoio;
- avisos visuais antes de areas de cuidado;
- reposicionamento de fragmentos e checkpoints.

Evite:

- inimigos complexos;
- combate;
- fisica complicada;
- fases longas demais;
- saltos de precisao frustrantes.

---

## Tutorial E Acessibilidade Infantil

Adicione ou melhore uma introducao/tutorial simples.

Pode ser:

- uma tela de ajuda acessivel pelo menu;
- instrucoes visuais na fase 1;
- mensagens curtas no HUD;
- pequenos desenhos dos controles.

Requisitos:

- textos curtos;
- vocabulario simples;
- nada de telas cheias de explicacao;
- teclado simples;
- manter legibilidade em 960x540.

Controles atuais que devem permanecer:

- A/D ou setas: mover;
- W, seta para cima ou espaco: pular;
- Enter: confirmar;
- N: nova sessao temporaria no menu;
- S: linha do tempo no menu;
- C: colecao;
- P: pausa;
- R: reiniciar fase;
- M: menu;
- Esc: sair.

Se adicionar novo controle, documente e mantenha simples.

---

## Feedback Visual

Melhore feedback visual dos elementos principais:

- fragmentos com brilho ou flutuacao leve;
- checkpoint com bandeira mais bonita ou animada;
- objetivo final como portal ou marco historico mais claro;
- feedback quando Mig tenta chegar ao objetivo sem todos os fragmentos;
- efeito simples ao coletar fragmento;
- efeito simples ao ativar checkpoint;
- efeito simples ao concluir fase.

Tudo deve continuar leve e desenhado por Pygame quando possivel.

Evite assets pesados.

---

## Visual E Atratividade

Preserve `abertura.png` como tela inicial principal.

Melhore a atratividade geral sem pesar:

- plataformas com estilo por tema;
- fragmentos mais chamativos;
- areas de cuidado mais claras;
- objetivo final mais especial;
- linha do tempo mais bonita e legivel;
- tela final visualmente mais recompensadora;
- colecao com aparencia de album historico.

Nao use dependencias externas novas sem necessidade.

---

## Conteudo Educativo

Revisar e, se fizer sentido, melhorar textos dos fragmentos:

- transformar alguns em frases tipo "Voce sabia?";
- manter informacoes curtas;
- manter tom infantil;
- manter respeito em temas sensiveis;
- evitar julgamento simplista;
- evitar "bons contra maus";
- evitar descricao grafica ou pesada.

Ao concluir cada fase, se couber, adicionar pergunta curta:

- "O que mudou nesse periodo?"
- "Quem ja vivia nesse territorio?"
- "Por que estudar isso com respeito?"
- "O que podemos aprender com esse momento?"

Nao transforme o jogo em livro didatico. O texto deve apoiar a aventura.

---

## Progressao E Motivacao

Melhore a motivacao do jogador com recompensas simples:

- medalha de fase concluida;
- indicador de todos os fragmentos coletados;
- destaque para proxima fase na linha do tempo;
- tela final mostrando quantos fragmentos foram coletados do total;
- mensagens positivas curtas.

Nao crie sistema complexo de conquistas se isso atrasar estabilidade.

---

## Colecao Historica

Melhore a colecao para parecer mais um album historico:

- mostrar fragmentos agrupados por fase;
- mostrar total coletado e total disponivel;
- indicar fases sem fragmentos coletados, se isso melhorar clareza;
- permitir rolagem;
- manter legibilidade;
- carregar dados do save quando disponivel;
- respeitar nova sessao temporaria com colecao vazia.

Se a mudanca ficar grande demais, mantenha a colecao atual funcionando e apenas melhore visual/legibilidade.

---

## Audio

Manter audio leve e seguro.

Pode melhorar `src/sounds.py` com:

- sons mais distintos para menu;
- coleta;
- checkpoint;
- portal final;
- erro leve;
- final da jornada;
- opcionalmente musica ambiente bem simples, apenas se nao pesar nem complicar.

Requisito absoluto:

- se audio falhar, o jogo continua funcionando normalmente.

---

## Salvamento

Preserve:

- save local em `caminhos_brasil_save.json`;
- fallback quando leitura/escrita falhar;
- `N` inicia nova jornada temporaria sem apagar nem sobrescrever o progresso salvo;
- progresso salvo com fases liberadas, fases concluidas e colecao.

Para web:

- avaliar se `src/progress.py` precisa adaptacao;
- se nao for possivel implementar armazenamento web agora, documentar claramente.

Nao deixe falha de save impedir gameplay.

---

## Preparacao Para Publicacao Online

Ao final, tentar validar ou preparar:

```powershell
pygbag .
```

Verificar:

- `main.py` continua com loop `async`;
- `abertura.png` carrega;
- `assets/images/personagem.png` carrega;
- nao ha caminhos absolutos;
- dependencias continuam minimas;
- assets nao foram duplicados sem necessidade;
- audio falha de forma segura;
- save nao quebra no ambiente web.

Se nao conseguir testar Pygbag, atualize README e SPEC explicando exatamente o que falta validar.

---

## Validacoes Automaticas Esperadas

No minimo, rode:

```powershell
python -m compileall main.py src
```

Se existir ambiente virtual:

```powershell
.\.venv_brasil\Scripts\python.exe -m compileall main.py src
```

Crie ou rode smoke tests simples, mesmo que sejam scripts temporarios, para conferir:

- existem 16 fases;
- cada fase tem fragmentos;
- cada fase tem checkpoint;
- cada fase tem area de cuidado;
- checkpoints nao colidem com areas de cuidado;
- respawns nao caem em areas de cuidado;
- fragmentos ficam em plataformas alcancaveis por criterio conservador;
- `Game` inicializa em modo dummy;
- menu carrega `abertura.png`.

Se criar testes permanentes, documente como rodar.

---

## Testes Manuais Obrigatorios

Ao final, testar manualmente o maximo possivel:

1. Abrir o jogo.
2. Ver `abertura.png` na tela inicial.
3. Pressionar `Enter` e iniciar a jornada salva.
4. Voltar ao menu.
5. Pressionar `N` e confirmar nova jornada temporaria.
6. Iniciar fase 1.
7. Mover e pular.
8. Coletar fragmentos.
9. Abrir colecao com `C`.
10. Ativar checkpoint.
11. Tocar em area de cuidado e confirmar retorno seguro.
12. Reiniciar fase com `R`.
13. Pausar e continuar com `P`.
14. Concluir fase.
15. Confirmar desbloqueio da fase seguinte.
16. Abrir linha do tempo com `S`.
17. Testar fase 2 com todos os fragmentos.
18. Testar uma fase intermediaria.
19. Testar fase 16.
20. Ver tela final.
21. Fechar e abrir novamente para conferir save.

Se nao for possivel testar tudo, documente claramente o que foi testado e o que nao foi.

---

## Documentacao Obrigatoria Ao Final

Atualize:

- `README.md`
- `SPEC.MD`
- `AGENTS.md`, se novas regras importantes surgirem.
- `PROMPT_YOLO.MD`, se o escopo ou estado do projeto mudar de forma relevante.

README deve conter:

- como executar;
- controles;
- estado atual;
- fases implementadas;
- como testar;
- observacoes sobre Pygbag;
- limites conhecidos.

SPEC deve conter:

- arquitetura atualizada;
- estados do jogo;
- modelo de dados;
- assets;
- salvamento;
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

- abrir sem erro com `python main.py`;
- manter a tela inicial com `abertura.png`;
- permitir continuar jornada salva com `Enter`;
- permitir nova jornada temporaria com `N`;
- permitir jogar do menu ate a tela final;
- manter 16 fases historicas;
- manter progressao cronologica;
- manter linha do tempo funcional;
- manter colecao historica funcional;
- manter pausa funcional;
- manter controles documentados;
- manter linguagem adequada para criancas;
- nao quebrar animacao do Mig;
- nao quebrar coleta;
- nao quebrar checkpoints;
- nao quebrar camera;
- nao deixar respawn em area de cuidado;
- nao deixar fragmentos inalcanccaveis;
- passar em `python -m compileall main.py src`;
- ter README, SPEC e AGENTS atualizados;
- estar pronto para primeiro teste com usuario final;
- ter Pygbag testado ou pendencia de Pygbag documentada.

---

## Estilo De Trabalho

Trabalhe com autonomia, mas:

- preserve o que ja funciona;
- faca mudancas coerentes;
- prefira pequenas melhorias acumuladas;
- nao adicione dependencias sem motivo forte;
- nao refatore por vaidade;
- rode validacoes;
- atualize documentacao;
- liste testes feitos;
- liste pendencias reais;
- seja honesto sobre o que nao foi testado.

---

## Resultado Esperado Na Resposta Final

Ao concluir, responda ao usuario com:

- resumo do jogo entregue;
- principais melhorias implementadas;
- arquivos alterados;
- como executar;
- como testar;
- validacoes executadas;
- resultado do teste Pygbag ou pendencia;
- limites conhecidos;
- proximas melhorias opcionais.

Nao entregue apenas uma proposta. Implemente.
