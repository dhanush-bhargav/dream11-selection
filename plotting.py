import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

def h2h_plot(batter, bowler, dates, runs, bf, wickets, home_or_away):
    fig, subplt = plt.subplots(2)
    fig.suptitle(batter + " vs " + bowler)

    barlist1 = subplt[0].bar(dates, runs, width=0.3)
    subplt[0].set_xlabel('Date(yyyy-mm-dd)')
    subplt[0].set_ylabel('Runs Scored')
    subplt[0].set_title('Runs scored in each innings')

    strk_rt = 100*runs/bf
    barlist2 = subplt[1].bar(dates, strk_rt, width=0.3)
    subplt[1].set_xlabel('Date(yyyy-mm-dd)')
    subplt[1].set_ylabel('Strike Rate')
    subplt[1].set_title('Innings Strike Rate')

    wicket = [float('nan') if x==0 else x for x in wickets]
    subplt[0].plot(dates, wicket*runs, marker='*', markersize=10, linestyle="", color='black')
    subplt[1].plot(dates, wicket*strk_rt, marker='*', markersize=10, linestyle="", color='black')

    for i in range(0, len(barlist1)):
            
        if home_or_away[i]==1:
            barlist1[i].set_color('r')
            barlist2[i].set_color('r')
        else:
            barlist1[i].set_color('b')
            barlist2[i].set_color('b')

    red_patch = mpatches.Patch(color="red", label="Home")
    blue_patch = mpatches.Patch(color="blue", label="Away/Neutral")
    star_patch = mlines.Line2D([], [], color="black", marker='*', markersize=10, linestyle="", label="Wicket")

    subplt[0].legend(handles=[red_patch, blue_patch, star_patch])
    subplt[1].legend(handles=[red_patch, blue_patch, star_patch])
    plt.show()