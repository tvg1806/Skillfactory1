#!/usr/bin/env python
# coding: utf-8

# In[120]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter


# In[121]:


data = pd.read_csv('movie_bd_v5.csv')
data.sample(5)


# In[222]:


data.describe()


# # Предобработка

# In[122]:


answers = {} # создадим словарь для ответов

# тут другие ваши предобработки колонок например:

#the time given in the dataset is in string format.
#So we need to change this in datetime format
# As far as in requests we need only months, it will be enouth to have separate month column.

from datetime import datetime # import date prosessing means
dateFormatter = "%m/%d/%Y"    # detting date format

data['month'] = data.release_date.apply(lambda x: datetime.strptime(str(x), dateFormatter).month)

# for each instance of release_date processes date and define month

# actor's names are listed with separator | in a single instance
# so we need to distribute them into columns

data.cast = data.cast.apply(lambda x: str(x).split('|'))


# director's names are listed with separator | in a single instance
# so we need to distribute them into columns

data.director = data.director.apply(lambda x: str(x).split('|'))


# production studio's names are listed with separator | in a single instance
# so we need to distribute them into columns

data.production_companies = data.production_companies.apply(lambda x: str(x).split('|'))


# genres definitions are listed with separator | in a single instance
# so we need to distribute them into columns

data.genres = data.genres.apply(lambda x: str(x).split('|'))


#dataset has no value that describes profit
# so we need to calculate profit and add it to the dataset
data['profit'] = data['revenue'] - data['budget']


data.sample(5)


# # 1. У какого фильма из списка самый большой бюджет?

# Использовать варианты ответов в коде решения запрещено.    
# Вы думаете и в жизни у вас будут варианты ответов?)

# In[123]:


# в словарь вставляем номер вопроса и ваш ответ на него
# Пример: 
answers['1'] = 'Pirates of the Caribbean: On Stranger Tides (tt1298650)'
# + 

"""Several tasks with correct results and special preprocessing are provided lower in the notebook in special section"""


# In[258]:


data_great = data.sort_values(['budget'],ascending = False).head(1)
data_great[['imdb_id','original_title']]


# ВАРИАНТ 2

# In[195]:


# another way to solve this task

budget_great = data.loc[(data.budget == data.budget.max())]
budget_great[['imdb_id','original_title']]


# # 2. Какой из фильмов самый длительный (в минутах)?

# In[124]:



answers['2'] = 'Gods and Generals (tt0279111)'
# +


# In[225]:


data_long = data.loc[data.runtime == data.runtime.max()].head(1)
data_long[['imdb_id','original_title']]


# # 3. Какой из фильмов самый короткий (в минутах)?
# 
# 
# 
# 

# In[125]:


answers['3'] = 'Winnie the Pooh (tt1449283)'
# +

data_short = data.loc[data.runtime == data.runtime.min()].head(1)
data_short[['imdb_id','original_title']]


# # 4. Какова средняя длительность фильмов?
# 

# In[126]:


answers['4'] = '110'
# +

mean_time = data['runtime'].mean()
print(mean_time)


# # 5. Каково медианное значение длительности фильмов? 

# In[127]:


answers['5'] = '107'
# +

median_time = data['runtime'].median()
print(median_time)


# # 6. Какой самый прибыльный фильм?
# #### Внимание! Здесь и далее под «прибылью» или «убытками» понимается разность между сборами и бюджетом фильма. (прибыль = сборы - бюджет) в нашем датасете это будет (profit = revenue - budget) 

# In[128]:


answers['6'] = 'Avatar (tt0499549)'
# +

film_rent_higher = data.loc[data.profit == data.profit.max()].head(1)
film_rent_higher[['imdb_id','original_title']]


# # 7. Какой фильм самый убыточный? 

# In[129]:


answers['7'] = 'The Lone Ranger (tt1210819)'
# +

film_nonrent_lower = data.loc[data.profit == data.profit.min()].head(1)
film_nonrent_lower[['imdb_id','original_title']]


# # 8. У скольких фильмов из датасета объем сборов оказался выше бюджета?

# In[130]:


answers['8'] = '1478'
# +

film_rent_num = data.loc[data.profit >= 0]
film_rent_num.imdb_id.nunique()


# # 9. Какой фильм оказался самым кассовым в 2008 году?

# In[131]:


answers['9'] = 'The Dark Knight (tt0468569)'
# +

