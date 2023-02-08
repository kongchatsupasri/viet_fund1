#%%
import streamlit as st
import pandas as pd
# import streamlit_nested_layout
import plotly.graph_objects as go
import plotly.express as px
#%%
st.set_page_config(layout="wide")
st.header('🇻🇳 vietnam 🇻🇳')
#%% sidebar
nav_df = pd.read_csv('./nav_df.csv')
nav_df['date'] = pd.to_datetime(nav_df['date'], format = '%Y-%m-%d')

indices_df = pd.read_csv('./index_df.csv')
indices_df['date'] = pd.to_datetime(indices_df['date'], format = '%Y-%m-%d')
indices_df['value'] = indices_df['value'].astype(float)

with st.sidebar:
    year_option = st.select_slider(
        'select year',
        options=[str(i) for i in range(2020, 2024)])
    st.write("--")

nav_df = nav_df[nav_df['date'].dt.year == int(year_option)].reset_index(drop = True)
indices_df = indices_df[indices_df['date'].dt.year == int(year_option)].reset_index(drop = True)

fund_performance_df = pd.DataFrame()
for short_code in nav_df.short_code.unique():
    df1 = nav_df[nav_df['short_code'] == short_code].sort_values(by = ['date'], ascending = True).reset_index(drop = True)
    type_ = df1['type'][0]
    df1['pct_change'] = df1['value'].pct_change()
    ret = (df1['value'][df1.shape[0] - 1] / df1['value'][0]) - 1
    stdev = df1['pct_change'].std()
    sharpe = ret / stdev
    fund_performance_df = pd.concat([fund_performance_df, 
                                pd.DataFrame([[type_, short_code, ret, stdev, sharpe]], columns = ['type', 'short_code', 'yearly return', 'standard deviation', 'sharpe ratio'])],
                                axis = 0).reset_index(drop = True)
                                
# st.dataframe(fund_performance_df.head())

index_performance_df = pd.DataFrame()
for index_ in indices_df['index'].unique():
    df1 = indices_df[indices_df['index'] == index_].sort_values(by = ['date'], ascending = True).reset_index(drop = True)
    df1['pct_change'] = df1['value'].pct_change()
    ret = (df1['value'][df1.shape[0] - 1] / df1['value'][0]) - 1
    stdev = df1['pct_change'].std()
    sharpe = ret / stdev
    index_performance_df = pd.concat([index_performance_df, 
                                pd.DataFrame([[index_, ret, stdev, sharpe]], columns = ['index', 'yearly return', 'standard deviation', 'sharpe ratio'])],
                                axis = 0).reset_index(drop = True)
# st.dataframe(index_performance_df.head())
# st.write(index_performance_df['index'])
with st.sidebar:
    fund_option = st.multiselect(
        'select fund for comparison (default selection: top 5 yearly return)',
        fund_performance_df['short_code'],
        fund_performance_df['short_code'][:5])

#%%

ind1, ind2, ind3, ind4 = st.columns(4)
        
with ind1:
    st.metric(label="SET Index", 
                value = indices_df[indices_df['index'] == 'SET Index']['value'].tolist()[-1], 
                delta="{0:.1%}".format(index_performance_df[index_performance_df['index'] == 'SET Index']['yearly return'].tolist()[0]),
                label_visibility = 'visible')

with ind2:
    st.metric(label="VN Index", 
                value = indices_df[indices_df['index'] == 'VN Index']['value'].tolist()[-1], 
                delta="{0:.1%}".format(index_performance_df[index_performance_df['index'] == 'VN Index']['yearly return'].tolist()[0]),
                label_visibility = 'visible')

with ind3:
    st.metric(label="SET 100", 
                value = indices_df[indices_df['index'] == 'SET 100']['value'].tolist()[-1], 
                delta="{0:.1%}".format(index_performance_df[index_performance_df['index'] == 'SET 100']['yearly return'].tolist()[0]),
                label_visibility = 'visible')

with ind4:
    st.metric(label="VN 100", 
                value = indices_df[indices_df['index'] == 'VN100']['value'].tolist()[-1], 
                delta="{0:.1%}".format(index_performance_df[index_performance_df['index'] == 'VN100']['yearly return'].tolist()[0]),
                label_visibility = 'visible')


