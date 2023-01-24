
try:
    import time
    import re
    from datetime import date, datetime
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import Select
    from bs4 import BeautifulSoup
    import pandas as pd
    from csv import writer
    import pyautogui
except Exception as e:
    print("Error while importing libraries: ", e)


print("----------------------Session Started-----------------------")
keyword = input("Please Enter Keyword: ")
location = input("Please Enter Location: ")

#browser user agent here

try:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
    options = uc.ChromeOptions()
    # options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    #options.add_argument("--start-maximized")
    options.add_argument("--window-position=0,0")
    options.add_argument("--window-size=1366,768")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False,
             "profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
except Exception as e:
    print("Error while creating driver :", e)

#login function here
try:
    with open("login_credentials.txt", "r") as f:
        lines = f.readlines()
        USERNAME = lines[0]
        PASSWORD = lines[1]

    # logging in
    driver.get("https://www.facebook.com/login")
    # Use Selenium to login to Facebook (you will need to enter your own login credentials here)
    time.sleep(5)
    username = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    username.send_keys(USERNAME)
    password = wait.until(EC.visibility_of_element_located((By.ID, "pass")))
    password.send_keys(PASSWORD)
    time.sleep(5)
    login_button = wait.until(EC.visibility_of_element_located((By.ID, "loginbutton")))
    login_button.click()
    time.sleep(5)
except Exception as e:
    print("Error while logging in: ", e)



