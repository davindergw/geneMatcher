# SETUP

    - At the top of the Gene Matcher page (https://github.com/davindergw/geneMatcher), click on the green 'clone' button
    - From the dialog that opens up, click 'download Zip'
    - When the download is complete, go to your downloads folder
    - Right click the geneMatcher-main.zip file and click 'Extract All'
    - Click extract (you can change the folder you want the files to appear in by clicking the browse button)
    - Within the extracted geneMatcher-main folder, run the gui.exe file at: dist/gui.exe
    - You may get a warning from windows saying the file is unprotected. If this occurs click 'More Info' and then 'Run Anyway'
    - The program may take a bit of time to load: After a while you should see a black console log appear. Then a bit later the control panel will appear

# FOR DEVELOPMENT

    - GeneMatcher is written in Python
    - To install the necessary dependencies:
        + Run the command 'pip install pandas openpyxl' from the root fodler
        + Run the command 'pip install odfpy' from the root folder

    - The entry point file is gui.py, inside the root folder
    - To run the program run the command python gui.py in the root folder
    - To create a new executable file for the program run the command pyinstaller --onefile gui.py in the root folder.


