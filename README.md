# A PREDICTIVE ANALYSIS OF HOSPITAL BED AVAILABILITY DURING COVID-19 PANDEMIC

In order to gain a deeper understanding of a megamodel and the process for the hypothesis-driven experiment design, we opted for a current and simple study domain to degrade the complexity of the proposed system. We consider that a hospital bed availability prediction system serves excellent for this purpose based on its importance, especially during COVID-19 pandemic.A rise in the number of COVID-19 patients burdens hospitals and it is also a valid indicator of the necessity of taking further measures against the pandemic.

# 1.1. Hospital Bed Availability
The Hospital Bed Availability study is modeled based on the hospitals in the capital city of Turkey, Ankara dedicated to serving the COVID-19 patients in Figure 1. There exist 6 hospitals and these hospitals are intentionally selected as they serve the most of the patients in Ankara. Authorities state that depending on the daily situation and their capacity, the hospitals transfer patients to the closest hospitals. For example, if the Bilkent Sehir Hastanesi gets filled up, the closest hospitals Ankara Gazi Universitesi Hastanesi and Sehit Sait Erturk Devlet Hastanesi will start to admit more patients than average, depending on the increase of daily COVID-19 patients. Thus, keeping the accurate number of occupancy and predicting the possible increase in the number of patients becomes quite important for the healthcare professionals.


Figure 1. Selected hospitals with Covid-19 services in Ankara

As we propose to study predictive analysis on hospital bed availability, we stipulated two main required data: First is the bed capacity of each hospital, second is the daily
number of hospitalized COVID-19 patients in Turkey. However, as of being the capital city of Turkey and its location, hospitals in Ankara also admit patients from other cities due to its hospital capacity. Therefore, a third parameter for the number of COVID-19 patients from neighbor cities are added to the study. Additionally, a state vector retains the number of daily bed occupancy of each hospital i, the number of daily COVID-19 patients j, and the daily number of admitted COVID-19 patients from the neighbor cities k at a certain state. We denote the daily number of bed occupancy hi on each hospital i.

The capacity of the hospitals is given in Table 1. The capacity of the hospitals is 117, 3810, 300, 1150, 115, and 480, respectively. Considering the capacity of the Bilkent
Sehir Hastanesi, the hospital becomes the major center where it should raise an alert in case of fullness. Finally, a hospital is considered to be over capacity by having many
patients over 80% of the capacity.

  |Number| Hospital Name|Bed Capacity|Bed Capacity|
	|h0|Ankara Gazi Universitesi Hastanesi|117|
	|h1|Bilkent Sehir Hastanesi|3810|
	|h2|Diskapi Yildirim Beyazit Egitim ve Arastirma Hastanesi|300|
	|h3| Gulhane education and research hospital|1150|
	|h4| Sehit Sait Erturk Devlet Hastanesi|115|
	|h5| Yeni Sincan Devlet Hastanesi|480|
  
  Table 1. Selected hospitals with COVID-19 services in Ankara and their capacities (TTB, 2019)

#1.1.1. System Specification and Data Collection
The identified hospital bed capacity system owns several specific features and constraints (e.g., the number of daily bed occupancy of each hospital and the overall capacity of the hospitals) defining the self and creating the recognized problem. Accordingly, those sets of specifications can be beneficial to introduce the system under investigation to the hypothesis-based experiment design workflow. The followings describe the fundamental specifications for the system under study. The capacity of the variables j and k were determined based on the total number of selected hospital capacities in Ankara multiplied by 10. The multiplication coefficient 10 represents the percentage of the daily number of hospitalized COVID-19 patients in Turkey, i.e., a maximum of 10% (T.C. Saglik Bakanligi, 2021).

(1) An integer array for the number of daily bed occupancy of each hospital, number of hospitalized COVID-19 patients in Turkey and number of admitted COVID-19 patients from neighbor cities counts: [0, 1, 2, 3, 4, 5, 6, 7],

(2) An integer array for the non-capacity factors that are numbers representing the number of hospitalized COVID-19 patients in Turkey and number of admitted COVID-19 patients from neighbor cities counts: [6, 7],

(3) A map for all the hospitals with their capacity: 'h0': [60, 117], 'h1': [1905,3810], 'h2': [150, 300], 'h3': [575, 1150], 'h4': [57, 115], 'h5': [240, 480], 'j':['0', '59720'], 'k': ['0', '59720'],

(4) A formula to trace the non-fitting time traces of the hospitals calculated with the multiplication of its capacity and the capacity fullness ratio, i.e., 80% (e.g., h1 < 3048)

Unfortunately, we found the acquisition of authentic test data difficult as they are not shared per city by the Turkish authorities. This impediment motivated us toward data generation alternatives for the prevalent problem domain, i.e., hospital bed availability during COVID-19. Therefore, for the purpose of this study, a data generation algorithm that simulates a system under study from random initial states was employed to create data sets for the hospital bed availability in Ankara during COVID-19. The algorithm generates data for the daily number of the occupied beds of each hospital and the transferred number of patients from the neighboring cities. The generated data were randomized upon the COVID-19 numbers shared by the Republic of Turkey Ministry of Health (Republic of Turkey Ministry of Health, 2021), i.e., number of patients for today. We assumed that the hospitals had half of their capacity was already occupied by non-COVID-19 patients, when the pandemic has started. The algorithm essentially builds data sets from random initial conditions for a provided number of time traces. The data contains the temporal operator P(previously) and the time interval [0, 101]. Although valuable for generating lots of data, this algorithm has the disadvantage of generating relatively small non-fitting data.

The decisions about data generation made upon a requirement that the overall time traces for a single hospital avoiding the fullness should be as approximate as possible to the hospital's fullness measure, i.e., 80%. As a result, we obtained 4 different data sets, and each data set contains 101 sequential time traces for every hospital and noncapacity
variables that are number of hospitalized COVID-19 patients in Turkey and number of admitted COVID-19 patients from neighbor cities. We eventually achieved 404 time traces representing the last 14 months of COVID-19, where 62 of the time traces have hospital h1 with over 80% capacity, i.e., h1 > 3048.

