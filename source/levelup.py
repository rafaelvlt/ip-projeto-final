import pygame

from settings import *
from weapon import Arma

class TelaDeUpgrade:
    def __init__(self, tela, jogador):
        self.fonte_grande = pygame.font.Font(None, 20)
        self.fonte_pequena = pygame.font.Font(None, 15)


        #lógica para gerar 3 opções de upgrade
        # TODO: Implementar uma lógica real para escolher 3 upgrades aleatórios e únicos.
        arma_existente = list(jogador.armas.values())[0]
        arma_existente_dois = list(jogador.armas.values())[1]
        self.opcoes_de_armas = [arma_existente, arma_existente_dois, arma_existente] 
        
        #cálculo do layout
        largura_painel, altura_painel = 800, 350
        self.painel_rect = pygame.Rect((largura_tela - largura_painel) // 2, (altura_tela - altura_painel) // 2, largura_painel, altura_painel)
        
        self.opcoes = []
        padding = 20
        largura_opcao = (self.painel_rect.width - padding * 4) // 3
        altura_opcao = self.painel_rect.height - padding * 3 - 50 # Espaço para título

        for i, arma in enumerate(self.opcoes_de_armas):
            posicao_x = self.painel_rect.x + padding + i * (largura_opcao + padding)
            posicao_y = self.painel_rect.y + padding + 50
            retangulo_opcao = pygame.Rect(posicao_x, posicao_y, largura_opcao, altura_opcao)
            self.opcoes.append(OpcaoDeUpgrade(arma, retangulo_opcao))

        self.opcao_selecionada = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.opcao_selecionada = (self.opcao_selecionada + 1) % len(self.opcoes)
            elif event.key == pygame.K_a:
                self.opcao_selecionada = (self.opcao_selecionada - 1) % len(self.opcoes)
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                return self.opcao_selecionada #retorna o índice da escolha
        
        return None

    def draw(self, surface):
        #escurece o fundo
        overlay = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        #desenha o painel principal
        pygame.draw.rect(surface, (30, 30, 40), self.painel_rect, border_radius=10)
        pygame.draw.rect(surface, (90, 90, 100), self.painel_rect, 3, border_radius=10)
        desenhar_texto(surface, "LEVEL UP!", (self.painel_rect.x + 20, self.painel_rect.y + 15), self.fonte_grande)

        #,anda cada card de opção se desenhar
        for i, opcao in enumerate(self.opcoes):
            esta_selecionada = (i == self.opcao_selecionada)
            opcao.draw(surface, esta_selecionada)

class OpcaoDeUpgrade:
    def __init__(self, arma_prototipo, retangulo):
        self.arma = arma_prototipo
        self.rect = retangulo
        self.fonte_grande = pygame.font.Font(None, 24)
        self.fonte_pequena = pygame.font.Font(None, 20)


    def draw(self, surface, esta_selecionada):
        #desenha o fundo do card
        pygame.draw.rect(surface, (45, 45, 60), self.rect, border_radius=8)

        #desenha a borda de destaque
        cor_borda = (220, 200, 60) if esta_selecionada else (120, 120, 130)
        pygame.draw.rect(surface, cor_borda, self.rect, 3, border_radius=8)

        #exibe o nome e o nível da arma
        nome_arma = self.arma.nome if hasattr(self.arma, 'nome') else "Arma Desconhecida"
        nivel_arma = self.arma.nivel
        desenhar_texto(surface, f"{nome_arma} - Nv. {nivel_arma}", (self.rect.x + 10, self.rect.y + 10), self.fonte_grande)

        #exibe uma descrição
        descricao = self.arma.descricao if hasattr(self.arma, 'descricao') else "Melhora esta arma."
        desenhar_texto(surface, descricao, (self.rect.x + 10, self.rect.y + 40), self.fonte_pequena)

        #pega estatisticas da arma agora e futura
        lista_stas = self.arma.get_estatisticas_para_exibir()

        posicao_y_stats = self.rect.y + 80
        
        for texto_stat in lista_stas:
            desenhar_texto(surface, texto_stat, (self.rect.x + 10, posicao_y_stats), self.fonte_pequena)
            posicao_y_stats += 25 


def desenhar_texto(surface, texto, pos, fonte, cor='white'):
    """Função auxiliar para desenhar texto na tela."""
    text_surface = fonte.render(str(texto), True, cor)
    surface.blit(text_surface, pos)
