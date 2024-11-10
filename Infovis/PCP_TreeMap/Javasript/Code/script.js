// Load the data using d3
d3.csv("HE Attrition Data Main, 2005-2013.csv").then(function(data) {
    // Select the first set of columns
    const selectedColumns1 = [
        "Reference_year",
        "attrition_rate",
        "nesbattrition",
        "disattrition",
        "seslow2006attrition",
        "seslow2011attrition",
        "indigenousattrition",
        "modeinternalatt",
        "modeexternalatt",
        "modemultiatt"
    ];

    // Select the second set of columns
    const selectedColumns2 = [
        "Reference_year",
        "typeftatt",
        "typeptatt",
        "genderfemaleatt",
        "gendermaleatt",
        "ageunder25att",
        "age25to39att",
        "agegt39att",
        "atarunder70att",
        "atar70to89att",
        "atargt89"
    ];
    const selectedColumns3 = [
        'Reference_year',
        'boahigheredatt', 'boasecondaryatt',
           'boavetatt', 'boamatureatt', 'boaproffatt', 'boaotheratt'
        ]
    // Helper function to create traces for a parallel coordinates plot
    function createParallelCoordinatesData(columns) {
        return columns.map(column => ({
            range: d3.extent(data, d => +d[column]),
            label: column,
            values: data.map(d => +d[column])
        }));
    }

    // First Parallel Coordinates Plot
    const trace1 = {
        type: 'parcoords',
        line: { 
            color: Array.from({ length: selectedColumns1.length }, (_, i) => i),
            colorscale: 'Jet' 
        },
        dimensions: createParallelCoordinatesData(selectedColumns1)
    };

    const layout1 = {
        title: "Parallel Coordinates Plot of Attrition Rate based on primary attributes"
    };

    Plotly.newPlot('pcp1', [trace1], layout1);

    // Second Parallel Coordinates Plot
    const trace2 = {
        type: 'parcoords',
        line: { 
            color: Array.from({ length: selectedColumns1.length }, (_, i) => i),
            colorscale: 'Jet' 
        },
        dimensions: createParallelCoordinatesData(selectedColumns2)
    };

    const layout2 = {
        title: "Parallel Coordinates Plot of Attrition Rate based on qualification"
    };

    Plotly.newPlot('pcp2', [trace2], layout2);


    const trace3 = {
        type: 'parcoords',
        line: { 
            color: Array.from({ length: selectedColumns1.length }, (_, i) => i),
            colorscale: 'Jet' 
        },
        dimensions: createParallelCoordinatesData(selectedColumns3)
    };

    const layout3 = {
        title: "Parallel Coordinates Plot of Attrition Rate based on Broad Field Of Education"
    };

    Plotly.newPlot('pcp3', [trace3], layout3);



    // TreeMap Heirarchy: Year -> Attribute
    const labels4 = [];
    const parents4 = [];
    const values4 = [];
    const attributeColumns4 = Object.keys(data[0]).filter(col => col !== "Reference_year");

    labels4.push("Root");
    parents4.push("");
    values4.push(0);

    data.forEach(row => {
        const year = row["Reference_year"];

        labels4.push(year);
        parents4.push("Root");
        values4.push(0);

        attributeColumns4.forEach(attribute => {
            const attritionRate = row[attribute] ? parseFloat(row[attribute]) : 0;
            labels4.push(`${year} - ${attribute}`);
            parents4.push(year);
            values4.push(attritionRate);
        });
    });


    const trace4 = {
        type: "treemap",
        labels: labels4,
        parents: parents4,
        values: values4,
        textinfo: "label+value",
        hoverinfo: "label+value+percent parent",
        marker: { colors: values4, colorscale: "Viridis" }
    };

    const layout4 = {
        title: "Attrition Rates by Year and Attribute",
    };

    Plotly.newPlot("treemap1", [trace4], layout4);

    // TreeMap for heirarchy : Attribute->Year

    const labels5 = [];
    const parents5 = [];
    const values5 = [];
    const attributeColumns5 = Object.keys(data[0]).filter(col => col !== "Reference_year");

    const maxAttritionRates5 = {};

    data.forEach(row => {
        const year = row["Reference_year"];
        attributeColumns5.forEach(attribute => {
            const attritionRate = row[attribute] ? parseFloat(row[attribute]) : 0; 
            if (!maxAttritionRates5[year]) {
                maxAttritionRates5[year] = attritionRate;
            } else {
                maxAttritionRates5[year] = Math.max(maxAttritionRates5[year], attritionRate);
            }
        });
    });

    const sortedYears = Object.keys(maxAttritionRates5).sort((a, b) => maxAttritionRates5[b] - maxAttritionRates5[a]);

    labels5.push("Root");
    parents5.push("");
    values5.push(0);

    sortedYears.forEach(year => {
        labels5.push(year);
        parents5.push("Root");
        values5.push(maxAttritionRates5[year]);

        attributeColumns5.forEach(attribute => {
            const attritionRate = data.find(row => row["Reference_year"] === year)[attribute]
                ? parseFloat(data.find(row => row["Reference_year"] === year)[attribute])
                : 0;
            labels5.push(`${year} - ${attribute}`);
            parents5.push(year);
            values5.push(attritionRate);
        });
    });

    const trace5 = {
        type: "treemap",
        labels: labels5,
        parents: parents5,
        values: values5,
        textinfo: "label+value",
        hoverinfo: "label+value+percent parent",
        marker: { colors: values5, colorscale: "Viridis" }
    };

    const layout5 = {
        title: "Attrition Rates by Year and Attribute",
    };

    Plotly.newPlot("treemap2", [trace5], layout5);



    // TreeMap for colors in parents


    const labels = [];
    const parents = [];
    const values = [];
    const colors = [];

    const attributeColumns = Object.keys(data[0]).filter(col => col !== "Reference_year");

    const maxAttritionRates = {};

    attributeColumns.forEach(attribute => {
        maxAttritionRates[attribute] = {};
        data.forEach(row => {
            const year = row["Reference_year"];
            const attritionRate = row[attribute] ? parseFloat(row[attribute]) : 0;
            if (!maxAttritionRates[attribute][year]) {
                maxAttritionRates[attribute][year] = attritionRate;
            } else {
                maxAttritionRates[attribute][year] = Math.max(maxAttritionRates[attribute][year], attritionRate);
            }
        });
    });

    // Viridis color array
    const viridisColors = [
        "#440154", "#482878", "#3e4989", "#31688e", "#26828e", "#1f9e89",
        "#35b779", "#6ece58", "#b5de2b", "#fee825"
    ];

    function getColorFromViridis(normalizedValue) {
        const colorIndex = Math.floor(normalizedValue * (viridisColors.length - 1));
        return viridisColors[colorIndex];
    }

    labels.push("Root");
    parents.push("");
    values.push(0);
    colors.push("#FFFFFF");  // Optional color for the root

    attributeColumns.forEach(attribute => {
        labels.push(attribute);
        parents.push("Root");
        values.push(0);

        colors.push(getColorFromViridis(0.5));

        const yearRates = Object.values(maxAttritionRates[attribute]);
        const minAttrition = Math.min(...yearRates);
        const maxAttrition = Math.max(...yearRates);

        const sortedYears = Object.keys(maxAttritionRates[attribute]).sort(
            (a, b) => maxAttritionRates[attribute][b] - maxAttritionRates[attribute][a]
        );

        sortedYears.forEach(year => {
            labels.push(`${year}`);
            parents.push(attribute);
            const value = maxAttritionRates[attribute][year];
            values.push(value);
            const normalizedValue = (value - minAttrition) / (maxAttrition - minAttrition);
            colors.push(getColorFromViridis(normalizedValue));
        });
    });

    // TreeMap function to try different spatial partitioning
    function createTreemap(divId, title, packingMethod, orientation) {
        const trace = {
            type: "treemap",
            labels: labels,
            parents: parents,
            values: values,
            textinfo: "label+value",
            hoverinfo: "label+value+percent parent",
            marker: {
                colors: colors,
            },
            tiling: {
                packing: packingMethod,
                orientation: orientation
            }
        };

        const layout = {
            title: title,
            margin: { t: 50, l: 25, r: 25, b: 25 },
        };

        Plotly.newPlot(divId, [trace], layout);
    }

    // One can change here the variations of "squarify" and "v" at end of function call

    createTreemap("treemapSquarify", "Attrition Rates by Attribute and Year (Spatial Partitioning : Squarify)", "squarify", "v");
    createTreemap("treemapBinary", "Attrition Rates by Attribute and Year (Spatial Partitioning : Binary)", "binary", "v");
    createTreemap("treemapSlice", "Attrition Rates by Attribute and Year (Spatial Partitioning : Slice)", "slice", "v");
    createTreemap("treemapDice", "Attrition Rates by Attribute and Year (Spatial Partitioning : Dice)", "dice", "v");




});
