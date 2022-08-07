import requests
import asyncio
import tkinter as tk
import sorting_algs


class Window(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.cache = []
        self.listdata = []
        self.seealso = []
        self.initwindow()
    def initwindow(self):
        self.master.title('Wookiedex')
        self.master.geometry('800x600')
        self.pack(fill='both', expand=1)

        self.searchpanel = tk.Frame(self)
        self.searchpanel.pack(fill='y', side='left')

        self.searchbar = tk.Frame(self.searchpanel)
        self.searchbar.pack(fill='x', side='top', pady=5)

        self.searchbutton = tk.Button(self.searchbar, text='Search', padx=1, pady=1, command=self.apisearch)
        self.searchbutton.pack(side='right', padx=2)

        self.searchentry = tk.Entry(self.searchbar)
        self.searchentry.pack(fill='both', padx=2, expand=1)

        self.resultspanel = tk.Frame(self.searchpanel)
        self.resultspanel.pack(fill='both', expand=1)

        self.resultscroll = tk.Scrollbar(self.resultspanel, orient='vertical')
        self.resultscroll.pack(side='right', fill='y')

        self.searchresults = tk.Listbox(self.resultspanel, yscrollcommand=self.resultscroll.set)
        self.searchresults.pack(fill='both', expand=1)
        self.resultscroll.config(command=self.searchresults.yview)

        self.viewbutton = tk.Button(self.searchpanel, text='View', padx=1, pady=1, command=self.viewresult)
        self.viewbutton.pack(fill='x', side='bottom', padx=5, pady=5)

        self.seealsopanel = tk.Frame(self)
        self.seealsopanel.pack(fill='both', side='bottom', expand=1)

        self.displaypanel = tk.Frame(self)
        self.displaypanel.pack(fill='both', side='bottom', expand=1)

        self.displayscroll = tk.Scrollbar(self.displaypanel, orient='vertical')
        self.displayscroll.pack(side='right', fill='y')

        self.display = tk.Text(self.displaypanel, relief='sunken', wrap='word', state='disabled', yscrollcommand=self.displayscroll.set)
        self.display.pack(fill='both', side='left', expand=1)
        self.displayscroll.config(command=self.display.yview)

        self.seealsolabel = tk.Label(self.seealsopanel, text='See Also:')
        self.seealsolabel.pack(side='top', fill='x')

        self.seealsoscroll = tk.Scrollbar(self.seealsopanel, orient='vertical')
        self.seealsoscroll.pack(side='right', fill='y')

        self.seealsolist = tk.Listbox(self.seealsopanel, yscrollcommand=self.seealsoscroll.set)
        self.seealsolist.pack(fill='both', expand=1)
        self.seealsoscroll.config(command=self.seealsolist.yview)

        self.seealsobutton = tk.Button(self.seealsopanel, text='View', padx=1, pady=1, command=self.seeingalso)
        self.seealsobutton.pack(fill='x', side='bottom', padx=5, pady=5)

    def apisearch(self):
        query = self.searchentry.get()
        results = []
        self.searchresults.delete(0)
        async def getinfo():
            async def inquire(category, st):
                response = requests.get(f'https://swapi.dev/api/{category}/?search={st}')
                results.append(response.json()['results'])
            await asyncio.gather(inquire('people', query), inquire('films', query), inquire('starships', query),
                                 inquire('vehicles', query), inquire('species', query), inquire('planets', query))
        asyncio.run(getinfo())
        if results[0] == [] and results[1] == [] and results[2] == [] and results[3] == [] and results[4] == [] and results[5] == []:
            self.searchresults.insert(1, 'No results found.')
            return
        count = 1
        for i in results:
            for j in i:
                try:
                    self.searchresults.insert(count, j['name'])
                    self.listdata.append(j)
                    self.cache.append(j)
                except KeyError:
                    pass
                try:
                    self.searchresults.insert(count, j['title'])
                    self.listdata.append(j)
                    self.cache.append(j)
                except KeyError:
                    pass
                count += 1

    def viewresult(self, seealso=False):
        displaytext = []
        updatedict = {}
        updatedict2 = {}
        seealsoupdate = []
        if seealso == True:
            selected = self.seealsolist.curselection()
            if not selected:
                return
            source = self.seealso[selected[0]]
        else:
            selected = self.searchresults.curselection()
            if not selected:
                return
            source = self.listdata[selected[0]]
        #preparing data that requires further lookup
        try:
            if source['updated']:
                pass
        except KeyError:
            if 'homeworld' in source and source['homeworld']:
                updatedict.update({'homeworld': source['homeworld']})
            if 'films' in source and source['films']:
                updatedict.update({'films': source['films']})
            if 'species' in source and source['species']:
                updatedict.update({'species': source['species']})
            if 'starships' in source and source['starships']:
                updatedict.update({'starships': source['starships']})
            if 'vehicles' in source and source['vehicles']:
                updatedict.update({'vehicles': source['vehicles']})
            if 'characters' in source and source['characters']:
                updatedict.update({'characters': source['characters']})
            if 'planets' in source and source['planets']:
                updatedict.update({'planets': source['planets']})
            if 'pilots' in source and source['pilots']:
                updatedict.update({'pilots': source['pilots']})
            if 'people' in source and source['people']:
                updatedict.update({'people': source['people']})
            if 'residents' in source and source['residents']:
                updatedict.update({'residents': source['residents']})
            #checking the cache for data
            for key in updatedict:
                for i in self.cache:
                    try:
                        if updatedict[key] == i['url']:
                            try:
                                updatedict2.update({key:i['title']})
                                seealsoupdate.append(i)
                            except KeyError:
                                updatedict2.update({key:i['name']})
                                seealsoupdate.append(i)
                    except KeyError:
                        pass
            for key in updatedict2:
                updatedict.pop(key)

        #requesting the data from the API

        async def getupdates():
            update = []
            tasklist = []

            async def getdata(url):
                response = requests.get(url)
                update.append(response.json())

            async def prepareupdate():
                for key in updatedict:
                    if type(updatedict[key]) == str:
                        tasklist.append(asyncio.create_task(getdata(updatedict[key])))
                    else:
                        for _ in range(len(updatedict[key])):
                            tasklist.append(asyncio.create_task(getdata(updatedict[key][_])))
                await asyncio.gather(*tasklist)

            await prepareupdate()
            for key in updatedict:
                if type(updatedict[key]) == str:
                    for i in update:
                        if i['url'] == updatedict[key]:
                            try:
                                updatedict2.update({key: i['name']})
                                seealsoupdate.append(i)
                            except KeyError:
                                updatedict2.update({key: i['title']})
                                seealsoupdate.append(i)
                else:
                    updatearray = []
                    for j in range(len(updatedict[key])):
                        for i in update:
                            if i['url'] == updatedict[key][j]:
                                try:
                                    updatearray.append(i['name'])
                                    seealsoupdate.append(i)
                                except KeyError:
                                    updatearray.append(i['title'])
                                    seealsoupdate.append(i)
                    updatedict2.update({key: updatearray})
            for i in update:
                self.cache.append(i)

        try:
            if source['updated']:
                pass
        except KeyError:
            asyncio.run(getupdates())
            #loading the data
            for key in updatedict2:
                source.update({key: updatedict2[key]})
            source.update({'updated': True})
        #displaying the data
        try:
            for key in source:
                if key != 'created' and key != 'edited' and key != 'url' and key != 'updated':
                    if not source[key]:
                        displaytext.append(' '.join((key[0].upper()+key[1:]).split('_')) + ':')
                    elif key == 'title':
                        displaytext.append(source[key])
                    elif key == 'episode_id':
                        displaytext.append('Episode ' + self.int_to_Roman(source[key]))
                    elif key == 'opening_crawl':
                        displaytext.append('\n' + source[key] + '\n')
                    elif key == 'height':
                        displaytext.append(key[0].upper()+key[1:] + ': ' + source[key] + ' cm')
                    elif key == 'mass':
                        displaytext.append(key[0].upper()+key[1:] + ': ' + source[key] + ' kg')
                    elif key == 'cost_in_credits':
                        displaytext.append(' '.join((key[0].upper()+key[1:]).split('_')) + ': ' + source[key] + ' credits')
                    elif key == 'length':
                        displaytext.append(key[0].upper()+key[1:] + ': ' + source[key] + ' m')
                    elif key == 'max_atmosphering_speed':
                        displaytext.append(' '.join((key[0].upper()+key[1:]).split('_')) + ': ' + source[key] + ' kph')
                    elif key == 'average_height':
                        displaytext.append(' '.join((key[0].upper()+key[1:]).split('_')) + ': ' + source[key] + ' cm')
                    elif key == 'average_lifespan':
                        displaytext.append(' '.join((key[0].upper()+key[1:]).split('_')) + ': ' + source[key] + ' years')
                    elif key == 'diameter':
                        displaytext.append(key[0].upper()+key[1:] + ': ' + source[key] + ' km')
                    elif key == 'gravity':
                        displaytext.append(key[0].upper()+key[1:] + ': ' + source[key] + ' Gs')
                    else:
                        if type(source[key]) == int:
                            source[key] = str(source[key])
                        try:
                            displaytext.append(' '.join((key[0].upper()+key[1:]).split('_')) + ': ' + source[key])
                        except TypeError:
                            subdisplay = [' '.join((key[0].upper()+key[1:]).split('_')) + ': ']
                            for i in range(len(source[key])):
                                if i < (len(source[key])-1):
                                    subdisplay.append(source[key][i] + ',')
                                else:
                                    subdisplay.append(source[key][i])
                            displaytext.append(' '.join(subdisplay))
            self.display.config(state='normal')
            self.display.delete('1.0', tk.END)
            self.display.insert('1.0', '\n'.join(displaytext))
            self.display.config(state='disabled')
            self.seealso.clear()
            self.seealsolist.delete(0, tk.END)
            for i in seealsoupdate:
                self.seealso.append(i)
            count = 1
            for i in self.seealso:
                try:
                    self.seealsolist.insert(count, i['title'])
                except KeyError:
                    self.seealsolist.insert(count, i['name'])
                count += 1
        except IndexError:
            return

    def seeingalso(self):
        self.viewresult(seealso=True)

    def int_to_Roman(self, num):
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
        ]
        syb = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
        ]
        roman_num = ''
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                roman_num += syb[i]
                num -= val[i]
            i += 1
        return roman_num


root = tk.Tk()
app = Window(root)
root.mainloop()
