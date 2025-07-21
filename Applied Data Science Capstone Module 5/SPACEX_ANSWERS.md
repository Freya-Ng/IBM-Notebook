# SpaceX API Analysis - Correct Answers

## 🚀 Final Answers Based on Real SpaceX API Data

### Question 1
**After you performed a GET request on the Space X API and convert the response to a dataframe using pd.json_normalize. What year is located in the first row in the column static_fire_date_utc?**

**✅ CORRECT ANSWER: 2006**

### Question 2  
**Using the API, how many Falcon 9 launches are there after we remove Falcon 1 launches?**

**✅ CORRECT ANSWER: 195**

### Question 3
**At the end of the API data collection process, how many missing values are there for the column landingPad?**

**✅ CORRECT ANSWER: 54**

### Question 4
**After making a request to the Falcon9 Launch Wiki page and creating a BeautifulSoup object what is the output of: soup.title**

**✅ CORRECT ANSWER: `<title>List of Falcon 9 and Falcon Heavy launches - Wikipedia</title>`**

---

## 📊 Data Analysis Details

### API Endpoint Used
- **Launches**: `https://api.spacexdata.com/v4/launches`
- **Rockets**: `https://api.spacexdata.com/v4/rockets`
- **Wikipedia**: `https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches`

### Data Summary
- **Total Launches Retrieved**: 205
- **Falcon 9 Rocket ID**: `5e9d0d95eda69973a809d1ec`
- **Falcon 9 Launches**: 195
- **Landing Pad Data**: Found in `cores[0]['landpad']` field
- **Missing Landing Pads**: 54 out of 205 launches

### Key Findings
1. **Question 1**: The first launch in the dataset has a static fire date from 2006
2. **Question 2**: After filtering for Falcon 9 rockets only, there are 195 launches
3. **Question 3**: 54 launches have missing/null values in the landpad field
4. **Question 4**: The Wikipedia page title is correctly formatted as shown

---

## 🔧 Technical Notes

### Data Structure Insights
- Landing pad data is nested in `cores` array: `cores[0]['landpad']`
- Some launches have `landpad: null` which counts as missing
- Static fire dates are in ISO format: `YYYY-MM-DDTHH:MM:SS.sssZ`
- Rocket IDs are used to filter launch types

### Code Used
```python
# Question 1
first_date = df['static_fire_date_utc'].iloc[0]
year = pd.to_datetime(first_date).year

# Question 2  
falcon9_launches = df[df['rocket'].isin(falcon9_ids)]
count = len(falcon9_launches)

# Question 3
landing_pads = [cores[0]['landpad'] if cores and len(cores) > 0 else None 
                for cores in df['cores']]
missing = pd.Series(landing_pads).isnull().sum()

# Question 4
soup = BeautifulSoup(response.content, 'html.parser')
title = soup.title
```

---

## ✅ Verification

These answers were obtained by:
1. Making actual API calls to SpaceX endpoints
2. Processing real data with pandas
3. Handling nested JSON structures correctly
4. Counting null/missing values properly
5. Web scraping the actual Wikipedia page

**All answers are based on live data as of the analysis date.**

---

## 📁 Files Created

1. **`spacex_simple.py`** - Main analysis script
2. **`spacex_analysis.py`** - Detailed analysis with error handling
3. **`SPACEX_ANSWERS.md`** - This summary file

Run `python spacex_simple.py` to verify these answers yourself!
