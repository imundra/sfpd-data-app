## sfpd-data-app for the Capital One Software Engineering Summit
I created an application that presents a data analysis of the San Francisco Police Department.

There is a live link available at: https://sfpd-data-app.herokuapp.com/

## Contents:
- [Deliverables Overview](#Deliverables Overview)
- [Python Data Parsing](#Python Data Parsing)
- [Flask Web App](#Flask Web App)
-[HTML, CSS, Javascript](#HTML, CSS, Javascript)

## Deliverables Overview

Deliverable 1: Data Visuals -- The data visuals I have created are present in the Data Overview tab of the website.

Deliverable 2: What is the most likely dispatch to be required? -- I created a Dispatch Predictor tab with a handy tool that aims to address this deliverable.

Deliverable 3: Which areas take the longest time to dispatch to? -- The Dispatch Timing tab has my attempts at visualizing the data relevant to this deliverable. For each of the addresses uncovered in the Dispatch Timing tab, I think the best way to address the issue of the areas that take a longer time to reach by dispatches is to either 1) create more SFPD branches in low access areas or  2) make patrols aware of which areas are typically out of reach and to reorganize the patrolling of SFPD to ensure that these areas have emergency personnel within reach. 

Bonus Deliverable: Crime Correlation -- My work in solving this deliverable is present in the Safety of Zipcodes section of my website. My python program looked at potentially life-threatening dispatches in order to compute a top 10 most dangerous and top 10 safest zip codes in San Francisco. The tables are organized in increasing numeric value for the zipcode.

## Python Data Parsing
 
The first section of app.py consists of functions that perform various data parsing tasks. Some of the key features are outlined below:
  
1. get_dispatch_times(): creates a dictionary 'dispatch_times' that has an address for its keys and something I created called a time_sum for values. A time_sum is a computation that takes into account the hour, minute, and second to create an easily comparable integer that represents a time on a particular day.
    
2. get_most_likely_dispatch(): takes a dictionary as input and returns the most likely dispatch that would be required for a particular time at an address. Useful for the dispatch predictor section of the website.
    
3. list_of_addresses() and addresses() were both functions that enabled me to create a text file containing all the addresses that were ever dispatched to so that I could have suggestions ready for users when they used my dispatch predictor feature.
    
4. get_most_dispatched_to(), types_of_dispatches(), and maximum_location_frequencies() are all functions that helped generate data analyses that I incorporated into the final project in the form of graphs and tables
    
5. longest_dispatch_times() and average_dispatch_time() were the functions I used to create the dispatch timing section of the website. These functions enabled me to see what the most notable cases were for dispatches that took a really long time to arrive at the scene, and for addresses that repeatedly saw longer times for dispatches to arrive to than others.
    
6. safest_neighborhoods() was a function I used to generate the safety of zip codes section of my website. This function allowed me to analyze the number of potentially life threatening dispatches that were made to specific zip codes by using a dictionary that had zip codes as keys and a running total of potentially life threatening dispatches for that key as its value.
    
## Flask Web App 

The second section of app.py contains various app routes that lead to different sections of the website.

1. Each section generally just performs a render_template function that displays the corresponding template. One function for the app route to the dispatch predictor is slightly more complicated and is explained below:
      
2. dispatch_generator(): this function performs some rudimentary error checking to make sure that the data provided by the user is in fact an actual address and time. If the data inputted is invalid, an error template is returned. Another check that occurs is to make sure that the data entered has at least 5 actual dispatches that are close to it. If there isn't that much data that is similar to the data inputted, then a template is generated saying that there is insufficient data to make a prediction. If both these checks prove to be valid, an actual template with a dispatch prediction is shown.

## HTML, CSS, Javascript

The images (tables and graphs) created were all done through the use of software such as Microsoft Excel (nothing too fancy), after taking the results of my python data parsing program as detailed above.

The templates used in this project were mostly default bootstrap samples that I modified to fit my own purposes. I also used some javascript to accomplish an autocomplete feature for the Dispatch Predictor section of my website. This was done in order to make it easier for users to enter addresses (rather than recall an entire address from memory).
