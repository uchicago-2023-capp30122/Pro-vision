# Pro-vision
## CAPP122 | Final Project
#### Setu Loomba - Diego Mendoza Martinez - Angel Rodriguez Gonzalez
#### March 2023

As foreign students in the University of Chicago, we felt a need to better understand how the public sector in the US provides its citizens with basic services at a municipal level. This project studies the geographical coverage of public services in the city of Chicago, accounting for the inequality regarding some socioeconomic indicators among neighborhoods.



## Table of Contents

- [Highlights](#highlights)
- [Installation and Execution](#installation-and-execution)
- [Interface Usage](#interface-usage)
- [Documentation](#license)
- [Data Sources](#data-sources)


## Highlights

### Coverage of the territory

First, we focused on the following relevant provision services:
- Neighborhood Health Clinics
- Warming Centers
- Polic Stations
- Fire Stations

For each of them, all the locations are plotted on a map of Chicago, along with isochrones centered in each point (isochrone delineate the geographic space in a 10 minute distance).

![isos](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/Isos.JPG)


### Visual correlation between socioeconomic indicators and coverage
  
Second, we sharpened the analysis by overlapping socioeconomic indicators to our maps, in order to capture patterns/visual correlations between the socioeconomic features of certain areas and their degree of coverage. We selected the following indicators:
- Uninsured rate (% of residents, 2015-2019)
- Homicide (crimes), 2017-2021
- Major crime (crimes), 2016-2020
- Violent crime (crimes), 2016-2020
- Eviction rate (% of renter-occupied households, 2018)
- Severely rent-burdened (% of renter-occupied housing units), 2015-2019
- Traffic crashes (number of crashes), 2021
- High School Graduation rate (% of residents), 2015-2019
- Unemployment rate (%), 2015-2019
- Median Household Income, 2015-2019
- Per Capita Income, 2015-2019
- Poverty rate (% of residents), 2015-2019
- Demographics, Minorities (% of residents), 2016-2020
- Population (residents), 2015-2019

Indicators values have been categorised in quartiles, for analytical reasons. Histograms for each indicator are provided.


![complete](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/dashboard_ProVision.png)  


### Simulating shocks
  
As a final step, we move from a geographical representation of Chicago to an abstract one by turning the city into a network, in order to make use of Graph Theory to simulate shocks. We build an adjacency matrix where each node is a community area and these are connected by edges if they are bordering. All nodes are labelled with the following binary attributes: {'Tensioned area': 0-1, 'Provision center within the area': 0-1}

| **Chicago as a network of nodes** | **Community areas with police station** | **Tensioned community areas** |
| --------------------------------- | --------------------------------------- | ----------------------------- |
| ![default](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/Graph_no_labels.JPG) | ![police stations](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/Graph_prov_labels.JPG) | ![tensioned](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/Graph_tens_labels.JPG) |
  
  
We restrict our analysis to homicide rate as socioeconomic indicator and police stations as provision service, and apply two independent kinds of shocks:
  - Stochastic allocation of tension degree to each community area
  - Reduction of the number of police stations by a factor of 0.4

  To measure the resilience of the system to these shocks (change in social tension patterns / abrupt budetary reduction), we build a table with the most tensioned areas and the distance to the nearest police stations after the shock.

| **Status quo** | **Shock in tensioned areas** | **Shock in number of provision centers** |
| --------------------------------- | --------------------------------------- | ----------------------------- |
| ![no_shock](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/Table_no_shock.JPG) | ![shock_tension](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/Table_shock_tens.JPG) | ![shock_num_stations](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/Table_shock_provs.JPG) |



## Installation and Execution
To run package in Linux:
1. Clone this repository to your linux machine.
2. Change the name of the repository from Pro-vision to ProVision using `mv Pro-vision ProVision`.
3. From inside the project directory (ProVision), run `poetry install` to install dependencies.
4. Run `poetry shell` to create a virtual environment.
5. Once the environment is running, you are ready to run the `ProVision` dashboard and simulation generator.
6. To run the quick version of the dashboard, go to your root directory (where the ProVision directory is stored), and run `python3 -m ProVision quick`.
7. To run the full version of the dashboard, go to your root directory (where the ProVision directory is stored), and run `python3 -m ProVision full`.
  
  
### Simulating shocks
  
This section is a complementary feature of the project, i.e. not included in the dashboard (yet!).
  
**To run the simulation:**
  1. Go to `Simulation`, and run `python3 run_simulation.py`
  2. Tables will be printed in the terminal, and graphs will be saved in current directory

**To generate the times matrix used for the simulation, from TravelTime API (one-off):**
  1. Go to `Simulation`, and run `python3 run_api_times.py`
  2. A JSON file will be saved in the current directory
  

## Interface Usage

Pro-vision's Dashboard and visual features are designed to allow the policymaker/analyst to derive key insights in an easy-to-understand and -interact manner. The display is divided in two columns. The left column contains a brief description of the Map's objective, two dropdown menus and a histogram. The first dropdown menu contains several socioeconomic variables that can be displayed in the map and the histogram. The second dropdown menu contains a list of Provisions (e.g., Neighborhood Health Clinics, Police Stations, etc.) that the user can select as well. At the end, there is a histogram that is only included if the user selected a socioeconomic variable. The histogram can be toggled between Quartiles (i.e., Q1 lowest quartile to Q4 highest quartile) to select/deselect socioeconomic groups; the user can also hover the histogram to see the ranges for each Quartile.

The right column of the dashboard shows the map, which is traced by Census Tacts (2010). If no socioeconomic variable and no provision is selected, the map is displayed in gray and the user can hover the map to see the GEOIDs. If a socioeconomic variable is selected without any provision, the map is displayed as a choropleth map where the user can toggle as well by Quartiles. If a provision is selected without any socioeconomic variable, the map is displayed as empty (i.e., no color) but with points indicating the exact longitude and latitude of all the facilities of this provision over the map. Most importantly, the 10-minute distance coverage of these facilities are traced as boundaries in this selection. If a socioeconomic variable and provision are selected, the map displays the choropleth map and the points with its coverage boundaries. This map is fully interactive, allows to toggle between Quartiles and hover over the points to get the address of the facility and hover over the colored census tacts to get the value of the socioeconomic variable.

The full dashboard looks as follows:

![complete](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/dashboard_quick/Images/dashboard_ProVision.png)  

## Documentation
![complete](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/ProVision_Guide.pdf)

## Data Sources
1. Data on public services provision
    - Chicago Data Portal: https://data.cityofchicago.org/
2. Data on socioeconomic indicators
    - Chicago Atlas Health: https://chicagohealthatlas.org/indicators/
3. Data on geographical coordinates for census tracts and community areas:
    - Chicago Data Portal: https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6
5. Data on time distances
    - TravelTime API: https://docs.traveltime.com/api/overview/introduction


## Contact

Setu Loomba - setu@uchicago.edu;
Diego Martin Mendoza - diegomendozamz@uchicago.edu;
Angel Rodriguez Gonzalez - angelrodriguezg@uchicago.edu

## Acknowledgments

We very much appreciate James Turk and Megan Moore's help and invaluable suggestions.
