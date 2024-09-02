import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime

# Load data from Excel
df = pd.read_excel('Test for Dashboard.xlsx')
df['INFLOW_DATE'] = pd.to_datetime(df['INFLOW_DATE'])
df['Year'] = df['INFLOW_DATE'].dt.year

# Initialize the Dash app
app = Dash(__name__)

#app.css.append_css({'external_url': '/static/style.css'})

# Define month order and mappings
month_order = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]
month_name_to_number = {name: i for i, name in enumerate(month_order, 1)}

# CSS styles


app.layout = html.Div(style={'fontFamily': 'Times New Roman, sans-serif', 'backgroundColor': '#f0f2f5'}, 
                      children=[
    # Dashboard Title Bar
    html.Div(style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)', 'marginBottom': '20px'},
             children=[
        html.Div(style={'backgroundColor': '#f9f9f9', 'height': '8px', 'width': '100%', 'position': 'relative'}),
        html.Div(style={'height': '60px', 'width': '100%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'},
                 children=[
            html.H1("PACE BTO DASHBOARD", style={'textAlign': 'center', 'color': 'black', 'fontSize': '36px'})
        ])
    ]),

    dcc.Tabs(style={'fontSize': '20px'}, children=[

        # Tab 1
        dcc.Tab(label='Overview', style={'backgroundColor': '#bad7f5', 'border': '1px solid #bad7f5'}, 
            children=[
            html.Div(style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)', 'marginBottom': '20px'},
                     children=[
                html.Div([
                    dcc.Checklist(
                        id='year-filter',
                        options=[{'label': year, 'value': year} for year in sorted(df['Year'].unique())],
                        value=[sorted(df['Year'].unique())[-1]],
                        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                    ),
                ], style={'textAlign': 'center', 'padding': '20px 0'}),

                html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'gap': '20px', 'flexWrap': 'wrap'}, children=[
                    html.Div(dcc.Graph(id='month-trend'), style={'flex': '1', 'minWidth': '300px', 'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),
                    html.Div(dcc.Graph(id='disease-trend'), style={'flex': '0.5', 'minWidth': '300px', 'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),
                ]),

                html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'gap': '20px', 'flexWrap': 'wrap'}, children=[
                    html.Div(dcc.Graph(id='client-trend'), style={'flex': '1', 'minWidth': '300px', 'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),
                    html.Div(dcc.Graph(id='quarter-trend'), style={'flex': '0.5', 'minWidth': '300px', 'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),
                ]),
            ])
        ]),

        # Tab 2
        dcc.Tab(label='Yearly Comparison', style={'backgroundColor': '#bad7f5', 'border': '1px solid #bad7f5'}, children=[
            html.Div(style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)', 'marginBottom': '20px'},
                     children=[
                html.Div([
                    dcc.Dropdown(
                        id='year-filter-1',
                        options=[{'label': year, 'value': year} for year in sorted(df['Year'].unique())],
                        value=sorted(df['Year'].unique())[-2],
                        style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'backgroundColor': '#ffffff', 'border': '1px solid #cccccc', 'color': '#003366'}
                    ),
                    dcc.Dropdown(
                        id='year-filter-2',
                        options=[{'label': year, 'value': year} for year in sorted(df['Year'].unique())],
                        value=sorted(df['Year'].unique())[-1],
                        style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'backgroundColor': '#ffffff', 'border': '1px solid #cccccc', 'color': '#003366'}
                    ),
                ], style={'width': '100%', 'textAlign': 'center', 'padding': '20px 0'}),

                html.Div(dcc.Graph(id='year-comparison'), style={'width': '100%', 'padding': '10px', 'backgroundColor': '#ffffff', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),
            ])
        ]),
    ])
])





