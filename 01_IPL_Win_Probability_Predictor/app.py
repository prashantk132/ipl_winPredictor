import streamlit as st
import pickle
import pandas as pd

teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Punjab Kings',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals',
 'Gujarat Titans',
 'Lucknow Super Giants']

cities = ['Ahmedabad', 'Kolkata', 'Mumbai', 'Navi Mumbai', 'Pune', 'Dubai',
       'Sharjah', 'Abu Dhabi', 'Delhi', 'Chennai', 'Hyderabad',
       'Visakhapatnam', 'Chandigarh', 'Bengaluru', 'Jaipur', 'Indore',
       'Bangalore', 'Raipur', 'Ranchi', 'Cuttack', 'Dharamsala', 'Nagpur',
       'Johannesburg', 'Centurion', 'Durban', 'Bloemfontein',
       'Port Elizabeth', 'Kimberley', 'East London', 'Cape Town']

pipe = pickle.load(open('pipe.pkl','rb'))
st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    BattingTeam = st.selectbox('Select the Batting Team',sorted(teams))
with col2:
    BowlingTeam = st.selectbox('Select the Bowling Team',sorted(teams))

selected_city = st.selectbox('Select Host City',sorted(cities))

target = st.number_input('Target')

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Score')
with col4:
    wickets = st.number_input('Wickets out')
with col5:
    overs = st.number_input('Overs completed')

balls_completed = (int(overs))*6 + (overs-(int(overs)))*10
overs_completed = balls_completed/6

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (balls_completed)
    wickets_left = 10 - wickets
    crr = score/overs_completed
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'BattingTeam':[BattingTeam],'BowlingTeam':[BowlingTeam],'City':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets_left':[wickets_left],'total_run_x':[target-1],'crr':[crr],'rrr':[rrr]})
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(BattingTeam + ": " + str(round(win*100)) + "%")
    st.header(BowlingTeam + ": " + str(round(loss*100)) + "%")
    st.table(input_df)