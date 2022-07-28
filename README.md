# WebCrawler
This web scrapper scrap the publication of all publishers of coventry university and then stores it to CSV file
This crawler uses Selinium and Beautiful soup laibraries of python. But as selinium is slow , therefore selenium is used only where absolutely necessary. 
The crawler scraps the web using Breadth First Search(BFS).Firstly, it goes through all pages of the website and stores the links of every author into an 
queue named as authour_url_list . Function named as crawling do this job and then from that queue it pop out the url and then scrap that url to find the publication name,publication year,and publication URL along with aurhor name and saves it to csv file. Function named as depth_crawling do this task. 
