# BCBA Stock Market

## General Description

This project is part of a personal project to consume public stock APIs from argentinian market and then calculate indicators from the collected data.

By now the only indicator calculated is the Exponential moving average.

## Detailed description

The Main.py file orchestrate all the scripts to run all the possible options.
These options are described bellow.

* **Update Symbol**: Allows to update in the database the information about one or more symbols.

* **Show historic data**: Show the historic data from one symbol allowing the user to add EMA and RSI indicators. It prints a table and a plot.

* **Create technical analysis graphics with saved parameters**: Calculates the EMA Crosover and RSI for one ore more symbols based on the Parameters.xlsx file. It saves the file in the Graphics folder.

* **Simulate Exponential Moving Average Crossover & Relative Strength Index**: Simulates parameters for the EMA Crossover and RSI to calculate the most profitable combination. It saves an Excel file with the 50 most profitable parameters.

* **Show parameters**: Shows the Parameters.xlsx file.


## Requirements.

* Python 3.X
* Pip3

## Step by step



1. Create an SQL Server instance. You can use [docker](https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver15&pivots=cs1-powershell) for it.

2. Execute the SQLQuery.sql script to create the database and tables.

    ```
    sqlcmd -S [ServerIPAdress],[SQLServer Port] -U [USER] -P "[Password]" -i [Path to SQLQuery.sql]
    ```

3. Create a config.json file with the configexample.json file. Using as value of the "st" key the database connection string. Use this [link](https://www.connectionstrings.com/sql-server-2019/) to create it.

4. Install requirements.

    ```
    pip3 install -r requirements.txt
    ```

5. Execute Main.py to start

    ```
    python3 Main.py
    ```
