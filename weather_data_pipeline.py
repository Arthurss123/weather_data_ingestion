from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import requests
import pandas as pd
from sqlalchemy import create_engine

def kelvin_to_celsius(temp_k):
    return temp_k - 273.15


def fetch_and_store_weather_data():
    api_key = "b7622a80bb77fdd937103abc681a82a9"
    lat = -15.78  # Latitude de Brasília
    lon = -47.92  # Longitude de Brasília
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,alerts&appid={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        
        weather_data = []
        for hour in data['hourly']:
            date_time = datetime.fromtimestamp(hour['dt']).strftime('%Y-%m-%d %H:%M:%S')
            temp = kelvin_to_celsius(hour['temp'])
            feels_like = kelvin_to_celsius(hour['feels_like'])
            pressure = hour['pressure']
            humidity = hour['humidity']
            weather_main = hour['weather'][0]['main']
            description = hour['weather'][0]['description']
            wind_speed = hour['wind_speed']
            clouds = hour['clouds']

            weather_data.append({
                'Date Time': date_time,
                'Temperature (°C)': temp,
                'Feels Like (°C)': feels_like,
                'Pressure (hPa)': pressure,
                'Humidity (%)': humidity,
                'Weather': weather_main,
                'Description': description,
                'Wind Speed (m/s)': wind_speed,
                'Cloudiness (%)': clouds
            })

        df = pd.DataFrame(weather_data)

       
        db_usernames = 'postgres'
        db_password = 'senha'
        db_host = 'localhost'
        db_port = '5432'
        db_name = 'postgres'

        try:
            engine = create_engine(f'postgresql://{db_usernames}:{db_password}@{db_host}:{db_port}/{db_name}')
            df.to_sql('weather_data', engine, if_exists='replace', index=False)
            print("Dados inseridos com sucesso no banco de dados!")
        except Exception as e:
            print(f"Erro ao inserir os dados: {e}")
        finally:
            engine.dispose()
    else:
        print(f"Erro ao buscar dados da API: {response.status_code}")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'weather_data_pipeline',
    default_args=default_args,
    description='Pipeline para buscar e salvar dados meteorológicos',
    schedule_interval='0 */12 * * *',  # Executar a cada 12 horas
    start_date=datetime(2025, 1, 26),
    catchup=False,
) as dag:
    
    fetch_weather_data = PythonOperator(
        task_id='fetch_weather_data',
        python_callable=fetch_and_store_weather_data
    )

    fetch_weather_data