film_of_the_2008 = data.loc[data.release_year == 2008].sort_values(['revenue'], ascending=False).head(1)
film_of_the_2008[['imdb_id','original_title']]


# # 10. Самый убыточный фильм за период с 2012 по 2014 г. (включительно)?
# 

# In[132]:


answers['10'] = 'The Lone Ranger (tt1210819)'
# +

bad_film = data.loc[(data.release_year >= 2012) & (data.release_year <= 2014)].sort_values(['profit']).head(1)
bad_film[['imdb_id','original_title']]


# # 11. Какого жанра фильмов больше всего?

# In[133]:


# эту задачу тоже можно решать разными подходами, попробуй реализовать разные варианты
# если будешь добавлять функцию - выноси ее в предобработку что в начале

answers['11'] = 'Drama'
# +
data = data.explode('genres')
favourite_genre = data.genres.value_counts()
print(favourite_genre)


# ВАРИАНТ 2

# In[17]:


favourite_genre_1 = data.groupby(['genres'])['imdb_id'].nunique().sort_values(ascending=False)
# favourite_genre_1 = data.groupby(['genres'])['imdb_id'].sum().sort_values().head(1)
print(favourite_genre_1)


# # 12. Фильмы какого жанра чаще всего становятся прибыльными? 

# In[134]:


answers['12'] = 'Drama'
# +

profit_genre = data.loc[data.profit >= 0]
favourite_profit_genre = profit_genre.genres.value_counts().head(1)
print(favourite_profit_genre)


# # 13. У какого режиссера самые большие суммарные кассовые сборы?

# In[135]:


answers['13'] = 'Peter Jackson'
# +
data = data.explode('director')
great_director = data.groupby(['director'])['revenue'].sum().sort_values(ascending=False).head(10)
print(great_director)


# # 14. Какой режисер снял больше всего фильмов в стиле Action?

# In[136]:


answers['14'] = 'Robert Rodriguez'
# +

data = data.explode('director')

action_director_1 = data.loc[(data.genres.str.contains("Action", na=False))]

action_director_1.director.value_counts().head(1)


# # 15. Фильмы с каким актером принесли самые высокие кассовые сборы в 2012 году? 

# In[137]:


# see special section


# # 16. Какой актер снялся в большем количестве высокобюджетных фильмов?

# In[139]:



# see special section


# # 17. В фильмах какого жанра больше всего снимался Nicolas Cage? 

# In[140]:


answers['17'] = 'Action'
# +
data = data.explode('genres')
data = data.explode('cast')
films_Cage = data.genres[data.cast.str.contains("Cage",na=False)].value_counts().head(1)
print(films_Cage)


# # 18. Самый убыточный фильм от Paramount Pictures

# In[141]:


answers['18'] = 'K-19: The Widowmaker'
# +
data = data.explode('production_companies')
Para_fail = data.profit[data.production_companies == "Paramount Pictures"].min()
data.loc[data.profit == Para_fail]['original_title'].head(1)


# # 19. Какой год стал самым успешным по суммарным кассовым сборам?

# In[142]:


answers['19'] = '2015'
# +

good_year_list = data.groupby(['release_year'])['revenue'].sum().sort_values(ascending=False).head(1)
print(good_year_list)


# # 20. Какой самый прибыльный год для студии Warner Bros?

# In[143]:


# see special section


# # 21. В каком месяце за все годы суммарно вышло больше всего фильмов?

# In[144]:


answers['21'] = '9 (сентябрь)'
# +

data['month'] = data.release_date.apply(lambda x: datetime.strptime(str(x), dateFormatter).month)
good_month = data.groupby(['month'])['imdb_id'].nunique().sort_values(ascending=False).head(1)
print(good_month)


# # 22. Сколько суммарно вышло фильмов летом? (за июнь, июль, август)

# In[145]:


answers['22'] = '450'
# +

summer = data.loc[(data.month == 6) | (data.month == 7) | (data.month == 8)].nunique().head(1)
print(summer)


# # 23. Для какого режиссера зима – самое продуктивное время года? 

# In[146]:


answers['23'] = 'Peter Jackson'
# +

winter = data.loc[(data.month == 12) | (data.month == 1) | (data.month == 2)]

winter_director = winter.groupby(['director'])['imdb_id'].nunique().sort_values(ascending=False).head(1)
print(winter_director)


