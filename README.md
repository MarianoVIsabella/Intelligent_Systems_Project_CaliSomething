# Fake News Detection MAS
This repo is intended for a project inside the Intelligent Agents module of Intelligent Systems course in AI & CS master Degree in Unical during A.Y 2025/26.
The course was held by prof. Calimeri F. and dr. Duca M.  
Group Members:  
Isabella Mariano Vincenzo  
Casella Alessandro  
Goitom Meles Negash  

## What's it
The aim of the project is to create a MAS to analyze news and understand whether they are real or fake news. To do so, a online interface was developed with Streamlit, where the user can enter the input news. The news is then analyzed by the following pipeline:
- Via NLTK and Spacy a sentiment analysis is performed on the news, and the output is also considered to determine the nature of the news
- A Domain Expert Agent reviews the news in order to understand the domain(s) of interest
- Five different Judge Agents, each with its own personality, debate whether the news is real or fake
- One last Verdict Agent sums up the votes of each Judge Agents and provides the final verdict

## Structure

### outputs Folder
This folder contains the reasoning of each agent in markdown files they generate, useful to debug and have better clarifications on why a news is labelled as real or fake.

### src Folder
This folder is the core of the project. At this level there are other folders and some utility files:
- The requirements.txt contains the dependencies of the project
- crew.py is the file where the final crew of agents is assembled
- streamlit_app.py is the file that launches the application, providing the web interface
- orchestrator.py is the file that handles the execution of the crew
- The tools folder contains the customized tools needed to do the sentiment analysis and the domain classification.
- The config folder contains the yaml files for both agents and tasks definition. 