index_options = ['SET Index', 'VN Index']
main_col1, main_col2, main_col3 = st.columns((7, 1, 7))



with main_col1:
    
    st.markdown("<h3 style='text-align: center;'>Chart name</h3>", unsafe_allow_html=True)
    scatter_fig = go.Figure()
    for index in index_options:
        index_df = indices_df[indices_df['index'] == index].reset_index(drop = True)
        # index_df['date'] = pd.to_datetime(index_df['date'], format = '%m/%d/%Y')
        index_df = index_df.sort_values(by = ['date'], ascending = True)

        if index_df['value'].dtype == 'float64':
            pass
        else:
            index_df['value'] = index_df['value'].map(lambda x: (''.join(x.split(',')))).astype(float)
        index_df['pct_chg'] = index_df['value'].pct_change().fillna(0)
        index_df['cum_ret'] = index_df['pct_chg'].cumsum()

        scatter_fig.add_trace(go.Scatter(x = index_df.date,
                                y = index_df.cum_ret,
                                mode = 'lines',
                                line = dict(width = 3, dash = 'dot'),
                                name = index,
                                hovertemplate = index + ': %{y:.2%}<extra></extra>'))

    for short_code in fund_option:
        nav_df1 = nav_df[nav_df['short_code'] == short_code].reset_index(drop = True)
        nav_df1['Index'] = (nav_df1['value'] / nav_df1.loc[0, 'value']) -1
        scatter_fig.add_trace(go.Scatter(x = nav_df1.date,
                                y = nav_df1.Index,
                                mode = 'lines',
                                line = dict(width = 3),
                                name = nav_df1.loc[0, 'short_code'],
                                hovertemplate = short_code + ': %{y:.2%}<extra></extra>'))
    scatter_fig.layout.yaxis.tickformat = ',.0%'
    scatter_fig.update_layout(
                        # title = 'chart title', 
                        # yaxis_title = 'y axis title',
                        # legend_title = 'legend title',
                        autosize=False,
                        # width=450,
                        # height=700,
                        legend=dict(
                            yanchor="auto",
                            y=0.99,
                            xanchor="left",
                            x=0.01
                        ),
                        margin=dict(l=0, t = 0, r=0, b=0)
                        )

    scatter_fig.update_layout(hovermode="x unified")
    scatter_fig.update_xaxes(showgrid = False)
    scatter_fig.update_yaxes(showgrid = True,  linewidth=0.5)
    st.plotly_chart(scatter_fig, use_container_width=True)

with main_col3:
    
    st.markdown("<h3 style='text-align: center;'>Chart name</h3>", unsafe_allow_html=True)
    dff = px.data.wind()
    fig = px.line_polar(dff, r="frequency", theta="direction", color="strength", line_close=True,
                        color_discrete_sequence=px.colors.sequential.Plasma_r,
                        template="plotly_dark",)
    # fig.show()
    st.plotly_chart(fig, use_container_width=True)

st.markdown('#')
st.markdown("<h3 style='text-align: center;'>table name</h3>", unsafe_allow_html=True)
bttm_col1, bttm_col2, bttm_col3, bttm_col4 = st.columns([1, 1, 4, 1])
with bttm_col2:
    st.markdown('#')
    top_performance_option = option = st.radio(
                                'top 5 performers --> select criteria',
                                ('yearly return', 'standard deviation', 'sharpe ratio'),
                                horizontal = False)

with bttm_col3:
    if top_performance_option in ['yearly return', 'sharpe ratio']:
        fund_performance_df = fund_performance_df.sort_values(by = [top_performance_option], ascending = False).reset_index(drop = True)
    else:
        fund_performance_df = fund_performance_df.sort_values(by = [top_performance_option], ascending = True).reset_index(drop = True)
    fund_performance_df1 = fund_performance_df.iloc[:5, 1:]
    fund_performance_df1 = fund_performance_df1.style.format({
                                                    'yearly return': '{:,.2f}%'.format,
                                                    'standard deviation': '{:,.2f}'.format,
                                                    'sharpe ratio': '{:,.2f}'.format,
                                                })


    # st.subheader(f'sorted by {top_performance_option}')
    st.dataframe(fund_performance_df1, use_container_width = True)

st.info('data source: set, siamchart, finnomena, investing.com', icon="ℹ️")
