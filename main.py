import pandas as pd
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
x_df = get_pd_df(x_var)
x_df = rename_columns(x_df)

# Saving new csv file
x_df.to_csv(output_path, index = False)
