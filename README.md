# sfpd-data-app
Application that presents a data analysis of the San Francisco Police Department

Overview:
-app.py contains all the backend for the project. 
  -The first section consists of functions that perform various data parsing tasks. Some of the key features are outlined below:
    -get_dispatch_times(): creates a dictionary 'dispatch_times' that has an address for its keys and something I created called a time_sum for values. A time_sum is a computation that takes into account the hour, minute, and second to create an easily comparable integer that represents a time on a particular day.
    -get_most_likely_dispatch(): takes a dictionary as input and returns the most likely dispatch that would be required for a particular time at an address. Useful for the dispatch predictor section of the website.
    -list_of_addresses() and addresses() were both functions that enabled me to create a text file containing all the addresses that were ever dispatched to so that I could have suggestions ready for users when they used my dispatch predictor feature.
    -get_most_dispatched_to(), types_of_dispatches(), and maximum_location_frequencies() are all functions that helped generate data analyses that I incorporated into the final project in the form of graphs and tables
    -longest_dispatch_times() and average_dispatch_time() were the functions I used to create the dispatch timing section of the website. These functions enabled me to see what the most notable cases were for dispatches that took a really long time to arrive at the scene, and for addresses that repeatedly saw longer times for dispatches to arrive to than others.
    -safest_neighborhoods() was a function I used to generate the safety of zip codes section of my website. This function allowed me to analyze the number of potentially life threatening dispatches that were made to specific zip codes by using a dictionary that had zip codes as keys and a running total of potentially life threatening dispatches for that key as its value.
    
    -The second section of this program contains various app routes that lead to different sections of the website. Each section generally just performs a render_template function that displays the corresponding template. One function for the app route to the dispatch predictor is slightly more complicated and is explained below:
      -dispatch_generator(): this function performs some rudimentary error checking to make sure that the data provided by the user is in fact an actual address and time. If the data inputted is invalid, an error template is returned. Another check that occurs is to make sure that the data entered has at least 5 actual dispatches that are close to it. If there isn't that much data that is similar to the data inputted, then a template is generated saying that there is insufficient data to make a prediction. If both these checks prove to be valid, an actual template with a dispatch prediction is shown.