# # 24. Какая студия дает самые длинные названия своим фильмам по количеству символов?

# In[147]:


answers['24'] = 'Four By Two Productions'
# +

"""it is worth noting that the answer itself is not directly given here"""

"""it is required to select one relevant name"""

# here a special preprocessing added: calculation of folm title length in symbols
# this data is relatively special, it is not pretty important in general analysis, so it is added ad hoc
data['title_length'] = data.original_title.apply(lambda x: len(str(x)))

data_1 = data.title_length.max()

data.loc[data.title_length == data_1]


# # 25. Описание фильмов какой студии в среднем самые длинные по количеству слов?

# In[148]:


answers['25'] = 'Midnight Picture Show'
# +

# here a special preprocessing added: calculation of folm title length in symbols
# this data is relatively special, it is not pretty important in general analysis, so it is added ad hoc
# the lenght of description in words is calculated regarding space symbols

data['descr_length'] = data.overview.apply(lambda x: str(x).count(' ')+1)
descr_long = data.groupby(['production_companies'])['descr_length'].mean().sort_values(ascending=False).head(1)

print(descr_long)


# # 26. Какие фильмы входят в 1 процент лучших по рейтингу? 
# по vote_average

# In[149]:


answers['26'] = 'Inside Out, The Dark Knight, 12 Years a Slave'
# +

"""it is worth noting that the answer itself is not directly given here"""

"""it was required to select relevant group of titles"""

border = data.quantile(0.99, numeric_only=True)['vote_average']

data.loc[data.vote_average >= border]


# # 27. Какие актеры чаще всего снимаются в одном фильме вместе?
# 

# ВАРИАНТ 2

# # Submission

# In[150]:


answers['27'] = 'Daniel Radcliffe & Rupert Grint'
# +

data = pd.read_csv('movie_bd_v5.csv')
from itertools import combinations

pairs = Counter()

for i in range(0,len(data)):
    artists = data.cast[i].split('|')
    for j in list(combinations(artists, 2)):
        if j not in pairs:
            pairs[j] = 1
        else:
            pairs[j] += 1

pairs.most_common(5)


# In[ ]:





# In[ ]:





# In[185]:


# special section


# In[ ]:





# In[151]:


answers['15'] = 'Chris Hemsworth'
# +

# Вопрос 15. Фильмы с каким актером принесли самые высокие кассовые сборы в 2012 году?

data = pd.read_csv('movie_bd_v5.csv')
data['profit'] = data['revenue'] - data['budget']
data['year'] = data.release_date.apply(lambda x:(int(x[-4::1])))
data.cast = data.cast.apply(lambda x: str(x).split('|'))
data = data.explode('cast')


data_1 = data.loc[data.year == 2012]


profit_actor = data_1.groupby(['cast'])['revenue'].sum().sort_values(ascending=False).head(1)
print(profit_actor)


# In[152]:


answers['16'] = 'Matt Damon'
# +

# Вопрос 16. Какой актер снялся в большем количестве высокобюджетных фильмов? Примечание: в фильмах, где бюджет выше среднего по данной выборке. correct
data = pd.read_csv('movie_bd_v5.csv')

data.cast = data.cast.apply(lambda x: str(x).split('|'))
data_1 = data.explode('cast')

films_budget_average = data_1.loc[data.budget >= data.budget.mean()]
actor_average = films_budget_average['cast'].value_counts().head(1)
print(actor_average)


# In[ ]:





# In[153]:


answers['20'] = '2014'
# +

# Вопрос 20. Какой самый прибыльный год для студии Warner Bros?

data = pd.read_csv('movie_bd_v5.csv')
data['profit'] = data['revenue'] - data['budget']
data['year'] = data.release_date.apply(lambda x:(int(x[-4::1])))
data.production_companies = data.production_companies.apply(lambda x: str(x).split('|'))
data_1 = data.explode('production_companies')

WB_year_1 = data_1.loc[data_1.production_companies.str.contains("Warner",na=False)]
WB_year_1.describe
WB_year_2 = data_1.loc[data_1.production_companies == "Warner Bros. Pictures"]
WB_year_2.describe

WB_good_year_lst = WB_year_1.groupby(['year'])['profit'].sum().sort_values(ascending=False).head(1)

print(WB_good_year_lst)


# In[154]:


# в конце можно посмотреть свои ответы к каждому вопросу
answers


# In[155]:


len(answers)


# In[ ]:




