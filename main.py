from requests_html import AsyncHTMLSession, HTMLSession
import asyncio

proxies = set()
data = HTMLSession().get('https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc').json()
for d in data['data']:
    if 'http' in d['protocols']:
        proxy = f"{d['ip']}:{d['port']}"
        proxies.add(proxy)        


async def test_proxy(s,proxy):
    try:
        r = await s.get('https://jsonplaceholder.typicode.com/posts/1',
                proxies={'http': f'http://{proxy}'})
        return proxy, r.ok
    except:
        return


async def main():
    s = AsyncHTMLSession()
    return await asyncio.gather(*(test_proxy(s, proxy) for proxy in proxies))


valid_proxies = [proxy for proxy,status in asyncio.run(main()) if status]