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
| `/Scivis/A2.ipynb`          | Jupyter notebook for processing and visualizing meteorological data.   |
| `/Scivis/Dataset`           | Contains meteorological data for the U.S. in 2019.               |
| `/Scivis/Images/*`          | Contains all generated images for analysis.                     |
| `/Scivis/Code/*`            | Contains all scripts required to produce images.                   |

### Data Processing

The dataset is in **netCDF** format and processed with the `netCDF4` library. The `xarray` library reads data from `.nc` files, and missing values are managed with `np.nan`.

### Important Folders for Images and Code

| File Path                       | Description                                                                                       |
|---------------------------------|---------------------------------------------------------------------------------------------------|
| `/Quiver/Black`                 | Quiver plots for wind with black arrows (length indicates wind speed).                            |
| `/Quiver/DifferentLength/*`     | Quiver plots with different colormaps for wind speed.                                            |
| `/Quiver/SameLength/*`          | Quiver plots with arrows of the same length for discrete/continuous colormaps.                   |
| `/Streamline/*`                 | Streamline plots for wind showing magnitude and direction.                                        |
| `/ForestFire/*`                 | Visualizations of wildfire conditions (e.g., Cow and Walker fires).                               |
| `/Drought`                      | Visualizations of drought conditions, highlighting wind direction and temperature contours.       |
| `/Hurricane`                    | Hurricane Barry conditions with overlays of precipitation and humidity data.                     |
| `/Temperature/*`                | Temperature trend visualizations using various colormaps.                                        |
| `Instruction.txt`               | Contains important functions usage for all python codes.                                         |

---

## Getting Started

### Prerequisites

1. **Python Installation**: Make sure Python 3.12.0 or later is installed.
    ```bash
    python3 --version
    ```
   If not installed, download from [Python Downloads](https://www.python.org/downloads/).

2. **pip Installation**: Ensure pip 24.3.1 or later is installed.
    ```bash
    pip3 --version
    ```
   If not installed, follow the [pip Installation Guide](https://pip.pypa.io/en/stable/installation/).

### Installation of Required Packages

Navigate to the main project directory and run:

```bash
pip3 install pandas xarray dask matplotlib numpy cartopy scipy imageio pillow hill
```

---
## Note
Please keep the project structure the same as provided. If any files or folders are moved, you will need to update file paths in the code to reflect the new structure (if changed, one could change file path as mentioned in step 4 of running the code using .py scripts section).

---
## Running the Code

You have two options for running the visualizations: using `.py` scripts or the provided `.ipynb` Jupyter notebook.

---

### Option 1: Run `.py` Scripts

1. **Navigate to the Folder**: Move to the folder containing the code for the desired visualization (e.g., `ForestFire/cow_fire/`).

2. **Run the Plot Generation Script**: Execute the main Python script (e.g., `cow_wildfire.py`) to generate plots, which will be saved in the same folder.

    ```bash
    python3 cow_wildfire.py
    ```

    *Optional*: Uncomment `plt.show()` in the script to display plots as they are generated.

3. **Run GIF Generation Script**: After generating images, use `gif.py` to create GIFs from the images.

    ```bash
    python3 gif.py
    ```

    - *Note*: Adjust the GIF frame duration by changing the `dpi` setting in `gif.py`.

4. **Adjust File Paths if Needed**: If files are relocated, update paths in the code, such as:

    ```python
    vs = xr.open_dataset("../../../Dataset/2019/vs_2019.nc", decode_times=False)
    ```

    Modify the file path based on your system structure.

---

### Option 2: Run Jupyter Notebook

1. **Run the Notebook**: Open and run the provided Jupyter notebook, `/Scivis/A2.ipynb`. The notebook steps through data processing and visualization.

2. **Load Dataset**: Ensure that the dataset files in `/Scivis/Dataset/2019/*` are uploaded or accessible within the Python environment to generate outputs. Existing output images are already provided in the notebook.

3. **Execute Cells**: Run each cell in sequence to generate visualizations. You can adjust paths as needed within each cell.

--- 


Marching square is applied using contourf and heatmaps are shown using imshow. Opted for multi plot type style i.e quiver or streamline, imshow and contourf together. In report, temperature part is not mentioned (showing compile runtime error) and it uses global colormap as it helps in comparing hottest days in the choosed timeline with other days.



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

**Gephi** (Version 9.2 only) - Available on the official Gephi website [to install gephi](https://gephi.org/users/download/).

### Preprocessing

Nodes were filtered based on degree:
- **Nodes with degree > 531**
- **Nodes with degree > 335** (to enhance cluster visibility)

### Implementation

**Note**: Please retain the project structure as provided. If you change the file paths, you will need to update them in the code.

This project uses Gephi to visualize clusters and analyze network relationships based on modularity and centrality metrics, highlighting major franchises such as Avengers, X-Men, and Spiderverse. All layout parameters in Gephi were set to their default values, so no modifications were made to the pre-configured settings.

To generate the layouts and visuals, follow these steps:

1. **Open the Gephi File**  
   - Locate and open the `.gephi` file provided in the `Dataset` folder.

2. **Filter Nodes by Degree**  
   - Go to the "Filters" panel.
   - In the "Library" section, navigate to **Topology** and drag **Degree Range** to the **Queries** panel.
   - Click on **Degree Range** to reveal the slider. Set the lower limit to the required degree as noted above and click **Filter** to apply the filter.
   - To set an exact degree value, double-click the slider value and enter the desired number.

3. **Apply Layouts**  
   - In the **Layout** panel on the left, select the layout method (e.g., **ForceAtlas** in this project) and click **Run**. If the layout process takes longer than expected, you may manually stop it after 1-2 minutes.

4. **Identify Clusters by Color**  
   - Open the **Statistics** panel and run **Modularity** and **Network Diameter** metrics to reveal clusters.
   - In the **Appearance** section, click on **Nodes**, then navigate to **Partition** and select **Modularity Class** to assign colors to clusters. You can customize colors based on your preference or follow the project’s original color scheme.

5. **Visualize and Style the Network**  
   - For a refined view, go to **Preview** and make the following adjustments:
     - Set **Node Images** visibility, ensuring the image folder path is correct.
     - Adjust **Edge Thickness** to `0.005`.
     - Set **Node Label Font Size** to bold with size `3` and enable proportional scaling.
   - Click **Refresh** to view the updated visualization.

6. **Explore Further**  
   - Feel free to experiment with additional attributes or adjustments to customize the visualization further.

### References
For a detailed walkthrough of Gephi features and visualization techniques, you can follow along with [this tutorial series](https://www.youtube.com/playlist?list=PLk_jmmkw5S2BqnYBqF2VNPcszY93-ze49).


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
3. **Open Project Folder** i.e /PCP_TreeMap/Javacript and start Live Server (Right-click HTML file > Open with Live Server).
4. **Stop Live Server**: Close the browser tab or stop within VS Code.



---

### Conclusion

This repository provides a comprehensive suite of visualizations aimed at both scientific and informational purposes. It covers complex datasets ranging from meteorological data to social network analysis and higher education attrition rates, all designed with both functionality and aesthetic clarity in mind.
