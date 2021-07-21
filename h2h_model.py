import calc_stats
import numpy as np
import pandas
from sklearn.linear_model import LinearRegression


def train(inputs_dict, outputs_dict):
    
    #Stats representing recent form
    rpb_wa = inputs_dict['Runs per Ball Weighted Avg']
    bf_wa = inputs_dict['Balls Faced Weighted Avg']
    wpb_wa = inputs_dict['Wickets per Ball Weighted Avg']
    
    #Sats representing previous H2H matchups
    rpb_h2h = inputs_dict['Runs per Ball H2H']
    bf_h2h = inputs_dict['Balls Faced H2H']
    wpb_h2h = inputs_dict['Wickets per Ball H2H']
    
    #Home or Away
    #home_or_away = inputs_dict['Home or Away']
    
    rpb = outputs_dict['Runs per Ball']
    bf = outputs_dict['Balls Faced']
    wpb = outputs_dict['Wickets per Ball']
    
    X1 = np.concatenate((bf_wa, bf_h2h), axis=1)
    y1 = bf
    reg1 = LinearRegression().fit(X1,y1)
    
    return reg1

def test(inputs_dict, reg1, outs):

    #Stats representing recent form
    rpb_wa = inputs_dict['Runs per Ball Weighted Avg']
    bf_wa = inputs_dict['Balls Faced Weighted Avg']
    wpb_wa = inputs_dict['Wickets per Ball Weighted Avg']
    
    #Sats representing previous H2H matchups
    rpb_h2h = inputs_dict['Runs per Ball H2H']
    bf_h2h = inputs_dict['Balls Faced H2H']
    wpb_h2h = inputs_dict['Wickets per Ball H2H']
    
    #Home or Away
    home_or_away = inputs_dict['Home or Away']
    X = np.concatenate((bf_wa, bf_h2h), axis=1)
    pred = reg1.predict(X)
    
    outs = outs*24
    pred = pred*24
    
    error = np.linalg.norm(outs-pred, ord=1)/pred.shape[0]    
    return error

def model(match_data, ball_by_ball, batter, bowler, batter_team, home):
    match_ids, dates, venues, runs, bf, wickets, _, _, _ = calc_stats.h2h_stats(match_data, ball_by_ball, batter, bowler)
    bf_wa_in, rpb_wa_in, wpb_wa_in = calc_stats.most_recent(match_data, ball_by_ball, batter, batter_team, match_ids)

    home_or_away = np.array([1 if x==home else 0 for x in venues], dtype='float64')

    runs_sum = runs.cumsum()[:-1]
    bf_sum = bf.cumsum()[:-1]
    wickets_sum = wickets.cumsum()[:-1]

    rpb_h2h = np.nan_to_num(runs_sum/bf_sum)
    bf_h2h = bf_sum/24
    bf_h2h = bf_h2h/np.arange(0, bf_h2h.shape[0])
    bf_h2h = np.nan_to_num(bf_h2h)
    wpb_h2h = np.nan_to_num(wickets_sum/bf_sum)

    bf_h2h = bf_h2h.reshape((bf_h2h.shape[0],1))
    rpb_h2h = rpb_h2h.reshape((rpb_h2h.shape[0],1))
    wpb_h2h = wpb_h2h.reshape((wpb_h2h.shape[0],1))

    home_or_away = home_or_away.reshape((home_or_away.shape[0],1))

    bf_wa_in = bf_wa_in/120
    bf_wa_in = bf_wa_in.reshape((bf_wa_in.shape[0],1))
    rpb_wa_in = rpb_wa_in.reshape((rpb_wa_in.shape[0],1))
    wpb_wa_in = wpb_wa_in.reshape((wpb_wa_in.shape[0],1))

    bf = bf[1:]
    rpb = runs[1:]/bf
    wpb = wickets[1:]/bf
    bf = bf/24

    bf = bf.reshape((bf.shape[0],1))
    rpb = rpb.reshape((rpb.shape[0],1))
    wpb = wpb.reshape((wpb.shape[0],1))

    inputs_dict = {}

    inputs_dict['Runs per Ball Weighted Avg'] = rpb_wa_in[:-2]
    inputs_dict['Balls Faced Weighted Avg'] = bf_wa_in[:-2]
    inputs_dict['Wickets per Ball Weighted Avg'] = wpb_wa_in[:-2]
    inputs_dict['Runs per Ball H2H'] = rpb_h2h[:-2]
    inputs_dict['Balls Faced H2H'] = bf_h2h[:-2]
    inputs_dict['Wickets per Ball H2H'] = wpb_h2h[:-2]
    inputs_dict['Home or Away'] = home_or_away[:-2]

    outputs_dict = {}

    outputs_dict['Runs per Ball'] = rpb[:-2]
    outputs_dict['Balls Faced'] = bf[:-2]
    outputs_dict['Wickets per Ball'] = wpb[:-2]

    model = train(inputs_dict, outputs_dict)

    inputs_dict_test = {}

    inputs_dict_test['Runs per Ball Weighted Avg'] = rpb_wa_in[-2:]
    inputs_dict_test['Balls Faced Weighted Avg'] = bf_wa_in[-2:]
    inputs_dict_test['Wickets per Ball Weighted Avg'] = wpb_wa_in[-2:]
    inputs_dict_test['Runs per Ball H2H'] = rpb_h2h[-2:]
    inputs_dict_test['Balls Faced H2H'] = bf_h2h[-2:]
    inputs_dict_test['Wickets per Ball H2H'] = wpb_h2h[-2:]
    inputs_dict_test['Home or Away'] = home_or_away[-2:]

    error = test(inputs_dict_test, model, bf[-2:])

    print(error)