import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from exchanges.coindesk import CoinDesk as cd
from datetime import datetime, timedelta

def fetch_btc_price_dict(delta):

	now = datetime.now()
	past = now - timedelta(days=delta)
	start = past.strftime('%Y-%m-%d')

	print("Retrieving bitcoin price data since: {}".format(start))
	price_dict = cd.get_historical_data_as_dict(start=start, end=None)
	int_days_price_dict = {(datetime.strptime(k, '%Y-%m-%d') - past).days: int(v) for k,v in price_dict.items()}

	return int_days_price_dict


app = dash.Dash()

app.css.append_css({
   'external_url': (
   'https://github.com/jstremme/bitcoin-price-app/blob/master/display.css'
   )
})

colors = {'background': '#111111', 'text': '#7FDBFF'}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
	html.H1(
		children='LAST N DAYS OF BITCOIN',
		style={
			'textAlign': 'center',
			'color': colors['text']
		}
	),

	html.Div(children='Updates Daily for Dynamic Price Checking', style={
		'textAlign': 'center',
		'color': colors['text']
	}),
    dcc.Graph(id='dynamic-graph', config={'displayModeBar': False}),
    dcc.Input(
   		id='input-id',
   		placeholder='Enter N Days',
   		type='text',
   		value=100,
   		max=2000,
   		min=1,
   		size=20
	),
])

@app.callback(dash.dependencies.Output('dynamic-graph', 'figure'), [dash.dependencies.Input('input-id', 'value')])
def update_figure(value=100):

	int_days_price_dict = fetch_btc_price_dict(delta=int(value))

	return {
        'data': [{
        	'x': list(int_days_price_dict.keys()),
        	'y': list(int_days_price_dict.values()),
        	'type': 'bar', 
        	'name': 'BTC Price'
        	}
         ],
        'layout': {
				'plot_bgcolor': colors['background'],
				'paper_bgcolor': colors['background'],
				'font': {
					'color': colors['text']
				}
		}
    }

if __name__ == '__main__':

	app.run_server(debug=True)
