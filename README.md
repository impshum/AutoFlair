## AutoFlair

Streams Reddit, counts submissions and assigns different flairs depending on score.

![](https://github.com/impshum/AutoFlair/blob/master/ss.jpg?raw=true)

### Features

-   Streams Reddit and applies flairs in real-time
-   SQLite database to store all the juicy data
-   Simple flair system setup
-   Does not eat the cat

### Instructions

-   Install requirements `pip install -r requirements.txt`
-   Create Reddit (script) app at <https://www.reddit.com/prefs/apps/> and get keys
-   Edit conf.ini with your details
-   Run it `python run.py`

### Settings Info

-   `target_subreddit` - Subreddit to target
-   `points_per_post` - Points to award for each new submission
-   `test_mode` - Run the script without changing the database or flairs

### Flair Setup Instructions

In the config.ini file you should see the code below. Each flair level is assigned here.

    [1]
    text = one
    class = one

    [3]
    text = three
    class = three

    [10]
    text = ten
    class = ten

The titles of these sections eg `[1]` and `[3]` are the minimum points needed to be awarded that flair.

The items under the section title are as follows

-   `text` - The flair text
-   `class` - The flair class to be applied (see CSS section below)

### CSS flair class

We declare the `class` here as `.flair-whatever`

So...

    [10]
    text = SQUIRREL
    class = squirrel

Would be

    .flair-squirrel {
        background-color: #19572a;
        color: #fff;
        padding: 2px 19px;
        font-weight: 600;
    }

Edit to your liking and add it to your CSS stylesheet. You can use the same class for all flairs if you like.

![](https://recycledrobot.co.uk/reddit_git.jpg)

--- 

BTC - 1AYSiE7mhR9XshtS4mU2rRoAGxN8wSo4tK
