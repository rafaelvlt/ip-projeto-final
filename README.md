# ip-projeto-final

> 

**Disciplina:** Introdução à Programação - CIn/UFPE  
**Período:** [2025.1]

---

## Equipe

| Nome Completo     | GitHub                               |
| :---------------- | :----------------------------------- | 
| `Rafael Barbosa`  | [@rafaelvlt](https://github.com/rafaelvlt) |
| `Eric Santiago`  | [@ARISE21](https://github.com/ARISE21)   |
| `Caio Amarante`  | [@IrineuACgasoso](https://github.com/IrineuACgasoso) |
| `Pedro Albuquerque`  | [@PHMA-PEDRO](https://github.com/PHMA-PEDRO) |
| `Kraus Junior`  | [@thatkraus](https://github.com/thatkraus) | 
| `Álvaro Lima`  | [@Alvarolima22](https://github.com/Alvarolima22) |

---

## Sobre o Jogo

Este projeto é um jogo de ação e sobrevivência 2D, onde o objetivo principal é resistir a hordas crescentes de inimigos pelo maior tempo possível. A jogabilidade é minimalista, com controles limitados à movimentação do personagem, exigindo do jogador reflexos rápidos e posicionamento estratégico para desviar das ameaças.

Os ataques são automáticos, e o jogador se fortalece ao coletar recursos deixados pelos adversários derrotados, que permitem aprimorar seu arsenal e aumentar as chances de sobrevivência. O jogo foi desenvolvido em Python com a biblioteca Pygame como projeto final da disciplina de Introdução à Programação (CIn/UFPE).

---

## Galeria

![Imagens do Game]()

---

## Como Executar

Siga os passos abaixo para rodar o projeto em seu ambiente local.

## Arquitetura do Projeto

O código foi estruturado de forma modular e orientada a objetos para garantir a organização, a manutenibilidade e a colaboração eficiente da equipe, conforme a estrutura de arquivos apresentada no início deste documento. A responsabilidade de cada componente principal é:
* **`main.py`**: Ponto de entrada que inicializa os módulos do Pygame e cria a instância principal da classe `Game`.
* **`src/game.py`**: Contém a classe `Game`, que gerencia o loop principal, os estados do jogo (menu, jogando, game over), a renderização dos elementos e a lógica de eventos.
* **`src/player.py`, `src/enemy.py`, etc.**: Cada arquivo define uma entidade ou sistema específico do jogo, seguindo o princípio de responsabilidade única.
* **`src/settings.py`**: Centraliza todas as constantes e configurações globais (tamanho da tela, cores, FPS, etc.) para facilitar ajustes.

---

## Conceitos da Disciplina Aplicados

Esta seção detalha como os principais conceitos de Introdução à Programação foram implementados no projeto.


---

## Desafios e Lições Aprendidas

---

## Ferramentas Utilizadas

* **Linguagem:** `Python 3`
    * **Justificativa:** Linguagem obrigatória da disciplina, escolhida por sua sintaxe clara e ecossistema robusto, o que agiliza o desenvolvimento de protótipos e projetos complexos.
* **Biblioteca:** `Pygame`
    * **Justificativa:** Framework consolidado para o desenvolvimento de jogos 2D em Python. Foi escolhido por nos dar controle total sobre o loop principal, eventos e renderização, sendo ideal para a mecânica de ação em tempo real do nosso jogo.
* **Versionamento:** `Git` & `GitHub`
    * **Justificativa:** Ferramentas essenciais para o trabalho colaborativo em software. O GitHub foi usado como nosso repositório central, enquanto o Git nos permitiu gerenciar diferentes versões do código e trabalhar em funcionalidades paralelas com *branches*.

