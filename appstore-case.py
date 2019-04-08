#!/usr/bin/env python
# coding: utf-8

# # Analysis into market opportunities for iOs and Android apps
# ### (A DataQuest guided project)
# 
# This project has the objective of discovering what mobile applications are the most profitable for our company to build.
# 
# For this project, I am a Data Analyst at a company which builds free apps with in-app advertisement. I provide analysis which helps the business and our developers understand what kind of app are likely to attract a lot of users.
# 
# Because there are millions of apps available, it would take a lot of time to gather all of them. Therefore I will use a sample dataset which can be found here: [android](https://www.kaggle.com/lava18/google-play-store-apps/home) and [ios](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home)

# In[1]:


from csv import reader

def open_read_list(dataset):
    opened_file = open(dataset)
    read_file = reader(opened_file)
    return list(read_file)
    
ios = open_read_list('AppleStore.csv')
ios_header = ios[0]
ios = ios[1:]

android = open_read_list('googleplaystore.csv')
android_header = android[0]
android = android[1:]

def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

print(ios_header,'\n\n')       
explore_data(ios,0,5,True)


# As we can see, the ios dataset contains 7197 rows and 16 columns. At first glance, variables (columns) that might be useful for an analysis on profitable applications might include:
# 1. 'track_name' and 'prime_genre' for an indication of what the application is about.
# 2. 'user_rating' and user_rating_ver (all versions, grade 1-5, with 5 being best), 'rating_count_tot' and 'rating_count_ver' (latest version) to measure popularity.
# 3. 'price' to differentiate free apps from paid apps analyse customer's willingness to pay.
# 
# Documentation on the variables in this dataset can be found [here](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home)

# In[2]:


print(android_header,'\n\n')       
explore_data(android,0,5,True)


# A first exploration of the google playstore dataset shows us that it has 10841 rows and 13 columns. At first glance, variables (columns) that might be useful for an analysis on profitable applications might include:
# 1. 'App', 'Category', 'Type',  'Genres' for an indication of what the application is about.
# 2. 'Rating' (grade 1-5, with 5 being best), (number of) 'Reviews' and (number of) 'Installs' to measure popularity.
# 3. 'Price' to differentiate free apps from paid apps analyse customer's willingness to pay.
# 
# Documentation on the variables in this dataset can be found [here](

# In the discussion section of this dataset, an error was pointed out in row 10472. [link](https://www.kaggle.com/lava18/google-play-store-apps/discussion/66015)

# In[3]:


print(android[10472])


# Indeed, a missing value seems to be the cause of the columns shifting, which results in a rating of 19, which is impossible on a 5 point scale. I will remove this row.

# In[4]:


del android[10472]


# When examining the discussion section of the AppleStore, no errors in the dataset are reported.

# The next step is to see if there are any duplicates in the dataset. Let's take a popular app and see how many times it is found.

# In[5]:


for app in android:
    name = app[0]
    if name == 'Instagram':
        print(app)


# It appears that the app is found 4 times. This indicates that we should check for duplicates in both datasets and remove them. It seems best to keep the most recent versions of every app. As can be seen above, they are of the same date. Therefore, I will keep the row with the highest number of reviews. More reviews means more data on variables like rating.

# In[6]:


duplicate_apps = []
unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
        
print('Number of duplicate apps:', len(duplicate_apps), '\n')
print('Examples of duplicate apps:', duplicate_apps[:10])


# In[7]:


