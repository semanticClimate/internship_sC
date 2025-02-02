Task: Evaluate the functionality of summarization model (https://huggingface.co/facebook/bart-large-cnn).

Checked through Google Colab https://colab.research.google.com/drive/1q73FJ1Bw0RDqENpnok8pRN1jrtaBk_xn?usp=sharing#scrollTo=6jBQG4fbhmsG\

Took two different articles to evaluate the model (https://www.who.int/emergencies/disease-outbreak-news/item/2025-DON550 , https://www.ipcc.ch/report/ar6/wg2/chapter/ccp6/)

## Install transformers
`!pip install transformers`

<br>

* Pipeline imported from transformers and model mentioned
* Article pasted


`from transformers import pipeline`

`summarizer = pipeline("summarization", model="facebook/bart-large-cnn")`

`article = """Situation at a glance
In many countries of the Northern Hemisphere, trends in acute respiratory infections increase at this time of year. These increases are typically caused by seasonal epidemics of respiratory pathogens such as seasonal influenza, respiratory syncytial virus (RSV), and other common respiratory viruses, including human metapneumovirus (hMPV), as well as mycoplasma pneumoniae. Many countries conduct routine surveillance for acute respiratory infections and common respiratory pathogens. Currently, in some countries in the temperate Northern hemisphere, influenza-like illness (ILI) and/or acute respiratory infection (ARI) rates have increased in recent weeks and are above baseline levels, following usual seasonal trends. Seasonal influenza activity is elevated in many countries in the Northern hemisphere. Where surveillance data is available, trends in RSV detections currently vary by region with decreases reported in most regions except in North America. Recently, there has been interest in hMPV cases in China including suggestions of hospitals being overwhelmed. hMPV is a common respiratory virus found to circulate in many countries in winter through to spring, although not all countries routinely test and publish data on trends in hMPV . While some cases can be hospitalized with bronchitis or pneumonia, most people infected with hMPV have mild upper respiratory symptoms similar to the common cold and recover after a few days. Based on data published by China, covering the period up to 29 December 2024, acute respiratory infections have increased during recent weeks and detections of seasonal influenza, rhinovirus, RSV, and hMPV, particularly in northern provinces of China have also increased. The observed increase in respiratory pathogen detections is within the range expected for this time of year during the Northern hemisphere winter. In China, influenza is the most commonly detected respiratory pathogen currently affecting people with acute respiratory infections. WHO is in contact with Chinese health officials and has not received any reports of unusual outbreak patterns. Chinese authorities report that the health care system is not overwhelmed and there have been no emergency declarations or responses triggered. WHO continues to monitor respiratory illnesses at global, regional and country levels through collaborative surveillance systems, and provides updates as needed."""`

<br>

* Device set to use cpu
 

### Executed using the default parameters.

`testsumm = summarizer(article, max_length=130, min_length=30  , do_sample=False)`\
`testsumm[0]['summary_text']`

### Output
`In some countries in the temperate Northern hemisphere, influenza-like illness (ILI) and/or acute respiratory infection (ARI) rates have increased. These increases are typically caused by seasonal epidemics of respiratory pathogens. These include seasonal influenza, respiratory syncytial virus (RSV), and other common respiratory viruses.`

```
From this I noticed that the output only contains the input article's first three lines.

I changed the parameters and increased both minimum and maximum word length to 70 and 250 respectively.
```

### Output
`In some countries in the temperate Northern hemisphere, influenza-like illness (ILI) and/or acute respiratory infection (ARI) rates have increased. These increases are typically caused by seasonal epidemics of respiratory pathogens. These include seasonal influenza, respiratory syncytial virus (RSV), and other common respiratory viruses, including human metapneumovirus (hMPV).`

It added the next sentence from the article to the previous output.

<br>

Out of curiosity I took a small paragraph from https://www.ipcc.ch/report/ar6/wg2/chapter/ccp6/ and it's word length is less than the default one.

### Output
`Your max_length is set to 130, but your input_length is only 120. Since this is a summarization task, where outputs shorter than the input are typically wanted, you might consider decreasing max_length manually, e.g. summarizer('...', max_length=60)`

From this output, it is evident that the word length of the query article must exceed the specified parameters.

