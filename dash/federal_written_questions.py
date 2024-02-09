# =============================================================================
# Setting up
# =============================================================================

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px
# import plotly.graph_objects as go

# import pickle

# from attendance_statistics import get_party

# =============================================================================
# Reading in relevant support data
# =============================================================================
# Load df with written questions and information about parties
federal_written_questions_df = pd.read_pickle('../data/federal_details_questions_df.pkl')

# Create a default value for amount_meetings, i.e. relevant meetings
federal_amount_questions = len(federal_written_questions_df)  # Set amount of all meetings as default, it will be updated in the callback

# # Load information about parties
# with open('../data/fracties.pkl', 'rb') as file:
#     fracties_dict = pickle.load(file)

# Extract respective party of each member
# Group by 'Parlementslid' and construct a dictionary with 'Parlementslid' as keys and 'Partij parlementslid' as values
parlementslid_dict = {parlementslid: partij for parlementslid, partij in zip(
    federal_written_questions_df['Parlementslid'], 
    federal_written_questions_df['Partij parlementslid']
    )}


# Dictionary mapping parties to colors
# # Use colours obtained from website: manual insertion or reading in dict
party_colors = {
    'Ecolo-Groen': '#83de62',
    'Onafhankelijk': '#787878',
    'Vooruit': '#FF2900',
    'Vlaams Belang': '#ffe500',
    'cd&v': '#f5822a',
    'N-VA': '#ffac12',
    'Open Vld': '#003d6d',
    'MR': "#002EFF", 
    'PVDA-PTB': '#AA050E',
    'Les Engagés': "#7ACFBA",
    'Défi': "#EE038C",
    'PS': "#FF0000",  
 }



minister_colors = {
    'Ecolo': '#88C40C',
    'Groen': '#83de62',
    'Vooruit': '#FF2900',
    'cd&v': '#f5822a',
    'Open Vld': '#003d6d',
    'MR': "#002EFF", 
    'PS': "#FF0000",  
 }


minister_2_party = {
    'François Bellot': 'MR', 
    'Wouter Beke': 'cd&v', 
    'Philippe De Backer': 'Open Vld',
    'Denis Ducarme': 'MR', 
    'Marie-Christine Marghem': 'MR', 
    'Maggie De Block': 'Open Vld',
    'Pieter De Crem': 'cd&v', 
    'Didier Reynders': 'MR', 
    'Alexander De Croo': 'Open Vld',
    'Koen Geens': 'cd&v', 
    'Charles Michel': 'MR', 
    'David Clarinval': 'MR',
    'Daniel Bacquelaine': 'MR', 
    'Nathalie Muylle': 'cd&v', 
    'Philippe Goffin': 'MR',
    'Sophie Wilmès': 'MR', 
    'Ludivine Dedonder': 'PS', 
    'Alexia Bertrand': 'Open Vld',
    'Annelies Verlinden': 'cd&v', 
    'Paul Van Tigchelt': 'Open Vld', 
    'Petra De Sutter': 'Groen',
    'Vincent Van Peteghem': 'cd&v', 
    'Georges Gilkinet': 'Ecolo', 
    'Pierre-Yves Dermagne': 'PS',
    'Zakia Khattabi': 'Ecolo', 
    'Frank Vandenbroucke': 'Vooruit', 
    'Sammy Mahdi': 'cd&v',
    'Marie-Colline Leroy': 'Ecolo', 
    'Mathieu Michel': 'MR', 
    'Tinne Van der Straeten': 'Groen',
    'Karine Lalieux': 'PS', 
    'Thomas Dermine': 'PS', 
    'Caroline Gennez': 'Vooruit',
    'Hadja Lahbib': 'MR', 
    'Nicole de Moor': 'cd&v',
    
    # Temp combinations
    'Alexander De Croo / Sophie Wilmès / Charles Michel': 'MR',
    'Sophie Wilmès / David Clarinval': 'MR', 
    'Vincent Van Quickenborne / Paul Van Tigchelt': 'Open Vld', 
    'Sarah Schlitz / Marie-Colline Leroy': 'Ecolo',
    'Eva De Bleeker / Alexia Bertrand': 'Open Vld',
}