reviews_max = {}
for app in android:
    name = app[0]
    n_reviews = float(app[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews

len(reviews_max)


# I created a dictionary which contains the apps with the most reviews as keys. An app is added to the dictionary and replaced when an app with the same name and a higher review count is encountered.

# In[8]:


android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    if n_reviews == reviews_max[name] and name not in already_added:
        android_clean.append(app)
        already_added.append(name)
        
print(android_clean[:5])
len(android_clean)


# This dictionary is used to loop through the Google Playstore dataset. Here I go through every row and add apps which are in the reviews_max dictionary (making sure I only add apps with the highest review count). Apps which are added, are also added to the already_added list. I had to include the already_added list to make sure we are not including cases in which apps have the same amount of reviews.

# Our company is interested in creating English apps. Therefore we should filter out apps with symbols not used in the English alphabet. Based on the ASCII, the characters found in the English alphabet have ord numbers in the range 0 to 127. We will filter out apps with names containing symbols outside that range.

# In[9]:


def english(string):
    for character in string:
        if ord(character) > 127:
            return False
    return True

print(english('Instagram'))
print(english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(english('Docs To Go™ Free Office Suite'))
print(english('Instachat 😜'))
        


# As we can see above, the function I wrote will detect apps with non-English names. But it will also say an app is non-English if it contains emoticons or symbols like '™', because they fall outside the ASCII range. We don't want to delete these apps. To minimize our data loss this way, I will only delete apps with more than 3 characters falling outside the ASCII range.

# In[10]:


def english(string):
    non_ascii = 0
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
        if non_ascii > 3:
            return False
    return True

print(english('Instagram'))
print(english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(english('Docs To Go™ Free Office Suite'))
print(english('Instachat 😜'))

android_english = []
ios_english = []

def filter_english(dataset, column):
    for app in dataset:
        name = app[column]
        if english(name):
            if dataset == android_clean:
                android_english.append(app)
            elif dataset == ios:
                ios_english.append(app)

filter_english(android_clean,0)
filter_english(ios,1)

print(len(android_english))
print(len(ios_english))


# Next, we want to isolate the free apps in the dataset for our analysis.

# In[11]:


#index price column: ios=4 android=7
final_android = []
final_ios = []

def free(dataset, column):
    for app in dataset:
        price = app[column]
        if dataset == android_english and price == '0':
            final_android.append(app)
        elif dataset == ios_english and price == '0.0':
            final_ios.append(app)

free(android_english, 7)
free(ios_english, 4)

print(len(final_android))
print(len(final_ios))
    


# We want to find an app profile that fits both the App Store and Google Play, since we want our app to be downloaded by as many people as possible. 
# 
# Instead of using a waterfall approach of building a large project, we want to minimize risk and shorten our feedback loops by building a minimum viable product first. 
# 
# If the MVP gets good response from users, we can then develop it further based on feedback. 
# 
# If the app is profitable in Android (which has the largest userbase), we can then build an iOS version of the app and add it to the App Store.

# In[12]:


print(android_header,'\n\n',ios_header)


# We can use the 'Genres' column for the android dataset, and the 'prime_genre' column for the ios dataset.

# In[13]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
        
display_table(final_ios, -5) #prime genre


# When examining the prime genre column of the App Store dataset, we can see that the most common genre is clearly 'Games' with 58%. 'Entertainment is the runner-up. In general, the pattern is that leisure activities are popular than practical apps, such as shopping or education.

# In[14]:


display_table(final_android, -4) #genre


# The genre distribution for the android dataset is more evenly distributed, with the number 1 genre being 'Tools' (8%) and the runner-up being 'Entertainment'. At first glance, practical apps seem to be more popular for android users than for apple. When examining the list of genres, we can see that a lot of genres are subgenres of games.

# In[15]:


display_table(final_android, 1) #category


# The category column shows a less granular picture. Here, 'Family' is number one and 'Game' is the runner-up. This suggests that gaming is indeed also very popular for android users. Examining the 'Family' category reveals that it contains a lot of games for children, which are also leisure activities. We can state that gaming apps are very popular, but the data suggest a high level of saturation in the gaming app market. It might be more interesting to explore a niche.

# Below, I explore a frequency table for the 'prime_genre'column for the Apple store dataset.

# In[16]:


genres_ios = freq_table(final_ios, -5)
genres_ios


# In[17]:


for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in final_ios:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)
    


# On average, the Navigation genre has the highest number of reviews. This includes, for example, Google Maps and Waze. The third highest navigation app is 'Geocaching', which could also be seen as entertainment, or fun.

# In[18]:


for app in final_ios:
    if app[-5] == 'Navigation':
        print(app[1],':', app[5]) #name and n of ratings


# If we examine 'Reference' we notice that it includes some apps which could be labeled 'Books', like Bible and Quran apps. Other popular apps are guides for popular games like Minecraft. Apps like this are low effort to make: It is simply turning existing guides into apps. 
# 
# One recommendation for a new app to create is creating a reference app for popular games, series, lifestyles, sports (or any other up and coming genre). I would not recommend creating an app for already saturated genres, like existing popular games (new games could be a possibility though).

# In[19]:


categories_android = freq_table(final_android, 1)


# In[35]:


for category in categories_android:
    total = 0
    len_category = 0
    for app in final_android:
        category_app = app[1]
        if category_app == category:
            n_installs = app[5]
            n_installs = n_installs.replace(',','')
            n_installs = n_installs.replace('+','')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)
    


# It is important to find a category or genre which is both popular, but which is not dominated by a few large apps. Social apps and communication apps seem to be dominated by a few large apps, and people tend to only use one or a few of these apps instead of multiple. This means there is a high entry barrier here.

# In[32]:


for app in final_android:
    if app[1] == 'SOCIAL':
        print(app[0],':', app[5]) #name and n of ratings


# In[34]:


for app in final_android:
    if app[1] == 'COMMUNICATION':
        print(app[0],':', app[5]) #name and n of ratings


# Games and entertainment are a large popular group, and it is not dominated by a handful of apps. It seems that people like to play different and new games. However, there is a lot of competition and the market seems saturated.

# In[38]:


for app in final_android:
    if app[1] == 'GAME':
        print(app[0],':', app[5]) #name and n of ratings


# Game development is costly if we are going for high quality, and easy to be copied if we go for low quality. Making a reference app for popular games, series or any other popular subject seems like a good choice. My recommendation would be to create a reference app, which can be used again and again for new popular subjects.
