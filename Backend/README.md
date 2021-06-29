# WhatToWatch - Backend

## About
WhatToWatch application has a scalable and resilient microservices architecture based backend which uses Amazon API Gateway, Lambda functions, Dynamo DB, Amazon RDS, Amazon SQS, Amazon SNS and Amazon Personalize. 


## Lambda Functions and associated API calls
API gateway is used and URL the path in it depends upon the application page and API calls based on their names. Details are given for the path and calls associated with each page within the application.

### Preference(s) page  
1.  API Call: **/account**  
    Method: GET  
    Lambda: ***load_account***  
    Purpose: Loads the User's details and preferences  

2.  API Call: **/account/update**  
    Method: POST  
    Lambda: ***lf1_update***  
    Purpose: Updates the details in the preference table  

### Home Page   
1.  API Call: **/watch**  
    Method: GET  
    Lambda: ***load_home***  
    Purpose: Loads 'Watchlist' and 'Watchnow' features for the home page  

2.  API Call: **/watch/addlist**  
    Method: POST  
    Lambda: ***lf2_addlist***  
    Purpose: Adds TVshow/movie to the 'Watchlist'  

3.  API Call: **/watch/removelist**  
    Method: POST  
    Lambda: ***lf2_removelist***  
    Purpose: Removes the TVshow/movie from the 'Watchlist'  

4.  API Call: **/watch/addnow**  
    Method: POST  
    Lambda: ***lf2_addnow***  
    Purpose: Adds a TVshow/movie records to 'Watchnow' and removes from the 'Watchlist'  

5.  API Call: **/watch/donenow**  
    Method: POST  
    Lambda: ***lf2_donenow***  
    Purpose: Removes completed TV show episodes or movies from the 'Watchnow'  

6.  API Call: **/watch/removenow**  
    Method: POST  
    Lambda: ***lf2_removenow***  
    Purpose: Removes all episodes/movie from 'Watchnow'  

7.  API Call: **/rating**  
    Method: POST  
    Lambda: ***update_model***  
    Purpose: Appends the rating for a TV show or a movie that a user has marked as watched to the interaction dataset on AWS Personalize to re-train the model and provide real-time recommendations  

### Search Page  
#### Trending and Recommendation
1.  API Call: **/recommend**  
    Method: GET  
    Lambda: ***load_search***  
    Purpose: Returns recommendations based on AWS Personalize and User preference, along with the trending movies/tv shows for search page  

#### Search results for the query
2.  API Call: **/search**  
    Method: GET  
    Lambda: ***lf3_search***  
    Purpose: returns TV shows and movies based on title or genre searched in the search box. This is done using the ElasticSearch service and dynamo DB  

### Social - Friends Page 
1.  API Call: **/friend**  
    Method: GET  
    Lambda: ***load_friend***  
    Purpose: Loads the friend list for the friends page  

2.  API Call: **/friend/add**  
    Method: POST  
    Lambda: ***lf4_addfriend***  
    Purpose: Adds a new friend to the 'friends' table  

3.  API Call: **/friend/remove**  
    Method: POST  
    Lambda: ***lf4_removefriend***  
    Purpose: Removes the friend from the 'friends' table  

### Social - Events Page 
1.  API Call: **/social**  
    Method: GET  
    Lambda: ***load_social***  
    Purpose: Load your friends' watching list and events list  

2.  API Call: **/social/createevent**  
    Method: POST  
    Lambda: ***lf5_eventcreate***  
    Purpose: Add a record for every invitee into event table with the status as 'pending' and with the status as 'accepted' for the creator and adds these details to SQS  

3.  API Call: **/social/createstatus**  
    Method: POST  
    Lambda: ***lf5_createstatus***  
    Purpose: Updates records in invitation with the status like accepted, declines, etc  

### General Functions using lambdas - NOT API calls 
1.  Lambda: ***data_load***  
    Purpose: Scrapes data from the 'moviedb' upon nightly trigger from Cloudwatch and loads into Dynamodb to keep the movie and TV show dataset up to date  

2.  Lambda: ***add_user***  
    Purpose: Adds user data to the user table upon invocation of the post authentication trigger in the Amazon Cognito service  

3.  Lambda: ***load_trending***  
    Purpose: Loads trending movies/shows in the database from 'moviedb' api   

4.  Lambda: ***lf6_notification***  
    Purpose: Polls queued events from SQS and sends email notification to users through SES  

## Data Source
The data is scraped from the [moviedb api](https://www.themoviedb.org/documentation/api) by a lambda function triggered using the Cloudwatch Event and then Loaded into the DynamoDb table. The following data gets scraped from the api:
-   Movie and TV Show Details and Release Dates
-   Trending Movie and TV Shows


## Recommendation System 
The system provides cross-platform movie and tv show recommendations based on user genre preference and ratings. 

### Recommendation using AWS Personalize
#### Model:
The system uses AWS User Personalization recipe, which is a hierarchical recurrent neural network (HRNN), and it models changes in user behavior to provide recommendations during a session. HRNN accommodates user intent and interests, which can change over time. It takes ordered user histories and automatically weights them to make better inferences. HRNN uses a gating mechanism to model the discount weights as a learnable function of the items and timestamps. In our system, the model uses ratings and genre information of the movies and tv shows for each of our users, and provides them with personalized recommendations in real-time.

#### Model Update in Real-time:
The system captures the user rating after they complete watching a tv show episode or a movie. This rating and genre information of the show or movie is added to the AWS Personalize event tracker with the help of a Lambda function in real-time. This tracker then updates the user interactions dataset with the new ratings, which then triggers the machine learning model to update in real-time to provide new recommendations

***[Guide for personalized movie recommendations](https://aws.amazon.com/getting-started/hands-on/real-time-movie-recommendations-amazon-personalize/)***

### Recommmentation using ElasticSearch 
Users can select their genre preferences from the preference page, and the system provides recommendations based on that using Elastic Search service.