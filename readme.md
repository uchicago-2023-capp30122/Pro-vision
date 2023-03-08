# Pro-vision
## CAPP122 | Final Project
#### Setu Loomba - Diego Mendoza Martinez - Angel Rodriguez Gonzalez
#### March 2023

As foreign students in the University of Chicago, we felt a need to better understand how the public sector in the US provides its citizens with basic services to at a municipal level. This project studies the geographical coverage of public services in the city of Chicago, accounting for the inequality regarding some socioeconomic indicators among neighborhoods.



## Table of Contents

- [Highlights](#highlights)
- [Installation and Execution](#installation-and-execution)
- [Interface Usage](#interface-usage)
- [Contributing](#contributing)
- [License](#license)
- [Data Sources](#data-sources)


## Highlights

### Coverage of the territory

First, we focused on the following relevant provision services:
  - .
  -
  -

For each of them, all the locations are plotted on a map of Chicago, along with isochrones centered in each point (isochrone delineate the geographic space in a 10 minute distance).

<INSERT SCREENSHOT OF **ONLY** ISOCHRONES>


### Visual correlation between socioeconomic indicators and coverage
  
Second, we sharpened the analysis by overlapping socioeconomic indicators to our maps, in order to capture patterns/visual correlations between the socioeconomic features odf certain areas and their degree of coverage. We selected the following indicators:
  - .
  -
  -

Indicators values have been categorised in quartiles, for analytical reasons. Histograms for each indicator are provided.


<INSERT SCREENSHOT OF THE **WHOLE** PICTURE>  


### Simulating shocks
  
As a final step, we move from a geographical representation of Chicago to an abstract one by turning the city into a network, in order to make use of Graph Theory to simulate shocks. We build an adjacency matrix where each node is a community area and these are connected by edges if they are bordering. All nodes are labelled with the following binary attributes: {'Tensioned area': 0-1, 'Provision center within the area': 0-1}

| **Chicago as a network of nodes** | **Community areas with police station** | **Tensioned community areas** |
| --------------------------------- | --------------------------------------- | ----------------------------- |
| ![default](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/Graph_no_labels.JPG) | ![police stations](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/Graph_prov_labels.JPG) | ![tensioned](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/Graph_tens_labels.JPG) |
  
  
We restrict our analysis to homicide rate as socioeconomic indicator and police stations as provision service, and apply two independent kinds of shocks:
  - Stochastic allocation of tension degree to each community area
  - Reduction of the number of police stations by a factor of 0.4

  To measure the resilience of the system to these shocks (change in social tension patterns / abrupt budetary reduction), we build a table with the most tensioned areas and the distance to the nearest police stations after the shock.

| **Statu quo** | **Shock in tensioned areas** | **Shock in number of provision centers** |
| --------------------------------- | --------------------------------------- | ----------------------------- |
| ![no_shock](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/Table_no_shock.JPG) | ![shock_tension](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/Table_shock_tens.JPG) | ![shock_num_stations](https://github.com/uchicago-capp122-spring23/Pro-vision/blob/main/Simulation/Images/Table_shock_provs.JPG) |



## Installation and Execution
To run package in Linux:
1. Clone this repository to your linux machine.
2. From inside the project directory (Pro-vision), run 'poetry install' to install dependencies.
3. Run 'poetry shell' to create a virtual environment.
4. Once the environment is running, you are ready to run the Pro-vision dashboard and simulation generator.
5. To run the quick version of the dashboard (uses pre-processed local files), go to 'Pro-vision/dashboard_quick' and run 'python3 app.py'.
6. To run the full version of the dashboard (includes back-end data cleaning and api-access to fetch isochrones), go to 'Pro-vision/dashboard_full' and run 'python3 app.py'
7. To run the simulation generator, go to the directory called 'Simulation' and run 'python3 simulation.py'
  
  
### Simulating shocks
  
This section is a complementary feature of the project, i.e. not included in the dashboard (yet!).
  
**To run the simulation:**
  1. Go to `Simulation`, and run `python3 run_simulation.py`
  2. Tables will be printed in the terminal, and graphs will be saved in current directory

**To generate the times matrix used for the simulation, from TravelTime API (one-off):**
  1. Go to `Simulation`, and run `python3 run_api_times.py`
  2. A JSON file will be saved in the current directory
  

## Interface Usage

<Instructions for how to use your project, including any relevant examples or code snippets. You can also include screenshots or other visuals to help users understand how your project works.>

## Contributing

<Information for users who want to contribute to your project, including guidelines for submitting pull requests or bug reports. You can also include a code of conduct here.>

## License

<Information about the license under which your project is released. You can include a link to the license file if you have one.>

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
