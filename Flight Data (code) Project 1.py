
import pandas as pd
import datetime as dt
#Import Table
df = pd.read_table('./Resources/flight_edges.tsv', names=['Origin Airport', 'Destination Airport', 'Origin City', 'Destination City', 
                                                          'Passengers', 'Seats', 'Flights', 'Distance', 'Fly Date', 'Origin Population', 'Destination Population'])
df.head()

#Check for NA
df.shape[0]

df.dropna(inplace=True)
df.shape[0]

#Check number of unique origins
len(df['Origin Airport'].unique())

#Split year month
df['Fly Date'] = df['Fly Date'].astype(str)
df['Year'], df['Month'] = df['Fly Date'].str[:4], df['Fly Date'].str[4:]
df.head()

df['Percent Full'] = round((df['Passengers'] / df['Seats']), 2)
df.head()

#Reorder columsns (not nessecary)
df = df[['Origin Airport', 'Origin City', 'Origin Population', 'Destination Airport',  'Destination City', 'Destination Population','Distance', 'Flights', 'Passengers', 
		   'Seats', 'Percent Full', 'Fly Date', 'Month', 'Year']]
df.head()

df.to_csv('./Resources/clean_data_ym_load.csv', index=False)
 
df = pd.read_csv('./Resources/clean_data_ym_load.csv')
df.head()

def numfmtTH(x, pos):
    s = '{}'.format(int(x/1000))
    return s

def numfmtMIL(x, pos):
    s = '{}'.format(int(x/1000000))
    return s

percentFormatter = tkr.PercentFormatter(xmax=1.0, decimals=0)
label_font = {
    'fontweight': 'bold',  
    'fontsize': 12,        
}

# Remove where two columns are equal, this step may be skipped
# New question: how may airports have flights originating and arriving at themselves?
count = df[df['Destination Airport'] == df['Origin Airport']]
df = df[df['Destination Airport'] != df['Origin Airport']]
len(count)

Get Route Frequency and Count of Unique Routes

#Count of unique routes, summing the value in the Flights column (number of flights in the given month)
uniqueRoutes = df.groupby(['Origin Airport', 'Destination Airport'])['Flights'].sum().reset_index()
uniqueRoutes.head()

#Total number of unique routes
uniqueRoutes.shape[0]

# Amadas code for getting route info
df["Route"] = df["Origin Airport"] + "_" + df["Destination Airport"]
passenger_count = df[["Route", "Passengers"]].groupby("Route").sum().sort_values("Passengers", ascending=False)

demand = passenger_count.merge(df[["Route", "Origin Airport", "Origin City", "Destination Airport", "Destination City", 'Distance']], on="Route", how="inner").groupby("Route").first().sort_values("Passengers", ascending=False)
demand.head(10)

# Amadas code for getting route info
# SLIGHTLY ALTERED FROM CELL ABOVE TO LOOK AT FLIGHT COUNT RATHER THAN PASSANGER LOAD
df["Route"] = df["Origin Airport"] + "_" + df["Destination Airport"]
flight_count = df[["Route", "Flights"]].groupby("Route").sum().sort_values("Flights", ascending=False)

flightDF = flight_count.merge(df[["Route", "Origin Airport", "Origin City", "Destination Airport", "Destination City", 'Distance']], on="Route", how="inner").groupby("Route").first().sort_values("Flights", ascending=False)
flightDF.head(10)

Pie Chart With Dest Code


#Get count of each occurance of a destination code
destFlights = df.groupby(['Destination Airport'])['Flights'].sum().reset_index()
destFlights.sort_values('Flights', inplace=True, ascending=False)
destFlights.head()

#Shows the top N Airports. Change numEntries to change N
#Should note that looks identical to the arrivals, the difference is in the 0.01% area, numbers round to the save value
numEntries = 10
shorteneda = destFlights.iloc[:numEntries]

plt.pie(shorteneda['Flights'], labels=shorteneda['Destination Airport'], autopct='%1.1f%%', radius=2)
plt.title(f"Percent Share of the Top {numEntries} Airports", y=1.4)
plt.show()

