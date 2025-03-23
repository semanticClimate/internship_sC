## Documentation for the ```html_with_ids``` folder
```html_with_ids``` folder contains following files:-

1. [workflow_html.py](https://github.com/semanticClimate/internship_sC/blob/sharon/html_with_ids/workflow_html.py)
2. [edit_command.JSON](https://github.com/semanticClimate/internship_sC/blob/sharon/html_with_ids/edit_command.json)
3. [fetched_html.html](https://github.com/semanticClimate/internship_sC/blob/sharon/html_with_ids/fetched_html.html)
4. [processed_html_ccp7.html](https://github.com/semanticClimate/internship_sC/blob/sharon/html_with_ids/processed_html_ccp7.html)
5. [html_with_ids.py](https://github.com/semanticClimate/internship_sC/blob/sharon/html_with_ids/html_with_ids.py)
6. [html_with_ids.html](https://github.com/semanticClimate/internship_sC/blob/sharon/html_with_ids/html_with_ids.html)

### Explaining each file

* [workflow_html.py](https://github.com/semanticClimate/internship_sC/blob/sharon/html_with_ids/workflow_html.py)

  In this file following steps occur:-

  1. _Fetch and clean the HTML._  After fetching & cleaning, you get file - [fetched_html.html](https://github.com/semanticClimate/internship_sC/blob/sharon/html_with_ids/fetched_html.html)
  
  2. _Load deletion commands from the JSON file._ Deletion command file - [edit_command.JSON](https://github.com/semanticClimate/internship_sC/blob/sharon/html_with_ids/edit_command.json)
  
  3. _Strip and modify the HTML based on the commands._
  
  4. _Save the final stripped HTML to the output file._  Output file named as processed file - [processed_html_ccp7.html](https://github.com/semanticClimate/internship_sC/blob/sharon/html_with_ids/processed_html_ccp7.html)
 
   This output file ```processed_html_ccp7.html``` is processed manually also by changing some heirarchy divs to make a better html file.
  
* [html_with_ids.py](https://github.com/semanticClimate/internship_sC/blob/sharon/html_with_ids/html_with_ids.py)

  Taking the output from above and using it to add ids to each divs and getting output as ```html_with_ids.html```

  The ```html_with_ids.py``` file contains the code in python for adding ids to each divs in the ```processed_html_ccp7.html``` and saving the output file as a html file - [html_with_ids.html](https://github.com/semanticClimate/internship_sC/blob/sharon/html_with_ids/html_with_ids.html)

> Short document of my work.
