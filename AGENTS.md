# AGENTS.md

Instrucoes para agentes de IA que forem trabalhar no projeto Caminhos do Brasil.

## Objetivo Do Projeto

Criar e manter um jogo de plataforma 2D educativo sobre a historia do Brasil, desde 1500 ate os dias atuais.

O jogo acompanha Mig, um menino ficticio nascido em 2018, que viaja por diferentes periodos historicos do Brasil. O objetivo e ensinar historia de forma leve, respeitosa e divertida para criancas.

## Perfil Do Projeto

- Genero: plataforma 2D.
- Linguagem: Python.
- Biblioteca principal: Pygame-CE.
- Publicacao futura desejada: navegador, usando Pygbag.
- Publico: criancas, com referencia principal em torno de 8 anos.
- Tom: educativo, acolhedor, simples e respeitoso.

## Diretrizes Gerais Para Agentes

- Leia `README.md`, `SPEC.MD`, `AGENTS.md`, `requirements.txt`, `main.py` e os arquivos de `src/` antes de alterar codigo.
- Trabalhe de forma incremental.
- Priorize sempre uma versao funcional antes de adicionar complexidade.
- Mantenha codigo organizado, claro e modular.
- Prefira pequenas melhorias coerentes em vez de grandes refatoracoes.
- Nao remova funcionalidades existentes sem motivo claro.
- Nao troque Python, Pygame-CE ou Pygbag sem confirmacao do usuario.
- Explique decisoes tecnicas de forma clara e curta.
- Ao finalizar, diga o que mudou, como testar e quais validacoes foram feitas.

## Diretriz De Linguagem Historica

Como o jogo e voltado para criancas:

- Use linguagem simples.
- Evite descricoes fortes, violentas ou graficas.
- Trate temas sensiveis com cuidado e respeito.
- Nao glorifique personagens ou processos historicos controversos.
- Valorize aprendizado historico, memoria, diversidade e cidadania.
- Ao mencionar povos indigenas, pessoas escravizadas ou grupos afetados por processos historicos, use linguagem respeitosa e cuidadosa.
- Prefira frases curtas nos fragmentos e notas de fase.

Exemplo de tom adequado:

```text
Esse periodo trouxe mudancas importantes e tambem desafios para muitas pessoas. E um tema que deve ser estudado com cuidado e respeito.
```

## Tecnologias E Dependencias

- Python.
- Pygame-CE.
- Pygbag.
- Evitar dependencias novas sem necessidade clara.
- Assets devem ser leves.
- Novos assets devem ficar preferencialmente em `assets/images/` ou `assets/audio/`.

## Compatibilidade Com Web

Pensar desde o inicio em Pygbag:

- Manter `main.py` com loop `async`.
- Evitar operacoes bloqueantes longas no loop principal.
- Evitar dependencias que nao funcionem bem no navegador.
- Preferir dados simples em Python, JSON ou formatos leves.
- Evitar caminhos absolutos para assets.
- Usar arquivos pequenos e formatos comuns.
- Testar Pygbag antes de considerar a versao pronta para publicacao; se houver venv ou save na raiz, usar `scripts/build_pygbag_clean.py`.

## Estado Atual Do Projeto

O jogo ja possui:

- Tela inicial com `abertura.png`.
- Menu com continuar, nova sessao, linha do tempo e colecao.
- Linha do tempo com fases bloqueadas, liberadas e concluidas.
- Progresso salvo localmente em JSON quando possivel.
- Nova jornada temporaria com `N`, sem apagar o save.
- Dezesseis fases historicas em ordem cronologica.
- Movimento lateral, pulo, gravidade e colisao.
- Camera horizontal.
- HUD ajusta discretamente titulos longos para caberem no painel.
- Fragmentos historicos coletaveis.
- Colecao historica agrupada por fase.
- Colecao historica com aparencia de album e progresso por fase.
- Introducao narrativa por fase.
- Ajuda rapida com `H`.
- Tela final com creditos simples.
- Tela de pausa.
- Checkpoints seguros.
- Areas de cuidado.
- Coyote time e buffer curto de pulo.
- Feedback visual para fragmentos, checkpoints, areas de cuidado e portal.
- Mensagens historicas ficam fixas no topo e se tornam translucidas quando Mig passa por tras.
- Sons leves gerados por codigo.
- Sprite animado do Mig usando folha de sprites.
- Cenarios desenhados por codigo.
- Smoke tests permanentes em `scripts/smoke_tests.py`.
- Build Pygbag limpo em `scripts/build_pygbag_clean.py`.

## Arquivos Importantes