shortSum = shorteneda['Flights'].sum()
longSum = destFlights['Flights'].sum()
pctShown = round(((shortSum/longSum) * 100), 2)

print(f"The above chart accounts for {pctShown}% of flights")

#Shows All flights, and the top N with respect to that
numEntries = 10

topN = destFlights.head(numEntries)
everythingElse = destFlights['Flights'][numEntries:].sum()

topN.loc[len(topN.index)] = [' ', everythingElse]

topN['Percent Makeup'] = round((topN['Flights']/topN['Flights'].sum()), 4)
topN['Percent Makeup'] = topN['Percent Makeup'].apply('{:.1%}'.format)

labels = topN['Destination Airport']
values = topN['Flights']

# plot the pie chart with 11 colors and custom text properties
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'purple', 'lightgreen', 'hotpink', 'darkturquoise', 'darkgray']

plt.pie(values, labels=labels, colors=colors, radius=2, textprops=label_font)
plt.rcParams.update({'font.size' : 10})

source_note = 'Source: infochimps.com'
plt.text(-2, -2, source_note, fontsize=10, ha='left', va='center')

plt.legend(topN['Percent Makeup'], title='Percent Share', loc='center left', bbox_to_anchor=(-.09, .5))
plt.title(f'Top {numEntries} Highest Frequency Airports', y=1.4, fontweight='bold', fontsize=20, loc='center')
plt.show()

#Generated another chart to try and have a simple alternative. Size may need touching up
numEntries = 10

topN = destFlights.head(numEntries)
totalTopN = topN['Flights'].sum()
everythingElse = destFlights['Flights'][numEntries:].sum()

#topN.loc[len(topN.index)] = ['Outside Top 10', everythingElse]

labels = [f'Top {numEntries} Airports', f'Outside Top {numEntries} Airports']
values = [totalTopN, everythingElse]

plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.title(f'Top {numEntries} Destinations in perspective')
plt.show()

Pie Chart With Orig Code

origFlights = df.groupby(['Origin Airport'])['Flights'].sum().reset_index()
origFlights.sort_values('Flights', inplace=True, ascending=False)
origFlights.head()

numEntries = 10
shortenedb = origFlights.iloc[:numEntries]

plt.pie(shortenedb['Flights'], labels=shortenedb['Origin Airport'], autopct='%1.1f%%', radius=2)
plt.title("Percent of flights starting at a given airport", y=1.4)
plt.show()

shortSum = shortenedb['Flights'].sum()
longSum = origFlights['Flights'].sum()
pctShown = round(((shortSum/longSum) * 100), 2)

print(f"The above chart accounts for {pctShown}% of flights")

avgPctFull = df.groupby(['Origin Airport', 'Destination Airport'])['Percent Full'].mean().reset_index()
avgPctFull.head()

fullFrame = pd.merge(uniqueRoutes, avgPctFull, on=['Origin Airport', 'Destination Airport'])
withNA = len(fullFrame)
fullFrame.dropna(inplace=True)
droppedNA = len(fullFrame)

print(f"There where {withNA - droppedNA} flights with NA values, assumed to be empty flights")

#List of flights over capacity to reference/analyze
flightsOverCapacity = df[df['Percent Full'] > 1]
flightsOverCapacity = flightsOverCapacity[flightsOverCapacity['Flights'] != 0]
flightsOverCapacity = flightsOverCapacity[flightsOverCapacity['Seats'] != 0]
print(f'There are {len(flightsOverCapacity)} instances of flights running over capacity')
flightsOverCapacity.sort_values('Percent Full', ascending=False)

#Trimmed dataframe with only flights that aren't over capacity
ignoreOverflow = fullFrame[fullFrame['Percent Full'] < 1]
ignoreOverflow.head()

#Scatter plot with full frame/outliers
plt.scatter(fullFrame['Percent Full'], fullFrame['Flights'])
yfmt = tkr.FuncFormatter(numfmtTH)
plt.gca().yaxis.set_major_formatter(yfmt)
plt.gca().xaxis.set_major_formatter(percentFormatter)
plt.ylabel('Number of Flights in 1,000s')
plt.xlabel('Average Percent Full for each route')
plt.title('Flight Frequency as a function of Passenger Load')
plt.show()