# =============================================================================
# # Initiate dash app
# =============================================================================

# Comment out in integrated approach
# # Dash app
# app = dash.Dash(__name__,
#                 assets_folder='assets') # Relative path to the folder of css file))

# =============================================================================
# Dash layout
# =============================================================================

## Comment in integrated approach
# app.
layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H2("Schriftelijke vragen",
                        className="header-subsubtitle"),
                # html.P("Welke parlementsleden stelden het meeste schriftelijke vragen? En welke ministers kregen de meeste schriftelijke vragen te verwerken?", className="header-description"),
                html.P("Welke parlementsleden stelden het meeste schriftelijke vragen?", className="header-description"),
                html.P("En welke ministers kregen de meeste schriftelijke vragen te verwerken?", className="header-description"),
            ],
            className="section-header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        # html.H3(
                        #     "Selecteer de relevante periode.",
                        #     className="header-subsubtitle",
                        # ),
                        # html.Div(
                        #     children=[
                        #         html.Div(
                        #             children="Relevante periode", 
                        #             className="menu-title"
                        #         ),
                    				# # html.Div(
                    				# # 	# Display the most recent meeting date
                    				# # 	id='most-recent-date-per-party',
                    				# # 	children=f"Laatste update: {date_most_recent_meeting_per_party}",
                    				# # 	style={'font-style': 'italic'}
                    				# # ),
                                
                        #         dcc.DatePickerRange(
                        #             id="date-range-written-questions",
                        #             min_date_allowed=federal_written_questions_df["datum beantwoord"].min(),
                        #             max_date_allowed=federal_written_questions_df["datum beantwoord"].max(),
                        #             start_date=federal_written_questions_df["datum beantwoord"].min(),
                        #             end_date=federal_written_questions_df["datum beantwoord"].max(),
                        #             display_format='DD/MM/YYYY',  # Set the display format to 'dd/mm/yyyy' instead of default 'mm/dd/yyyy'
                        #         ),
                        #     ],
                        #     className="menu-element"
                        # ),
                        
                        # # Theme filter dropdown
                        # html.Div(
                        #     children=[
                        #         html.Div(
                        #             children="Selecteer thema", 
                        #             className="menu-title"
                        #         ),
                        #         dcc.Dropdown(
                        #             id="theme-filter",
                        #             options=[
                        #                 {'label': 'Alle', 'value': 'Alle'}
                        #                 ] + [
                        #                 # check if theme exists to avoid empty theme option
                        #                 {'label': theme, 'value': theme} for theme in federal_written_questions_df['thema'].unique() if theme
                        #                 ],
                        #             multi=True,
                        #             value='Alle',
                        #             placeholder="Selecteer thema's",
                        #         ),
                        #     ],
                        #     className="menu-element"
                        # ),
                        
                        # Minister dropdown
                        html.Div(
                            children=[
                                html.Div(
                                    children="Selecteer minister ", 
                                    className="menu-title"
                                ),
                                dcc.Dropdown(
                                    id="federal-minister-filter",
                                    options=[
                                        {'label': 'Alle', 'value': 'Alle'},
                                        ] + [
                                        {'label': minister, 'value': minister} for minister in federal_written_questions_df['Minister'].unique()
                                    ],
                                    multi=False,
                                    value='Alle',
                                    placeholder="Selecteer minister",
                                ),
                            ],
                            className="menu-element"
                        ),
                        
                    		# Display impact of data selection (i.e. how many written questions are taken into account)	
                    		html.Div(
                    			children=[
                    				html.Div(id='federal_amount_questions',
                    						 children=f"Deze selectie resulteert in {federal_amount_questions} schriftelijke vragen."),
                    			],
                    			className="menu-element"
                    		),
                    ], 
                    className="flex-container",
                ),
            ],
            className="wrapper",
        ),
    
                                            
        dcc.Tabs([
            dcc.Tab(
                label='Algemeen',
                children=[
                    html.Div([
                        dcc.Dropdown(
                            id='federal-x-axis-dropdown',
                            options=[
                                {'label': 'Parlementslid', 'value': 'Parlementslid'},
                                {'label': 'Partij', 'value': 'Partij parlementslid'},
                                {'label': 'Minister', 'value': 'Minister'},
                            ],
                            value='Parlementslid', # Default value
                            style={'width': '50%'}
                        ),
                        
                        dcc.Graph(id='federal_written_questions_graph'),
                        
                        ]),
                    ]),
            dcc.Tab(
                label='Specifieke parlementsleden',
                children=[
                    # New Div for Dropdown and DataTable
                    html.Div([
                        dcc.Dropdown(
                            id='federal-member-dropdown',
                            # Sort options alphabetically. Important to wrap dicts in list
                            options=[
                                {'label': member, 'value': member} for member in sorted(federal_written_questions_df['Parlementslid'].unique())
                            ],
                            multi=False,
                            value=None, # Set default value as None to avoid table being rendered automatically 
                            placeholder="Selecteer parlementslid",
                            style={'width': '50%'}
                        ),
                        html.Div(
                            id='federal-datatable-info', 
                            style={'margin-top': '10px', 'font-size': '14px'}
                        ),

                        dash_table.DataTable(
                            id='federal-written-questions-table',
                            columns=[
                                # {'name': 'Datum vraag gesteld', 'id': 'datum gesteld'},
                                {'name': 'Bevoegde minister', 'id': 'Minister'},
                                # use markdown represention to leverage clickable links of df
                                # {'name': 'Onderwerp', 'id': 'onderwerp_markdown', 'presentation': 'markdown'}, 
                                {'name': 'Onderwerp', 'id': 'Onderwerp'}, 
                            ],
                            page_size=25, #  Set the number of rows per page
                            style_table={'overflowX': 'auto'},
                            style_cell={
                                'fontFamily': 'Lato, sans-serif',
                                'fontSize': 14,
                                'textAlign': 'left',
                                'minWidth': '150px',
                                'whiteSpace': 'normal',
                                'textOverflow': 'ellipsis',
                            },
                            style_header={
                                'fontWeight': 'bold',
                                'fontSize': 16,
                            },
                            # Allow sorting of columns
                            sort_action='native',  # Enable sorting
                            sort_mode='single',  # Allow only single column sorting
                            # sort_by=[{'column_id': 'datum gesteld', 'direction': 'desc'}],  # Default sorting column and orientation
                            
                        ),
                    ], className='custom-datatable-container'),
                ]
            ),
            # dcc.Tab(
            #     label='Antwoordtermijn',
            #     children=[
            #         html.Div([
            #             dcc.Graph(
            #                 id='question-duration-bar-plot',
            #             ),
            #         ]),
            #     ]
            # )
        ]),
    ],
    # use CSS flexbox approach to easily structure graphs and titles
    style={"display": "flex", "flex-direction": "column"} 
)