- `README.md`: explicacao para executar, jogar e testar.
- `SPEC.MD`: especificacao tecnica e funcional para continuidade do projeto.
- `AGENTS.md`: instrucoes de trabalho para agentes de IA.
- `main.py`: ponto de entrada compativel com Pygbag.
- `requirements.txt`: dependencias do projeto.
- `abertura.png`: imagem principal da tela inicial.
- `assets/images/personagem.png`: folha de sprites do Mig durante o jogo.
- `src/game.py`: loop principal, estados, telas, HUD, fluxo e progresso.
- `src/player.py`: movimento, colisao, animacao e desenho do Mig.
- `src/level_data.py`: dados das fases historicas e geracao simples de layout.
- `src/levels.py`: conversao dos dados das fases em objetos usados pelo Pygame.
- `src/backgrounds.py`: desenho dos cenarios por tema.
- `src/progress.py`: salvamento local simples de progresso e colecao em JSON.
- `src/sounds.py`: sons simples gerados por codigo.
- `src/settings.py`: constantes gerais.
- `scripts/smoke_tests.py`: validacao automatica leve de fases, assets e fluxo basico.
- `scripts/build_pygbag_clean.py`: gera build web a partir de copia minima, sem empacotar venv ou save local.

## Fluxo Recomendado De Trabalho

1. Ler a documentacao e os arquivos relevantes.
2. Entender a mudanca pedida.
3. Fazer a menor alteracao coerente com o objetivo.
4. Validar com:

```powershell
python -m compileall main.py src
```

5. Rodar smoke test quando a mudanca tocar fases, fisica, player, save, assets ou fluxo:

```powershell
python scripts\smoke_tests.py
```

Se o Python global nao tiver `pygame-ce`, use a venv local.

6. Se existir ambiente virtual, repetir com:

```powershell
.\.venv_brasil\Scripts\python.exe scripts\smoke_tests.py
```

7. Se a mudanca tocar jogabilidade, testar manualmente a fase afetada.
8. Se a mudanca tocar menu, imagens ou telas, renderizar/abrir o jogo e conferir visualmente.
9. Atualizar `README.md`, `SPEC.MD` ou `AGENTS.md` quando a mudanca afetar comportamento, arquitetura ou processo.

## Pontos De Atencao Recentes

- Checkpoints nao devem ficar sobre areas de cuidado.
- O respawn de checkpoints tambem nao pode cair em areas de cuidado.
- Fragmentos devem ficar apoiados em plataformas alcancaveis pelo pulo atual do Mig.
- A fase 2 ja teve problemas de checkpoint e fragmentos inalcancaveis; revisar com cuidado se alterar layout.
- A tela inicial usa `abertura.png`; se esse arquivo faltar, `src/game.py` tem fallback desenhado por Pygame.
- A nova sessao com `N` nao deve sobrescrever o save salvo.
- O controle `H` abre a ajuda rapida e deve continuar simples e legivel.
- Nao reposicionar dinamicamente a mensagem historica durante o pulo; isso distrai o jogador. Preserve painel fixo com translucidez.
- `pygbag .` na raiz pode empacotar `.venv_brasil` e `caminhos_brasil_save.json`; para build web, prefira `scripts/build_pygbag_clean.py`.

## Testes Recomendados

Validacao tecnica:

```powershell
python -m compileall main.py src
python scripts\smoke_tests.py
```

Teste manual minimo:

- Abrir o jogo.
- Confirmar imagem de abertura.
- Pressionar `Enter` e iniciar fase.
- Pressionar `N` no menu e confirmar nova jornada temporaria.
- Pressionar `H` no menu ou na fase e confirmar ajuda rapida.
- Mover e pular.
- Coletar fragmentos.
- Conferir se a mensagem historica nao atrapalha o pulo; ela deve ficar fixa e translucida se Mig passar por tras.
- Abrir colecao com `C`.
- Ativar checkpoint.
- Tocar em area de cuidado e confirmar retorno seguro.
- Reiniciar fase com `R`.
- Pausar com `P`.
- Concluir fase.
- Confirmar desbloqueio da fase seguinte.
- Abrir linha do tempo com `S`.
- Testar fase 2.
- Testar uma fase intermediaria.
- Testar a ultima fase e tela final.

## Proximas Evolucoes Provaveis

- Ajustar sensacao de movimento e pulo.
- Melhorar feedback visual para coleta, checkpoint e objetivo final.
- Melhorar visual de plataformas, fragmentos, checkpoints e portal final.
- Polir colecao historica como album.
- Testar build Pygbag limpo em navegador real.
- Adaptar `src/progress.py` para armazenamento web, se necessario.
- Separar telas de `src/game.py` se o arquivo crescer muito.

## Restricoes

- Nao criar sistemas avancados prematuramente.
- Nao adicionar dependencias sem necessidade.
- Nao substituir Pygame-CE por outra engine sem pedido explicito.
- Nao tornar o jogo pesado para web.
- Nao usar linguagem historica inadequada para criancas.
- Nao quebrar `main.py` com loop `async`.
- Sempre validar a etapa atual antes de entregar.
- Manter `src/progress.py` tolerante a falhas de leitura e escrita.
- Manter `scripts/smoke_tests.py` atualizado quando novas regras de fase ou fluxo forem adicionadas.
