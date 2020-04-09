# AliexpressOrderHelper

AliexpressOrderHelper is a simple tool that helps you to get summary about your orders. Because of the absence of customer API at Aliexpress side this tool is using <a href="https://github.com/SeleniumHQ/selenium/tree/master/py">Python Selenium.</a><br>
Currently this tool has very limited functionality, but it will be expanded later.<br>

<strong> TODO: </strong>
1. Multiaccount (reading from a txt file, that contains multiple accounts)
2. More functionality (dispute status, order description, account level etc.)
3. Efficiency (opening webdriver every time is veeery slow)

<strong> Usage: </strong>
1. Install geckodriver for browser that you wish to use, for example <a href="https://github.com/mozilla/geckodriver"> Firefox</a>
2. Pass your data in <code>writing_to_db.py</code> file:
<code>get_information = Aliexpress(
      driver=webdriver.Firefox(), login='', password=''
    ).getting_orders() </code> Your account's data is not going to be saved into local database. <br>
Local database <code> AliexpressOrderData.db </code> is gonna be created in folder of repo.
After job is done, you will see table with your orders.
