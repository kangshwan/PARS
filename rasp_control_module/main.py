import Gettime


Open_files = Gettime.File_control("babo.txt", "w", "r")
Open_files.openfile()
lines = Open_files.readlines_obo()

Split = Gettime.Time_split(lines)
Split.split_time()
