# Sendgrid Webhook Receiver


## Instalação dos pacotes necessários (Ubuntu 18.04)

### Softwares necessários

* python2.7
* apache2
* libapache2-mod-wsgi
* postgresql e postgresql-contrib 
  * [Aqui tem um bom tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04) de como instalar no Ubuntu 18.04
* build-essential
* git
* gettext 
  * para uso das funcionalidade de compilação de mensagens traduzidas
* python-pip


> Depois é só fazer um `sudo apt update` e instalar os pacotes apresentados acima com o `sudo apt install`

> 2) Pode ser necessário instalar também o pacote libq-dev em atualizações mais recentes do Ubuntu. A biblioteca psycopg2 foi atualizada para a versão 2.8.5 e há relatos de que esse pacote é necessário. 


> 3) A versão do Django utilizada nesta versão é a [1.11.28](https://docs.djangoproject.com/en/1.11/).

## Preparação do ambiente para instalação d

Recomendo que crie um usuário no sistema específico para o hook, por exemplo, usuário `hook`. 

### Configuração do banco de dados PostgreSQL

Editar o arquivo `pg_hba.conf` e inserir a linha:

Logo acima da linha:
```bash
local   all             all         peer
```

inserir a seguinte linha:
```bash
local   all              hook                         md5
```

Baixe o código fonte desse repositório:
```bash
git clone https://github.com/AleSMendes/mailwebhook
```

Não é obrigatório, mas é uma boa prática, criar um ambiente virtual python, pois isso permite separar as dependências do projeto e não interferir em outros sistemas na mesma máquina. 

Instale o `virtualenv` por meio do `pip`:

```bash
pip install virtualenv
```

Dentro do diretório onde o mailwebhook foi baixado, execute o comando:

```bash
virtualenv venv
```

Isso criará um ambiente virtual python dentro do subdiretório chamado `venv`. Por fim, carregue o script `venv/bin/activate` para fazer uso do ambiente virtual: 

```bash
source venv/bin/activate
```

Com o ambiente virtual ativado, instale os pacotes que estão listados no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

Edite o arquivo `mailwebhook\settings.py` e localize a seção databases. Adicione as informações para conexão no banco de dados, conforme o exemplo:

```bash
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql_psycopg2',
'NAME': 'hook',
'USER': 'hook',
'HOST': 'localhost',
'PASSWORD': 'SENHA'
}}
```

Por fim, você precisará executar o script `reset.sh` (não faça como root) que fará a inicialização do esquema no banco de dados (criará as tabelas, etc.)
```bash
./reset.sh
```

> **Observação:** Se tiver algum problema ao executar o script acima, provavelmente vai ser relacionado à configuração do PostgreSQL e, nesse caso, o *Google é seu amigo.* Porém, o erro mais comum é que você tenha executado o script como root e o `postgres` acuse que não há um usuário root. Recomendo criar um usuário que não seja root (por exemplo, helios) e usar o mesmo nome para usuário do banco. Ou executar os comandos contidos no script com o usuário adequado do banco.

### Testando a instalação em ambiente de desenvolvimento

Ao executar o script `reset.sh`, você teve que criar um usuário de administração do django. Isso se deve ao fato de aplicação `admin` estar habilitada no arquivo `settings.py` (django.contrib.admin), pois iremos utilizá-la em algumas personalizações.

>*Observação*: você sempre pode criar um novo usuário para o django admin site executando o comando `python manage.py createsuperuser`

Se tudo estiver correto até aqui, agora você poderá executar o servidor web para desenvolvimento que é provido pelo próprio django. Use esse servidor somente para verificar se a instalação foi feita com sucesso, porém não use-o caso queira colocar o Helios no ambiente de produção.

Execute o seguinte comando:

```bash
python manage.py runserver 0.0.0.0:8000
```


## Preparando ambiente de produção

Na seção anterior foi usado o servidor web de desenvolvimento provido pelo próprio Django (`python manage.py runserver 0.0.0.0:8000`). No entanto, ele é apenas para desenvolvimento e **não deve** ser usado em um ambiente de produção.

É possível trabalhar com diversos servidores web, porém no caso em questão optou-se pelo [Apache](https://docs.djangoproject.com/en/1.8/topics/install/#install-apache-and-mod-wsgi).

### Configuração apache

Módulos a serem habilitados, para a configuração exemplo:
```bash
sudo a2enmod rewrite
sudo a2enmod ssl
```
Para configurar o `httpd.conf` ou equivalente, siga as instruções em [How to use Django with Apache and mod_wsgi](https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/modwsgi/).


## Configurações Gerais:

- Para o ambiente de produção, em `settings.py`, configurar `ALLOWED_HOSTS` para o seu domínio. Exemplo:
  ```bash
  # set a value for production environment, alongside with debug set to false
  ALLOWED_HOSTS = get_from_env('ALLOWED_HOSTS', 'endereco-do-seu-servidor-helios').split(",")
  ```

- Em `settings.py` alterar de `True` para `False` o valor da constante `DEBUG`
- Alterar obrigatoriamente o valor do [SECRET_KEY](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY). Há ferramentas na web pra isso, como a disponível em [http://www.miniwebtool.com/django-secret-key-generator/](http://www.miniwebtool.com/django-secret-key-generator/)
- Conforme indicado no `settings.py`, não se deve alterar o valor da opção `SECURE_URL_HOST` após você já ter o sistema em produção, com eleições criadas (em andamento ou finalizadas), pois caso contrário a URL para depósito da cédula se tornará inválida.
- Em `settings.py` alterar o valor da variável SENDGRID_WEBHOOK_TOKEN de acordo com token do sendgrid
