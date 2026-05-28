# Caminhos do Brasil

Jogo de plataforma 2D educativo sobre a historia do Brasil, feito em Python com Pygame-CE e pensado para futura publicacao web com Pygbag.

## Etapa atual

MVP jogavel:

- Janela 2D simples.
- Personagem Mig controlavel.
- Movimento lateral.
- Pulo.
- Gravidade.
- Colisao com plataformas.
- Objetivo de fase.
- Mensagem historica ao concluir a fase.
- Reinicio da fase com R.
- Avanco entre fases com Enter.
- Duas fases iniciais organizadas em ordem historica.
- Camera horizontal acompanhando Mig em fases maiores que a tela.
- Tela inicial simples.
- Introducao narrativa antes de cada fase.
- Estados de jogo: menu, introducao, jogando e fase concluida.

## Como executar no computador

```powershell
python -m venv .venv_brasil
.\.venv_brasil\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Controles

- Setas esquerda/direita ou A/D: mover.
- Espaco, seta para cima ou W: pular.
- R: reiniciar a fase.
- Enter: avancar no menu, iniciar a fase depois da introducao ou seguir para a proxima fase depois de concluir.
- Esc: sair.

## Como testar esta etapa

Verifique:

- O jogo abre na tela inicial.
- Enter mostra a introducao da primeira fase.
- Enter novamente inicia a fase.
- Mig aparece no lado esquerdo da tela.
- O personagem anda para os lados.
- O pulo funciona apenas quando ele esta no chao ou sobre uma plataforma.
- Ele nao atravessa o chao nem as plataformas.
- Ao avancar para a direita, a camera acompanha Mig.
- Mig continua impedido de sair pelos limites esquerdo e direito da fase.
- Ao tocar no marcador verde no fim da fase, aparece a mensagem de conclusao.
- Depois de concluir, a tecla R reinicia a fase.
- Depois de concluir, a tecla Enter carrega a introducao da proxima fase.

## Publicacao web futura

A entrada principal ja usa um loop `async`, que facilita a compatibilidade com Pygbag. Nesta etapa ainda estamos validando o jogo localmente. Quando a base estiver estavel, o caminho esperado sera:

```powershell
pygbag .
```

Depois disso, o Pygbag gera uma versao web que pode ser hospedada gratuitamente em servicos como GitHub Pages ou Itch.io.
