# ♟️ Jogo de Damas em Python (Pygame)

Uma implementação completa e orientada a objetos do clássico **Jogo de Damas**, desenvolvida em Python com a biblioteca **Pygame**. O projeto segue as regras oficiais de movimentação, promoção de damas e capturas obrigatórias.

---

## 📋 Funcionalidades

- **Mecânica Completa de Damas:**
  - Movimentação diagonal simples para peças comuns.
  - **Captura Obrigatória:** O jogo detecta e força o jogador a realizar a captura quando disponível.
  - **Captura Múltipla / Em Cadeia:** Mantém o turno com a mesma peça caso haja sequências de capturas.
  - **Promoção a Dama:** Peças que atingem a última fileira oposta tornam-se Damas (identificadas pelo símbolo `D`).
  - **Movimentação da Dama:** Capacidade de andar e capturar tanto para frente quanto para trás.
- **Interface Gráfica Limpa:**
  - Destaque visual da peça selecionada (borda amarela).
  - Indicação clara das casas para onde a peça pode se mover (pontos verdes).
- **Detecção de Fim de Jogo:** Notificação automática do vencedor via console ao eliminar todas as peças adversárias.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.8+
- **Biblioteca Gráfica:** [Pygame](https://www.pygame.org/)

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter o **Python** e o **pip** instalados em sua máquina.

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/jogo-de-damas-python.git](https://github.com/seu-usuario/jogo-de-damas-python.git)
   cd jogo-de-damas-python