import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import time
from collections import deque
import plotly.graph_objs as go
import random
from dash.exceptions import PreventUpdate

max_length = 50
times = deque(maxlen=max_length)
blades_speed = deque(maxlen=max_length)
power_produced = deque(maxlen=max_length)
energy_losses = deque(maxlen=max_length)


data_dict = {'Blades (Rotation Speed)': blades_speed,
             'Power Produced': power_produced,
             'Energy Losses': energy_losses,
             }



def update_values(times, blades_speed, power_produced, energy_losses,):

    times.append(time.time())
    if len(times) == 1:
        #starting values for each category
        blades_speed.append(random.randrange(60, 300))
        power_produced.append(random.randrange(30, 430))
        energy_losses.append(random.randrange(10, 35))
    else:
        for get_data in [blades_speed, power_produced, energy_losses]:
            get_data.append(get_data[-1]+get_data[-1]*random.uniform(-0.0001, 0.0001))

    return times, blades_speed, power_produced, energy_losses

times, blades_speed, power_produced, energy_losses = update_values(times, blades_speed, power_produced, energy_losses)

app = dash.Dash('Wind Energy')

app.layout = html.Div([
        html.Div([
           html.Div([
              html.P('Select category', className = 'fix_label', style = {'text-align': 'center', 'color': 'white'}),
              dcc.RadioItems(id='radio_items',
                             labelStyle = {"display": "inline-block"},
                             options=[{'label': 'Blades (Rotation Speed)', 'value': 'live1'},
                                      {'label': 'Power Produced', 'value': 'live2'},
                                      {'label': 'Energy Losses', 'value': 'live3'}
                                      ],
                             value='live1',
                             style = {'text-align': 'center', 'color': 'white'}, className = 'dcc_compon'),

                  ], className = "create_container2 five columns", style = {'margin-bottom': '30px'}),

               ], className = "row flex-display"),

     html.Div([
         html.Div([
              html.Div(id='live_text1'),

         ], className = "create_container3 eight columns", style = {'text-align': 'center'}),

    ], className = "row flex-display"),

    html.Div([
         html.Div([
              dcc.Graph(id='line_chart',
                        animate=True,
                        config = {'displayModeBar': 'hover'}),
              dcc.Interval(
                        id='update_chart',
                        interval=1000,
                        n_intervals=0),

         ], className = "create_container2 eight columns"),

    ], className = "row flex-display"),

], id= "mainContainer", style={"display": "flex", "flex-direction": "column"})

@app.callback(
    Output('live_text', 'children'),
    [Input('radio_items', 'value')],
    [Input('update_chart', 'n_intervals')]
    )
def update_graph(radio_items, n_intervals):
    update_values(times, blades_speed, power_produced, energy_losses)
    style1 = {'padding': '25px', 'fontSize': '16px', 'color': '#09F3F0'}
    style2 = {'padding': '25px', 'fontSize': '16px', 'color': '#F3B309'}
    style3 = {'padding': '25px', 'fontSize': '16px', 'color': '#FF00FF'}

    if n_intervals == 0:
        raise PreventUpdate

    elif radio_items == 'live1':
        return [
            html.Span('Blades (Rotation Speed) (Max):' + ' ' + str(max(blades_speed)) + ' ' + '(m/s)', style = style1),
            html.Span('Blades (Rotation Speed) (Min):' + ' ' + str(min(blades_speed)) + ' ' + '(m/s)', style = style1)
        ]

    elif radio_items == 'live2':
        return [
            html.Span('Power Produced (Max):' + ' ' + str(max(power_produced)) + ' ' + '(mw)', style = style2),
            html.Span('Power Produced (Min):' + ' ' + str(min(power_produced)) + ' ' + '(mw)', style = style2)
        ]

    elif radio_items == 'live3':
        return [
            html.Span('Energy Losses (Max):' + ' ' + str(max(energy_losses)) + ' ' + '(%)', style = style3),
            html.Span('Energy Losses (Min):' + ' ' + str(min(energy_losses)) + ' ' + '(%)', style = style3)
        ]


