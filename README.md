# Deel

## Overview
This repository contains a technical challenge project named "Deel." The project focuses on reversing client IP addresses and storing them in a SQLite database.

## Features
- Extracts client IP addresses even when behind a proxy
- Reverses the IP addresses
- Stores reversed IP addresses in a SQLite database

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BoazHalter/Deel.git
   cd Deel
## Run the application:

Access the application through your web browser at http://localhost:5000. It will display the reversed IP address of the client and store it in the database.

## Files
- app.py: The main application file.
- Dockerfile: Configuration for building a Docker image.
- .github/workflows: Contains GitHub Actions for CI/CD (since deployed localy no automated CD).
- ip-reverse-chart: Helm chart for deploying the application on Kubernetes.
