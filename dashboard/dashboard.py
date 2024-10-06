import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import requests
from datetime import datetime
import pytz

# Constants for IP and port
IP_ADDRESS = "20.197.230.60"
PORT_STH = 8666
DASH_HOST = "0.0.0.0"  # Set this to "0.0.0.0" to allow access from any IP

# Função para obter dados de luminosidade da API
def get_luminosity_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Sens/id/urn:ngsi-ld:Sens:002/attributes/luminosity?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            values = data['contextResponses'][0]['contextElement']['attributes'][0]['values']
            return values
        except KeyError as e:
            print(f"Key error (Luminosidade): {e}")
            return []
    else:
        print(f"Erro ao acessar {url}: {response.status_code}")
        return []

# Função para obter dados de temperatura da API
def get_temperature_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Sens/id/urn:ngsi-ld:Sens:002/attributes/temperature?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            values = data['contextResponses'][0]['contextElement']['attributes'][0]['values']
            return values
        except KeyError as e:
            print(f"Key error (Temperatura): {e}")
            return []
    else:
        print(f"Erro ao acessar {url}: {response.status_code}")
        return []

# Função para obter dados de umidade da API
def get_humidity_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Sens/id/urn:ngsi-ld:Sens:002/attributes/humidity?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            values = data['contextResponses'][0]['contextElement']['attributes'][0]['values']
            return values
        except KeyError as e:
            print(f"Key error (Umidade): {e}")
            return []
    else:
        print(f"Erro ao acessar {url}: {response.status_code}")
        return []

# Função para converter timestamps UTC para o fuso horário de São Paulo
def convert_to_sao_paulo_time(timestamps):
    utc = pytz.utc
    sao_paulo = pytz.timezone('America/Sao_Paulo')
    converted_timestamps = []
    for timestamp in timestamps:
        try:
            timestamp = timestamp.replace('T', ' ').replace('Z', '')
            converted_time = utc.localize(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')).astimezone(sao_paulo)
        except ValueError:
            # Lidar com caso onde milissegundos não estão presentes
            converted_time = utc.localize(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')).astimezone(sao_paulo)
        converted_timestamps.append(converted_time)
    return converted_timestamps

# Definir valor lastN
lastN = 10  # Obter os 10 pontos mais recentes a cada intervalo

# Inicializar a aplicação Dash
app = dash.Dash(__name__)

# Layout da Dashboard
app.layout = html.Div([
    html.H1('Data Sphere - Monitoramento dos valores do Sensor', style={'textAlign': 'center'}),
    
    # Gráfico de Luminosidade
    html.Div([
        html.H2('Luminosidade', style={'textAlign': 'center'}),
        dcc.Graph(id='luminosity-graph'),
        dcc.Store(id='luminosity-data-store', data={'timestamps': [], 'luminosity_values': []}),
    ], style={'padding': '20px'}),
    
    # Gráfico de Temperatura
    html.Div([
        html.H2('Temperatura', style={'textAlign': 'center'}),
        dcc.Graph(id='temperature-graph'),
        dcc.Store(id='temperature-data-store', data={'timestamps': [], 'temperature_values': []}),
    ], style={'padding': '20px'}),
    
    # Gráfico de Umidade
    html.Div([
        html.H2('Umidade', style={'textAlign': 'center'}),
        dcc.Graph(id='humidity-graph'),
        dcc.Store(id='humidity-data-store', data={'timestamps': [], 'humidity_values': []}),
    ], style={'padding': '20px'}),
    
    # Componente de Intervalo para atualização
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # em milissegundos (10 segundos)
        n_intervals=0
    )
])

# Callback para atualizar os dados de Luminosidade
@app.callback(
    Output('luminosity-data-store', 'data'),
    Input('interval-component', 'n_intervals'),
    State('luminosity-data-store', 'data')
)
def update_luminosity_data_store(n, stored_data):
    # Obter dados de luminosidade
    data_luminosity = get_luminosity_data(lastN)
    
    if data_luminosity:
        # Extrair valores e timestamps
        luminosity_values = [float(entry['attrValue']) for entry in data_luminosity]  # Garantir que os valores são floats
        timestamps = [entry['recvTime'] for entry in data_luminosity]
        
        # Converter timestamps para horário de São Paulo
        timestamps = convert_to_sao_paulo_time(timestamps)
        
        # Adicionar novos dados aos dados armazenados
        stored_data['timestamps'].extend(timestamps)
        stored_data['luminosity_values'].extend(luminosity_values)
        
        # Limitar o armazenamento a, por exemplo, 100 pontos para evitar sobrecarga
        if len(stored_data['timestamps']) > 100:
            stored_data['timestamps'] = stored_data['timestamps'][-100:]
            stored_data['luminosity_values'] = stored_data['luminosity_values'][-100:]
        
        return stored_data
    
    return stored_data

# Callback para atualizar os dados de Temperatura
@app.callback(
    Output('temperature-data-store', 'data'),
    Input('interval-component', 'n_intervals'),
    State('temperature-data-store', 'data')
)
def update_temperature_data_store(n, stored_data):
    # Obter dados de temperatura
    data_temperature = get_temperature_data(lastN)
    
    if data_temperature:
        # Extrair valores e timestamps
        temperature_values = [float(entry['attrValue']) for entry in data_temperature]
        timestamps = [entry['recvTime'] for entry in data_temperature]
        
        # Converter timestamps para horário de São Paulo
        timestamps = convert_to_sao_paulo_time(timestamps)
        
        # Adicionar novos dados aos dados armazenados
        stored_data['timestamps'].extend(timestamps)
        stored_data['temperature_values'].extend(temperature_values)
        
        # Limitar o armazenamento a 100 pontos
        if len(stored_data['timestamps']) > 100:
            stored_data['timestamps'] = stored_data['timestamps'][-100:]
            stored_data['temperature_values'] = stored_data['temperature_values'][-100:]
        
        return stored_data
    
    return stored_data

# Callback para atualizar os dados de Umidade
@app.callback(
    Output('humidity-data-store', 'data'),
    Input('interval-component', 'n_intervals'),
    State('humidity-data-store', 'data')
)
def update_humidity_data_store(n, stored_data):
    # Obter dados de umidade
    data_humidity = get_humidity_data(lastN)
    
    if data_humidity:
        # Extrair valores e timestamps
        humidity_values = [float(entry['attrValue']) for entry in data_humidity]
        timestamps = [entry['recvTime'] for entry in data_humidity]
        
        # Converter timestamps para horário de São Paulo
        timestamps = convert_to_sao_paulo_time(timestamps)
        
        # Adicionar novos dados aos dados armazenados
        stored_data['timestamps'].extend(timestamps)
        stored_data['humidity_values'].extend(humidity_values)
        
        # Limitar o armazenamento a 100 pontos
        if len(stored_data['timestamps']) > 100:
            stored_data['timestamps'] = stored_data['timestamps'][-100:]
            stored_data['humidity_values'] = stored_data['humidity_values'][-100:]
        
        return stored_data
    
    return stored_data

# Callback para atualizar o gráfico de Luminosidade
@app.callback(
    Output('luminosity-graph', 'figure'),
    Input('luminosity-data-store', 'data')
)
def update_luminosity_graph(stored_data):
    if stored_data['timestamps'] and stored_data['luminosity_values']:
        # Calcular a média da luminosidade
        mean_luminosity = sum(stored_data['luminosity_values']) / len(stored_data['luminosity_values'])
        
        # Criar as traces para o gráfico
        trace_luminosity = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['luminosity_values'],
            mode='lines+markers',
            name='Luminosidade',
            line=dict(color='orange')
        )
        trace_mean = go.Scatter(
            x=[stored_data['timestamps'][0], stored_data['timestamps'][-1]],
            y=[mean_luminosity, mean_luminosity],
            mode='lines',
            name='Média Luminosidade',
            line=dict(color='blue', dash='dash')
        )
        
        # Criar a figura
        fig_luminosity = go.Figure(data=[trace_luminosity, trace_mean])
        
        # Atualizar o layout
        fig_luminosity.update_layout(
            title='Luminosidade ao Longo do Tempo',
            xaxis_title='Timestamp',
            yaxis_title='Luminosidade',
            hovermode='closest'
        )
        
        return fig_luminosity
    
    return {}

