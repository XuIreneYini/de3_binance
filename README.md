# Data Engineering 3: Real-time Data Processing & API

This repository contains the final project for the ECBS5211 course. It includes a Python-based API for crypto analytics and an automated data pipeline for price monitoring.

## 🚀 Features

### 1. Crypto Analytics API (ECS & Fargate)
A FastAPI-based application deployed using Docker and AWS ECS/Fargate.
- **Summary Endpoint**: Returns min/mean/max price stats in JSON.
- **Volume Chart**: Generates a real-time PNG bar chart of trading volume.
- **Data Export**: Allows downloading historical klines data in CSV format.
- **Dashboard**: An interactive HTML page integrating analytics and visualizations.

### 2. Price Monitoring Pipeline (Jenkins)
An automated pipeline that tracks ETH prices every hour.
- **Real-time Alerts**: Calculates hourly price volatility and sends summaries to MS Teams.
- **Automation**: Managed via Jenkins with periodic build triggers and email notifications.

## 🛠 Tech Stack
- **Languages**: Python (FastAPI, Pandas, Matplotlib)
- **Cloud**: AWS (ECR, ECS, Fargate, EC2)
- **DevOps**: Docker, Jenkins, Git
- **Tools**: Binance API, Apprise (MS Teams Webhooks)


