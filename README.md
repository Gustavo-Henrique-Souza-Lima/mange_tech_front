🚀 Guia de Instalação e Configuração
Este repositório contém o backend (Django) e o frontend (React) do sistema. Siga os passos abaixo para configurar o ambiente de desenvolvimento.

📋 Pré-requisitos
Antes de começar, certifique-se de ter instalado:

Python 3.11 - 3.12
Node.js 16+ e npm
pip (gerenciador de pacotes Python)


⚙️ Configuração do Backend
1️⃣ Navegue até a pasta do backend
bashcd back/sistema_chamados
2️⃣ Crie e ative o ambiente virtual
Windows:
bashpython -m venv venv
venv\Scripts\activate
Linux/MacOS:
bashpython3 -m venv venv
source venv/bin/activate
3️⃣ Instale as dependências
bashpip install -r requirements.txt
4️⃣ Inicie o servidor
bashpython manage.py runserver
✅ O backend estará rodando em http://localhost:8000

🎨 Configuração do Frontend
1️⃣ Navegue até a pasta do frontend
bashcd mange-tech
2️⃣ Instale as dependências
bashnpm install
3️⃣ Inicie o servidor de desenvolvimento
bashnpm run dev
✅ O frontend estará rodando em http://localhost:5173 (ou a porta indicada no terminal)
