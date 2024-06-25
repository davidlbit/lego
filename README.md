# LEGO Brick Image Recognition Case Study

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

This project is part of a case study conducted during the interview process for the Senior Software Engineering Position at the LEGO Group. The repository demonstrates my software engineering skills.

![Lego Logo](/assets/lego.jpeg)

## Sample Exercise

Create a mockup source code solution for an application that focuses on image recognition of LEGO bricks, limited to a maximum of two attributes.

### Background Information

The application is intended for use on a production line where machinery is configured to select specific LEGO sets containing the LEGO bricks of interest before initialization. Once configured, the necessary data generation can begin.

### Assumptions

1. We are interested only in specific LEGO bricks from selected LEGO sets.
2. We will generate synthetic data (both 2D and 3D) for the LEGO bricks of interest on the fly.
3. All LEGO bricks are fully disassembled and in flawless (original) condition.

## Solution Layout

1. **Connect to the Database**:
   - Scan a unique ID (order identifier) to retrieve the order history with the complete product summary.
   - Query the following information:
     - Total number of LEGO bricks
     - The CAT models of the specific LEGO bricks

2. **Create Reference Images**:
   - Forward the product ID to the pipeline responsible for generating synthetic images of the LEGO bricks.

3. **Video Stream Processing**:
   - Open a video stream and wait for the LEGO bricks to pass by.

4. **Object Detection and Comparison**:
   - Use state-of-the-art object detectors (YOLOv4 / RT-DETR) and compare the detected objects via a CNN (ResNet-18) against all reference images (support set).
   - Label the detected objects as either "Redundant Brick" if the LEGO brick is not part of the recognized set or with their product ID.
   - Create a dictionary during initialization that tracks all LEGO brick IDs and counts. Decrement the count each time a LEGO brick is recognized. This dictionary will provide information on how many LEGO bricks are missing.


### Flowchart

![LEGO Flowchart](/assets/Lego_Platform_Concept_Flowchart.png)

> Note: This flowchart is a draft version and is subject to change in the future. Its intention is to fully depict the conceptual architecture of a LEGO brick sorting platform.

### Database Design

![Database Design](/assets/db_diagram.png)


## Project Organization

```
├── LICENSE                    <- License file if one is chosen
├── README.md                  <- Top-level README for developers
├── poetry.lock                <- Poetry lock file (dependency resolution)
├── pyproject.toml             <- Poetry project configuration file
├── requirements.txt           <- Traditional requirements file for pip
├── assets                     <- Directory for non-code assets
│   ├── db_diagram.pdf         <- Database Design PDF asset
│   └── db_diagram.png         <- Database Design PNG asset
├── config                     <- Configuration files
│   └── config.yaml            <- Image-recognition configuration file
├── src                        <- Source code root
│   ├── __init__.py            <- Initialization module for src package
│   ├── data                   <- Scripts for data handling
│   │   ├── __init__.py
│   │   └── synthetic_data.py  <- Script for synthetic dummy data generation
│   ├── database               <- Scripts related to database operations
│   │   ├── __init__.py
│   │   ├── config.py          <- Database configuration
│   │   ├── create_dummy_db.py <- Main database script
│   │   └── schema.py          <- Database schema
│   ├── mockup                 <- Scripts for generating mock data
│   │   ├── __init__.py
│   │   └── fake_db_data_generation.py <- Database related operations using dummy data
│   ├── models                 <- Scripts for model training and inference
│   │   ├── __init__.py
│   │   ├── checkpoints        <- Directory for model checkpoints
│   │   ├── custom_dataset.py  <- Example custom dataset script
│   │   ├── image_recognition_train.py <- Image recognition script
│   │   ├── inference.py       <- NotImplemented
│   │   └── video_stream_run.py <- NotImplemented
│   └── utils                  <- Utility scripts and modules
└── unit_tests                 <- Unit tests directory
    └── database.py            <- NotImplemented

```

--------

> Note: The code is not fully functional, and certain parts are not yet implemented
> or connected to other parts in the source code where they are supposed to be integrated.
> The project organization layout (shown above) illustrates these parts.

## Getting Started

To run this project, follow these steps:

1. Clone the repository.
2. Set up the database connection.
3. CD into the src folder.
4. Play around, by executing the provided scripts.


## License

This project is licensed under the MIT License. See the LICENSE file for details.