#Scatter plot without full frame/outliers
plt.scatter(ignoreOverflow['Percent Full'], ignoreOverflow['Flights'])
yfmt = tkr.FuncFormatter(numfmtTH)
plt.gca().yaxis.set_major_formatter(yfmt)
plt.gca().xaxis.set_major_formatter(percentFormatter)
plt.ylabel('Number of Flights (in thousands)', fontweight='bold')
plt.xlabel('Average Load Factor', fontweight='bold')
plt.title('Flight Frequency vs Load Factor', fontweight='bold')

medLoad = ignoreOverflow['Percent Full'].median()
meanLoad = ignoreOverflow['Percent Full'].mean()
plt.axvline(x = medLoad, color = 'y', label = 'axvline - full height')
plt.axvline(x = meanLoad, color = 'r', label = 'axvline - full height')

plt.show()

print(round(ignoreOverflow['Percent Full'].median(),2))
print(round(ignoreOverflow['Percent Full'].mean(),2))

#Regression function/p-value including outliers
(slope, intercept, rvalue, pvalue, stderr) = st.linregress(ignoreOverflow['Flights'], ignoreOverflow['Percent Full'])
print(pvalue)

print(f'p = {slope}f + {intercept}')
print(stderr)
print(str(stderr * stderr))

st.ttest_ind(ignoreOverflow['Flights'], ignoreOverflow['Percent Full'])

#Regression function/p-value excluding outliers
(slope, intercept, rvalue, pvalue, stderr) = st.linregress(ignoreOverflow['Flights'], ignoreOverflow['Percent Full'])
print(pvalue)

print(f'p = {slope}f + {intercept}')

#Distribution check of all passenger loads
plt.hist(fullFrame[['Percent Full']], bins = 30)

plt.gca().xaxis.set_major_formatter(percentFormatter)
plt.ylabel('Frequency of Value')
plt.xlabel('Average Percent Full for each route')
plt.title('Distribution of Passenger Load')
ax = plt.gca()
ax.set_xlim([0.0, 1.1])
plt.show()

#Distribution of passenger load ignoring outliers
plt.hist(ignoreOverflow[['Percent Full']], bins = 30)

plt.gca().xaxis.set_major_formatter(percentFormatter)
plt.ylabel('Frequency of Value')
plt.xlabel('Average Percent Full for each route')
plt.title('Distribution of Passenger Load')
plt.show()

test = fullFrame[fullFrame['Percent Full'] == 0]
print(f'We currently have {len(test)} routes that are running at an average of 0% full')

dropEmptyRouteWithOverflow = fullFrame[fullFrame['Percent Full'] != 0]
dropEmptyRouteWithoutOverflow = ignoreOverflow[ignoreOverflow['Percent Full'] != 0]
#Distribution of passenger load with upper outliers but no "empty" flights. 
plt.hist(dropEmptyRouteWithOverflow[['Percent Full']], bins = 30)

plt.gca().xaxis.set_major_formatter(percentFormatter)
plt.ylabel('Frequency of Value')
plt.xlabel('Average Percent Full for each route')
plt.title('Distribution of Passenger Load')
plt.show()

#Distribution of passenger load without upper outliers and no "empty" flights. 
plt.hist(dropEmptyRouteWithoutOverflow[['Percent Full']], bins = 30)

plt.gca().xaxis.set_major_formatter(percentFormatter)
plt.ylabel('Frequency of Value', fontweight='bold')
plt.xlabel('Average Load Factor', fontweight='bold')
plt.title('Distribution of Load Factor', fontweight='bold')
ax = plt.gca()
ax.set_xlim([0.0, 1])
plt.show()

test = df[df['Destination Airport'] == 'TSS']
test.head()

df2 = df.copy()
oriDest = 'Origin'

portCode = f'{oriDest} Airport'
coi = f'{oriDest} Population'

