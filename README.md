# jmcomic-exe Project

## Overview
This project is designed to utilize the `jmcomic` library to provide a comic management application. It includes various components that interact with the library and facilitate the main functionalities of the application.

## Project Structure
```
jmcomic-exe
├── src
│   ├── main.py          # Entry point of the application
│   ├── jmcomic_client.py # Handles interactions with the jmcomic library
│   └── utils.py         # Utility functions for data processing
├── requirements.txt     # Python dependencies
├── build.sh             # Shell script for building the project on Linux
├── build.ps1            # PowerShell script for building the project on Windows
├── .gitignore           # Files and directories to ignore in version control
└── README.md            # Project documentation
```

## Installation
To install the required dependencies, run the following command:

```
pip install -r requirements.txt
```

## Usage
To run the application, execute the following command:

```
python src/main.py
```

## Building the Executable
To build the project and create an executable, use the appropriate script based on your operating system:

- For Linux:
  ```
  ./build.sh
  ```

- For Windows:
  ```
  .\build.ps1
  ```

## Contributing
Feel free to submit issues or pull requests if you would like to contribute to this project.