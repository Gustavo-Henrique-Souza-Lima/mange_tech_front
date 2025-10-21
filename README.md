# 🚀 Guia de Instalação e Configuração

<div align="center">
  
Este repositório contém o **backend (Django)** e o **frontend (React)** do sistema.  
Siga os passos abaixo para configurar o ambiente de desenvolvimento.

</div>

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- ✅ **Python 3.11 - 3.12**
- ✅ **Node.js 16+** e **npm**
- ✅ **pip** (gerenciador de pacotes Python)

---

## ⚙️ Configuração do Backend

### 1️⃣ Navegue até a pasta do backend

```bash
cd back/sistema_chamados
```

### 2️⃣ Crie e ative o ambiente virtual

<table>
<tr>
<td width="50%">

**🪟 Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

</td>
<td width="50%">

**🐧 Linux/MacOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

</td>
</tr>
</table>

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Inicie o servidor

```bash
python manage.py runserver
```

> ✅ **O backend estará rodando em** `http://localhost:8000`

---

## 🎨 Configuração do Frontend

### 1️⃣ Navegue até a pasta do frontend

```bash
cd mange-tech
```

### 2️⃣ Instale as dependências

```bash
npm install
```

### 3️⃣ Inicie o servidor de desenvolvimento

```bash
npm run dev
```

> ✅ **O frontend estará rodando em** `http://localhost:5173` (ou a porta indicada no terminal)

---

## 🎯 Pronto!

<div align="center">

Agora você tem o sistema rodando localmente! 🎉  
Acesse o frontend no navegador e comece a desenvolver. 🚀

</div>

---

## 💡 Dicas

- 🔹 Mantenha o ambiente virtual ativado enquanto trabalha no backend
- 🔹 Para desativar o ambiente virtual, use o comando `deactivate`
- 🔹 Certifique-se de que ambos os servidores (backend e frontend) estejam rodando simultaneamente

---

<div align="center">

**Desenvolvido pelos estudantes da turma de ADS do Senai Roberto Mange**

**Membros do grupo:**

**Eduardo Costa de Sousa,**
**Eduardo Diniz Confessor,**
**Gabriel Campopiano Rosa,**
**Gustavo Henrique Souza Lima**

</div>
