import numpy as np
import pandas
import os

def h2h_stats(match_data, ball_by_ball, batter, bowler):
    
    per_batsman = ball_by_ball.groupby(['batsman'])
    per_match = per_batsman.get_group((batter))
    per_match = per_match.groupby(['id'])
    
    match_ids = []
    dates = []
    venues = []
    tot_runs = [0]
    runs = [0]
    tot_bf = [0]
    bf = [0]
    tot_wickets = [0]
    wickets = [0]
    
    for name, group in per_match:
       if bowler in group['bowler'].unique():
            match_ids.append(name)
            dates.append(list(match_data[match_data['id']==name]['date'])[0])
            venues.append(list(match_data[match_data['id']==name]['venue'])[0])
            tot_runs.append(group['batsman_runs'].sum())
            runs.append(group[group['bowler']==bowler]['batsman_runs'].sum())
            tot_bf.append(group[group['extras_type']!='wides'][group['extras_type']!='noballs']['ball'].count())
            bf.append(group[group['bowler']==bowler][group['extras_type']!='wides'][group['extras_type']!='noballs']['ball'].count())
            tot_wickets.append(group[group['dismissal_kind']!='run out']['is_wicket'].sum())
            wickets.append(group[group['bowler']==bowler][group['dismissal_kind']!='run out']['is_wicket'].sum())
    
    tot_bf = np.array(tot_bf,dtype='float64')
    bf = np.array(bf,dtype='float64')
    tot_runs = np.array(tot_runs,dtype='float64')
    runs = np.array(runs, dtype='float64')
    tot_wickets = np.array(tot_wickets, dtype='float64')
    wickets = np.array(wickets, dtype='float64')
    
    return match_ids, dates, venues, runs, bf, wickets, tot_runs, tot_bf, tot_wickets
    

def most_recent(match_data, ball_by_ball, batter, batter_team, match_ids):
    match_data.set_index('id', inplace=True)
    match_data = match_data[(match_data.team1==batter_team) |  (match_data.team2==batter_team)]
    ball_by_ball = ball_by_ball.groupby(['batsman', 'id'])
    
    bf_wa_in = []
    rpb_wa_in = []
    wpb_wa_in = []
    
    for match_id in match_ids:
        idx = match_data.index.get_loc(match_id)
        recent_matches = match_data.iloc[idx-3:idx]
        
        recent_ids = list(recent_matches.index)
        recent_ids = recent_ids[::-1]
                
        rpb_wa = 0
        bf_wa = 0
        wpb_wa = 0
        
        for i in range(3):
            try:
                group = ball_by_ball.get_group((batter, recent_ids[i]))
                bf = group[group['extras_type']!='wides'][group['extras_type']!='noballs']['ball'].count()
                runs = group['batsman_runs'].sum()
                wicket = group['is_wicket'].sum()
                wpb = wicket/bf
                rpb = runs/bf
            except:
                wpb = wicket/bf
                rpb = runs/bf
            
            rpb_wa = rpb_wa + (0.4**(i))*rpb
            wpb_wa = wpb_wa + (0.4**(i))*wpb
            bf_wa = bf_wa + (0.4**(i))*bf
        
        bf_wa_in.append(bf_wa)
        rpb_wa_in.append(rpb_wa)
        wpb_wa_in.append(wpb_wa)
    
    bf_wa_in = np.array(bf_wa_in)
    rpb_wa_in = np.array(rpb_wa_in)
    wpb_wa_in = np.array(wpb_wa_in)
    
    return bf_wa_in, rpb_wa_in, wpb_wa_in