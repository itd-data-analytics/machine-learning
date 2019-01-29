# Machine Learning

# Authors
  - Hayden Phothong (Research Analyst Intern @ ITD)
  - Chapman Munn (Data Analytics Manager @ ITD)

# Notes:
The definition of having a guardrail is kind of different for traffic. In order to evaluate to "True" the image must have a visible guardrail in the lower right quadrant of the image (this is if you split the image into 4 equal sections). This is done due to the location matching to the ascending direction only. All other images that contain guardrails outside of the lower right quadrant are considered "False".

## The classifier
The classifier is a Tkinter window that allows the user to classify images and have that data stored to the local SQLite3 database named "ImageRecognition.db". All of the filepaths are relative, therefore, the structure of the code must remain intact for the programs to work correctly. The data that is stored in the SQLite3 database is also relative pathing, therefore, this produces the same issue with structure and location of the database file in relation to the source code.
