import re

def prune_data(num):
    in_file = '../Dataset/AOL-user-ct-collection/user-ct-test-collection-'+num+'.txt'
    out_file = '../Dataset/AOL-user-ct-collection/pruned_user-ct-test-collection-'+num+'.txt'

    out_f = open(out_file,'w')
    in_f = open(in_file,'r')

    # In regex, \d stands for digit
    time_pattern = r'\d{2}:\d{2}:\d{2}'
    url_pattern = r'[a-zA-Z]\.[a-z]'

    # The first line contains the headings; skip it
    in_f.readline()
    for line in in_f:
        till_time = line[:re.search(time_pattern,line).end()]
        if till_time.split('\t')[1] == '-':
            continue
        if not re.search(url_pattern,till_time):
            out_f.write(till_time+'\n')

def main():
    for i in range(1,10):
        prune_data('0'+str(i))
        print str(i),'done'
    prune_data('10')

if __name__ == '__main__':
    main()
