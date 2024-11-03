from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from StationTime import StationTime as Station
import requests
import time
from datetime import datetime

# A list of all the station in the WAMATA network with their attached web address ends
station_lst = {
    'Addison Road': '#G03|Addison Road-Seat Pleasant',
    'Anacostia': '#F06|Anacostia',
    'Archives-Navy Memorial-Penn Quarter': '#F02|Archives-Navy Memorial-Penn Quarter',
    'Arlington Cemetery': '#C06|Arlington Cemetery',
    'Ashburn': '#N12|Ashburn',
    'Ballston-MU': '#K04|Ballston-MU',
    'Benning Road': '#G01|Benning Road',
    'Bethesda': '#A09|Bethesda',
    'Braddock Road': '#C12|Braddock Road',
    'Branch Ave': '#F11|Branch Ave',
    'Brookland-CUA': '#B05|Brookland-CUA',
    'Capitol Heights': '#G02|Capitol Heights',
    'Capitol South': '#D05|Capitol South',
    'Cheverly': '#D11|Cheverly',
    'Clarendon': '#K02|Clarendon',
    'Cleveland Park': '#A05|Cleveland Park',
    'College Park-U of Md' : '#E09|College Park-U of Md',
    'Columbia Heights': '#E04|Columbia Heights',
    'Congress Heights': '#F07|Congress Heights',
    'Court House': '#K01|Court House',
    'Crystal City': '#C09|Crystal City',
    'Deanwood': '#D10|Deanwood',
    'Downtown Largo': '#G05|Downtown Largo',
    'Dunn Loring-Merrifield': '#K07|Dunn Loring-Merrifield',
    'Dupont Circle': '#A03|Dupont Circle',
    'East Falls Church': '#K05|East Falls Church',
    'Eastern Market': '#D06|Eastern Market',
    'Eisenhower Avenue': '#C14|Eisenhower Avenue',
    'Farragut North': '#A02|Farragut North',
    'Farragut West' : '#C03|Farragut West',
    'Federal Center SW': '#D04|Federal Center SW',
    'Federal Triangle': '#D01|Federal Triangle',
    'Foggy Bottom-GWU': '#C04|Foggy Bottom-GWU',
    'Forest Glen': '#B09|Forest Glen',
    'Fort Totten': '#B06,E06|Fort Totten',
    'Franconia Springfield': '#J03|Franconia-Springfield',
    'Friendship Heights': '#A08|Friendship Heights',
    'Gallery PI-Chinatown': '#B01,F01|Gallery Pl-Chinatown',
    'Georgia Ave-Petworth': '#E05|Georgia Ave-Petworth',
    'Glenmont': '#B11|Glenmont',
    'Greenbelt': '#E10|Greenbelt',
    'Greensboro': '#N03|Greensboro',
    'Grosvenor-Strathmore': '#A11|Grosvenor-Strathmore',
    'Herndon': '#N08|Herndon',
    'Huntington': '#C15|Huntington',
    'Hyattsville Crossing': '#E08|Hyattsville Crossing',
    'Innovation Center': '#N09|Innovation Center',
    'Judiciary Square': '#B02|Judiciary Square',
    'King St-Old Town': '#C13|King St-Old Town',
    "L'Enfant Plaza": "#D03,F03|L'Enfant Plaza",
    'Landover': '#D12|Landover',
    'Loudoun Gateway': '#N11|Loudoun Gateway',
    'McLean': '#N01|McLean',
    'McPherson Square': '#C02|McPherson Square',
    'Medical Center': '#A10|Medical Center',
    'Metro Center': '#A01,C01|Metro Center',
    'Minnesota Ave': '#D09|Minnesota Ave',
    'Morgan Boulevard': '#G04|Morgan Boulevard',
    'Mt Vernon Sq 7th St-Convention Center': '#E01|Mt Vernon Sq 7th St-Convention Center',
    'Navy Yard-Ballpark': '#F05|Navy Yard-Ballpark',
    'Naylor Road': '#F09|Naylor Road',
    'New Carrollton': '#D13|New Carrollton',
    'NoMA-Gallaudet U': '#B35|NoMa-Gallaudet U',
    'North Bethesda': '#A12|North Bethesda',
    'Pentagon' : '#C07|Pentagon',
    'Pentagon City': '#C08|Pentagon City',
    'Potomac Ave': '#D07|Potomac Ave',
    'Potomac Yard': '#C11|Potomac Yard',
    'Reston Town Center': '#N07|Reston Town Center',
    'Rhode Island Ave-Brentwood': '#B04|Rhode Island Ave-Brentwood',
    'Rockville': '#A14|Rockville',
    'Ronald Regan Washington National Airport': '#C10|Ronald Reagan Washington National Airport',
    'Rosslyn': '#C05|Rosslyn',
    'Shady Grove': '#A15|Shady Grove',
    'Shaw-Howard U': '#E02|Shaw-Howard U',
    'Silver Spring': '#B08|Silver Spring',
    'Silver Spring Transit Center': '#T81|Silver Spring Transit Center',
    'Smithsonian': '#D02|Smithsonian',
    'Southern Avenue': '#F08|Southern Avenue',
    'Spring Hill': '#N04|Spring Hill',
    'Stadium-Armory': '#D08|Stadium-Armory',
    'Suitland': '#F10|Suitland',
    'Takoma': '#B07|Takoma',
    'Tenleytown-AU': '#A07|Tenleytown-AU',
    'Twinbrook': '#A13|Twinbrook',
    'Tysons': '#N02|Tysons',
    'U Street-Cardozo': '#E03|U Street/African-Amer Civil War Memorial/Cardozo',
    'Union Station': '#B03|Union Station',
    'Van Dorn Street': '#J02|Van Dorn Street',
    'Van Ness-UDC': '#A06|Van Ness-UDC',
    'Vienna/Fairfax-GMU': '#K08|Vienna/Fairfax-GMU',
    'Virginia Square-GMU': '#K03|Virginia Square-GMU',
    'Washington Dulles International Airport': '#N10|Washington Dulles International Airport',
    'Waterfront': '#F04|Waterfront',
    'West Falls Church': '#K06|West Falls Church',
    'West Hyattsville': '#E07|West Hyattsville',
    'Wheaton': '#B10|Wheaton',
    'Wiehle-Reston East': '#N06|Wiehle-Reston East',
    'Woodley Park-Zoo/Adams Morgan': '#A04|Woodley Park-Zoo/Adams Morgan'
}
station = {}
obj_lst = []

