from features.models import ConferencesCache
from datetime import datetime, timezone
import requests
import bs4

def fetch_conferences():
    url = 'http://www.wikicfp.com/cfp/allcfp'
    response = requests.get(url, timeout=5, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    })
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        tableContainer = soup.find('form', {'name': 'myform'})
        table = tableContainer.find('table').find_all('tr')[2]
        rows = []
        i = 0
        for row in table.find_all('tr')[1:]:
            if i % 2 == 0:
                rows.append(row.find_all('td'))
            else:
                rows[-1].extend(row.find_all('td'))
            i += 1
        for row in rows:
            url, name, _, _, venue, deadline = row
            url = url.find('a')['href']
            name = name.text
            venue = venue.text
            deadline = deadline.text
            conference_id = url.split('=')[-1].split('&')[0]
            print(conference_id, name, deadline, venue, url)
            try:
                conference = ConferencesCache(conference_id=conference_id, conference_name=name, deadline=deadline, venue=venue, conference_link=url)
                conference.save()
            except:
                pass

def get_conferences():
    if ConferencesCache.objects.count() == 0:
        fetch_conferences()
        return ConferencesCache.objects.all()
    else:
        last_fetch = ConferencesCache.objects.order_by('-fetch_date').first()
        if (datetime.utcnow().astimezone(timezone.utc) - last_fetch.fetch_date.astimezone(timezone.utc)).days > 1:
            ConferencesCache.objects.all().delete()
            fetch_conferences()
        return ConferencesCache.objects.all()
