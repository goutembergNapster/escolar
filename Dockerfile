FROM python:3.11-alpine3.18
LABEL mantainer="Escolinha"


# Essa variável de ambiente é usada para controlar se o Python deve 
# gravar arquivos de bytecode (.pyc) no disco. 1 = Não, 0 = Sim
ENV PYTHONDONTWRITEBYTECODE 1

# Define que a saída do Python será exibida imediatamente no console ou em 
# outros dispositivos de saída, sem ser armazenada em buffer.
# Em resumo, você verá os outputs do Python em tempo real.
ENV PYTHONUNBUFFERED 1

# Copia a pasta "clinica_medica" e "scripts" para dentro do container.
COPY ./ /escolinha
COPY scripts /scripts
COPY requirements.txt /prantaopro/requirements.txt
#COPY /escolinha/home/migrations /clinica_medica/home/migrations
 

# Entra na pasta djangoapp no container
WORKDIR /escolinha

# A porta 8000 estará disponível para conexões externas ao container
# É a porta que vamos usar para o Django.
EXPOSE 8000

# RUN executa comandos em um shell dentro do container para construir a imagem. 
# O resultado da execução do comando é armazenado no sistema de arquivos da 
# imagem como uma nova camada.
# Agrupar os comandos em um único RUN pode reduzir a quantidade de camadas da 
# imagem e torná-la mais eficiente.
RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /prantaopro/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  mkdir -p /escolinha/staticfiles && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chown -R duser:duser /data/web/media && \
  chown -R duser:duser /escolinha/staticfiles && \
  chown -R duser:duser /escolinha/home/migrations && \
  chmod -R 755 /escolinha/home/migrations && \
  chmod -R 775 /escolinha/data_base && \
  #chmod -R 666 /escolinha/data_base/banco.sqlite3 && \
  chown -R duser:duser /escolinha/data_base && \
  #chown -R duser:duser /escolinha/data_base/banco.sqlite3 && \
  chmod -R 766 /data/web/static && \
  chmod -R 766 /data/web/media && \
  chmod -R 766 /escolinha/staticfiles && \
  chmod -R +x /scripts

ENV PATH="/scripts:/venv/bin:$PATH"

# Muda o usuário para duser
USER duser

# Executa o arquivo scripts/commands.sh
CMD ["commands.sh"]



