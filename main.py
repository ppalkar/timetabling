import pandas as pd
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


def make_gantt_chart(output_path : str, timeLength : int) : 
    # Step 1: Load the CSV data
    df = pd.read_csv(output_path)

    # Step 2: Create a list of tasks for the Gantt chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # Step 3: Iterate over each row to add it to the Gantt chart
    for i, row in df.iterrows():
        team = row["TEAMS"]
        start_time = row["TIMESLOTS"]
        if row["x"] == 1 : 
            ax.barh(team, timeLength, left=(start_time-1)*timeLength)

    # Step 4: Customize the chart
    ax.set_xlabel("TIMESLOTS")
    ax.set_ylabel("TEAMS")
    ax.set_title("Timetable for Thermal Presentations")

    # Set yticks to intervals of 1
    ax.set_yticks(df["TEAMS"].unique())
    
    # Set xticks to intervals of 15 (each interval represents one timeslot of 15 minutes)
    ax.set_xticks(range(0, df["TIMESLOTS"].max() * timeLength + 1, timeLength))

    # TODO : 1. add related prof name on blocks of each team

    plt.grid(True)

    # Show plot
    plt.show()


x_df = get_pd_df(x_var)
x_df = rename_columns(x_df)

# Saving new csv file
x_df.to_csv(output_path, index = False)

# making gantt chart assuming time interval is 15min
make_gantt_chart(output_path, 15)
