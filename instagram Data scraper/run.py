from instaloader import Instaloader, Profile

# scrape followers
def scrape_followers(username, password, target_username):
    L = Instaloader()
    L.login(username, password)
    # Save session
    L.save_session_to_file(filename="session.txt")
    # Load session later


    profile = Profile.from_username(L.context, target_username)
    followers = []
    for follower in profile.get_followers():
        username_x = str(follower.username)
        print(username_x)
        followers.append(username_x)

    return followers

