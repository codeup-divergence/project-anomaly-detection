# Anomoly-Detection-Project
### Corey Hermesch and Scott Barnett
### 15 June 2023
## Project description with goals
### Description
* We are tasked with answering the questions provided by our boss. Providing a professional email, final notebook, readme file, and google slide to him te address a minimun of 5 of his questions.

### Goals¶
* Construct an email answering at least 5 of 8 questions 
* Deliver a final report to the data science team 
* Deliver a slide with key points

## Initial hypotheses and/or questions you have of the data, ideas

* 1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
* 2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
* 3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
* 4. Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping iss happening? Are there any suspicious IP addresses?
* 5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?
* 6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
* 7. Which lessons are least accessed?
* 8. Anything else I should be aware of?

*****************************************
## Project Plan 
* Data acquired from the Codeup Database and the provided anonymized-curriculum-access.txt document 
    * Files were concated on id and cohort_id respectively
* It contained **900,223 rows and 8 columns**
* The data was aquired on **14 JUNE 2023**
* Each row represents a time the Codeup lesson server was accessed
* Each column represents a feature of the access event
* Prepare data
    * The only column with null values from the .txt file was cohort_id which we filled with 0
    * After adding the sql pull to get the cohort's name, start_date, end-date, and program_id; nulls were created in those columns when cohort_id was We filled those nulls with with "Unknown cohort", 2000-01-01, 2000-01-01, and 0 respectively.
    * The date column was changed to a datetime, set as the index, and the index was sorted (earliest to latest)
    * No columns were removed or renamed
    * No additional features were added
    * No encoding, scaling was accomplished
    * Data was not split into train/validate/test for this analysis
    * Outliers were not adressed as they were part of the target
   
## Explore data in search of answers
* Answer the following initial questions
    * 1. Which lesson appears to attract the most traffic consistently across cohorts (per program)? 
    * 2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
    * 3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
    * 4. Not addressed
    * 5.Not addressed
    * 6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
    * 7.Which lessons are least accessed?

### Draw conclusions
* 1. The lessons with the most traffic consistently across cohorts (per program) are:
    * WebDev (Pro.1): javascript-i 
    * WebDev (Pro.2): javascript-i 
    * Data Science (Pro.3): classification/overview is the most accessed lesson
    * Apollo cohort (Pro.4):  content/html-css 
    * Unkown Grouo (Pro.0): javascript-i 
* 2. The only program where a cohort that referred to a lesson significantly more than other cohorts was the Data Science program
    * The advanced-dataframes lesson was accessed a lot by Bayes, but very little by Curie and Darden
    * The Timeseries explore lesson was accessed a lot by Bayes and Curie, but very little by Darden
* 3. There are 10 users in the dataset who, while active, accessed the curriculum <= 10 times
        * All users were in program 2
        * They were in 9 separate cohorts (2 users in the same cohort)
    * Seven of the ten users accessed the curriculum on the first or second day of class only, indicating students who may have dropped out
    * 3 of the 10 accessed the curriculum much later in the program
        * User 278, 812, 832 from Voyageurs, Hyperion, and Jupiter cohorts respectively
        * No good explanation for this: could be an error in capturing the data or some sort of unauthorized access
* 6. The most referenced topics after graduation are:
    * Web Development - Java and Javascript
    * Data Science - SQL and classification
* 7. Lesson accessed the least is collection of 457 lesson pages that were only accessed once.
## Data Dictionary
| Feature | Datatype | Key | Definition |
|---|---|---|---|
| Date | datetime64 | YYYY-MM-DD | Date of activity; Index |
| endpoint | object | unique | The highest value reached that day |
| user_id | int64 | unique # | Unique ID # assigned to user |
| cohort_id | int64 | unique # | Unique ID # assigned to cohort |
| source_ip | object | IP ##.###.##.## | Unique IP address assigned to location of user |
| name | object | unique | Name assigned to cohort |
| start_date | datetime64 | YYYY-MM-DD | Date cohort started |
| end_date | datetime64 | YYYY-MM-DD | Date cohort graduated |
| program_id | int64 | 1,2,3,4 | Designation given to type of program |

## Steps to Reproduce
* 1. Data acquired from the Codeup Database and the provided anonymized-curriculum-access.txt document 
    * Files were concated on id and cohort_id respectively
    * Ensure you have your .env with credentials in the same folder
    * Ensure you have your anonymized-curriculum-access.txt document in the same folder
* 2. Clone this repo.
* 3. Put the anonymized-curriculum-access.txt file and your .env containing credentials into project folder containing the cloned repo.
* 4. Run notebook.

## Takeaways and Conclusions
1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
    * The lessons withe most traffic consistently across cohorts (per program) are:
        * WebDev Programs 1, 2 and unassigned:  javascript-i 
        * Data Science Program 3: classification overview 

2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
    * The only program where a cohort that referred to a lesson significantly more than other cohorts was the Data Science program
        * The advanced-dataframes lesson was accessed a lot by Bayes, but very little by Curie and Darden
        * The Timeseries explore lesson was accessed a lot by Bayes and Curie, but very little by Darden

3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
    * There are 10 users in the dataset who, while active, accessed the curriculum <= 10 times
        * All users were in program 2
        * They were in 9 separate cohorts (2 users in the same cohort)
    * Seven of the ten users accessed the curriculum on the first or second day of class only, indicating students who may have dropped out
    * 3 of the 10 accessed the curriculum much later in the program
        * User 278, 812, 832 from Voyageurs, Hyperion, and Jupiter cohorts respectively
        * No good explanation for this: could be an error in capturing the data or some sort of unauthorized access

6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
	* The most referenced topics after graduation are: 
		* Web Development - Java and Javascript
	    * Data Science - SQL and classification

7. Which lessons are least accessed?
    * Lesson accessed the least is collection of 457 lesson pages that were only accessed once


# Recomendations
* Provide additional takaways or downloadable docs for extensivly used topics
* Investigate the need to redo or reorganize the information on the 457 seldom used pages

# Next Steps
* * If provided more time we could have looked further into the additional two questions, and connected unknown users to cohorts