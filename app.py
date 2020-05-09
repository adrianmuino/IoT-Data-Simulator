import wx
import faker, random, json
from datetime import timedelta
import datetime
import pandas as pd

import matplotlib.pyplot as plt
plt.style.use(['classic', 'ggplot'])

import pylab 
pylab.rcParams.update({'font.family' : 'serif'})

class windowClass(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(windowClass, self).__init__(*args, **kwargs) 
        
        self.Centre()
        self.basicGUI()

    def basicGUI(self):
        self.panel = wx.Panel(self)
        menuBar = wx.MenuBar()
        fileButton = wx.Menu()
        statisticsButton = wx.Menu()
        
        
        exitItem = fileButton.Append(wx.ID_EXIT, 'Exit\tCtrl+Q', 'Quit Application...')

        generateItem = fileButton.Append(wx.ID_ANY, 'Generate IoT\tCtrl+G', 'Generate IoT data...')
        jsonItem = fileButton.Append(wx.ID_ANY, 'Save JSON\tCtrl+J', 'Save IoT data into a JSON file...')
        csvItem = fileButton.Append(wx.ID_ANY, 'Save CSV\tCtrl+S', 'Save IoT data into a CSV file...')

        descriptiveItem = statisticsButton.Append(wx.ID_ANY, 'Descriptive\tCtrl+D', 'Show statistical description of IoT data...')
        plotAItem = statisticsButton.Append(wx.ID_ANY, 'Plot A\tCtrl+A', 'Generate histogram of outside temperature...')
        plotBItem = statisticsButton.Append(wx.ID_ANY, 'Plot B\tCtrl+B', 'Generate line graph of the outside temperature vs the inside temperature...')
        plotCItem = statisticsButton.Append(wx.ID_ANY, 'Plot C\tCtrl+C', 'Generate histogram of the room temperature, outside temperature, and humidity for all users...')
        

        menuBar.Append(fileButton, 'File')
        menuBar.Append(statisticsButton, 'Statistics')
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.Quit, exitItem)
        self.Bind(wx.EVT_MENU, self.GenerateIoT, generateItem)
        self.Bind(wx.EVT_MENU, self.SaveJSON, jsonItem)
        self.Bind(wx.EVT_MENU, self.SaveCSV, csvItem)
        self.Bind(wx.EVT_MENU, self.Descriptive, descriptiveItem)
        self.Bind(wx.EVT_MENU, self.PlotA, plotAItem)
        self.Bind(wx.EVT_MENU, self.PlotB, plotBItem)
        self.Bind(wx.EVT_MENU, self.PlotC, plotCItem)

        self.statusBar = self.CreateStatusBar(1)
        self.statusBar.SetStatusText('Waiting to analyze IoT data')
        
        self.SetTitle('Environment Analyzer')
        self.Show(True)

    def Quit(self,e):
        yesNoBox = wx.MessageDialog(None, 'Are you sure you want to Quit?', 'Question', wx.YES_NO)
        yesNoAnswer = yesNoBox.ShowModal()
        yesNoBox.Destroy()
        if yesNoAnswer == wx.ID_YES:
            self.Close()
        
    def GenerateIoT(self,e):
        wx.MessageBox('Generating IoT data in progress.\nThis may take a few seconds!', 'Generating data', wx.OK | wx.CENTRE | wx.ICON_INFORMATION | wx.STAY_ON_TOP)
        
        fake = faker.Faker()
        
        usernames = set()
        username_no = 1000
        while len(usernames) < username_no:
            usernames.add(fake.user_name())

        sensor_records_no = 1000
        start_date = datetime.datetime(2015, 1, 1)

        def get_sensor_record():
            def gen_date_time(start_date, sensor_records_no):
                for sensor in range(sensor_records_no):
                    date, time = str(start_date).split()
                    yield date, time
                    start_date += timedelta(hours = 6)
  
            sensor_record = []
    
            for date, time in gen_date_time(start_date, sensor_records_no):
                outside_temp = random.randint(70, 95)
                outside_hum = random.randint(50, 95)
        
                sensor_info = {
                    'date': date,
                    'time': time,
                    'outside_temp': outside_temp,
                    'outside_hum': outside_hum,
                    'room_temp': outside_temp - random.randint(0, 10),
                    'room_hum': outside_hum - random.randint(0, 10)
                }
                sensor_record.append(sensor_info)
            return sensor_record

        def get_users():
            def random_name_gender():
                if random.random() > 0.5:
                    name, gender = fake.name_male().split(), 'M'
                else:
                    name, gender = fake.name_female().split(), 'F'
                return name[0], name[1], gender
    
            users = []
            for username in usernames:
                first, last, gender = random_name_gender()
                user = {
                    'first_name' : first,
                    'last_name' : last,
                    'age' : fake.random_int(min = 18, max = 90),
                    'gender' : gender,
                    'username' : username,
                    'address' : fake.address(),
                    'email' : fake.email(),
                    'sensor_record' : get_sensor_record()
                }
                users.append(user)
            return users
        
        self.df = pd.DataFrame(get_users())

        rows = []
        for record_no in range(len(self.df)):
            rows.append(pd.DataFrame(self.df['sensor_record'][record_no]))
        self.sensor_data = pd.concat(rows, ignore_index = True)

        column_names= ['Date', 'Time', 'Outside Temperature', 'Outside Humidity', 'Room Temperature', 'Room Humidity']
        self.sensor_data.columns = column_names

        wx.MessageBox('IoT data has been successfully generated.', 'Generating data', wx.OK | wx.CENTRE | wx.ICON_INFORMATION | wx.STAY_ON_TOP)
        self.statusBar.SetStatusText('Data generated')

    def SaveJSON(self,e):
        try:
            if len(self.df) == 0:
                raise AttributeError
            with wx.FileDialog(self,'Save JSON file', wildcard = 'JSON Files (*.json)|*.json', style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
    
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return
                else:
                    path = fileDialog.GetPath()
                    try:
                        self.df.to_json(path)
                        self.statusBar.SetStatusText('IoT data successfully saved to JSON file')
                    except IOError:
                        wx.LogError("Cannot save current data in file '%s'." % path)
        except AttributeError:
            wx.MessageBox('IoT data has to be generated first.', 'App Error', wx.OK | wx.CENTRE | wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
            
    def SaveCSV(self,e):
        try:
            if len(self.df) == 0:
                raise AttributeError
            with wx.FileDialog(self,'Save CSV file', wildcard = 'CSV Files (*.csv)|*.csv', style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
    
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return
                else:
                    path = fileDialog.GetPath()
                    try:
                        self.df.to_csv(path)
                        self.statusBar.SetStatusText('IoT data successfully saved to CSV file')
                    except IOError:
                        wx.LogError("Cannot save current data in file '%s'." % path)
        except AttributeError:
            wx.MessageBox('IoT data has to be generated first.', 'App Error', wx.OK | wx.CENTRE | wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
    
    def Descriptive(self,e):
        try:

            stats_df = self.sensor_data.describe()

            description = ''
            for col in stats_df.columns:
                description += col + '\n'
                for row in stats_df.index:
                    description += '\t'+ row + ': '+ str(stats_df.loc[row][col]) + '\n'

            statsDialog = wx.MessageDialog(None, description, 'Description', wx.OK | wx.CENTRE | wx.STAY_ON_TOP | wx.ICON_NONE)
            userClick = statsDialog.ShowModal()
            statsDialog.Destroy()
        except AttributeError:
            wx.MessageBox('IoT data has to be generated first.', 'App Error', wx.OK | wx.CENTRE | wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)

    def PlotA(self,e):
        try:
            if len(self.sensor_data) == 0:
                raise AttributeError
            fig, axes = plt.subplots(nrows = 2, ncols = 2 , figsize = (15,8))
            self.sensor_data[self.sensor_data.Time == '00:00:00']['Outside Temperature'].plot(title = 'Outside Temperature at 12AM', kind = 'hist', bins = 26, ax = axes[0,0])
            axes[0][0].title.set_size(18)

            self.sensor_data[self.sensor_data.Time == '06:00:00']['Outside Temperature'].plot(title = 'Outside Temperature at 6AM', kind = 'hist', bins = 26, ax = axes[0,1], color = 'green')
            axes[0][1].title.set_size(18)

            self.sensor_data[self.sensor_data.Time == '12:00:00']['Outside Temperature'].plot(title = 'Outside Temperature at 12PM', kind = 'hist', bins = 26, ax = axes[1,0], color = 'blue')
            axes[1][0].title.set_size(18)

            self.sensor_data[self.sensor_data.Time == '18:00:00']['Outside Temperature'].plot(title = 'Outside Temperature at 6PM', kind = 'hist', bins = 26, ax = axes[1,1], color = 'teal')
            axes[1][1].title.set_size(18)

            fig.tight_layout(pad = 3)

            plt.show()    
        except AttributeError:    
            wx.MessageBox('IoT data has to be generated first.', 'App Error', wx.OK | wx.CENTRE | wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)

    def PlotB(self,e):
        try:
            if len(self.sensor_data) == 0:
                raise AttributeError
            grouped_data_mean = self.sensor_data.groupby('Outside Temperature').mean()
            grouped_data_mean.plot(y = 'Room Temperature', subplots = True)
            plt.show()
        except AttributeError:
            wx.MessageBox('IoT data has to be generated first.', 'App Error', wx.OK | wx.CENTRE | wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)

    def PlotC(self,e):
        try:
            if len(self.sensor_data) == 0:
                raise AttributeError
            fig, axes = plt.subplots(nrows = 2, ncols = 2 , figsize = (15,8))
            self.sensor_data['Room Temperature'].plot(title = 'Room Temperature', kind = 'hist', bins = 18, ax = axes[0,0])
            axes[0][0].title.set_size(18)

            self.sensor_data['Outside Temperature'].plot(title = 'Outside Temperature', kind = 'hist', bins = 13, ax = axes[0,1], color = 'teal')
            axes[0][1].title.set_size(18)

            self.sensor_data['Room Humidity'].plot(title = 'Room Humidity', kind = 'hist', bins = 28, ax = axes[1,0])
            axes[1][0].title.set_size(18)

            self.sensor_data['Outside Humidity'].plot(title = 'Outside Humidity', kind = 'hist', bins = 23, ax = axes[1,1], color = 'teal')
            axes[1][1].title.set_size(18)

            fig.tight_layout(pad = 3)

            plt.show()

        except AttributeError:
            wx.MessageBox('IoT data has to be generated first.', 'App Error', wx.OK | wx.CENTRE | wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)

def main():
    app = wx.App()
    windowClass(None, 0, size = (500, 400))

    app.MainLoop()

main()
