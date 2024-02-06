# Involvement of members of the Belgian Federal Parliament 2019-2024
This repository holds code to set up a Dash application to dynamically assess the involvement of members of parliament of the Belgian Federal Parliament.
It uses the data as available on the[website of the Belgian Federal Parliament](www.dekamer.be).

Initial data extraction from the Parliament's website was done using a Jupyter Notebook script (see `code` folder). The resulting data is stored in the `data` folder. 
<!-- However, a `.py` script was rendered of this extraction script to allow extraction outside of a Notebook environment. -->

The eventual implementation is available in .py files in the `dash` folder.

<!-- The data can be updated through the update script located at `code/vlaams_parlement_API_update_data.py`.-->

A working version of the application is available at a [dedicated website](http://erpohk.ddns.net/visualisaties/betrokkenheid-federaal-parlement/). <!-- A cron job is set up to run the update script every Sunday with regard to this application.-->
 