# =============================================================================
# Callback
# =============================================================================
#Define function to filter data based on user selection
def filter_data(
        # start_date, end_date, theme_filter, 
                minister_filter, federal_written_questions_df):   
    # # Ensure correct date format
    # start_date = pd.to_datetime(start_date).date()
    # end_date = pd.to_datetime(end_date).date()
    
    
    # # Filter DataFrame with all questions further based on the date range
    # written_questions_filtered_df = federal_written_questions_df[
    #      (federal_written_questions_df['datum beantwoord'] >= start_date) &
    #      (federal_written_questions_df['datum beantwoord'] <= end_date)
    #  ]
    
    # # Filter DataFrame based on the selected theme
    # if theme_filter is not None and theme_filter != 'Alle':
    #     written_questions_filtered_df = written_questions_filtered_df[
    #         written_questions_filtered_df['thema'].isin(theme_filter)
    #     ]
    
    ####### TEMPORARY VARIABLE ####################"
    written_questions_filtered_df = federal_written_questions_df
    
    # Exclude entries with the same minister value
    if minister_filter is not None and minister_filter != 'Alle':
        written_questions_filtered_df = written_questions_filtered_df[
            written_questions_filtered_df['Minister'] == minister_filter
        ]
        
    return written_questions_filtered_df


