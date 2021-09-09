# WhatToWatch

## What is it and what does it do?

### Description
What to Watch application is a personalized service that will allow users to track upcoming Movies and TV Shows, get recommendations based on their preferences and watchlist history, and create events to schedule watch parties with friends.

### Problem to Solve 
At present, if one wants to track the release date of movies or air date of tv shows, get movie recommendations, and create watch parties to watch TV together with friends, they need to use multiple mobile and/or web applications as there is no option in the market to achieve them in one application. 
Our goal is to minimize the effort of the user and provide them with all the aforementioned services in one location and more.

### Features
-   Users can track upcoming movies/Tv shows and get Notified via email/message. It shows the new episodes that have been released, for the shows that you are currently watching and keeps track of the watched episodes.
-   Provides a watchlist to add/remove a show or a movie. Watchlist is a placeholder from where we can start watching a show
-   Users can see Trending shows and search for Movies/TV based on genre or title.
-   Personalized Recommendation for movies and tv shows based on user preference and watchlist history. Factors like the completed shows, stopped watching shows, added to watchlist, along with the preference data will be considered for giving recommendations using AWS Personalise which uses a hierarchical recurrent neural network (HRNN).
-   Holds a Social Page where users can follow/unfollow friends and see what they are currently watching.
-   Plan watch parties and invite friends (through joining link). Invitees receive event links through email and can choose to accept or decline from the social page.


## What is the design and what all resources are needed? 

### Architecture Design

<img alt="architecturediag" src="https://user-images.githubusercontent.com/26367904/123538222-69115b00-d751-11eb-84b0-bd7b11949b7a.png">

### AWS Services used
-   **Amplify**: Amplify is used to host the web application and deployment of cognito as well as the front-end code, which is developed using Vue.js
-   **API Gateway**: API gateway is used to decouple frontend and backend and provide rest api architecture for the application
-   **Cognito**: Cognito provides account management services like user sign-up, sign-in and access control
-   **Dynamo DB**: The movie and tv show data from the moviedb api is scraped periodically and loaded into the Dynamodb table
Schema:  id, type, title, year, genre, episodes, poster_url, overview
-   **Cloud Watch**: Triggers the Lambda function every night to lead data into Dynamodb table from the moviedb api
-   **Elastic Search**: Elastic search is used to provide search functionality and user can search by genre and title
-   **Lambda**: Various lambda functions are used for backend serverless computing and connecting services
-   **SQS**: SQS is used to queue up the watch party invitations from different users
-   **SNS**: SNS is used to notify users via email, about their watch party invitation
-   **RDS**: Web application backend data is stored in various RDS tables built on MySQL
    Schema:
    user - <ins>userid<ins>, name, email
    watchnow - <ins>userid<ins>, <ins>id<ins>, name, type, poster_path, episode, air_date
    watchlist - <ins>userid<ins>, <ins>id<ins>, <ins>type<ins>, poster_path, release_date
    friend - <ins>userid<ins>, <ins>friendid<ins>, friendname
    event - <ins>eventid<ins>, description, time, invitee, creator url, status
    preference - <ins>userid<ins>, <ins>genre<ins>
	***Note***: Primary Keys are <ins>underlined<ins>
-   **S3**: stores historical data for fine tuning the AWS Personalise ML model
-   **Personalise**: Real-time recommendations are provided using AWS Personalise   
