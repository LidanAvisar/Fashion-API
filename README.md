# Fashion API

## Overview
Our Fashion API leverages AI and computer vision to recommend personalized outfits based on user preferences or uploaded photos. It includes a virtual try-on feature that enhances the online shopping experience by allowing users to see how clothes would look on them virtually.

## Demo
Check out our demo video to see the Fashion API in action: [Fashion API Demo](https://youtu.be/dgodYz6R7hA)

## Features

### Photo Upload
- **Upload a photo** of an outfit you like.
- Utilizes **OpenAI Vision API** and **Hugging Face's Embedding Library** to analyze the photo and find similar styles in our database.

### Style Quiz
- Take a quick **style quiz** if you don't have a specific outfit in mind.
- Recommends outfits that match your taste based on your answers.

### Virtual Try-On
- After selecting an outfit, use our **virtual try-on feature** to see how the outfit looks on you.
- Powered by advanced computer vision technology.

## Technologies Used
- **FastAPI**: For building the API.
- **OpenAI Vision API** and **Hugging Face Embedding Library**: For photo analysis and style matching.
- **SQLite**: For data management.
- **CVZone API** and **CV2 API**: For motion analysis and frame processing.
- **Docker**: For containerization.
- **Azure**: Hosting and CI/CD with Azure Pipelines.
- **GitHub**: Version control and Continuous Integration.

## Continuous Integration
Each push to the repository triggers Azure Pipelines which automatically publishes the latest version of our code to Azure, ensuring that our application is always up-to-date with the latest features and bug fixes.

## Getting Started
To get started with using the Fashion API, please visit the following link: [Fashion API Documentation](https://apiimage--qwk2g5c.jollyforest-8bfb57eb.eastus.azurecontainerapps.io)

## Instructor
- David Kalmanson

## Contributors
- Lidan Avisar
- Neta Handelsman


