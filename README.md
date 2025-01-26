# weather_data_ingestion
 
## Weather Data Pipeline 🌦️
Este é um projeto básico de Engenharia de Dados desenvolvido para praticar conceitos de orquestração de tarefas com o Apache Airflow e manipulação de dados com Python.

O pipeline utiliza a API do OpenWeather para buscar dados meteorológicos de Brasília, realiza transformações nos dados e os armazena em um banco de dados PostgreSQL. Tudo isso rodando dentro de um ambiente Docker.

## 🛠️ Tecnologias Utilizadas
Apache Airflow: Orquestração das tarefas.
Python: Extração, transformação e carregamento dos dados.
PostgreSQL: Armazenamento dos dados processados.
Docker: Contêiner para o banco de dados PostgreSQL.

## 📋 Funcionamento do Pipeline
Extração: Faz uma requisição à API do OpenWeather e coleta dados meteorológicos de Brasília, incluindo:

>- Temperatura
>- Sensação térmica
>- Umidade
>- Velocidade do vento
>- Condições climáticas
>- Entre outros.
>- Transformação: Os dados brutos são processados, incluindo:

Conversão de temperaturas de Kelvin para Celsius.
Organização das informações para fácil leitura e análise.
Carregamento: Os dados processados são inseridos em uma tabela PostgreSQL chamada weather_data.

Orquestração: Uma DAG simples do Airflow executa todo o pipeline automaticamente a cada 12 horas.