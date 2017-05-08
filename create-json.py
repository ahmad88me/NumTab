def create(class_wd, wd_p, db_p, values, propValue, wd_values_file, log_file):
        print 'class: ' + class_wd
        print 'prop wd: ' + wd_p
        print 'prop dbp: ' + db_p
        print 'propValue: ' + propValue
        #log_file.write('class: ' + class_wd.encode('utf-8') + ' prop wd: ' + wd_p.encode('utf-8') + ' prop dbp: ' + db_p.encode('utf-8') + ' numer values: ' + ','.join(str(e).encode('utf-8') for e in $
        try:
                wd_values_file.write(db_p + '\n' + str(len(values)) + '\n' + '\n'.join(str(e).encode('utf-8') for e in values) + '\n')
        except Exception as e:
                print e