# Callback para atualizar o gráfico de Temperatura
@app.callback(
    Output('temperature-graph', 'figure'),
    Input('temperature-data-store', 'data')
)
def update_temperature_graph(stored_data):
    if stored_data['timestamps'] and stored_data['temperature_values']:
        # Calcular a média da temperatura
        mean_temperature = sum(stored_data['temperature_values']) / len(stored_data['temperature_values'])
        
        # Criar as traces para o gráfico
        trace_temperature = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['temperature_values'],
            mode='lines+markers',
            name='Temperatura',
            line=dict(color='red')
        )
        trace_mean = go.Scatter(
            x=[stored_data['timestamps'][0], stored_data['timestamps'][-1]],
            y=[mean_temperature, mean_temperature],
            mode='lines',
            name='Média Temperatura',
            line=dict(color='green', dash='dash')
        )
        
        # Criar a figura
        fig_temperature = go.Figure(data=[trace_temperature, trace_mean])
        
        # Atualizar o layout
        fig_temperature.update_layout(
            title='Temperatura ao Longo do Tempo',
            xaxis_title='Timestamp',
            yaxis_title='Temperatura (°C)',
            hovermode='closest'
        )
        
        return fig_temperature
    
    return {}

# Callback para atualizar o gráfico de Umidade
@app.callback(
    Output('humidity-graph', 'figure'),
    Input('humidity-data-store', 'data')
)
def update_humidity_graph(stored_data):
    if stored_data['timestamps'] and stored_data['humidity_values']:
        # Calcular a média da umidade
        mean_humidity = sum(stored_data['humidity_values']) / len(stored_data['humidity_values'])
        
        # Criar as traces para o gráfico
        trace_humidity = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['humidity_values'],
            mode='lines+markers',
            name='Umidade',
            line=dict(color='blue')
        )
        trace_mean = go.Scatter(
            x=[stored_data['timestamps'][0], stored_data['timestamps'][-1]],
            y=[mean_humidity, mean_humidity],
            mode='lines',
            name='Média Umidade',
            line=dict(color='purple', dash='dash')
        )
        
        # Criar a figura
        fig_humidity = go.Figure(data=[trace_humidity, trace_mean])
        
        # Atualizar o layout
        fig_humidity.update_layout(
            title='Umidade ao Longo do Tempo',
            xaxis_title='Timestamp',
            yaxis_title='Umidade (%)',
            hovermode='closest'
        )
        
        return fig_humidity
    
    return {}

# Executar o servidor Dash
if __name__ == '__main__':
    app.run_server(debug=True, host=DASH_HOST, port=8050)
