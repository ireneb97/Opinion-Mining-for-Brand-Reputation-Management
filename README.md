# Opinion Mining for Brand Reputation Management

![Alt text](https://miro.medium.com/max/722/1*RGQMR7xPqcpXyZlNTNP3ig.jpeg)

# Introduction
Any brand, nowadays, knows that one of the keys for success in their brand management rely on the opinion that the single customer has about the company. 
Thanks to the usage of their products or services in general, people build in their mind and subsequently online an overall opinion. Using such information to improve the decision making of the company is one of the differences between a leading company and an average one.

A a wide world of data exist online. Every day, millions of consumers add to this data when they share their opinion on a range of things, including feedback about their experiences with products and services. 
Through opinion mining  it's possible to extract as much information as possible to understand thoroughly what the users on social media or on the internet in general think.

# motivation and main steps
Companies can study their specific target and their target response in terms of their business using opinions of the mass. Data mining can be applied to social media and e-commerce sites to extract as much raw data as its needed. In this project we propose the analysis of two different competitors brand: Sony and Micrsoft, basing such analysis on their main products which are their gaming console(Playstation and Xbox,respectively). Since users are very fervent on social media also about the so called "console war" phenomenon, these target are extremely thorough in terms of amount of data, data quality and data sentiment.
two different sources of data where scraped from the internet: amazon and twitter.   
            1) Amazon was thought to be a nice recipient of technical opinions on such products since people leave reviews specifically to criticize or to praise their purchase.   
            2) Twitter, on the other hand, is where is mostly "fought" the console war: people tends to do comparison and listen to other people's response through retweet.                    Furthermore, hashtags can lead the search through raw data in a smart way.  
            
Data where collected from four different sources on Amazon, which are the four main consoles for the two brands: playstation 4, playstation 5, XboxOne, Xbox series.Reviews where simply scraped from the english pages of the products. 
For twitter, two different time windows where chosen, which are basically placed around the release of the old XboxOne console in 2017-2018, and the prerelease&release of the new ones on 2020-2021(Ps5 and XboxSeries). 

# main goal
We want to extract as much information as possible about how user perceive the company based on their gaming purchase habit. Moreover, we would like to recognize the criticalities of the business strategy adopted by the brand. Such information may be useful by the company to compensate weakenesses in their decision making.

# data analysis performed
Preprocessing where performed on the raw data accordingly to the source. For more detail, we suggest the reader to check in detail the code.

Exploratory data analysis was performed to study data and analyze their distribution related in terms of time and sentiment.

Unsupervised learning techniques like k-means and Gaussian Mixture Model where used to cluster data in a proper way. Topics where extracted to understand more deeply the strengths and weaknesses related to each product.

# snippet of the results
Nice and informative clusterization and topics where extracted from the data. Entire clusters dedicated to specific topics where identified when analyzing tweet, recognizing those elements that made people tweet the most. Here is reported an example:
![Alt text](https://i.gyazo.com/70c5b1af31472d06047ef95cd9dac6a4.png)


