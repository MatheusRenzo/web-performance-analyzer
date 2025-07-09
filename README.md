# 🚀 Web Performance Analyzer

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

Aplicação desktop para análise de desempenho de websites usando o PageSpeed Insights da Google. Obtém métricas de desempenho para dispositivos móveis e desktop com exportação para Excel.

## ✨ Funcionalidades

- Análise completa de desempenho para qualquer URL pública
- Coleta de métricas para dispositivos móveis e desktop
- Interface gráfica intuitiva e amigável
- Logs de execução em tempo real
- Exportação de resultados para Excel
- Visualização prévia dos dados coletados
- Sistema de cancelamento de operações

## ⚙️ Pré-requisitos

- Python 3.7 ou superior
- Google Chrome instalado
- ChromeDriver compatível com sua versão do Chrome

## 🛠️ Instalação

### 1. Clonar o repositório

git clone https://github.com/MatheusRenzo/web-performance-analyzer.git
cd web-performance-analyzer

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```
### 3. Configurar ChromeDriver

Verifique sua versão do Chrome (digite chrome://settings/help na barra de endereços)

Baixe o ChromeDriver compatível: https://chromedriver.chromium.org/downloads

Coloque o executável na pasta do projeto ou adicione ao PATH do sistema

### 🚦 Como Usar

Execute o aplicativo:

```bash
python web_performance_analyzer.py
Passo a passo:
Insira a URL a ser analisada (ex: https://www.example.com)
```
Clique em "Iniciar Análise"

Acompanhe o progresso pelos logs

Visualize a prévia dos resultados

Exporte para Excel com "Salvar Como..."

### 📊 Métricas Coletadas
```bash
Performance	Pontuação geral de desempenho
First Contentful Paint	Primeira renderização de conteúdo
Largest Contentful Paint	Renderização do maior elemento
Speed Index	Índice de velocidade de carregamento
Time to Interactive	Tempo até interatividade
Total Blocking Time	Tempo total de bloqueio
Cumulative Layout Shift	Mudanças cumulativas de layout
```

### 📁 Estrutura de Arquivos
```bash
web-performance-analyzer/
├── web_performance_analyzer.py   # Código principal da aplicação
├── requirements.txt              # Dependências do projeto
├── README.md                     # Este arquivo
├── LICENSE                       # Licença MIT
├── .gitignore                    # Arquivos ignorados pelo Git
└── chromedriver(.exe)            # ChromeDriver (opcional)
```

### 🤝 Contribuição

Contribuições são bem-vindas! Siga estes passos:

Faça um fork do projeto

Crie sua branch (git checkout -b feature/sua-feature)

Faça commit das mudanças (git commit -m 'Adiciona nova funcionalidade')

Faça push para a branch (git push origin feature/sua-feature)

Abra um Pull Request

⚠️ Limitações Conhecidas
Análise pode falhar para sites com proteção anti-bot

Requer conexão estável com a internet

Processo pode levar 1-2 minutos dependendo do site

📄 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.

✉️ Contato
Matheus Renzo - @matheusrenzo.exe (intagram) - matheus.renzo.gama@gmail.com 

Link do Projeto: https://github.com/MatheusRenzo/web-performance-analyzer