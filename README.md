# Caminhos do Brasil

Jogo de plataforma 2D educativo sobre a historia do Brasil, feito em Python com Pygame-CE e pensado para futura publicacao web com Pygbag.

O jogador controla Mig, um menino ficticio nascido em 2018, que viaja por diferentes periodos historicos do Brasil. A proposta e ensinar historia de forma leve, visual, respeitosa e adequada para criancas.

## Estado Atual

O projeto ja possui uma versao jogavel com jornada cronologica completa, do ano de 1500 ao Brasil contemporaneo.

Principais recursos:

- Tela inicial com imagem `abertura.png`.
- Menu com continuar jornada, nova sessao, linha do tempo e colecao.
- Linha do tempo com fases bloqueadas, liberadas e concluidas.
- Dezesseis fases historicas jogaveis.
- Progresso salvo localmente quando possivel.
- Opcao de nova jornada temporaria com `N`, sem apagar o save.
- Movimento lateral, pulo, gravidade e colisao.
- Camera horizontal.
- Fragmentos historicos coletaveis.
- Colecao historica agrupada por fase.
- Introducao narrativa por fase.
- Nota historica ao concluir fase.
- Objetivo final liberado apenas apos coletar todos os fragmentos da fase.
- Checkpoints seguros como pontos de retorno.
- Areas de cuidado que retornam Mig ao ultimo checkpoint.
- Tela de pausa.
- Tela final com creditos simples.
- Cenarios por tema desenhados com Pygame.
- Sprite animado do Mig usando `assets/images/personagem.png`.
- Sons leves gerados por codigo.

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
- pelo menos 3 fragmentos;
- pelo menos 1 checkpoint;
- pelo menos 1 area de cuidado;
- objetivo final.

## Como Executar

```powershell
python -m venv .venv_brasil
.\.venv_brasil\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Controles

- Setas esquerda/direita ou A/D: mover.
- Espaco, seta para cima ou W: pular.
- Enter: confirmar, iniciar fase ou avancar.
- N: iniciar nova jornada temporaria sem apagar o progresso salvo.
- S: abrir linha do tempo no menu.
- Setas ou W/S: navegar na linha do tempo e na colecao.
- P: pausar ou continuar durante a fase.
- C: abrir ou fechar a colecao historica.
- R: reiniciar a fase.
- M: voltar ao menu em telas internas.
- Esc: sair.

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
```

Teste manual recomendado:

1. Abrir com `python main.py`.
2. Verificar se `abertura.png` aparece na tela inicial.
3. Pressionar `Enter` e iniciar a fase liberada.
4. Testar `N` no menu e confirmar que a jornada temporaria comeca na fase 1.
5. Mover, pular e cair em plataformas.
6. Coletar fragmentos.
7. Abrir a colecao com `C`.
8. Ativar checkpoint.
9. Tocar em area de cuidado e confirmar retorno seguro.
10. Reiniciar fase com `R`.
11. Pausar e continuar com `P`.
12. Concluir fase.
13. Confirmar desbloqueio da fase seguinte.
14. Entrar pela linha do tempo com `S`.
15. Testar a fase 2, especialmente fragmentos e checkpoints.
16. Testar uma fase intermediaria.
17. Testar a ultima fase.
18. Ver tela final.
19. Fechar e abrir novamente para confirmar save.

## Estrutura De Arquivos

```text
main.py
requirements.txt
README.md
AGENTS.md
SPEC.MD
abertura.png
caminhos_brasil_save.json       # gerado em execucao local
assets/
  images/
    personagem.png
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
- `src/game.py`: controla estados, telas, HUD, progresso, colecao, abertura e loop principal.
- `src/player.py`: controla Mig, movimento, colisao e animacao.
- `src/level_data.py`: contem dados das 16 fases e geradores simples de layout.
- `src/levels.py`: converte dados das fases em objetos `pygame.Rect`.
- `src/backgrounds.py`: desenha cenarios por tema.
- `src/progress.py`: salva e carrega progresso local em JSON.
- `src/sounds.py`: gera sons simples por codigo.
- `src/settings.py`: constantes gerais.

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

Teste esperado:

```powershell
pygbag .
```

Pontos a validar antes de publicar:

- `abertura.png` entra corretamente no build.
- `assets/images/personagem.png` entra corretamente no build.
- O jogo roda no navegador com audio habilitado ou falhando de forma segura.
- `src/progress.py` deve ser avaliado para armazenamento web, pois hoje usa arquivo JSON local.
- Nao usar caminhos absolutos em assets.

## Proximas Melhorias Recomendadas

Prioridade sugerida:

1. Ajustar sensacao de movimento e pulo para ficar mais confortavel.
2. Adicionar feedback visual leve para fragmentos, checkpoint e portal final.
3. Melhorar visual das plataformas e itens por tema.
4. Criar uma tela simples de ajuda com controles.
5. Polir a colecao historica como album.
6. Rodar teste com Pygbag.
7. Adaptar salvamento para web, se necessario.
8. Fazer rodada manual completa em todas as fases.