# Using Firefox Web Browser
driver = webdriver.Firefox()
url = 'https://www.wmata.com/js/nexttrain/nexttrain.html'

# Creates a StationTime object for every station in the station_lst
for stop in station_lst:
    obj_lst.append(Station(stop))


# This code runs for 3600s (1hr) gathering data
output_filename = datetime.now().strftime("%Y%m%d-%H%M%S") + "_wama.csv"
end_time = time.time()+3600
while time.time() < end_time:
    for i, entity in enumerate(station_lst):
        # Accesses the web address of each station in station_lst
        new_url = url + station_lst[entity]
        driver.get(new_url)
        platforms = driver.find_elements(By.CLASS_NAME, 'panel-col')

        # Counter for each potential platform at the station, reset
        counter = 1

        # Sleep step assures that all the data is scraped correctly (and not missed)
        time.sleep(0.5)

        # Loop for each platform
        for platform in platforms:
            # Organizes and gathers the data
            trains = platform.find_elements(By.CLASS_NAME, 'train-data')
            timetable = trains[0].text.split('\n')

            # Assures that the data exists
            if len(timetable[0]) > 1 and timetable[0] != '-- Data not available.':
                # For each possible train arriving at the specified platform
                for j,item in enumerate(timetable):
                    raw = item.split(' ')
                    try:
                        raw.remove('Line')
                    except:
                        continue
                    raw[0] = raw[0] + ' Line'
                    while len(raw) != 4:
                        destination = raw.pop(len(raw)-2)
                        raw[2] = raw[2] + ' ' + destination
                    timetable[j] = tuple(raw)
            else:
                timetable[0] = None

            # Appends the data on the next incoming train to the station tuple that was initialized above
            station[counter] = timetable
            counter += 1

        # Checks to see if a train has arrived and creates a datapoint if so
        obj_lst[i].difference(station)

# Prints all of the stations and the corresponding datapoints that were gathered during the trial
with open(output_filename, "a") as csvfile:
    for obj in obj_lst:
        print(obj, file=csvfile)

# Closes the webdriver
driver.close()
