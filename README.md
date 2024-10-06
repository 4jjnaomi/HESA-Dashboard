# COMP0034 2023/24 Coursework 2 repository

In this coursework, I created a dashboard application that uses Dash and the Estates Management Record from HESA. The data used in this dashboard app was obtained by HESA and cleaned & prepared by me. Details of data cleaning can be seen here: [https://github.com/4jjnaomi/HESA-DataCleaning](https://github.com/4jjnaomi/HESA-DataCleaning)

To run the app:

1. Fork this repository: [https://github.com/ucl-comp0035/comp0034-cw2i-4jjnaomi](https://github.com/ucl-comp0035/comp0034-cw2i-4jjnaomi)
2. Clone the resulting repository locally and to your IDE
3. Create and activate a virtual environment
4. Install the requirements using `pip install -r requirements.txt`
5. Run the app by using your IDE to run the `app.py` file in the `src` folder
6. Open a browser and go to [http://127.0.0.1:8051/](http://127.0.0.1:8051/)
7. Go to the various URLs outlined in List of URLs below
8. Stop the app using `CTRL+C`
9. Run tests using `pytest -v` or look at the GitHub Actions workflows to see previous runs of tests

**List of URLs**

| URL             | Explanation                                                                               |
|-----------------|-------------------------------------------------------------------------------------------|
| /               | Homepage – landing page for user with navigation to all other pages provided and a map of all HEs in England. |
| /ranking_table  | Ranking table of all HEs in the database of various metrics within classes. The user can choose which metrics they’d like to see. |
| /university/<he_name> | Variable route where each university in the database has an overview page allowing the user to analyse that HE’s data specifically. |
| /comparison     | Users can select a subset of HEs to compare using the bar charts. They can choose which metrics are shown on the bar chart. |

