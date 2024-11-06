# Ticket Automation Project

This project automates the management and updating of tickets within a JIRA system, leveraging data from external sources. It is intended to streamline ticket processing by converting CSV data into JSON format and updating JIRA tickets with the relevant details based on risk levels and other criteria.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Resources](#resources)

## Project Overview

The Ticket Automation Project is designed to enhance ticket management efficiency by automating parts of the process, especially for large teams managing complex workflows. The system:
- Reads and converts CSV data into JSON format for easier data handling.
- Interacts with JIRA using an API, updating tickets based on predefined criteria (e.g., risk level).
- Supports a straightforward configuration through environment variables.

For a more detailed overview, please refer to the [project presentation](https://drive.google.com/file/d/1xUtINLrt09F1nBuPau_z0xjDJ_QTVk0V/view?usp=sharing).

## Features

- **CSV to JSON Conversion**: Quickly converts CSV files to JSON format, making data integration seamless.
- **JIRA Integration**: Uses JIRA’s API to update tickets based on data-driven decisions.
- **Risk-Based Due Dates**: Sets ticket due dates according to risk levels (Critical, High, Medium, Low).
- **Flexible Configuration**: Environment-based configuration for secure API access.
