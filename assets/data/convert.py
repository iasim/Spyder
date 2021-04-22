import pandas as pd

df = pd.DataFrame(pd.read_csv(r'C:\Users\Radha\OneDrive - Drexel University\College\INFO\Senior Design\CI 491 Senior Project I\Website Search\assets\data\Courses_List.csv', sep = ",", header=0, names = ["GraphDB1", "GraphDB2","Course_ID","Course_Name","Course_Full","Course_Description"], index_col = False))

df.to_json(r'C:\Users\Radha\OneDrive - Drexel University\College\INFO\Senior Design\CI 491 Senior Project I\Website Search\assets\data\courses.json', orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)

#df = pd.read_csv (r'C:\Users\Radha\OneDrive - Drexel University\College\INFO\Senior Design\CI 491 Senior Project I\Website Search\assets\data\Work_Roles_List.csv')
#df.to_json (r'C:\Users\Radha\OneDrive - Drexel University\College\INFO\Senior Design\CI 491 Senior Project I\Website Search\assets\data\careers.json')

#df = pd.read_json(r'C:\Users\Radha\OneDrive - Drexel University\College\INFO\Senior Design\CI 491 Senior Project I\Website Search\assets\data\careers.json')

print(df.to_string())
