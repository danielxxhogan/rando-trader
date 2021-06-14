from sentiment import Sentiment

s = Sentiment('AAPL')

print(dir(s))



results = s.get_stocktwits()
print('\n\n LAST LINE:', results)

results = s.get_insider_trading()
print('\n\n LAST LINE:', results)

results = s.get_news()
print('\n\n LAST LINE:', results)

results = s.get_press_releases()
print('\n\n LAST LINE:', results)

results = s.get_quiver_data()
print('\n\n LAST LINE:', results)

results = s.get_analyst_ratings()
print('\n\n LAST LINE:', results)