# 💰 Treasury Management System

Sistema web desenvolvido em **Django** para gerenciamento das informações da área de **Tesouraria**.  
O projeto tem como objetivo centralizar e automatizar processos financeiros, oferecendo controle, padronização e transparência nas operações.

Atualmente, o módulo de **Seguros** está em funcionamento, permitindo o cadastro e controle das apólices corporativas.

---

## 🚀 Funcionalidades Principais

### 🔹 Módulo de Seguros
- Cadastro de seguradoras, apólices e empresas associadas.  
- Armazenamento de documentos em **PDF**.  
- Controle de **valores segurados**, **vencimentos** e **tipos de seguro**.  
- Visualização e gerenciamento via **Django Admin** customizado.  

### 🔹 (Em desenvolvimento)
- Módulo de **aplicações financeiras**.  
- Controle de **contas bancárias**, saldos e movimentações.  
- Dashboards e relatórios gerenciais.  
- Integração com **SAP** e **Finnet**.

---

## 🧩 Estrutura do Projeto

```
/accounts       → autenticação e controle de usuários  
/apolicies      → módulo de seguros (apólices, seguradoras, PDFs, etc.)  
/companies      → cadastro de empresas  
/media          → arquivos enviados pelos usuários  
/static         → arquivos estáticos (CSS, JS, imagens)  
/templates      → templates HTML  
/app            → configuração principal do projeto  
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.13**
- **Django 5.2**
- **SQLite3** (banco de dados local)
- **Bootstrap 5**
- **Pathlib** para manipulação de arquivos
- **HTML / CSS / JavaScript**
- **Virtualenv** para isolamento de ambiente

---

## ⚙️ Instalação e Execução

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/SEU-USUARIO/treasury-management.git
cd treasury-management
```

### 2️⃣ Crie o ambiente virtual
```bash
python -m venv venv
```

### 3️⃣ Ative o ambiente virtual
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

### 4️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

### 5️⃣ Execute as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Inicie o servidor
```bash
python manage.py runserver
```

Acesse o sistema em:  
👉 **http://127.0.0.1:8000/**

---

## 🔐 Acesso Administrativo

Crie um superusuário para acessar o painel administrativo:
```bash
python manage.py createsuperuser
```

Acesse o painel em:  
🔗 [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📊 Estrutura de Dados — Exemplo (Módulo de Seguros)

| Campo | Descrição |
|-------|------------|
| **Empresa** | Empresa proprietária da apólice |
| **Seguradora** | Nome da companhia seguradora |
| **Tipo de Seguro** | Categoria (ex: patrimonial, vida, frota) |
| **Valor Segurado** | Montante total coberto |
| **Vencimento** | Data de expiração da apólice |
| **Documento (PDF)** | Arquivo vinculado à apólice |

---

## 📅 Roadmap

- [x] Módulo de Seguros  
- [ ] Módulo de Contas Bancárias  
- [ ] Relatórios e dashboards interativos  
- [ ] Integração com sistemas ERP  

---

## 🧑‍💻 Autor

**Alessandro Purcineli**  
💼 Analista Financeiro com experiência em automação e desenvolvimento de soluções de controle gerencial.  
🔗 [LinkedIn](https://www.linkedin.com/in/alessandro-purcineli)  
📧 [alepurbttf@gmail.com]  

---

## 📄 Licença

Projeto de portfólio pessoal — uso livre para fins educacionais e demonstrativos.  
Distribuição comercial não é permitida sem autorização.

---
