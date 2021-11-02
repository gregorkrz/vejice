# VejiceBot

Chatbot to help practice commas in Slovene. Try it out on Telegram: https://t.me/vejicebot
The Vejica corpus (https://www.clarin.si/repository/xmlui/handle/11356/1185) is used for training examples.

### Setup

Download sentence embeddings (https://k00.fr/0fbxwuis) and put the file into `models/`.
Alternatively, generate them from scripts/ directory. A very simple autoencoder is used to try to capture the part-of-speech structure of the sentences.
The embeddings will be used for the very simple recommendations.

### Deployment

`Procfile` and `runtime.txt` should tell Heroku or similar services how to deploy.