# Callback for Month-wise Trend
@app.callback(
    Output('month-trend', 'figure'),
    [Input('year-filter', 'value')]
)
def update_month_trend(selected_years):
    filtered_df = df[df['Year'].isin(selected_years)].copy()
    filtered_df['Month'] = filtered_df['INFLOW_DATE'].dt.strftime('%b')
    # Group by month and count cases
    month_trend = filtered_df.groupby('Month')['CASE_NAME'].count().reindex(month_order, fill_value=0).reset_index()
    month_trend.columns = ['Month', 'No of Case']

    # Create line chart with data labels
    fig = px.line(month_trend, x='Month', y='No of Case', title='Month-wise Trend', markers=True, text='No of Case')

    # Update hovertemplate and text position, font weight
    fig.update_traces(
        hovertemplate='Month = %{x}<br>No of Case = %{y}',
        textposition='top center',
        textfont=dict(size=10, color='#003366', family='Times New Roman', weight='bold'),
        line_color='#00695c'
    )

    fig.update_layout(
        xaxis_title='Month', 
        yaxis_title='No of Case',  
        title_font=dict(size=24, color='black', family='Times New Roman', weight='bold'), 
        plot_bgcolor='#e8f5e9', 
        paper_bgcolor='#f0f2f5', 
        font_color='#003366'
    )

    return fig

# Callback for Quarterly Trend (Pie Chart)
@app.callback(
    Output('quarter-trend', 'figure'),
    [Input('year-filter', 'value')]
)
def update_quarter_trend(selected_years):
    filtered_df = df[df['Year'].isin(selected_years)].copy()
    quarter_trend = filtered_df.groupby(filtered_df['INFLOW_DATE'].dt.quarter)['CASE_NAME'].count().reset_index()
    quarter_trend['Quarter'] = quarter_trend['INFLOW_DATE'].apply(lambda x: f'Q{x}')

    fig = px.pie(quarter_trend, values='CASE_NAME', names='Quarter', title='Quarterly Trend', hole=.3)

    # Update hovertemplate and bold text labels
    fig.update_traces(
        hovertemplate='Quarter = %{label}<br>No of Case = %{value}',
        textfont=dict(size=10, color='#003366', family='Times New Roman', weight='bold'),
        marker=dict(colors=['#ff8a65', '#4db6ac', '#9575cd', '#ffb74d'])
    )

    fig.update_layout(title_font=dict(size=24, color='black', family='Times New Roman', weight='bold'), 
                      plot_bgcolor='#ffe0b2', 
                      paper_bgcolor='#f0f2f5', 
                      font_color='#003366')
    return fig

# Callback for Disease-wise Trend (Pie Chart)
@app.callback(
    Output('disease-trend', 'figure'),
    [Input('year-filter', 'value')]
)
def update_disease_trend(selected_years):
    filtered_df = df[df['Year'].isin(selected_years)].copy()
    disease_trend = filtered_df.groupby('DISEASE')['CASE_NAME'].count().reset_index()

    fig = px.pie(disease_trend, values='CASE_NAME', names='DISEASE', title='Disease-wise Trend', hole=.3)

    # Update hovertemplate and bold text labels
    fig.update_traces(
        hovertemplate='Disease = %{label}<br>No of Case = %{value}',
        textfont=dict(size=10, color='#003366', family='Times New Roman', weight='bold'),
        marker=dict(colors=['#66bb6a', '#64b5f6', '#ffb74d'])
    )

    fig.update_layout(title_font=dict(size=24, color='black', family='Times New Roman', weight='bold'), 
                      plot_bgcolor='#f1f8e9', 
                      paper_bgcolor='#f0f2f5', 
                      font_color='#003366')
    return fig

# Callback for Top 10 Clients (Bar Chart)
@app.callback(
    Output('client-trend', 'figure'),
    [Input('year-filter', 'value')]
)
def update_client_trend(selected_years):
    filtered_df = df[df['Year'].isin(selected_years)].copy()
    client_trend = filtered_df.groupby('CLIENT_NAME')['CASE_NAME'].count().reset_index()
    top_10_clients = client_trend.nlargest(10, 'CASE_NAME')

    fig = px.bar(top_10_clients, x='CLIENT_NAME', y='CASE_NAME', title='Top 10 Clients', text='CASE_NAME')

    # Update hovertemplate and bold text labels
    fig.update_traces(
        hovertemplate='Client = %{x}<br>No of Case = %{y}',
        textfont=dict(size=10, color='#003366', family='Times New Roman', weight='bold'),
        textposition='outside',
        marker_color='#5e35b1'
    )

    fig.update_layout(
        xaxis_title='Client', 
        yaxis_title='No of Case', 
        title_font=dict(size=24, color='black', family='Times New Roman', weight='bold'),
        plot_bgcolor='#ede7f6', 
        paper_bgcolor='#f0f2f5', 
        font_color='#003366',
        margin = dict(t = 50, b=50, l=100, r = 50)
        
    )
    return fig

