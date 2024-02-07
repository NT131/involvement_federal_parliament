#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 09:37:00 2024

@author: niels_tack
"""
import dash
from dash import html
from dash import dcc


import federal_written_questions


app = dash.Dash(__name__, 
		url_base_pathname='/visualisaties/betrokkenheid-federaal-parlement/',
		assets_folder='assets') # Relative path to the folder of css file)
app.title = "Betrokkenheid federale parlementsleden" # title of tab in browser

app.layout = html.Div([
    # Header section
    html.Div(
        children=[
            # Title
            html.H1(
                children="Betrokkenheid federale parlementsleden",
                className="header-title",
                style={"color": "#FFFFFF"}
            ),
            
            # Markdown description (simpler than htlm.P for including hyperlinks)
            dcc.Markdown(
                """               
                De Kamer geeft op haar [website](https://www.dekamer.be/kvvcr/showpage.cfm?section=/qrva&language=nl&cfm=qrvaList.cfm) 
                een overzicht van de schriftelijke vragen die parlementsleden stelden, alsook de antwoorden hierop. 
                Onderstaande visualisaties laten toe om met deze gegevens te interageren.
                """,
                className="header-description",
                style={"color": "#FFFFFF"}
            )
        ],
        className="section-header",
        style={"background-color": "#222222"} # Set dark background for this section
    ),
    dcc.Tabs([
        dcc.Tab(
            label='Vragen',
            children=[
                dcc.Tabs(
                    children=[
                        dcc.Tab(
                            label='Schriftelijke vragen', 
                            children=federal_written_questions.layout),

                        ]
                    ),
                ],
            ),
        ]
	),
    
	# Footer with hyperlink to GitHub
	html.Footer(
		className='footer', # Assign a class name for styling
		children=[
			"De code en data voor deze toepassing is beschikbaar op ",
			html.A("GitHub", href="https://github.com/NT131/involvement_federal_parliament")
		]
	),
])

  
    
# Register callbacks for each visualization
federal_written_questions.register_callbacks(app)


# Define a callable application object for Gunicorn
application = app.server


# Run app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=5004)

