steps to run the bot:
--------------------
1) run the bot.exe file
2) write the keyword then press enter
3) write the city name, it should be precise (like chicago, salt lake, colorado etc.)
4) then press enter
5) please leave the computer and don't disturb the mouse, bot needs to control the mouse till it starts its process.
6) it will take less than 1 minute
7) after that you can use your pc.
8) bot will take some time to complete the session, you can check the progress on the chrome browser and bot tab.
9) at the end, all the data will be updated in the two files, separately (comments.csv, posts.csv)
10) bot requires a dummy account, you can change login credentials in the text file
11) if you face any problem, just message me on fiverr.

Objectives:
-----------

1) scrape facebook posts data (user name, profile url, location of post, location of user, text of post)
2) scrape all its comments (usernames, their profile links, location, comment text)
3) make two csv files for posts and comments, with the date and time, location, keyword in the file names.

Technical Working of the program:
--------------------------------
1) Goes to facebook, search posts with a specific keyword
2) then selects location provided by the user
3) it selects the frist location from the list, that appears after writing the 
   location name in location_button >> location_bar
5) currently it selects the first location by controlling the mouse using pyautogui
6) mouse points can be changed in the mouse-points.txt file
7) to locate the position of the desired coordinates of the facebook buttton, 
   run the mouse_pos.py file and it will give your screen size and then,
9) open a facebook page, search for a post, type a location
10) then bring the mouse to the first location button. 
    leave it there for a few seconds, then check the log you will be able to identify the 
    coordinate points that appear the most recently.
    
Further Improvements:
---------------------
1) next goal is to remove the functionality of mouse clicking altogether and find the xpath/id/class name of the 
    first location button. It should work for all keywords and location names.
2) location of the user profile works fine if there is a location already,
   if there is not, then the program writes user name in its place.
   Find the unique element of the location only.
3) instead of just one keyword and location, a text file containing lists of keywords and location (like shabbat, newyork) will be provided
   program will loop through them and create separate files for each session. 
