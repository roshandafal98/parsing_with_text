import re
import pandas as pd
rx_dict = {
    'school': re.compile(r'School = (?P<school>.*)\n'),
    'grade': re.compile(r'Grade = (?P<grade>\d+)\n'),
    'name_score': re.compile(r'(?P<name_score>Name|Score)'),
}

def _parse_line(line):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None

    
def parse_file(filepath):
    data = []  # create an empty list to collect the data
    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line:
            # at each line check for a match with a regex
            key, match = _parse_line(line)
            # extract school name
            if key == 'school':
                school = match.group('school')
            # extract grade
            if key == 'grade':
                grade = match.group('grade')
                grade = int(grade)
            # identify a table header
            if key == 'name_score':
                # extract type of table, i.e., Name or Score
                value_type = match.group('name_score')
                line = file_object.readline()
                # read each line of the table until a blank line
                while line.strip():
                    # extract number and value
                    number, value = line.strip().split(',')
                    value = value.strip()
                    # create a dictionary containing this row of data
                    row = {
                        'School': school,
                        'Grade': grade,
                        'Student number': number,
                        value_type: value
                    }
                    # append the dictionary to the data list
                    data.append(row)
                    line = file_object.readline()
            line = file_object.readline()
        # create a pandas DataFrame from the list of dicts
        data = pd.DataFrame(data)
        # set the School, Grade, and Student number as the index
        data.set_index(['School', 'Grade', 'Student number'], inplace=True)
        # consolidate df to remove nans
        data = data.groupby(level=data.index.names).first()
        # upgrade Score from float to integer
        data = data.apply(pd.to_numeric, errors='ignore')
    return data
if __name__ == '__main__':
    filepath = r"C:/Users/Roshan Dafal/Desktop/Python/parse.txt"
    dat = parse_file(filepath)
    print(dat)
