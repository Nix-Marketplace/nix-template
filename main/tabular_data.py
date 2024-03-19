"""
Template for a common Nix tool: generating tabular data.
Key components include:
    - main: entrypoint for tool. Contains interface built with NixGUI (which extends NiceGUI). Purpose is to configure core function arguments
    - core function: performs the main functionality of the tool. Should not contain any UI elements
    - on_click: inner function that handles the initiation of the core function. This is done asynchronously to prevent blocking the UI
"""
# Import statements
from nixgui import ui, run
import pandas as pd

# ----- ENVIRONMENT VARIABLES ----- #

TABLE_COLUMNS = ["Column 1", "Column 2", "Column 3"] # Replace with columns relevant to the data you are working with

# ----- USER INTERFACE ----- #
"""
Define a function main(), annotated with @ui.page("/") to create the main page of the tool.
This function should contain the UI elements that will be used to configure the core function.
An inner function then handles tool initiation by the user; this involves invoking the core function with the appropriate arguments.
"""
@ui.page("/")
def main():

    # Initial UI, displayed to the user on start
    ui.label("Hello, world!")
    inputs = ui.textarea(label="Enter some text, separated by commas")
    ui.button("Click me!", on_click=lambda: on_click())
    ui.separator()

    # Button callback function that initiates the core function. 
    # It's async as we want to await a response from the core function without blocking the UI
    async def on_click():
        # Display a loading spinner while the core function is running to keep user informed
        loading_row = ui.row()
        with loading_row:
            ui.spinner()
            ui.label("Getting data...")
        
        # Instantiate dataframe and use it to build a table in the UI
        df = pd.DataFrame(columns=TABLE_COLUMNS)
        results_table = ui.table.from_pandas(df)

        string_list = inputs.value.split(",") # Split the input string into a list of strings
        for string in string_list:
            try:
                # Assuming the core function takes a long time to run, we use run.io_bound to run it asynchronously
                response = await run.io_bound(core_function, string)
            except Exception as e:
                # Provide an informative message to the user if an error occurs
                ui.notify(f"Error getting data from {string}: {e}", position="top-right", type="warning")
                continue
            
            # Build the output table row by row
            df = pd.concat([df, pd.DataFrame([response])], ignore_index=True)
            results_table.add_rows(response)

        # Remove the loading spinner once the core function has finished running
        loading_row.delete()
        
        # Allow user to download the results
        ui.button("Download CSV", 
            on_click=lambda: ui.download(bytes(df.to_csv(lineterminator='\r\n', index=False), encoding='utf-8'), filename="output.csv")
        )

# ----- SCRIPT ----- #
"""
If you have an existing script, paste it below.
The function should take in any inputs required and return a structure that can be added to a dataframe.
"""
def core_function(input: str):
    return ["I'm functioning!", input, "<- that's the input!"]

# Main guard to be used for testing. 
if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
