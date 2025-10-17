# Desafio Técnico - BlueTape

Este projeto automatiza a coleta de métricas de desempenho de empresas da categoria "Casa de Aposta" no site [Reclame Aqui](https://www.reclameaqui.com.br/), utilizando Python, Selenium e Pandas.

Repositório oficial: [github.com/Victor1v/desafioscraping](https://github.com/Victor1v/desafioscraping)

---

## Objetivo

Extrair informações sobre as 3 melhores e 3 piores empresas do ramo “Casa de Aposta”, com base nas métricas apresentadas pelo Reclame Aqui, e salvar os resultados em planilha Excel.

---

## Funcionalidades

- Abertura automática do site Reclame Aqui
- Seleção da categoria Casa de Aposta
- Extração dos seguintes dados de cada empresa:
  - Reclamações respondidas (%)
  - Voltariam a fazer negócio (%)
  - Solução (%)
  - Nota
- Salvamento dos resultados em arquivo Excel (`dados_reclameaqui.xlsx`)

---

## Tecnologias utilizadas

- [Python 3.10+](https://www.python.org/)
- [Selenium](https://pypi.org/project/selenium/)
- [Undetected Chromedriver](https://pypi.org/project/undetected-chromedriver/)
- [Pandas](https://pypi.org/project/pandas/)

---

## Como executar

### 1. Clonar o repositório
```bash
git clone https://github.com/Victor1v/desafioscraping.git
cd desafioscraping
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Executar o script
```bash
python desafio.py
```

### 4. Resultado
Após a execução, o arquivo `dados_reclameaqui.xlsx` será gerado automaticamente na pasta do projeto, contendo os dados das 6 empresas coletadas (3 melhores e 3 piores).

---

## Exemplo de saída (Excel)

| empresa   | respondidas | voltariam | solucao | nota | tipo      |
|------------|--------------|------------|---------|------|-----------|
| betou      | 100%         | 99.3%      | 99.3%   | 9.85 | melhores  |
| f12-bet    | 98.9%        | 98.4%      | 99.8%   | 9.5  | melhores  |
| luva-bet   | 98.2%        | 97.8%      | 98.6%   | 9.4  | melhores  |

---

## Observações técnicas

- O projeto utiliza undetected_chromedriver para evitar bloqueios automáticos do Reclame Aqui.  
- Todos os elementos são localizados via WebDriverWait, garantindo maior estabilidade na coleta.  
- Os dados são limpos e estruturados antes de serem exportados com Pandas.

---

## Autor

Victor Marcolino  
Desenvolvido como parte do processo seletivo da BlueTape.  
Contato: morenovictor4@yahoo.com.br  
LinkedIn: [linkedin.com/in/victormarcolino](https://www.linkedin.com/in/victor-marcolino03/)

---

## Licença

Este projeto foi desenvolvido para fins de avaliação técnica e não possui fins comerciais.