codeLookup = df2[[portCode, coi]].drop_duplicates(keep='first')
codeLookup = codeLookup.groupby(portCode)[coi].mean().reset_index()
codeLookup
#Column of interest will be abreviated to coi
dataOfInterest = pd.merge(uniqueRoutes, codeLookup, on=portCode)
dataOfInterest.tail()
withNA = len(dataOfInterest)
dataOfInterest.dropna(inplace=True)
droppedNA = len(dataOfInterest)

#No NA values found, skipping print statement
#print(f"There where {withNA - droppedNA} flights with NA values, assumed to be empty flights")
#dataOfInterest[coi].max()
dataOfInterest.sort_values(coi, ascending=False, inplace=True)
dataOfInterest

plt.scatter(dataOfInterest[coi], dataOfInterest['Flights'])
plt.ylabel('Number of Flights (thousands)', fontweight = 'bold')
plt.xlabel(f'{coi} (millions)', fontweight = 'bold')
plt.title(f'{coi} vs Number of Flights', fontweight = 'bold')

yfmt = tkr.FuncFormatter(numfmtTH)
plt.gca().yaxis.set_major_formatter(yfmt)
xfmt = tkr.FuncFormatter(numfmtMIL)
plt.gca().xaxis.set_major_formatter(xfmt)
#Change wording of axes and make it thousands rather than raw
#Change color of dots (teal? get hexcode/name)
#paleturqouise
plt.show()

(slope, intercept, rvalue, pvalue, stderr) = st.linregress(dataOfInterest[coi], dataOfInterest['Flights'])
print(rvalue)

Big City Small City Correlation
#This cell determines relative size of each city
destMed = df['Destination Population'].median()
origMed = df['Origin Population'].median()

destBins = [0, destMed, df['Destination Population'].max()]
origBins = [0, origMed, df['Origin Population'].max()]

glabels = ['Small City', 'Big City']

df['Origin Size'] = pd.cut(df['Origin Population'], origBins, labels=glabels)
df['Destination Size'] = pd.cut(df['Destination Population'], destBins, labels=glabels)
citySizeDf = df.groupby(['Origin Size', 'Destination Size'])['Flights'].sum().reset_index()
#Pie showing the percent share of route type. Route type is categorised by if it is leaving/arriving from a big/small city
#Of note: city category is determined by MEDIAN POPULATION as of writing. This can be changed by manipulating a cell above
labels = []
for item, row in citySizeDf.iterrows():
    labels.append(row['Origin Size'] + " to " + row['Destination Size'])

citySizeDf.index = labels

citySizeDf.plot(kind='pie', y='Flights', figsize=(9 , 9), autopct= '%1.1f%%', textprops=label_font)
plt.ylabel(' ')
plt.title('Percent of flights by route type', fontweight='bold')
plt.show()

#Route distance compared with route frequency: do shorter or longer routes fly more often?
#Included linear regression line in this one, exponential may be a better fit
x = flightDF['Distance']
y = flightDF['Flights']

(slope, intercept, rvalue, pvalue, stderr) = st.linregress(x, y)
regLine = (slope*x) + intercept

plt.plot(x, regLine, color='r', label=f'y = {slope}x + {intercept}')


plt.scatter(x, y)
yfmt = tkr.FuncFormatter(numfmtTH)
plt.gca().yaxis.set_major_formatter(yfmt)
plt.title('Route Distance vs Route Frequency')
plt.xlabel('Route Distance (miles)')
plt.ylabel('Route Frequency (in thousands of flights)')
plt.show()

#Route distance compared with route frequency: do shorter or longer routes fly more often?
#Regression line excluded so we have a 'tidy' chart if we decide we need one.
x = flightDF['Distance']
y = flightDF['Flights']

plt.scatter(x, y)
yfmt = tkr.FuncFormatter(numfmtTH)
plt.gca().yaxis.set_major_formatter(yfmt)
plt.title('Route Distance vs Route Frequency', fontweight='bold')
plt.xlabel('Route Distance (miles)', fontweight='bold')
plt.ylabel('Route Frequency (in thousands of flights)', fontweight='bold')
ax = plt.gca()
ax.set_xlim([0 - 100, x.max() + 100])
ax.set_ylim([0 - 10000, y.max() + 10000])
plt.show()

