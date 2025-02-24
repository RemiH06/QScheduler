![Made with Python](https://forthebadge.com/images/badges/made-with-python.svg)

```ascii
 ██████╗ ███████╗ ██████╗██╗  ██╗███████╗██████╗  
██╔═══██╗██╔════╝██╔════╝██║  ██║██╔════╝██╔══██╗ 
██║   ██║███████╗██║     ███████║█████╗  ██║  ██║ 
██║▄▄ ██║╚════██║██║     ██╔══██║██╔══╝  ██║  ██║ 
╚██████╔╝███████║╚██████╗██║  ██║███████╗██████╔╝ 
 ╚══▀▀═╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝  

       by HectorH06 (@HectorH06)          version 3.0
```

### General Description

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
