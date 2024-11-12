import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from amplpy import AMPL, add_to_path, variable

# Initiailize the AMPL enviorment
add_to_path("/Users/Rehan/Downloads/AMPL")
ampl = AMPL()

ampl.setOption('solver', '/Users/Rehan/Downloads/ampl_macos64/gurobi')
ampl.setOption('gurobi_options', 'timelimit=60')

# path to input and optput files.
model_path = 'initial_model.mod'
data_path = 'initial_model.dat'
output_path = "output.csv"

# reading model and data
ampl.read(model_path)
ampl.readData(data_path)


# Run the ampl model
ampl.solve()

# Taking x variable.
x_var = ampl.get_variable('x')

# function to convert variable to pd.DataFrame
def get_pd_df(x_var : variable.Variable) -> pd.DataFrame : 
    x_ampldf = x_var.get_values()
    
    headers = x_ampldf._get_headers()
    columms = {
        header: x_ampldf._get_column(header).to_list() for header in headers
    }
    x_df = pd.DataFrame(columms)
    return x_df

# function to rename columns of obtained pandas dataframe
def rename_columns(x_df : pd.DataFrame) -> pd.DataFrame :
    x_df.columns = ['TEAMS', 'TIMESLOTS', 'x']
    return x_df


def make_gantt_chart(output_path : str, timeLength : int, teams_per_prof : dict) : 
    # Step 1: Load the CSV data
    df = pd.read_csv(output_path)

    def give_colors() -> dict : 
        professors = list(teams_per_prof.keys())
        num_professors = len(professors)
        cmap = plt.get_cmap("tab20")  # "tab20" provides up to 20 distinct colors

        colors = [cmap(i % 20) for i in range(num_professors)]
        np.random.seed(42)  # Fix random seed for consistency
        np.random.shuffle(colors)
        color_map = {prof: colors[i] for i, prof in enumerate(professors)}
        return color_map
    
    color_map = give_colors()

    # Step 2: Create a list of tasks for the Gantt chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # Step 3: Iterate over each row to add it to the Gantt chart
    for prof, teams in teams_per_prof.items():
        prof_color = color_map[prof]  # Assign unique color for each professor
        for team in teams:
            team_slot = df[(df['TEAMS'] == team) & (df['x'] == 1)] # This will be a row for our case
            
            # check for team_slot has only one row! # TODO:
            if len(team_slot) != 1 :
                raise ValueError(f"Expected exactly one row for team :  {team} in TIMESLOTS with 'x' == 1, but \
                                 found {len(team_slot)} rows.")

            for _, row in team_slot.iterrows():
                start_time = row['TIMESLOTS']
                ax.barh(prof, timeLength, left=(start_time - 1) * timeLength, color = prof_color)

    # Step 4: Customize the chart
    ax.set_xlabel("TIMESLOTS")
    ax.set_ylabel("PROFESSORS")
    ax.set_title("Gantt Chart for Thermal Presentations")

    # Set yticks to intervals of 1
    ax.set_yticks(range(len(teams_per_prof)))
    ax.set_yticklabels(list(teams_per_prof.keys()))    

    # Set xticks to intervals of 15 (each interval represents one timeslot of 15 minutes)
    ax.set_xticks(range(0, df["TIMESLOTS"].max() * timeLength + 1, timeLength))

    plt.grid(True)

    # Show plot
    plt.show()


x_df = get_pd_df(x_var)
x_df = rename_columns(x_df)

# Saving new csv file
x_df.to_csv(output_path, index = False)

teams_per_prof = {
    'p1': [3, 8, 16],
    'p2': [3, 5, 16, 18, 21],
    'p3': [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27],
    'p4': [3, 15, 19, 20],
    'p5': [12, 14, 20],
    'p6': [15, 19],
    'p7': [8, 9],
    'p8': [9, 17, 18, 22, 24, 27],
    'p9': [4, 10, 17, 24],
    'p10': [10, 22],
    'p11': [25],
    'p12': [2, 25, 26, 27],
    'p13': [26],
    'p14': [4, 7],
    'p15': [7, 12],
    'p16': [5, 11],
    'p17': [11],
    'p19': [2, 21],
    'p20': [6],
    'p21': [6],
    'p22': [14]
}

# making gantt chart assuming time interval is 15min
make_gantt_chart(output_path, 15, teams_per_prof)
