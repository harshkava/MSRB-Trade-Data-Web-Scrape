# MSRB_TRADE_DATA
This repository contains code to scrape trade data from Municipal Securities Rulemaking Board(MSRB) website using python, selenium and google chrome.</br></br>
**Web-Address: https://emma.msrb.org/Home/Index**</br></br>
The code is complete autonomous & customizable. It allows the user to configure the input filename and output filename while generating an error log file for any cusip that might have been missed.

**Detailed Description:**

**Inputs to Python Code:: (CSV file with 4 columns)** Example:

***Cusip,Source,StartDate,EndDate***<br/>
010869CD5,MSRB,9/1/2020,10/5/2020<br/>
02765UCY8,MSRB,9/1/2020,10/5/2020<br/>


**Input File:**
![Image](/2020-10-05_20-15-08.png?raw=true)



**Output File Generated:: (CSV file with 9 columns)** Example:

***Trade Date/Time,Settlement Date,Price (%),Yield (%)	,Calculation Date & Price (%),Trade Amount ($),Trade Type,SpecialCondition,Cusip*** <br/>
10/05/2020 10:53 AM,10/07/2020,125.788,3.265,"10/01/2029@ 100","250,000",Customer bought,-,010869CD5<br/>
10/02/2020 09:45 AM,10/06/2020,125.75,3.27,"10/01/2029@ 100","250,000",Customer sold,-,010869CD5<br/>
10/01/2020 02:31 PM,10/05/2020,126.465,3.19,"10/01/2029@ 100","250,000",Customer bought,-,010869CD5 <br/>
09/03/2020 03:12 PM,09/08/2020,124.728,3.406,"10/01/2029@ 100","20,000",Inter-dealer trade,,010869CD5<br/>
09/03/2020 03:12 PM,09/08/2020,124.728,3.406,"10/01/2029@ 100","20,000",Inter-dealer trade,,010869CD5<br/>
09/08/2020 01:29 PM,09/10/2020,135.023,4.107,"02/15/2044@ 100","10,000",Customer bought,-,02765UCY8<br/>
09/03/2020 02:32 PM,09/08/2020,133.129,4.211,"02/15/2044@ 100","10,000",Customer sold,-,02765UCY8<br/>
09/03/2020 02:32 PM,09/08/2020,133.157,4.209,"02/15/2044@ 100","10,000",Inter-dealer trade,,02765UCY8<br/>

**Output File:**
![Image](/2020-10-05_20-15-35.png?raw=true)
</br>
</br>
**Program Execution Steps**
</br>
</br>

![Image](/2020-10-05_20-09-16.png?raw=true)


![Image](/2020-10-05_20-10-34.png?raw=true)


![Image](/2020-10-05_20-13-22.png?raw=true)


![Image](/2020-10-05_20-14-10.png?raw=true)