# Callback for Yearly Comparison (Bar Chart)
@app.callback(
    Output('year-comparison', 'figure'),
    [Input('year-filter-1', 'value'), Input('year-filter-2', 'value')]
)
def update_year_comparison(year1, year2):
    current_date = datetime.now()
    current_month_number = current_date.month  # integer 1-12
    current_year = current_date.year

    # Filter data for both years
    filtered_df1 = df[df['Year'] == year1].copy()
    filtered_df2 = df[df['Year'] == year2].copy()

    # Group by month and count cases, reindex to include all months
    month_trend1 = filtered_df1.groupby(filtered_df1['INFLOW_DATE'].dt.strftime('%b'))['CASE_NAME'].count().reindex(month_order, fill_value=0).reset_index()
    month_trend2 = filtered_df2.groupby(filtered_df2['INFLOW_DATE'].dt.strftime('%b'))['CASE_NAME'].count().reindex(month_order, fill_value=0).reset_index()
    month_trend1.columns = ['Month', 'No of Case']
    month_trend2.columns = ['Month', 'No of Case']

    # Add year information
    month_trend1['Year'] = year1
    month_trend2['Year'] = year2

    # Combine data for ordering
    combined_df = pd.concat([month_trend1, month_trend2])

    fig = go.Figure()

    # Add bars for the selected years
    fig.add_trace(go.Bar(x=month_trend1['Month'], y=month_trend1['No of Case'], name=str(year1), marker_color='black'))
    fig.add_trace(go.Bar(x=month_trend2['Month'], y=month_trend2['No of Case'], name=str(year2), marker_color='orange'))

    # Determine which months to add arrows based on year2 and current date
    for month in month_order:
        month_number = month_name_to_number[month]
        # Decide whether to add arrows based on year and month
        add_arrow = True
        if year2 == current_year and month_number > current_month_number:
            add_arrow = False
        # Proceed only if add_arrow is True
        if add_arrow:
            # Get values for both years
            year1_value = month_trend1[month_trend1['Month'] == month]['No of Case'].values[0]
            year2_value = month_trend2[month_trend2['Month'] == month]['No of Case'].values[0]
            # Compute difference
            if year1_value == 0:
                diff = 0
            else:
                diff = ((year2_value - year1_value) / year1_value) * 100
            # Determine arrow and color
            if diff > 0:
                arrow = "⬆️"
                direction = "+"
                color = "green"
            elif diff < 0:
                arrow = "⬇️"
                direction = ""
                color = "red"
            else:
                arrow = ""
                direction = ""
                color = "black"
            # Only show arrows if there is a difference
            if diff != 0:
                # Position the text slightly above the higher bar
                y_position = max(year1_value, year2_value) + (max(year1_value, year2_value) * 0.05)
                # Format the diff
                if diff > 0:
                    diff_text = f"{arrow} +{int(diff)}%"
                else:
                    diff_text = f"{arrow} {int(diff)}%"
                # Add the text to the figure
                fig.add_trace(go.Scatter(
                    x=[month], 
                    y=[y_position], 
                    text=[diff_text], 
                    mode='text', 
                    textposition='top center', 
                    showlegend=False, 
                    textfont=dict(color=color, weight='bold')  # Bold text
                ))

    fig.update_layout(
        barmode='group',  # Grouped bars
        title=f'Yearly Comparison: {year1} vs {year2}', 
        xaxis={'categoryorder':'array', 'categoryarray': month_order},  # Ensures the X-axis is ordered by months
        plot_bgcolor='#f9f9f9', 
        font_color='#003366',
        title_font=dict(size=24, color='black', family='Times New Roman', weight='bold'),
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)