import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd


# ===================== Funções =====================

def selecionar_categoria(driver, wait, categoria_nome="Casa de Aposta"):
    """Seleciona a categoria desejada no Reclame Aqui"""
    categoria_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder*='categoria']")))
    categoria_input.click()
    opcao = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(., '{categoria_nome}')]")))
    opcao.click()
    time.sleep(3)

def extrair_metricas(driver, wait):
    """Extrai dados de desempenho da empresa no Reclame Aqui (limpo e formatado)"""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
    time.sleep(2)

    desempenho_div = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.go267425901"))
    )

    spans = desempenho_div.find_elements(By.CSS_SELECTOR, "span.go2549335548")

    respondidas = voltariam = solucao = nota = "--"

    for s in spans:
        texto = s.text.strip()
        if not texto:
            continue

        strongs = s.find_elements(By.TAG_NAME, "strong")
        strong_values = [st.text.strip() for st in strongs if st.text.strip()]

        # % de respostas
        if "Respondeu" in texto:
            match = re.search(r"(\d+(?:[.,]\d+)?%)", texto)
            respondidas = match.group(1) if match else "--"

        # % voltariam a fazer negócio
        elif "voltariam a fazer negócio" in texto:
            match = re.search(r"([\d.,]+%)", texto)
            voltariam = match.group(1) if match else "--"

        # % de índice de solução
        elif "resolveu" in texto:
            match = re.search(r"([\d.,]+%)", texto)
            solucao = match.group(1) if match else "--"

        # nota média
        elif "nota média" in texto:
            if strong_values:
                nota_bruta = strong_values[-1]
                nota = re.sub(r"[^\d.,]", "", nota_bruta)
            else:
                match = re.search(r"([\d.,]+)", texto)
                nota = match.group(1) if match else "--"

    empresa = driver.current_url.rstrip("/").split("/")[-1]

    # Corrige valores vazios que ficaram só com ponto
    def limpar(valor):
        v = valor.strip()
        return "--" if v in [".", "", "--."] else v

    return {
        "empresa": empresa,
        "respondidas": limpar(respondidas),
        "voltariam": limpar(voltariam),
        "solucao": limpar(solucao),
        "nota": limpar(nota)
    }

def coletar_empresas(driver, wait, tipo="melhores"):
    """Coleta as 3 primeiras empresas da aba especificada"""
    resultados = []
    aba = "tab-best" if tipo == "melhores" else "tab-worst"

    print(f"\nColetando Top 3 {tipo.capitalize()}...\n")

    for idx in range(3):
        aba_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-testid='{aba}']")))
        aba_btn.click()
        time.sleep(2)

        cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-testid='listing-ranking']")))
        if idx >= len(cards):
            print(f"Menos de {idx+1} empresas disponíveis na aba {tipo}.")
            break

        card = cards[idx]
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", card)
        time.sleep(1)
        card.click()
        print(f"> Entrando no #{idx+1} ({tipo})…")
        time.sleep(3)

        dados = extrair_metricas(driver, wait)
        dados["tipo"] = tipo
        resultados.append(dados)

        # Volta pra home e reabre categoria
        driver.get("https://www.reclameaqui.com.br/")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='categoria']")))
        time.sleep(2)
        selecionar_categoria(driver, wait, "Casa de Aposta")

    return resultados

# ===================== Execução principal =====================

if __name__ == "__main__":
    driver = uc.Chrome(use_subprocess=False)
    driver.get("https://www.reclameaqui.com.br/")
    driver.maximize_window()
    wait = WebDriverWait(driver, 25)

    # Seleciona categoria inicial
    selecionar_categoria(driver, wait)
    print("Categoria 'Casa de Aposta' selecionada com sucesso!")

    # Coleta Top 3 melhores e piores
    resultados = []
    resultados.extend(coletar_empresas(driver, wait, "melhores"))
    resultados.extend(coletar_empresas(driver, wait, "piores"))

    # Salva em Excel
    df = pd.DataFrame(resultados)
    df.to_excel("dados_reclameaqui.xlsx", index=False)
    print("\nDados salvos em 'dados_reclameaqui.xlsx' com sucesso!")
    driver.quit()

