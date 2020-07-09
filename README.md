# goMenu
Multi-restaurant edition of DjangoMenu
https://github.com/tiagocordeiro/djmenu

![Python application](https://github.com/tiagocordeiro/gomenu/workflows/Python%20application/badge.svg?branch=master)
[![Build Status](https://travis-ci.org/tiagocordeiro/gomenu.svg?branch=master)](https://travis-ci.org/tiagocordeiro/gomenu)
[![Updates](https://pyup.io/repos/github/tiagocordeiro/gomenu/shield.svg)](https://pyup.io/repos/github/tiagocordeiro/gomenu/)
[![codecov](https://codecov.io/gh/tiagocordeiro/gomenu/branch/master/graph/badge.svg)](https://codecov.io/gh/tiagocordeiro/gomenu)


### Como rodar o projeto

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/tiagocordeiro/gomenu.git
cd gomenu
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
```

### Configurar administrador
Para cria um usuário administrador
```
python manage.py createsuperuser --username dev --email dev@foo.bar
```

### Rodar em ambiente de desenvolvimento
Para rodar o projeto localmente
```
python manage.py runserver
```

### Banco de dados para ambiente de desenvolvimento com Docker
```
docker-compose up -d
```
