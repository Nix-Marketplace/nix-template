"""
Template for the most basic Nix tool. Runs a function and that's it.
Key components include:
    - main: entrypoint for tool. Contains interface built with NixGUI (which extends NiceGUI). Purpose is to configure core function arguments
    - core function: performs the main functionality of the tool. Should not contain any UI elements
"""
# Import statements
from nixgui import ui

# ----- ENVIRONMENT VARIABLES ----- #

# ----- USER INTERFACE ----- #
"""
Define a function main(), annotated with @ui.page("/") to create the main page of the tool.
This function should contain the UI elements that will be used to configure the core function.
An inner function then handles tool initiation by the user; this involves invoking the core function with the appropriate arguments.
"""
@ui.page("/")
def main():

    # Button callback function that initiates the core function
    def on_click():
        ui.label(core_function())

    ui.label("Hello, world!")
    ui.button("Click me!", on_click=lambda: on_click())

# ----- SCRIPT ----- #
"""
If you have an existing script, paste it below.
"""
def core_function():
    return "I'm functioning!"

# Main guard to be used for testing. 
if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
