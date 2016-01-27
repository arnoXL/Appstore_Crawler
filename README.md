# Appstore_Crawler
This is a project completed by me under the instruction of bittiger's staff.

This is a crawler used to crawl down the app info from Huawei Android Market website. Written in Python 2.7.

1. It will crawl down the app info, including appID, url, title, introduction, url of the app's thumbnail, and recommended apps for each app.

2. The crawled data will be saved in the "appstore.dat" file. (The "appstore.dat" file just stores first 5 pages of two list on homepage and all the searches, you can just uncomment and comment some code in "huawei_spider.py" to get all apps info. The details can be found in that file's comments.)

3. The apps in each list on the homepage will be crawled down. Also apps which are relevant in the themes listed below will also be crawled down: "game", "software".

4. It uses splash and scrapyjs to render javascript on the website. The splash service is assumed at http://192.168.99.100:8050, you can change it to your splash service in settings.py file.

5. The program will use random proxy for user-agent in order to crawl the data from Huawei website without being obstructed.