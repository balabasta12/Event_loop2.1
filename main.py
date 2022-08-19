import aiohttp
from more_itertools import chunked
import asyncio

const_cor = 1


async def aio_http(url: str, session: aiohttp.ClientSession):  # Асинхронные функции (сопрограммы)
    async with session.get(url, ssl=False) as resp:
        if resp.status == 200:
            resp_json = await resp.json()  # await передает управление из функции обратно в event_loop, чтобы диспечер мог запустить другие программы
            return resp_json
        elif resp.status == 500:
            pass


async def aio_http_session():
    async with aiohttp.ClientSession() as session:
        res = await aio_http("https://swapi.dev/api/people/", session)
        # print(res)

        coros = []
        api_responces = []
        id_person = []

        for i in res['results']:
            people_url = i['url']
            id = people_url.split('/')[-2]
            coros_id = asyncio.create_task(aio_http(f"https://swapi.dev/api/people/{id}", session))
            id_person.append(id)
            coros.append(coros_id)

        for i in chunked(coros, const_cor):
            api_responce = await asyncio.gather(*i)
            api_responces.append(api_responce)

        persons_dict = dict(zip(id_person, api_responces))  # Запомнить! Как объединять спсики.

        return persons_dict


aio_http_session = asyncio.get_event_loop().run_until_complete(aio_http_session())





# if __name__ == '__main__':
#     main_run = asyncio.get_event_loop().run_until_complete(main())  # event_loop - диспечер событий, сообщаем диспечеру событий,
#                                                             # что он должен рабоать до тех пор пока не закончатся выполняться все сопрограммы main()


