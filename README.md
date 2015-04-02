# Next-Episode

Class created to provide a easy access to your next episode watch list and easy integrate information with tvrage

# Usage

`from nextepisode import NextEpisode`
`ne = NextEpisode("username", "password")`

now ne is populated with all your watchlist :

`>>> ne[0]`
`{'URL': 'http://next-episode.net/666-park-avenue', 'index': '39172b56-2230-30f9-87a6-b7a98ccce060', 'Name': [u'666 Park Avenue']}`

# Add tvrage info

`>>> ne.attach_tvrage_info()`

this method can take a while depending on internet connection and watch list size.
When the method end the object will have the following information :

`>>> ne[0]
{'URL': 'http://next-episode.net/666-park-avenue', 'index': 'd022b2d5-cd19-3fe0-b84f-78e0007fede1', 'Name': [u'666 Park Avenue'], 'TV Rage': {'Genres': 'Horror/Supernatural', 'Network': 'ABC', 'URL': 'http://www.tvrage.com/666-park-avenue', 'Country': 'USA', 'Premiered': '2012', 'Airtime': 'Saturday at 09:00 pm', 'Next Episode': {'Air Date': 'N/A', 'Number': 'N/A', 'Title': 'N/A'}, 'Status': 'Canceled/Ended', 'Classification': 'Scripted', 'Latest Episode': {'Air Date': 'Jul/13/2013', 'Number': '01x13', 'Title': 'Lazarus: Part 1'}, 'Show ID': '30744', 'Show Name': '666 Park Avenue'}}`

also a today_list attribute will be provided with a portion of episode airing today.

`>>> ne.today_list
[{'URL': 'http://next-episode.net/arrow', 'index': '11aa9858-ee00-37fa-a5a2-bf9d9030a5b7', 'Name': [u'Arrow'], 'TV Rage': {'Genres': 'Action | Super Heroes', 'Network': 'CW', 'URL': 'http://www.tvrage.com/Arrow', 'Country': 'USA', 'Premiered': '2012', 'Airtime': 'Wednesday at 08:00 pm', 'Next Episode': {'Air Date': 'Apr/01/2015', 'Number': '03x18', 'Title': 'Public Enemy'}, 'Status': 'Returning Series', 'Classification': 'Scripted', 'Latest Episode': {'Air Date': 'Mar/25/2015', 'Number': '03x17', 'Title': 'Suicidal Tendencies'}, 'Show ID': '30715', 'Show Name': 'Arrow'}}, {'URL': 'http://next-episode.net/supernatural', 'index': '1e1f39ae-8c56-394e-afed-349b7bb79c9b', 'Name': [u'Supernatural'], 'TV Rage': {'Genres': 'Action | Adventure | Drama | Horror/Supernatural', 'Network': 'CW', 'URL': 'http://www.tvrage.com/Supernatural', 'Country': 'USA', 'Premiered': '2005', 'Airtime': 'Wednesday at 09:00 pm', 'Next Episode': {'Air Date': 'Apr/01/2015', 'Number': '10x17', 'Title': 'Inside Man'}, 'Status': 'Returning Series', 'Classification': 'Scripted', 'Latest Episode': {'Air Date': 'Mar/25/2015', 'Number': '10x16', 'Title': 'Paint it Black'}, 'Show ID': '5410', 'Show Name': 'Supernatural'}}, {'URL': 'http://next-episode.net/the-americans-2013', 'index': '56065866-33f4-3a4b-8997-953539a73bcd', 'Name': [u'The Americans (2013)'], 'TV Rage': {'Genres': 'Crime | Drama | Mystery', 'Network': 'FX', 'URL': 'http://www.tvrage.com/The_Americans', 'Country': 'USA', 'Premiered': '2013', 'Airtime': 'Wednesday at 10:00 pm', 'Next Episode': {'Air Date': 'Apr/01/2015', 'Number': '03x10', 'Title': 'Stingers'}, 'Status': 'Returning Series', 'Classification': 'Scripted', 'Latest Episode': {'Air Date': 'Mar/25/2015', 'Number': '03x09', 'Title': 'Do Mail Robots Dream of Electric Sheep?'}, 'Show ID': '30449', 'Show Name': 'N/A'}}]`