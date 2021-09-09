# GamedayExport

Gameday Export is a Python script which downloads MLB game data for a specified date, and exports the data via a CSV file. 
The CSV file will be stored in the same directory as the GamedayExport.py file and will be named for the date which you requested. 

Example: 2016-08-04_GamedayData.csv

## Installation

In order to run GamedayExport.py, you will first need to install Python2 or 3. Once Python is installed, install the GamedayExport dependencies 
by opening up Terminal (Mac/Linux) or Command Prompt (Windows), navigating to the GamedayExport directory and typing the following command:

    pip install -r requirements.txt

This will install two Python modules, "Pandas" and "Requests". You can manually install these dependencies with the pip install MODULENAME command as well.

## Usage

There are two ways to run the script, with parameters and without. 

    WITHOUT PARAMETERS
    Open Terminal (Mac/Linux) or Command Prompt (Windows) and type: 

        python GamedayExport.py 
    
    The script will then ask you for a date, please enter in your desired date in the YYYY-MM-DD format. If the date is formatted correctly, the script will ask
    for a new entry. If there is no game data for that date, the script will ask if you want to try for another date. 

    WITH PARAMETERS
    Open Terminal (Mac/Linux) or Command Prompt (Windows) and type:

        python GamedayExport.py DATE 
        
        NOTE: Replace DATE with your desired date, in YYYY-MM-DD format. 
    This way, you can quickly specify a target date without the program asking. This is useful if you want to run this script for multiple dates quickly. 
    Please note if there is no data for that date the script will exit. If the date format is incorrect, the script will ask you for a new date.

    If at any time you get stuck while using this script, press Ctrl + C to end script execution and exit. 

## Contributing
    N/A
    
## License
    N/A    