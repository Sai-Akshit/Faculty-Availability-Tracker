# algorithm for data extraction
import pandas as pd
import numpy as np
from .models import faculty_details, courseChampions, faculty_details_even, courseChampions_even


# default path where files are stored: media/{file_name}
def dataExtraction(filePath: str, sem: str) -> None:
    '''This function requires one argument.
    filePath: a string file path of the excel file to be read
    This function does not return any value
    It reads the Master data sheet from the given excel file and extracts faculty name, id and timetable data from it'''
    # deleting data in db_table
    if sem == 'odd':
        faculty_details.objects.all().delete()
    else:
        faculty_details_even.objects.all().delete()

    df = pd.read_excel(filePath, sheet_name = 'Master data', skiprows=1) #Reading the 'Master data' sheet and skipping first row.
    df.drop('Unnamed: 0', axis=1, inplace = True) #dropping first column ()
    df.fillna(value= '0', axis= 1, inplace = True) #filling the null values with a default '0' string
    df['Unnamed: 2'] = df['Unnamed: 2'].astype(int) #chaging datatype of id column from object (string) to int32 type
    shape: tuple = df.shape  #shape (number of rows, number of columns)
    for i in range(shape[0]):
        facName: str = df.iloc[i][0] # faculty name
        id_: int = df.iloc[i][1] #faculty ID
        tt: list = [] #faculty timetable
        for j in range(2, shape[1], 9):
            day_tt = list(df.iloc[i][j:j+9])  #Accessing day wise timetable
            tt.append(day_tt)  #Adding day wise timetable to main timetable(tt) list
        
        if sem == 'odd':
            det = faculty_details(name= facName, idno= id_, timetable= tt) #creating faculty_details object
            det.save() #saving the object and pushing it to DB
        else:
            det = faculty_details_even(name= facName, idno= id_, timetable= tt)
            det.save()

def defineTime(post_request):
    """Genrates time indices and appends to a list"""
    indices = []
    for key in post_request:
        if post_request[key] == 'clicked':
            temp = key.replace('c', '')
            try:
                indices.append(int(temp))
            except ValueError:
                indices.append(temp)
    
    return indices


def timeIndex(timeList):
    """Subtracts 8 from every value at the index"""
    res = []
    for time in timeList:
        timeInd = time - 8
        res.append(timeInd)

    return res

def funFree(timeindex, dayList):
    res = None
    for i in timeindex:
        if dayList[i] == '0':
            res = True
        else:
            res = False
            break
    return res

def searchingFree(query_set, dayIndex, timeIndexList):
    eligibleEmps = []
    count = 1
    for emp in query_set:
        if funFree(timeIndexList, emp.timetable[dayIndex]):
            eligibleEmps.append([count, emp.name, emp.idno])
            count += 1

    return eligibleEmps

def funBusy(timeindex, daylist):
    res = None
    for i in timeindex:
        if daylist[i] != '0':
            res = True
        else:
            res = False
            break
    
    return res


def searchingBusy(query_set, dayIndex, timeIndexList):
    eligibleEmps = []
    count = 1
    for emp in query_set:
        if funBusy(timeIndexList, emp.timetable[dayIndex]):
            eligibleEmps.append([count, emp.name, emp.idno])
            count += 1

    return eligibleEmps


def download(empList: list):  # empList format: [[count, emp_id, emp_name], ...]
    emp_dict = {'emp_names':[], 'emp_ids':[]}
    for emp in empList:
        emp_dict['emp_names'].append(emp[1])
        emp_dict['emp_ids'].append(emp[2])
    emp_df = pd.DataFrame(emp_dict)
    emp_df.to_csv('media/download/data.csv', header=['Employee Name', 'Employee ID'])

def course_and_champions_input(path, sem) -> None:
    df_courseChampions = pd.read_excel(path, sheet_name = "Course Champions")
    
    #changing index as per requirements
    df_courseChampions.set_index('Course Code', inplace = True)
    
    # deleting pre-existing data from table
    if sem == 'odd':
        courseChampions.objects.all().delete()
    else:
        courseChampions_even.objects.all().delete()

    #Adding course champion
    for i in df_courseChampions.iterrows():
        if i[1][1]!=np.nan:
            subCode: str = i[0]
            sub: str = i[1][0]
            champion: str = i[1][1]
            year: int = i[1][2]
            if sem == 'odd':
                champ = courseChampions(subCode, sub, champion, year)
                champ.save()
            else:
                champ = courseChampions_even(subCode, sub, champion, year)
                champ.save()