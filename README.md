# Santiment
Data Collection from Santiment's Grafana in CSV.
This code is written to extract data from Grafana using their API named sanpy -https://github.com/santiment/sanpy. 
You need to have access to their API for which details are given on their API link page.
Then you just run this code by giving your api code, filepath, interval, and days. It will extract data for all the slugs (ERC20 tokens) listed in slug list and save into individual csv files.
You can change the slug list to extract data of your favourite ERC20 tokens
