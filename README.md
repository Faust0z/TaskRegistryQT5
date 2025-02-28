# Simple Task Registy
This app is meant to be a simple way to register and list your tasks aided by a GUI made on PyQt5. 

This app does:
1. Allows you to create your own types of tasks (and also delete them).
2. Allows you register every time you do those tasks (and also delete them).
3. Provides data persistence by using CSV files: one for the tasks done and another for the types of tasks registered.
   4. The routes for each csv can be changed in the [csvmanager.py](csvmanager.py) file.
4. Simple use with the GUI. 

The app currently doesn't support tasks that begin in a day and finish on another. It's such an edge case that I didn't even bother accounting for it.

Honestly, this project would be better suited to a database, since that would take care of a lot of type checking and formatting that I had to take into consideration, but it was meant to be a practice exercise.

To use, either download latest release or download the project and install the requirements.txt
