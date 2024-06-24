# LEGO Brick Image Recognition Case Study

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

This project is part of a case study conducted during the interview process for the Senior Software Engineering Position at the LEGO Group. The repository demonstrates my software engineering skills.

## Sample Exercise

Create a mockup source code solution for an application that focuses on image recognition of LEGO bricks, limited to a maximum of two attributes.

### Background Information

The application is intended for use in a production line. The machinery is configured to select specific LEGO sets containing the LEGO bricks of interest before initialization. Once configured, the necessary data generation can begin.

### Assumptions

1. We're only interested in specific LEGO bricks from selected LEGO sets.
2. We will generate synthetic data (both 2D and 3D) for the LEGO bricks of interest on the fly.
3. All LEGO bricks are fully disassembled and in flawless (original) condition.

## Solution Layout

1. **Connect to the Database**:
   - Scan a unique ID (order identifier) to get an overview of all LEGO sets.
   - Query the following information:
     - Total number of LEGO sets
     - Total number of LEGO bricks
     - Number of different LEGO sets
     - Number of different LEGO bricks

2. **Create Reference Images**:
   - Forward the product ID to the pipeline responsible for generating synthetic images of the LEGO bricks.

3. **Video Stream Processing**:
   - Open a video stream and wait for the LEGO bricks to pass by.

4. **Object Detection and Comparison**:
   - Detect objects and compare them using techniques such as a Siamese Network, CNN, or Few-Shot Learning against all reference images (support set).
   - Label the detected objects as either "Redundant Brick" or a unique code if the LEGO brick is not part of the recognized set.
   - Create a dictionary at initialization that tracks all LEGO brick IDs and counts. Decrement the count each time a LEGO brick is recognized. This dictionary will provide information on how many LEGO bricks are missing.


### Flowchart

![LEGO Flowchart]()


## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for lego
│                         and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── lego                <- Source code for use in this project.
    │
    ├── __init__.py    <- Makes lego a Python module
    │
    ├── data           <- Scripts to download or generate data
    │   └── make_dataset.py
    │
    ├── features       <- Scripts to turn raw data into features for modeling
    │   └── build_features.py
    │
    ├── models         <- Scripts to train models and then use trained models to make
    │   │                 predictions
    │   ├── predict_model.py
    │   └── train_model.py
    │
    └── visualization  <- Scripts to create exploratory and results oriented visualizations
        └── visualize.py
```

--------

## Getting Started

To run this project, follow these steps:

1. Clone the repository.
2. Set up the database connection.
3. Configure the synthetic image generation pipeline.
4. Initialize the video stream processing.
5. Run the object detection and comparison algorithm.


## License

This project is licensed under the MIT License. See the LICENSE file for details.
