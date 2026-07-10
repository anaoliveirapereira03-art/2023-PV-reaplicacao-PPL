from PIL import Image
import os

def encontrar_faixa_preta(imagem, cor_alvo=(0, 0, 0), tolerancia=15, altura_faixa=4, largura_faixa=50):
    """
    Encontra posições onde há uma faixa horizontal da cor especificada com largura definida no meio da imagem
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    
    # Define o ponto de início X no meio da imagem para analisar a largura estipulada
    x_inicio = (largura // 2) - (largura_faixa // 2)
    
    # Percorre a imagem de cima para baixo
    y = 0
    while y < altura - altura_faixa:
        faixa_encontrada = True
        
        # Verifica todos os pixels dentro do bloco (altura_faixa x largura_faixa) no centro
        for dy in range(altura_faixa):
            for dx in range(largura_faixa):
                pixel = pixels[x_inicio + dx, y + dy]
                
                if len(pixel) == 4:  # RGBA
                    r, g, b, a = pixel
                else:  # RGB
                    r, g, b = pixel[:3]
                
                # Verifica se a cor está dentro da tolerância
                if (abs(r - cor_alvo[0]) > tolerancia or 
                    abs(g - cor_alvo[1]) > tolerancia or 
                    abs(b - cor_alvo[2]) > tolerancia):
                    faixa_encontrada = False
                    break
            if not faixa_encontrada:
                break
        
        if faixa_encontrada:
            # Corta 38 pixels ANTES de começar o padrão
            posicao_corte = y - 45
            if posicao_corte < 0:  # Evitar posições negativas
                posicao_corte = 0
                
            posicoes_corte.append(posicao_corte)
            print(f"Padrão encontrado começando em y={y}, cortando em y={posicao_corte}")
            # Pula a faixa inteira para evitar detecções múltiplas
            y += altura_faixa
        else:
            y += 1
    
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_alvo):
    """
    Divide a imagem verticalmente cortando ANTES das faixas
    """
    # Abre a imagem
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    # Encontra as posições com o novo padrão de faixa preta de 4px de altura
    posicoes_corte = encontrar_faixa_preta(imagem, cor_alvo)
    
    if not posicoes_corte:
        print("Nenhum padrão encontrado na imagem!")
        return
    
    print(f"Encontradas {len(posicoes_corte)} faixas para corte")
    
    # Cria a pasta de saída se não existir
    os.makedirs(pasta_saida, exist_ok=True)
    
    # Corta as seções da imagem
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        # Garantir que a posição de corte é válida
        if posicao_corte <= posicao_anterior:
            continue
            
        # Corta a seção ANTES da faixa (do início anterior até o início do corte calculado)
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        # Salva a imagem cortada
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        # A próxima seção começa após o final desta faixa (altura_faixa = 4)
        posicao_anterior = posicao_corte + 4
    
    # Corta a seção final (após a última faixa)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    # OBS5: Alterne as linhas abaixo conforme instruído para o seu fluxo (concatenadas vs inteiras)
    caminho_imagem = "./inteiras/pagina_enem_27.png"  
    pasta_saida = "27" 

    # caminho_imagem = "./inteiras/pagina_enem_15.png"  
    # pasta_saida = "pagina_15" 
    
    # Define a cor alvo diretamente como RGB (0, 0, 0)
    cor_do_padrao = (0, 0, 0)
    print(f"Cor alvo definida: RGB {cor_do_padrao}")
    
    # Executa a divisão
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_do_padrao)
    
    print("Divisão concluída!")