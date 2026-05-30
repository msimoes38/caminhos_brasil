# PROMPT_YOLO.MD

Use este prompt para pedir a outro agente de IA que continue o projeto Caminhos do Brasil em modo "yolo", com autonomia para implementar, testar, documentar e entregar os ultimos ajustes finais antes da preparacao para publicacao.

Modo "yolo" aqui nao significa descuido. Significa agir com criterio: preservar o que funciona, fazer melhorias pequenas e coerentes, validar tecnicamente, testar o maximo possivel e deixar o projeto mais pronto para criancas e para build web.

---

## Prompt Para O Proximo Agente

Voce e um agente de IA trabalhando no projeto `Caminhos do Brasil`, um jogo de plataforma 2D educativo sobre a historia do Brasil, feito em Python com Pygame-CE e pensado para futura publicacao web com Pygbag.

Seu objetivo e fazer os ultimos ajustes finais antes da preparacao para publicacao: polir experiencia, corrigir problemas remanescentes, validar jogo local, validar build web limpo e atualizar documentacao. Nao entregue apenas proposta. Implemente, valide e documente.

Trabalhe com autonomia, mas preserve o jogo atual. Nao transforme o projeto em outro jogo.

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

Depois disso, inspecione tambem:

- `abertura.png`
- `assets/images/personagem.png`
- estado atual do save local, se existir `caminhos_brasil_save.json`

Preserve funcionalidades existentes que ja funcionam. Refatore apenas quando isso ajudar claramente estabilidade, manutencao ou experiencia do jogador.

---

## Contexto Do Jogo

O jogo acompanha Mig, um menino ficticio nascido em 2018, que viaja por periodos historicos do Brasil.

O jogo deve:

- ser plataforma 2D leve;
- ser educativo;
- ser adequado para criancas, com referencia principal por volta de 8 anos;
- usar linguagem simples, cuidadosa e respeitosa;
- evitar descricoes fortes, violentas ou graficas;
- nao glorificar processos historicos controversos;
- funcionar localmente com Pygame-CE;
- ser pensado para futura execucao no navegador com Pygbag;
- priorizar clareza, estabilidade e simplicidade.

---

## Estado Atual Do Projeto

O projeto ja possui:

- tela inicial usando `abertura.png`;
- menu com `Enter` para continuar, `N` para nova sessao temporaria, `S` para linha do tempo, `C` para colecao e `H` para ajuda;
- linha do tempo com fases bloqueadas, liberadas, proximas e concluidas;
- progresso salvo localmente em `caminhos_brasil_save.json`;
- nova jornada temporaria com `N`, sem apagar ou sobrescrever o save salvo;
- 16 fases historicas em ordem cronologica;
- movimento lateral, pulo, gravidade, colisao, coyote time, buffer curto de pulo, controle no ar e limite de queda;
- camera horizontal;
- HUD com ajuste discreto para titulos longos;
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
- documentacao atualizada em `README.md`, `AGENTS.md` e `SPEC.MD`.

Observacoes importantes:

- A fase 2 ja teve problemas de checkpoints sobre areas de cuidado e fragmentos inalcancaveis. Nao reintroduza esses problemas.
- Checkpoints e respawns nunca devem cair em areas de cuidado.
- Fragmentos devem estar apoiados em plataformas alcancaveis pelo pulo atual.
- A mensagem historica nao deve mudar de lugar durante o pulo. Preserve painel fixo e translucido quando necessario.
- A abertura deve continuar usando `abertura.png` quando disponivel.
- O sprite usado pelo jogo e `assets/images/personagem.png`.
- O jogo deve continuar funcionando se audio ou save falharem.
- `pygbag .` na raiz pode empacotar `.venv_brasil` e `caminhos_brasil_save.json`; para publicacao, prefira `scripts/build_pygbag_clean.py`.
- A pasta `build/` e artefato gerado. Ela pode ser apagada e recriada.

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

Nao e prioridade adicionar fases. A prioridade e polir, validar e preparar a versao existente.

---

## Prioridades Para Os Ajustes Finais

Siga esta ordem:

1. Estabilidade.
2. Jogabilidade justa.
3. Legibilidade e conforto visual.
4. Experiencia infantil acolhedora.
5. Validacao das fases e do save.
6. Validacao Pygbag.
7. Documentacao final.

Se houver conflito entre polimento e estabilidade, escolha estabilidade.

---

## Ajustes Finais Que Voce Deve Avaliar

Nao implemente tudo automaticamente se nao houver necessidade. Avalie o jogo atual, corrija o que estiver ruim e mantenha o escopo pequeno.

Prioridades provaveis:

- Rodar o jogo local e observar se menus, HUD, colecao, linha do tempo, ajuda e final estao legiveis em 960x540.
- Conferir se as mensagens historicas fixas e translucidas nao atrapalham o pulo.
- Testar fase 1, fase 2, uma fase intermediaria e fase 16.
- Conferir se fragmentos continuam alcancaveis.
- Conferir se checkpoints e respawns continuam seguros.
- Melhorar pequenos detalhes visuais somente se estiverem claramente atrapalhando leitura ou prazer de jogar.
- Conferir se a colecao com muitos fragmentos continua legivel e rolavel.
- Conferir se linha do tempo destaca bem a proxima fase.
- Conferir se a tela final resume bem a jornada e a colecao.
- Conferir se a nova sessao temporaria com `N` continua sem gravar no save.
- Conferir se falha de audio ou save nao quebra o jogo.
- Rodar build Pygbag limpo e, se possivel, abrir em navegador real.
- Atualizar README, SPEC e AGENTS se qualquer comportamento mudar.

