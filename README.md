# MSRB_TRADE_DATA

This repository contains code to scrape trade data from Municipal Securities Rulemaking Board(MSRB) website using python, selenium and google chrome.

The code is complete autonomous & customizable. It allows the user to configure the input filename and output filename while generating an error log file for any cusip that might have been missed.

**Detailed Description:**

**Inputs to Python Code:: (CSV file with 4 columns)** Example:

***Cusip,Source,StartDate,EndDate***

010869CD5,MSRB,9/1/2020,10/5/2020
02765UCY8,MSRB,9/1/2020,10/5/2020


**Output File Generated:: (CSV file with 9 columns)** Example:

***Trade Date/Time,Settlement Date,Price (%),Yield (%)	,Calculation Date & Price (%),Trade Amount ($),Trade Type,SpecialCondition,Cusip***

10/05/2020 10:53 AM,10/07/2020,125.788,3.265,"10/01/2029@ 100","250,000",Customer bought,-,010869CD5
10/02/2020 09:45 AM,10/06/2020,125.75,3.27,"10/01/2029@ 100","250,000",Customer sold,-,010869CD5
10/01/2020 02:31 PM,10/05/2020,126.465,3.19,"10/01/2029@ 100","250,000",Customer bought,-,010869CD5



The code is designed to make use of TRADE Search (Window) available at the MSRB website to fetch all transaction data from Jan 2019 to Jul 2019.


**Web-Address: https://emma.msrb.org/Home/Index**