def update_chart(selected_axis, federal_written_questions_df_input):
  
    if selected_axis == 'Parlementslid':      
        # Create a DataFrame with member, count, and party columns
        grouped_data = federal_written_questions_df_input['Parlementslid'].value_counts().reset_index()
        grouped_data.columns = ['Parlementslid', 'Aantal vragen']
        
        # print(len(grouped_data))

        # # Apply function to create a new column 'Partij' based on fracties_dict
        # grouped_data['Partij parlementslid'] = grouped_data.apply(get_party, axis=1,
        #                                             facties_dict_input=fracties_dict)
        
        # Map values from the dictionary to a new column 'Partij parlementslid'
        grouped_data['Partij parlementslid'] = grouped_data['Parlementslid'].map(parlementslid_dict)


        fig = px.bar(grouped_data,
                      # x='Parlementslid',
                      # y='Aantal vragen',
                      x='Aantal vragen',
                      y='Parlementslid',
                      color='Partij parlementslid',
                      color_discrete_map=party_colors,
                      labels={'x': 'Parlementslid', 'y': 'Aantal vragen'},
                      title='Vragen per parlementslid')
        
        
        # Update y-axis to reflect the sorted order
        fig.update_yaxes(categoryorder='total ascending')
        
        # Modify height of entire graph (static) to ensure all entries are properly shown 
        fig.update_layout(
            height= len(grouped_data) * 20,  # Set the height of the figure based on amount of members filtered
            bargap=0.3,  # Set the gap between bars
        )
        
        # Adjust the space between y-axis labels and the axis
        fig.update_layout(
            yaxis=dict(
                tickmode='linear',  # Set tickmode to 'linear'
                dtick=1  # Set dtick to 1 to show every value on the y-axis
            )
        )
        
        # # Adjust the space between y-axis labels and the axis
        # fig.update_layout(
        #     yaxis=dict(
        #         tickmode='array',  # Set tickmode to 'array'
        #         tickvals=fig.data[0]['y'],  # Use the actual y values as tickvals
        #         tick0=-0.8,  # Adjust the tick0 to control the space
        #         dtick=1  # Set dtick to control the interval between ticks
        #     )
        # )


    elif selected_axis == 'Minister':
        grouped_data = federal_written_questions_df_input['Minister'].value_counts().reset_index()
        grouped_data.columns = ['Minister', 'Aantal vragen']
        grouped_data['Partij minister'] = grouped_data['Minister'].map(minister_2_party)
        fig = px.bar(grouped_data,
                     x='Minister',
                     y='Aantal vragen',
                     color='Partij minister',
                     color_discrete_map=minister_colors,
                     labels={'x': 'Minister', 'y': 'Aantal vragen'},
                     title='Vragen aan ministers')
        # Update x-axis to reflect the sorted order
        fig.update_xaxes(categoryorder='total descending')
        
        # Reset height of entire graph (enlarged for 'vraagsteller)
        fig.update_layout(height=500)
        
    elif selected_axis == 'Partij parlementslid':
        grouped_data = federal_written_questions_df_input['Partij parlementslid'].value_counts().reset_index()
        grouped_data.columns = ['Partij parlementslid', 'Aantal vragen']
        fig = px.bar(grouped_data,
                     x='Partij parlementslid',
                     y='Aantal vragen',
                     color='Partij parlementslid',
                     color_discrete_map=party_colors,
                     labels={'x': 'Partij parlementslid', 'y': 'Aantal vragen'},
                     title='Vragen gesteld per partij')
        
        # Reset height of entire graph (enlarged for 'vraagsteller)
        fig.update_layout(height=500)
        
    # elif selected_axis == 'thema':
    #     grouped_data = federal_written_questions_df_input['thema'].value_counts().reset_index()
    #     grouped_data.columns = ['Thema', 'Aantal vragen']
    #     fig = px.bar(grouped_data,
    #                  x='Aantal vragen',
    #                  y='Thema',
    #                  # color='Thema',  # You can use 'color_discrete_map' if needed
    #                  labels={'x': 'Thema', 'y': 'Aantal vragen'},
    #                  title='Vragen per thema')
        
        # # Modify height of entire graph (static) to ensure all entries are properly shown 
        # fig.update_layout(
        #     height=600,  # Set the height of the figure
        #     bargap=0.2,  # Set the gap between bars
        #     )
        # # Update y-axis to reflect the sorted order
        # fig.update_yaxes(categoryorder='total ascending')
  
    else:
        fig = px.bar()

    return fig



