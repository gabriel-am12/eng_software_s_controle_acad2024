# SIGMIN
Sistema de gestão de departamento escolar

# Instalação e Execução
1. Criar venv do python e instalar dependências
```sh
# Criar um ambiente virtual local para python
python -m venv venv

# Ativar o ambiente virtual
./venv/scripts/activate.bat

# Instalar dependências necessárias para executar o projeto
pip install -r requirements.txt
```

2. Criar estrutura do banco de dados:
```sh
# Criar tabelas do banco de dados
python controle_academico/manage.py makemigrations
python controle_academico/manage.py migrate
```
3. Agora, execute o seguinte comando para criar um super usuário (administrador1)
```sh
python controle_academico/manage.py createsuperuser
```

3. Iniciar o servidor
```sh
python controle_academico/manage.py runserver
```