(slope, intercept, rvalue, pvalue, stderr) = st.linregress(x, y)
print(pvalue)

print(f'p = {slope}f + {intercept}')

df = pd.read_table('flight_edges.tsv')
df = pd.read_table('flight_edges.tsv', names=['Origin Airport', 'Destination Airport', 'Origin City', 'Destination City', 
                                                          'Passengers', 'Seats', 'Flights', 'Distance', 'Fly Date', 'Origin Population', 'Destination Population'])
df['Fly Date'] = df['Fly Date'].astype(str)
df['Year'], df['Month'] = df['Fly Date'].str[:4], df['Fly Date'].str[4:]
df.head()

# Code to retrieve the year of interest into separate data frames. 

_2004_df = df[df["Year"] == "2004"].copy()
_2005_df = df[df["Year"] == "2005"].copy()
_2006_df = df[df["Year"] == "2006"].copy()
_2007_df = df[df["Year"] == "2007"].copy()
_2008_df = df[df["Year"] == "2008"].copy()
_2009_df = df[df["Year"] == "2009"].copy()

# Code to retrieve the year of interest into separate data frames. 

_2004_df = df[df["Year"] == "2004"].copy()
_2005_df = df[df["Year"] == "2005"].copy()
_2006_df = df[df["Year"] == "2006"].copy()
_2007_df = df[df["Year"] == "2007"].copy()
_2008_df = df[df["Year"] == "2008"].copy()
_2009_df = df[df["Year"] == "2009"].copy()
# Defined the seasons based on the month of the flight

def season(row): 
    if row["Month"] =="12" or row["Month"] == "01" or row["Month"] == "02":
        return "Winter"
    elif row["Month"] =="03" or row["Month"] == "04" or row["Month"] == "05":
        return "Spring"
    elif row["Month"] =="06" or row["Month"] == "07" or row["Month"] == "08":
        return "Summer"
    else:
         return "Fall"
    
# Add a season's column to each data frame
    
_2004_df["Season"] = _2004_df.apply(season, axis =1)
_2005_df["Season"] = _2005_df.apply(season, axis =1)
_2006_df["Season"] = _2006_df.apply(season, axis =1)
_2007_df["Season"] = _2007_df.apply(season, axis =1)
_2008_df["Season"] = _2008_df.apply(season, axis =1)
_2009_df["Season"] = _2009_df.apply(season, axis =1)
# Calculated the number of passengers based on season and per year

_2004_passengers = _2004_df[["Season", "Passengers"]].groupby("Season").sum()
_2005_passengers = _2005_df[["Season", "Passengers"]].groupby("Season").sum()
_2006_passengers = _2006_df[["Season", "Passengers"]].groupby("Season").sum()
_2007_passengers = _2007_df[["Season", "Passengers"]].groupby("Season").sum()
_2008_passengers = _2008_df[["Season", "Passengers"]].groupby("Season").sum()
_2009_passengers = _2009_df[["Season", "Passengers"]].groupby("Season").sum()
# Plot the data to show the number of passengers per season, per year. 

x = np.arange(4)
width = 0.1

plt.figure(figsize=(10, 8))
plt.bar(x-0.3, _2004_passengers["Passengers"], width)
plt.bar(x-0.2, _2005_passengers["Passengers"], width)
plt.bar(x-0.1, _2006_passengers["Passengers"], width)
plt.bar(x, _2007_passengers["Passengers"], width)
plt.bar(x+0.1, _2008_passengers["Passengers"], width)
plt.bar(x+0.2, _2009_passengers["Passengers"], width)
plt.ylim(100000000, 170000000)
plt.yticks(fontweight = 'bold', fontsize = 12)
plt.xticks(x, ["Spring", "Summer", "Fall", "Winter"], fontweight = 'bold', fontsize = 14)
plt.xlabel("Seasons", fontweight = 'bold', fontsize = 16)
plt.ylabel("Number of Passengers in Millions", fontweight = 'bold', fontsize = 16)
plt.legend(["2004", "2005", "2006", "2007", "2008", "2009"], loc='upper right')
plt.title("Seasonal Air Travel", fontweight = 'bold', fontsize = 22)
current_values = plt.gca().get_yticks()
plt.gca().set_yticklabels(['{:,.0f}'.format(x / 1000000) for x in current_values])
plt.show()

