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

Scheduler for Outlook meetings, two weeks in advance

I created this originally to reserve cubicles at ITESO's library, but it's obsolete (at least for these purposes) since they moved their system to a local webpage.

## Installation

1. Install requirements with the following command :

   `pip install pywin32`
   `pip install python-dotenv`

2. Make sure you have Outlook (old) installed

3. Windows Only

   If you have another OS, replace the win32 libraries in order for you to access Outlook

4. Secrets

   You will need to create a .secrets file with 2 params: email and location

5. Task Scheduler

   Used MS Task Scheduler to program the task so it runs everyday


## Future Features

- GUI
