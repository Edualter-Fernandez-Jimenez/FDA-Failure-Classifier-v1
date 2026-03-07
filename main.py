"""
developer: Brian Rodríguez Orozco
email: brian.rodriguez1@ulatina.net or rodriguezbrian2302@gmail.com
id: 20200110702

Application Bootstrap Script.

This is the main execution file that launches the FDA Failure Classifier.
It instantiates the MainApp and starts the graphical event loop.
"""

import view.main_page as mp


if __name__ == '__main__':
    """
    Entry point of the program. 
    Instantiates the MainApp and enters the main loop to listen for user events.
    """
    app = mp.MainApp()
    app.mainloop()