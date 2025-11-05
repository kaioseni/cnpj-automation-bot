# cnpj-automation-bot
Robô automatizado em Python para consultas em massa de CNPJs utilizando a API pública ReceitaWS. Inclui controle de progresso, logs detalhados e exportação de resultados para Excel.

# 🧠 Robô de Consulta CNPJ – ReceitaWS Automator

Automatize consultas de **CNPJs** em massa com Python!  
Este projeto utiliza a **API pública ReceitaWS** para coletar dados cadastrais de empresas, processá-los e exportar as informações organizadas em planilhas Excel.

---

## 🚀 Funcionalidades Principais
- 📄 Leitura de CNPJs a partir de arquivo `CNPJS.csv`
- 🔍 Consulta automática à API ReceitaWS com controle de tempo e revezamento de lotes
- 💾 Persistência de progresso — retoma automaticamente de onde parou
- 🧹 Normalização de dados:
  - Limpeza de CNPJs (`.` `/` `-`)
  - Separação de códigos e descrições de atividades principal/secundárias
  - Extração de DDD e número de telefone
- 📊 Exportação consolidada para **Excel**
- 🪵 Geração de logs (`log_consulta.txt`) e arquivo de controle (`progresso.json`)

---

## 🛠️ Tecnologias Utilizadas
- **Python 3.10+**
- **Pandas** → manipulação e exportação de dados  
- **Requests** → integração com API ReceitaWS  
- **JSON / Regex / Ast** → tratamento e normalização de dados  

---

## 📂 Estrutura do Projeto
```
📁 Projeto_CNPJ
├── consulta_receita_robusta.py   # Script principal
├── CNPJS.csv                     # Lista de CNPJs a consultar
├── dados_empresas.xlsx           # Saída final
├── log_consulta.txt              # Log de execução
└── progresso.json                # Registro de CNPJs processados
```

---

## ⚙️ Como Usar

### 1️⃣ Preparar o ambiente
Certifique-se de ter o **Python 3.10+** instalado e as dependências abaixo:
```bash
pip install pandas requests openpyxl
```

### 2️⃣ Criar o arquivo `CNPJS.csv`
Adicione na primeira coluna os CNPJs que deseja consultar.  
Exemplo:
```csv
A2_CGC
12345678000195
98765432000101
```

### 3️⃣ Executar o robô
```bash
python consulta_receita_robusta.py
```

### 4️⃣ Acompanhar a execução
- O progresso é exibido no console.  
- Logs detalhados ficam em `log_consulta.txt`.  
- Caso o script seja interrompido, ele **retoma automaticamente** de onde parou.  

### 5️⃣ Ver resultados
Os dados consolidados serão exportados para o arquivo **`dados_empresas.xlsx`**.

---

## 🧩 Observações
- O script respeita o limite de requisições por minuto da **API ReceitaWS**.  
- Ideal para **auditorias fiscais, cadastros comerciais e levantamentos empresariais**.  
- Projeto modular fácil de adaptar para novas fontes de dados ou formatos de saída.

---

## 📚 Licença
Este projeto está sob a licença **MIT** fique à vontade para usar, modificar e distribuir.

---

## 💬 Contato
Desenvolvido por **Kaio Seni**  
💼 [LinkedIn]([https://www.linkedin.com/in/kaioseni](https://www.linkedin.com/in/kaio-serradela-333794189/))  
🐙 [GitHub](https://github.com/kaioseni)
