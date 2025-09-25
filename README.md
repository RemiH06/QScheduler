![Made with Python](https://forthebadge.com/images/badges/made-with-python.svg)

```ascii
 ██████╗ ███████╗ ██████╗██╗  ██╗███████╗██████╗  
██╔═══██╗██╔════╝██╔════╝██║  ██║██╔════╝██╔══██╗ 
██║   ██║███████╗██║     ███████║█████╗  ██║  ██║ 
██║▄▄ ██║╚════██║██║     ██╔══██║██╔══╝  ██║  ██║ 
╚██████╔╝███████║╚██████╗██║  ██║███████╗██████╔╝ 
 ╚══▀▀═╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝  

       by Hex (@RemiH06)          version 3.0
```

### General Description

```diff
- THIS PROJECT DOESN'T WORK ANYMORE (since august 2025) due to two factor auth is now needed to login into anything related to ITESO. 
- Its sole purpose now is to be used as a learning tool for people interested in creating email senders or scrapers.
- If you're reading this, thank you very much for the interest. 
```

Scheduler for Outlook meetings, two weeks in advance (sender uses scheduler). NOT RECOMMENDED ❌

Scheduler for meetings via smartway2book (sch uses scraper). RECOMMENDED ✅

I created this originally to reserve cubicles at ITESO's library, but at least for these purposes it stopped working since they moved their system to smartway2book. Because of this I had to create a scraper. It works and it's functional.

## Installation

1. Install requirements with the following command :

   `pip install pywin32`
   `pip install python-dotenv`
   `pip install playwright`

2. Make sure you have the webdriver for a chrome version

   If you're trying to use the old version make sure you have Outlook (old) installed (only works with MS tho)

3. Secrets

   You will need to create a .secrets file with 2 params: email and password

4. Task Scheduler

   Used MS Task Scheduler to program the task so it runs everyday


## Future Features

- GUI
- More browsers support