#redundant function
def main_search(keyword):
    '''
    :param keyword:
    :return: dict of data
    '''
    driver.get('''https://www.facebook.com/search/posts?q=%20'''+keyword)

    print("Loading posts...")
    for i in range(0,10):
        #multiple scrolling
        time.sleep(2)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")



    # Use Beautiful Soup to parse the HTML of the search results page

    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Find all the posts on the page using the Beautiful Soup object
    posts = soup.find_all("div", class_="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")

    count=0
    # Loop through the posts and print the text of each one
    data_list=[]
    for post in posts:

        #print("POST ", post.prettify())
        # print("POST TEXT", post.text)

        # profile_name = post.findNext("div", class_="x1i10hfl xjbqb8w")
        # print("profile_name :", profile_name.text)

        #counter
        count=count+1
        print("POST: ", count)
        post_dict={}

        try:
            profile_name=post.find("a", class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f")
            print("profile_name: ", profile_name.text)
            post_dict["profile_name"]=profile_name.text

        except:
            "no profile name found"
            post_dict["profile_name"] = "na"

        try:
            #same class as profile name
            profile_url=post.find("a", class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f").get("href")
            print("profile_url: ", profile_url)
            post_dict["profile_url"] = profile_url.text
        except:
            "no profile_url found"
            post_dict["profile_url"] = "na"

        try:
            post_text= post.find("div", class_="x11i5rnm xat24cr x1mh8g0r x1vvkbs xdj266r x126k92a")
            print("post_text:", post_text.text)
            post_dict["post_text"] = post_text.text

        except:
            print("no post text")
            post_dict["post_text"] = "na"

        try:
            post_date=post.find("span", class_="x4k7w5x x1h91t0o x1h9r5lt xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j x1jfb8zj").text
            print("post_date :", post_date)
            post_dict["post_date"] = post_date
        except:
            print("no post date found")
            post_dict["post_date"] = "na"
        try:
            post_url = post.find("a", class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm").get("href")
            print("post_url :", post_url)
            post_dict["post_url"] = post_url
        except:
            print("no post url found")
            post_dict["post_url"] = "na"

        data_list.append(post_dict)
        df = pd.DataFrame(data_list)
    return df

def comments_of_post(post_link, keyword):
    '''
    :param post_link: url link of a post
    :return: list of comments dict: text, writer name, profile url
    '''

    #post_link='''https://www.facebook.com/sandra.torres.5201/posts/pfbid02xnkyMmDZWSomLZRWSz95187kJudzi8SDuyMhvTAAXYv5tHBtncDqVVSQahiwBm2tl'''
    driver.get(post_link)
    time.sleep(2)
    #loading comments
    for i in range(0, 5):
        # multiple scrolling
        time.sleep(2)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Find all the posts on the page using the Beautiful Soup object
    comments = soup.find_all("div", class_="xdl72j9 x1iyjqo2 xs83m0k xeuugli xh8yej3")

    comments_list=[]
    count=0
    for comment in comments:
        count=count+1
        print("COMMENT : ", count)
        comment_dict={}

        try:
            comment_writer=comment.find("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa x1s688f xzsf02u")
            print("comment_writer:", comment_writer.text)
            comment_dict["comment_writer"] = comment_writer.text
        except:
            print("no comment writer")
            comment_dict["comment_writer"] = "na"

        try:
            profile_url=comment.find("a", class_= '''x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv''').get("href")
            print("profile_url:", profile_url)
            comment_dict["profile_url"] = profile_url
        except:
            print("no profile_url")
            comment_dict["profile_url"] = "na"

        try:
            comment_dict["keyword"]=keyword
        except:
            comment_dict["keyword"]="na"

        try:
            comment_text = comment.find("div", class_="x11i5rnm xat24cr x1mh8g0r x1vvkbs xdj266r")
            print("comment_text:", comment_text.text)
            comment_dict["comment_text"] = comment_text.text
        except:
            print("no comment text")
            comment_dict["comment_text"] = "na"
        try:
            profile_location = get_pofile_location(profile_url)
            print("profile_location:", profile_location)
            comment_dict["profile_location"] = profile_location
        except Exception as e:
            print(e)
            print("no profile location")
            comment_dict["profile_location"] = "na"
            pass


        comments_list.append(comment_dict)
        #df = pd.DataFrame(comments_list)
    return comments_list

def comments_filter(comments_list, keyword):
    new_comments_list=[]
    keyword=keyword.lower()

    for comment in comments_list:
        #print("comment:", comment)
        comment_text = comment["comment_text"].lower()
        #print("comment text:", comment_text)
        if re.search(keyword, comment_text):
            new_comments_list.append(comment)

    return new_comments_list

def get_posts(keyword, location):

    '''
    :param keyword: search keyword
    :param location: location, proper city name etc San Jose
    :return: df of relevant posts, post text, user name, profile link, post link, post date
    '''
    link = "https://www.facebook.com/search/posts/?q=" + keyword
    try:
        try:
            #location button 1
            driver.get(link)
            time.sleep(2)
            tagged_location_button = wait.until(EC.visibility_of_element_located((By.XPATH, '''//span[text()='Tagged location']'''))).click()
            # tagged_location_button.click()
            # tagged_location_button.click()
            print("location Button 1 Clicked")
        except Exception as e:
            # location button 2
            print("Error while selecting location button: ", e)
            driver.get(link)
            time.sleep(2)
            tagged_location_button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'''xu06os2 x1ok221b xgujvf1'''))).click()
            # tagged_location_button.click()
            # tagged_location_button.click()
            print("location Button 2 Clicked")

        try:

            #location bar 1
            print(e)
            time.sleep(.5)
            tagged_location_bar = wait.until(EC.visibility_of_element_located((By.XPATH, '''(//input[contains(@class,'x1qlo5rv x5zoitm')])[2]''')))
            tagged_location_bar.send_keys(location)
            print("location Bar 1 Clicked")

        except Exception as e:
            #location bar 2
            time.sleep(.5)
            tagged_location_bar = wait.until(EC.visibility_of_element_located((By.XPATH,'''//input[@placeholder='Choose a location...']''')))
            tagged_location_bar.send_keys(location)
            print("location Bar 2 Clicked")

        try:
            print("Selecting button by mouse")
            #selecting the first location option using mouse
            with open("mouse_points.txt", "r") as f:
                lines = f.readlines()
                x_coordinate = int(lines[0])
                y_coordinate = int(lines[1])
            # print("points: ", x_coordinate, y_coordinate)
            # print("type: ", type(x_coordinate), type(y_coordinate))

        except Exception as e:
            print("While opening mouse points file:", e)

        try:
            time.sleep(2)
            pyautogui.moveTo(x_coordinate, y_coordinate, duration=1)
            print("Mouse Position :", pyautogui.position())
            pyautogui.click()
            print("Button Selected by mouse")
        except Exception as e:
            print("Error while clicking mouse :", e)

    except Exception as e:
        #Main try
        print("Error while selecting location: ", e)
        pass


    print("Loading posts...")
    #set posts scrolling range
    for i in range(0, 10):
        # multiple scrolling
        time.sleep(2)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    # Use Beautiful Soup to parse the HTML of the search results page

    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Find all the posts on the page using the Beautiful Soup object
    posts = soup.find_all("div", class_="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")

    count=0
    # Loop through the posts and print the text of each one
    data_list=[]
    for post in posts:

        #counter
        count=count+1
        print("------------------------------------------------------")
        print("POST: ", count)
        post_dict={}

        try:
            profile_name=post.find("a", class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f")
            print("profile_name: ", profile_name.text)
            post_dict["profile_name"]=profile_name.text

        except:
            "no profile name found"
            post_dict["profile_name"] = "na"

        try:
            post_dict["post_location"]=location
        except:
            post_dict["post_location"]="na"

        try:
            post_dict["keyword"]=keyword
        except:
            post_dict["keyword"]="na"

        try:
            #same class as profile name
            profile_url=post.find("a", class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f").get("href")
            print("profile_url: ", profile_url)
            post_dict["profile_url"] = profile_url
        except:
            "no profile_url found"
            post_dict["profile_url"] = "na"

        try:
            post_text= post.find("div", class_="x11i5rnm xat24cr x1mh8g0r x1vvkbs xdj266r x126k92a")
            print("post_text:", post_text.text)
            post_dict["post_text"] = post_text.text

        except:
            print("no post text")
            post_dict["post_text"] = "na"

        try:
            post_date=post.find("span", class_="x4k7w5x x1h91t0o x1h9r5lt xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j x1jfb8zj").text
            print("post_date :", post_date)
            post_dict["post_date"] = post_date
        except:
            print("no post date found")
            post_dict["post_date"] = "na"
        try:
            post_url = post.find("a", class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm").get("href")
            print("post_url :", post_url)
            post_dict["post_url"] = post_url
        except:
            print("no post url found")
            post_dict["post_url"] = "na"

        data_list.append(post_dict)
        df = pd.DataFrame(data_list)
    return df

def get_pofile_location(profile_url):
    '''
    :param profile_url:
    :return: string location of profile
    '''
    try:
        time.sleep(1)
        driver.get(profile_url)
        time.sleep(2)
        #twice
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        user_soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            #lives in
            locations=user_soup.find_all("span", class_="xt0psk2")
            location=locations[1].text
        except:
            #From
            locations=user_soup.find_all("span", class_="xt0psk2")
            location=locations[2].text

    except Exception as e:
        print("Error while gettig location of profile: ", e)
        location="na"
        pass
    return (location)

def main():
    try:
        # keyword="Shabbat"
        # location="San Jose"

        now = datetime.now()
        current_date_time = str(now.strftime("%Y-%m-%d %H-%M-%S"))

        posts = get_posts(keyword, location)
        #posts.to_csv(f'OUTPUT/posts_{keyword.lower()}_{location.lower()}_{current_date_time}.csv')
        posts.to_csv('''OUTPUT/posts.csv''', mode="a", index=False, header=True)

        posts_urls = posts["post_url"]

        count=0
        print("Scraping comments of posts...")
        #comments_file=(f'''OUTPUT/comments_{keyword.lower()}_{current_date_time}.csv''')
        comments_file = ('''OUTPUT/comments.csv''')

        # with open(comments_file, 'a') as f:
        #     writer_object = writer(f)
        #     writer_object.writerow(['comment_writer', 'profile_url','keyword','location','comment_text'])
        #     f.close()

        for post_url in posts_urls:
            count = count + 1
            print("-------------------------------------------------------------------")
            print("POST :", count)
            try:
                #----------------------------------------------
                comments_list = comments_of_post(post_url,keyword)
                #print("comments list:", comments_list)
                filtered_comments_list = comments_filter(comments_list, keyword)
                comments_df = pd.DataFrame(filtered_comments_list)
                print("Filtered comments dataframe :", comments_df)
                comments_df.to_csv(comments_file, mode="a", index=False, header=True)
            except Exception as e:
                print("Error :", e, "\n", "Skipping this post.")
                pass


        print("----------------------Session Complete------------------------")
    except Exception as e:
        print("Session Failed : ", e)


if __name__ == "__main__":
   main()