@app.callback(
    Output('line_chart', 'figure'),
    [Input('radio_items', 'value')],
    [Input('update_chart', 'n_intervals')]
    )
def update_graph(radio_items, n_intervals):
    update_values(times, blades_speed, power_produced, energy_losses)

    if n_intervals == 0:
        raise PreventUpdate

    elif radio_items == 'live1':


      return {
          'data': [go.Scatter(
            x=list(times),
            y=list(blades_speed),
            mode = 'markers+lines',
            line = dict(width = 3, color = '#09F3F0'),
            marker = dict(size = 10, symbol = 'circle', color = '#FF00FF',
                          line = dict(color = '#09F3F0', width = 2)
                          ),


            )],

              'layout': go.Layout(
                  plot_bgcolor = '#1f2c56',
                  paper_bgcolor = '#1f2c56',
                  hovermode = 'x',
                  margin = {'t': 45, 'b': 45},

                  title = {
                      'text': 'Wind Energy',

                      'y': 0.96,
                      'x': 0.5,
                      'xanchor': 'center',
                      'yanchor': 'top'},

                  titlefont = {
                      'color': 'white',
                      'size': 20},


                  xaxis = dict(range = [min(times), max(times)],
                               title = '<b>Time</b>',
                               color = 'white',
                               showline = True,
                               showgrid = True,
                               linecolor = 'white',
                               linewidth = 1,
                               ),
                  yaxis = dict(range = [min(blades_speed), max(blades_speed)],
                               title = '<b></b>',
                               color = 'white',
                               showline = False,
                               showgrid = True,
                               linecolor = 'white',
                               ),


                   )

                 }

    elif radio_items == 'live2':

        return {
            'data': [go.Scatter(
                x = list(times),
                y = list(power_produced),
                mode = 'markers+lines',
                line = dict(width = 3, color = '#F3B309'),
                marker = dict(size = 10, symbol = 'circle', color = '#2BE618',
                              line = dict(color = '#F3B309', width = 2)
                              ),
            )],

            'layout': go.Layout(
                plot_bgcolor = '#1f2c56',
                paper_bgcolor = '#1f2c56',
                hovermode = 'x',
                margin = {'t': 45, 'b': 45},

                xaxis = dict(range = [min(times), max(times)],
                             title = '<b>Time</b>',
                             color = 'white',
                             showline = True,
                             showgrid = True,
                             linecolor = 'white',
                             linewidth = 1,
                             ),
                yaxis = dict(range = [min(power_produced), max(power_produced)],
                             title = '<b></b>',
                             color = 'white',
                             showline = False,
                             showgrid = True,
                             linecolor = 'white',
                             ),

            )

        }

    elif radio_items == 'live3':

        return {
            'data': [go.Scatter(
                x = list(times),
                y = list(energy_losses),
                mode = 'markers+lines',
                line = dict(width = 3, color = '#FF00FF'),
                marker = dict(size = 10, symbol = 'circle', color = '#2BE618',
                              line = dict(color = '#FF00FF', width = 2)
                              ),
            )],

            'layout': go.Layout(
                plot_bgcolor = '#1f2c56',
                paper_bgcolor = '#1f2c56',
                hovermode = 'x',
                margin = {'t': 45, 'b': 45},



                titlefont = {
                    'color': 'white',
                    'size': 15},

                xaxis = dict(range = [min(times), max(times)],
                             title = '<b>Time</b>',
                             color = 'white',
                             showline = True,
                             showgrid = True,
                             linecolor = 'white',
                             linewidth = 1,
                             ),
                yaxis = dict(range = [min(energy_losses), max(energy_losses)],
                             title = '<b></b>',
                             color = 'white',
                             showline = False,
                             showgrid = True,
                             linecolor = 'white',
                             ),

            )

        }


if __name__ == '__main__':
    app.run_server(debug=True)