# generate_rss.py
import json
import datetime
from feedgen.feed import FeedGenerator

try:
    with open('news.json', 'r', encoding='utf-8') as f:
        news_data = json.load(f)
except Exception as e:
    print(f"⚠️Ошибка чтения news.json: {e}")
    exit(1)

if not isinstance(news_data, list):
    print("news.json должен содержать массив [...]")
    exit(1)

fg = FeedGenerator()
fg.title('Read the news in RSS-PlotDot')
fg.link(href='https://digitaleternities.github.io/RSS-PlotDot/')
fg.description('Актуальные новости и обновления в RSS-PlotDot')
fg.language('ru')
fg.lastBuildDate(datetime.datetime.now(datetime.timezone.utc))
fg.ttl(60)

for item in news_data:
    fe = fg.add_entry()
    fe.title(item.get('title', 'Без заголовка'))
    fe.link(href=item.get('link', ''))
    fe.description(item.get('description', ''))
    
    try:
        pub_date = datetime.datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc)
        fe.published(pub_date)
    except KeyError:
        print("⚠️У новости отсутствует поле 'date'")
    except ValueError:
        print("⚠️Неверный формат даты. 'YYYY-MM-DD HH:MM:SS'")
        
    fe.guid(item.get('link', ''), isPermaLink=True)

# Генерация файла
fg.rss_file('bin.rss', pretty=True)
print("bin.rss успешно")
