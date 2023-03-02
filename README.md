# Python bs4 mongodb webscraping
## Title: Forum Scraper and MongoDB Cloud Storage  
 
 Description: This repository contains a Python-based web scraper that retrieves data from website forums and stores it in MongoDB cloud. The scraper can be customized to extract specific data elements from forum threads, including the title, author, post date, and content. The scraped data is then stored in a MongoDB cloud database, making it easily accessible for further analysis. Customizable scraping options: the scraper is highly customizable, allowing you to extract the data elements that are most relevant to your analysis. Automatic data storage: once the data has been scraped, it is automatically stored in a MongoDB cloud database, making it easy to manage and access. Simple deployment: the scraper can be easily deployed to a cloud-based service like Heroku, allowing you to run it on a schedule or as needed. Overall, this repository provides a flexible and powerful tool for collecting and storing forum data in the cloud, making it ideal for researchers, analysts, and anyone else who needs to work with online discussion forums.
 
 # Usage
 1. Clone the repository:

 `git clone https://github.com/bmuzuraimov/Forum-Scraper-and-MongoDB-Cloud-Storage.git`
 
 2. Install the required dependencies:
 ```
 cd yourproject
 pip install -r requirements.txt
 ```
 
 3. Set up the .env file:
 Create a .env file in the root directory of the project and add the following variables, replacing the values with your own MongoDB credentials:
 ```
 MONGODB_USERNAME=yourusername
 MONGODB_PASSWORD=yourpassword
 MONGODB_DBNAME=yourdbname
 MONGODB_CLUSTERNAME=yourclustername
 ```

 4. Run the application:
 ```
 python3 main.py --action scrape_forum
 python3 main.py --action scrape_discussions
 ```
 The first command will store all forums on MongoDB Cloud.
 The second command will update existing forums with their content data.