Evite:

- adicionar inimigos;
- adicionar combate;
- adicionar fisica complexa;
- adicionar dependencias novas;
- alongar fases;
- refatorar por vaidade;
- mexer em conteudo historico sensivel sem necessidade;
- reposicionar dinamicamente a mensagem historica durante o pulo.

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

Se adicionar novo controle, documente e mantenha simples.

---

## Arquivos Importantes

- `main.py`: ponto de entrada com loop `async`, importante para Pygbag.
- `src/game.py`: estados, telas, HUD, efeitos, colecao, linha do tempo, fluxo e progresso.
- `src/player.py`: movimento, colisao, coyote time, buffer de pulo e animacao.
- `src/level_data.py`: dados das 16 fases e geracao simples de layout.
- `src/levels.py`: conversao dos dados das fases em objetos usados pelo Pygame.
- `src/backgrounds.py`: desenho dos cenarios por tema.
- `src/progress.py`: salvamento local em JSON, tolerante a falhas.
- `src/sounds.py`: sons simples gerados por codigo, com fallback silencioso.
- `src/settings.py`: constantes gerais.
- `scripts/smoke_tests.py`: validacao automatica leve.
- `scripts/build_pygbag_clean.py`: build web limpo sem empacotar venv ou save local.
- `README.md`: como executar, jogar, testar e publicar.
- `SPEC.MD`: especificacao tecnica para continuidade.
- `AGENTS.md`: regras para agentes de IA.
- `PROMPT_YOLO.MD`: prompt para futuras rodadas autonomas.

---

## Regras De Salvamento

Preserve:

- save local em `caminhos_brasil_save.json`;
- fallback quando leitura/escrita falhar;
- `N` inicia nova jornada temporaria sem apagar nem sobrescrever o progresso salvo;
- progresso salvo com fases liberadas, fases concluidas e colecao.

Para web:

- avaliar se `src/progress.py` precisa adaptacao;
- se nao for possivel implementar armazenamento web agora, documentar claramente;
- nao deixe falha de save impedir gameplay.

---

## Preparacao Para Publicacao Online

O projeto deve continuar pronto para Pygbag:

- `main.py` deve manter loop `async`;
- assets devem usar caminhos relativos;
- dependencias devem permanecer minimas;
- audio deve falhar de forma segura;
- save nao pode impedir gameplay.

Nao use `pygbag .` como unica validacao se `.venv_brasil` ou `caminhos_brasil_save.json` estiverem na raiz. Use:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\build_pygbag_clean.py
```

Saida esperada:

```text
build/pygbag_app/build/web
```

Se possivel, abra o `index.html` gerado em navegador real e teste:

- abertura;
- sprite do Mig;
- audio;
- primeira fase;
- colecao;
- linha do tempo;
- save/fallback;
- tela final.

Se nao for possivel testar navegador real, documente a pendencia.

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

O smoke test deve conferir:

- existem 16 fases;
- cada fase tem fragmentos;
- cada fase tem checkpoint;
- cada fase tem area de cuidado;
- checkpoints nao colidem com areas de cuidado;
- respawns nao caem em areas de cuidado;
- fragmentos ficam em plataformas alcancaveis por criterio conservador;
- `Game` inicializa em modo dummy;
- menu carrega `abertura.png`;
- sprite do Mig carrega;
- fluxo basico de menu, nova sessao, colecao, checkpoint, area de cuidado, conclusao e final passa sem alterar save;
- mensagem historica fica em posicao estavel e usa translucidez quando Mig passa por tras.

Se alterar UI, renderize/abra o jogo e confira visualmente.

---

## Testes Manuais Recomendados

Teste manual minimo:

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
19. Testar fase 2 com todos os fragmentos.
20. Testar uma fase intermediaria.
21. Testar fase 16.
22. Ver tela final.
23. Fechar e abrir novamente para conferir save.

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

- abrir sem erro com `python main.py` ou com a venv local;
- manter a tela inicial com `abertura.png`;
- permitir continuar jornada salva com `Enter`;
- permitir nova jornada temporaria com `N`;
- permitir jogar do menu ate a tela final;
- manter 16 fases historicas;
- manter progressao cronologica;
- manter linha do tempo funcional;
- manter colecao historica funcional;
- manter pausa funcional;
- manter ajuda rapida com `H`;
- manter controles documentados;
- manter linguagem adequada para criancas;
- nao quebrar animacao do Mig;
- nao quebrar coleta;
- nao quebrar checkpoints;
- nao quebrar camera;
- nao deixar respawn em area de cuidado;
- nao deixar fragmentos inalcancaveis;
- manter mensagens historicas fixas e translucidas quando Mig passar por tras;
- passar em `python -m compileall main.py src`;
- passar no smoke test na venv local;
- ter README, SPEC e AGENTS atualizados se houver mudancas;
- ter build Pygbag limpo testado ou pendencia documentada;
- estar pronto para primeiro teste com usuario final.

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

Se algo nao foi testado, diga claramente.

Nao entregue apenas proposta. Implemente, valide e documente.
