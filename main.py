import sys
import pygame

# ==========================================
# CONSTANTES E CONFIGURAÇÕES DE INTERFACE
# ==========================================
LARGURA, ALTURA = 600, 600
LINHAS, COLUNAS = 8, 8
TAMANHO_CASA = LARGURA // COLUNAS

# Cores (RGB)
COR_CLARA = (240, 217, 181)
COR_ESCURA = (181, 136, 99)
COR_VERMELHA = (205, 38, 38)
COR_BRANCA = (245, 245, 245)
COR_DESTAQUE = (50, 205, 50)
COR_SELECAO = (255, 215, 0)
COR_TEXTO = (30, 30, 30)

# ==========================================
# CLASSE PEC
# ==========================================
class Peca:
    def __init__(self, linha, coluna, cor):
        self.linha = linha
        self.coluna = coluna
        self.cor = cor
        self.e_dama = False

    def promover_a_dama(self):
        self.e_dama = True

    def desenhar(self, tela):
        raio = TAMANHO_CASA // 2 - 10
        centro_x = self.coluna * TAMANHO_CASA + TAMANHO_CASA // 2
        centro_y = self.linha * TAMANHO_CASA + TAMANHO_CASA // 2

        # Sombra
        pygame.draw.circle(tela, (50, 50, 50), (centro_x + 2, centro_y + 2), raio)
        # Peça
        pygame.draw.circle(tela, self.cor, (centro_x, centro_y), raio)
        # Borda interna para destaque
        pygame.draw.circle(tela, (100, 100, 100), (centro_x, centro_y), raio, 2)

        # Símbolo de Dama
        if self.e_dama:
            fonte = pygame.font.SysFont("Arial", 22, bold=True)
            cor_coroa = (255, 215, 0) if self.cor == COR_VERMELHA else (50, 50, 50)
            texto = fonte.render("D", True, cor_coroa)
            rect = texto.get_rect(center=(centro_x, centro_y))
            tela.blit(texto, rect)

    def mover(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna


# ==========================================
# CLASSE TABULEIRO
# ==========================================
class Tabuleiro:
    def __init__(self):
        self.grade = []
        self.pecas_vermelhas = 12
        self.pecas_brancas = 12
        self._inicializar_tabuleiro()

    def _inicializar_tabuleiro(self):
        for linha in range(LINHAS):
            self.grade.append([])
            for coluna in range(COLUNAS):
                if (linha + coluna) % 2 != 0:
                    if linha < 3:
                        self.grade[linha].append(Peca(linha, coluna, COR_VERMELHA))
                    elif linha > 4:
                        self.grade[linha].append(Peca(linha, coluna, COR_BRANCA))
                    else:
                        self.grade[linha].append(None)
                else:
                    self.grade[linha].append(None)

    def desenhar(self, tela):
        # Desenha as casas do tabuleiro
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                cor = COR_CLARA if (linha + coluna) % 2 == 0 else COR_ESCURA
                pygame.draw.rect(
                    tela,
                    cor,
                    (coluna * TAMANHO_CASA, linha * TAMANHO_CASA, TAMANHO_CASA, TAMANHO_CASA)
                )

        # Desenha as peças
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                peca = self.grade[linha][coluna]
                if peca is not None:
                    peca.desenhar(tela)

    def mover_peca(self, peca, linha, coluna):
        # Atualiza a posição na matriz
        self.grade[peca.linha][peca.coluna] = None
        self.grade[linha][coluna] = peca
        peca.mover(linha, coluna)

        # Checa promoção a Dama
        if linha == 0 and peca.cor == COR_BRANCA:
            peca.promover_a_dama()
        elif linha == LINHAS - 1 and peca.cor == COR_VERMELHA:
            peca.promover_a_dama()

    def remover_peca(self, peca):
        if peca is not None:
            self.grade[peca.linha][peca.coluna] = None
            if peca.cor == COR_VERMELHA:
                self.pecas_vermelhas -= 1
            else:
                self.pecas_brancas -= 1

    def obter_peca(self, linha, coluna):
        return self.grade[linha][coluna]


# ==========================================
# CLASSE DE GERENCIAMENTO DO JOGO
# ==========================================
class JogoDamas:
    def __init__(self, tela):
        self.tela = tela
        self.tabuleiro = Tabuleiro()
        self.turno = COR_BRANCA  # Brancas começam
        self.peca_selecionada = None
        self.movimentos_validos = {}  # {(linha, col): [pecas_capturadas]}
        self.deve_continuar_capturando = False

    def atualizar(self):
        self.tabuleiro.desenhar(self.tela)
        self._desenhar_destaques()
        pygame.display.update()

    def _desenhar_destaques(self):
        # Destaca a peça selecionada
        if self.peca_selecionada:
            centro_x = self.peca_selecionada.coluna * TAMANHO_CASA + TAMANHO_CASA // 2
            centro_y = self.peca_selecionada.linha * TAMANHO_CASA + TAMANHO_CASA // 2
            pygame.draw.circle(self.tela, COR_SELECAO, (centro_x, centro_y), TAMANHO_CASA // 2 - 5, 3)

        # Destaca os movimentos possíveis
        for pos in self.movimentos_validos:
            linha, coluna = pos
            centro_x = coluna * TAMANHO_CASA + TAMANHO_CASA // 2
            centro_y = linha * TAMANHO_CASA + TAMANHO_CASA // 2
            pygame.draw.circle(self.tela, COR_DESTAQUE, (centro_x, centro_y), 12)

    def selecionar(self, linha, coluna):
        if self.deve_continuar_capturando:
            # Em captura múltipla, só pode interagir com a mesma peça
            if self.peca_selecionada and (linha, coluna) in self.movimentos_validos:
                self._executar_movimento(linha, coluna)
            return

        peca = self.tabuleiro.obter_peca(linha, coluna)

        # Se já tiver uma peça selecionada e clicar numa casa de destino válida
        if self.peca_selecionada and (linha, coluna) in self.movimentos_validos:
            self._executar_movimento(linha, coluna)
            return

        # Seleção de uma nova peça
        if peca is not None and peca.cor == self.turno:
            # Regra de captura obrigatória no turno
            todas_capturas = self._obter_todas_capturas_obrigatorias(self.turno)
            if todas_capturas:
                if peca in todas_capturas:
                    self.peca_selecionada = peca
                    self.movimentos_validos = todas_capturas[peca]
                else:
                    self.peca_selecionada = None
                    self.movimentos_validos = {}
            else:
                self.peca_selecionada = peca
                self.movimentos_validos = self._obter_movimentos_validos(peca)

    def _executar_movimento(self, linha, coluna):
        capturadas = self.movimentos_validos[(linha, coluna)]
        self.tabuleiro.mover_peca(self.peca_selecionada, linha, coluna)

        if capturadas:
            for peca in capturadas:
                self.tabuleiro.remover_peca(peca)

            # Checa se há mais capturas em cadeia para esta peça
            novas_capturas = self._obter_capturas_peca(self.peca_selecionada)
            if novas_capturas:
                self.deve_continuar_capturando = True
                self.movimentos_validos = novas_capturas
                return

        # Fim de turno
        self.deve_continuar_capturando = False
        self._mudar_turno()

    def _mudar_turno(self):
        self.peca_selecionada = None
        self.movimentos_validos = {}
        self.turno = COR_VERMELHA if self.turno == COR_BRANCA else COR_BRANCA

    def _obter_todas_capturas_obrigatorias(self, cor):
        capturas_dict = {}
        for r in range(LINHAS):
            for c in range(COLUNAS):
                peca = self.tabuleiro.obter_peca(r, c)
                if peca and peca.cor == cor:
                    capturas = self._obter_capturas_peca(peca)
                    if capturas:
                        capturas_dict[peca] = capturas
        return capturas_dict

    def _obter_movimentos_validos(self, peca):
        movimentos = {}
        capturas = self._obter_capturas_peca(peca)

        if capturas:
            return capturas

        # Direções de movimento simples
        direcoes = []
        if peca.cor == COR_BRANCA or peca.e_dama:
            direcoes.extend([(-1, -1), (-1, 1)])  # Para cima
        if peca.cor == COR_VERMELHA or peca.e_dama:
            direcoes.extend([(1, -1), (1, 1)])    # Para baixo

        for dr, dc in direcoes:
            nr, nc = peca.linha + dr, peca.coluna + dc
            if 0 <= nr < LINHAS and 0 <= nc < COLUNAS:
                if self.tabuleiro.obter_peca(nr, nc) is None:
                    movimentos[(nr, nc)] = []

        return movimentos

    def _obter_capturas_peca(self, peca):
        capturas = {}
        direcoes = []

        if peca.cor == COR_BRANCA or peca.e_dama:
            direcoes.extend([(-1, -1), (-1, 1)])
        if peca.cor == COR_VERMELHA or peca.e_dama:
            direcoes.extend([(1, -1), (1, 1)])

        for dr, dc in direcoes:
            r_meio, c_meio = peca.linha + dr, peca.coluna + dc
            r_dest, c_dest = peca.linha + (dr * 2), peca.coluna + (dc * 2)

            if 0 <= r_dest < LINHAS and 0 <= c_dest < COLUNAS:
                peca_meio = self.tabuleiro.obter_peca(r_meio, c_meio)
                peca_dest = self.tabuleiro.obter_peca(r_dest, c_dest)

                if peca_meio and peca_meio.cor != peca.cor and peca_dest is None:
                    capturas[(r_dest, c_dest)] = [peca_meio]

        return capturas

    def verificar_vencedor(self):
        if self.tabuleiro.pecas_vermelhas <= 0:
            return "BRANCAS"
        elif self.tabuleiro.pecas_brancas <= 0:
            return "VERMELHAS"
        return None


# ==========================================
# LOOP PRINCIPAL
# ==========================================
def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Jogo de Damas - Engenharia de Software")

    relogio = pygame.time.Clock()
    jogo = JogoDamas(tela)

    rodando = True
    while rodando:
        relogio.tick(60)

        vencedor = jogo.verificar_vencedor()
        if vencedor:
            print(f"Fim de jogo! Vencedor: {vencedor}")

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                coluna = pos[0] // TAMANHO_CASA
                linha = pos[1] // TAMANHO_CASA
                jogo.selecionar(linha, coluna)

        jogo.atualizar()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()