df = pd.read_table('flight_edges.tsv', names=['Origin Airport', 'Destination Airport', 'Origin City', 'Destination City', 
                                                          'Passengers', 'Seats', 'Flights', 'Distance', 'Fly Date', 'Origin Population', 'Destination Population'])
df.head()
df = pd.read_table('flight_edges.tsv', names=['Origin Airport', 'Destination Airport', 'Origin City', 'Destination City', 
                                                          'Passengers', 'Seats', 'Flights', 'Distance', 'Fly Date', 'Origin Population', 'Destination Population'])
df.head()

# Set the API base URL

url = "http://api.openweathermap.org/data/2.5/weather?"

city_coordinates = {}

# Determine the latitude and longitude of the origin city and destination city

for city in top_ten_routes_df["Origin City"]:
    if city not in city_coordinates:
        city_coordinates[city] = {}
        city_url = f"{url}q={city[:-4]}&appid={weather_api_key}"

        try:
            city_data = requests.get(city_url).json()
            city_coordinates[city]["longitude"] = city_data["coord"]["lon"]
            city_coordinates[city]["latitude"] = city_data["coord"]["lat"]

        except:
            pass




for city in top_ten_routes_df["Destination City"]:
    if city not in city_coordinates:
        city_coordinates[city] = {}
        city_url = f"{url}q={city[:-4]}&appid={weather_api_key}"

        try:
            city_data = requests.get(city_url).json()
            city_coordinates[city]["longitude"] = city_data["coord"]["lon"]
            city_coordinates[city]["latitude"] = city_data["coord"]["lat"]

        except:
            pass

    
# Defined coordinates for latitude and longitude of the origin cities and destination cities

def get_coordinates(coord_type):
    def inner(city):
        return city_coordinates[city][coord_type]
    return inner


top_ten_routes_df["Origin Longitude"] = top_ten_routes_df["Origin City"].apply(get_coordinates("longitude"))
top_ten_routes_df["Origin Latitude"] = top_ten_routes_df["Origin City"].apply(get_coordinates("latitude"))

top_ten_routes_df["Destination Longitude"] = top_ten_routes_df["Destination City"].apply(get_coordinates("longitude"))
top_ten_routes_df["Destination Latitude"] = top_ten_routes_df["Destination City"].apply(get_coordinates("latitude"))

top_ten_routes_df

# Plot the origin and destination cities

origin_plot = top_ten_routes_df.hvplot.points(
    "Origin Longitude",
    "Origin Latitude",
    geo = True,
    tiles = "OSM",
    frame_width = 800, 
    frame_height = 600,
    scale = 1,
    size = 100,
    marker = "^",
    color = "Origin City",
    title = "Top Seven Originating Cities",
    hover_cols = ["Origin City", "Origin Airport", "Destination City", "Destination Airport"]    
)
origin_plot.opts(fontsize={'title':16},title="Top Seven Originating Cities")
# destination_plot = top_ten_routes_df.hvplot.points(
#     "Destination Longitude",
#     "Destination Latitude",
#     geo = True,
#     tiles = "OSM",
#     frame_width = 800, 
#     frame_height = 600,
#     scale = 1,
#     size = 100,
#     marker = "v",
#     color = "Destination City",
#     hover_cols = ["Origin City", "Origin Airport", "Destination City", "Destination Airport"]
# )

# city_plot = origin_plot * destination_plot
# city_plot
origin_plot
destination_plot = top_ten_routes_df.hvplot.points(
    "Destination Longitude",
    "Destination Latitude",
    geo = True,
    tiles = "OSM",
    frame_width = 800, 
    frame_height = 600,
    scale = 1,
    size = 100,
    marker = "o",
    color = "Destination City",
    title = "Top Six Destination Cities",
    hover_cols = ["Origin City", "Origin Airport", "Destination City", "Destination Airport"]
)

destination_plot.opts(fontsize={'title':16},title="Top Six Destination Cities")
destination_plot