# def answer_term_bar_chart(federal_written_questions_df_input, num_bins=20):
#     # Ensure 'termijn antwoord (werkdagen)' is converted to numeric
#     federal_written_questions_df_input['termijn antwoord (werkdagen)'] = pd.to_numeric(federal_written_questions_df_input['termijn antwoord (werkdagen)'], errors='coerce')

#     # Create bins using pd.cut
#     federal_written_questions_df_input['termijn bins'] = pd.cut(federal_written_questions_df_input['termijn antwoord (werkdagen)'], bins=num_bins)

#     # Group by the bins and count the number of questions in each bin
#     bin_counts = federal_written_questions_df_input.groupby('termijn bins').size().reset_index(name='Number of Questions')

#     # Create the bar chart using px.bar
#     fig = px.bar(
#         bin_counts,
#         x='termijn bins',
#         y='Number of Questions',
#         labels={'termijn bins': 'Time to Answer (Workdays)', 'Number of Questions': 'Number of Questions'},
#         title='Distribution of Time to Answer Questions',
#         color_discrete_sequence=['skyblue'],  # Bar color
#     )

#     # # Customize layout
#     # fig.update_layout(
#     #     showlegend=False,  # Hide legend for a single bar
#     # )

#     return fig



#Create function to load app in integrated appraoch
def register_callbacks(app):
    @app.callback(
        [Output('federal_amount_questions', 'children'),
         Output('federal_written_questions_graph', 'figure'),
         # Output('question-duration-bar-plot', 'figure'),
         Output('federal-written-questions-table', 'data'),
         Output('federal-datatable-info', 'children')],
        [
         # Input('date-range-written-questions', 'start_date'),
         # Input('date-range-written-questions', 'end_date'),
         # Input("theme-filter", "value"),
         Input("federal-minister-filter", "value"),
         Input('federal-x-axis-dropdown', 'value'),
         Input('federal-member-dropdown', 'value')
         ]
        )
    def update_display(
            # start_date, end_date, theme_filter, 
            minister_filter, 
                       selected_axis, selected_member):
        # Filter data based on user input
        written_questions_filtered_df = filter_data(
            # start_date, end_date,
            #                                         theme_filter, 
                                                    minister_filter,
                                                    federal_written_questions_df)
        
        # Create graph using user selected axis and filtered df
        written_questions_graph = update_chart(selected_axis, 
                                               written_questions_filtered_df)
          
        # # Create graph for answering term
        # duration_answer_graph = answer_term_bar_chart(written_questions_filtered_df)
        
        # Check if the selected axis is 'vraagsteller' to update DataTable
        if selected_axis == 'Parlementslid' and selected_member:
            # Filter data for the selected member
            selected_member_data = written_questions_filtered_df[written_questions_filtered_df['Parlementslid'] == selected_member][['Minister', 'Onderwerp']]

        else:
            # If the selected axis is not 'vraagsteller', provide an empty DataFrame
            selected_member_data = pd.DataFrame()
         
        return [f"Deze selectie resulteert in {len(written_questions_filtered_df)} relevante schriftelijke vragen.", # Use text formatting to allow easier build of layout
                written_questions_graph,
                # duration_answer_graph,
                selected_member_data.to_dict('records'),
                f"Dit parlementslid stelde {len(selected_member_data)} vragen."]


# =============================================================================
# Run dash app
# =============================================================================
# # Comment out in integrated account
# if __name__ == '__main__':
#     app.run_server(debug=True)
