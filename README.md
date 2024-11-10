# Scientific and Informative Visualization - DAS732 - A2

This repository contains two types of visualizations: **Scientific Visualization (Scivis)** and **Information Visualization (Infovis)**. The main focus is on meteorological data analysis, Marvel Social Network analysis, and higher education attrition rate analysis.

## Folder Structure

- **/Infovis**: Contains files related to Informative Visualization.
- **/Scivis**: Contains files related to Scientific Visualization.



---

## Scientific Visualization

### Dataset

We use the **gridMET** dataset, which includes daily, high-spatial-resolution (~4 km, 1/24th degree) surface meteorological data covering the contiguous U.S. from 1979 to the present. For this project, the focus is on the timeline of July - September 2019. Key meteorological variables include:

- **sph**: Near-Surface Specific Humidity
- **vpd**: Mean Vapor Pressure Deficit
- **pr**: Precipitation
- **rmin**: Minimum Near-Surface Relative Humidity
- **rmax**: Maximum Near-Surface Relative Humidity
- **srad**: Surface Downwelling Solar Radiation
- **tmmn**: Minimum Near-Surface Air Temperature
- **tmmx**: Maximum Near-Surface Air Temperature
- **vs**: Wind Speed at 10 m
- **th**: Wind Direction at 10 m
- **pdsi**: Palmer Drought Severity Index
- **pet**: Reference Grass Evapotranspiration
- **etr**: Reference Alfalfa Evapotranspiration
- **ERC**: Model-G
- **BI**: Model-G
- **FM100**: 100-hour Dead Fuel Moisture
- **FM1000**: 1000-hour Dead Fuel Moisture

*Note: Not all variables were used in visualization, but multiple variables were analyzed together to infer information.*

### File Paths

| File Path                   | Description                                                       |
|-----------------------------|-------------------------------------------------------------------|
| `/Scivis/A2.ipynb`          | Source code used to process and visualize meteorological data.   |
| `/Scivis/Dataset`           | Contains meteorological data for the U.S. in 2019.               |
| `/Scivis/Images/*`          | Contains all images produced to derive inferences.               |

### Data Processing

The dataset for specific dates was downloaded in **netCDF** format and processed using the `netCDF4` library in Python. The `xarray` library was used to read data from `.nc` files. Missing values were handled using `np.nan` functions.

### Implementation

The code can be run using the provided Jupyter notebook. Datasets in `/Scivis/Dataset/2019/*` should be uploaded to the Python environment to generate outputs (existing outputs are already provided). Marching square is applied using contourf and heatmaps are shown using imshow. Opted for multi plot type style i.e quiver or streamline, imshow and contourf together. In report, temperature part is not mentioned and it uses global colormap as it helps in comparing hottest days in the choosed timeline with other days.

### Important Folders

| File Path                       | Description                                                                                       |
|---------------------------------|---------------------------------------------------------------------------------------------------|
| `/Quiver/Black`                 | Quiver plots for wind with black color (length represents wind speed).                            |
| `/Quiver/DifferentLength/*`     | Quiver plots for wind with different colormaps.                                                   |
| `/Quiver/SameLength/*`          | Quiver plots with the same length of arrows for discrete and continuous colormaps.               |
| `/Streamline/*`                 | Streamline plots for wind with colormaps showing magnitude and direction.                          |
| `/ForestFire/*`                 | Visualization of wildfire conditions for events like Cow and Walker fires.                        |
| `/Drought`                      | Drought conditions observed through wind direction and temperature contours.                      |
| `/Hurricane`                    | Conditions for Hurricane Barry with overlays of precipitation and humidity data.                  |
| `/Temperature/*`                | Observations on temperature trends using global/local colormaps.                                  |

---

## Information Visualization (Infovis)

### Node-Link Diagrams

#### Files

| File Path                           | Description                                                                                         |
|-------------------------------------|-----------------------------------------------------------------------------------------------------|
| `/Node-Link/Dataset/*`              | Contains Marvel Social Network dataset files and superhero images.                                  |
| `/NodeLink/Images*`                 | Contains layout visualizations of different superhero clusters and connections.                    |
| `/NodeLink/Modularity`              | Contains information about modularity and cluster distribution in the network.                     |

*Note on Images:* For nodes with a degree greater than 531, animated images of major superheroes were added to enhance visualization. This was achieved by adding an `image` column in the dataset and using the **Image Preview** plugin in Gephi.

### Dataset

The **Marvel Social Network** dataset shows relationships among Marvel characters. It includes 10,469 nodes and 178,115 undirected edges, representing the number of common appearances in comics.

#### Requirements

**Gephi** (Version 9.2 only) - Available on the official Gephi website.

### Preprocessing

Nodes were filtered based on degree:
- **Nodes with degree > 531**
- **Nodes with degree > 335** (to enhance cluster visibility)

### Implementation

Gephi was used to visualize clusters based on modularity and centrality metrics, highlighting major franchises like Avengers, X-Men, and Spiderverse.

---

### Parallel Coordinates Plot and TreeMap

These were implemented in two ways: JavaScript and Python.

#### Files

| File Path                         | Description                                                                      |
|-----------------------------------|----------------------------------------------------------------------------------|
| `/Dataset/*`                      | Contains datasets for plotting graphs.                                           |
| `/PCP_TreeMap/Python/*`           | Contains images and source code generated using Python (Plotly.js).              |
| `/PCP_TreeMap/Javascript/*`       | Contains images and source code generated using JavaScript (Plotly.js and d3.js).|

#### Dataset

The **Higher Education Attrition Rate** dataset for Australia (2005-2013) was used, focusing on statistics based on gender, social factors, scores, origin, and geographical data.

#### Data Processing

Empty attributes were converted to zero as needed.

#### Requirements

JavaScript libraries:
- **Plotly.js**
- **d3.js**

Python requirements:
- Provided in the Python notebook with installation commands.

### Implementation

- **TreeMap:** Implemented with hierarchical partitioning strategies for visualizing attrition rates based on year and attributes.
- **Parallel Coordinate Plot:** Divided into three categories - primary variables, qualification levels, and fields of study, with interactions for filtering and axis reordering.

#### Running the Live Server for JavaScript

1. **Install Visual Studio Code** from the official website.
2. **Install Live Server Extension** in VS Code (Ctrl+Shift+X > Search "Live Server" > Install).
3. **Open Project Folder** and start Live Server (Right-click HTML file > Open with Live Server).
4. **Stop Live Server**: Close the browser tab or stop within VS Code.



---

### Conclusion

This repository provides a comprehensive suite of visualizations aimed at both scientific and informational purposes. It covers complex datasets ranging from meteorological data to social network analysis and higher education attrition rates, all designed with both functionality and aesthetic clarity in mind.