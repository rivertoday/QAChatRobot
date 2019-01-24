import os



APPDIR = "QASystemOnMedicalKG-master"
cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
data_path = os.path.join(cur_dir, APPDIR+'/data/medical.json')
print(">>>filepath:%s"%data_path)

count = 0
for data in open(data_path):
    count += 1
print(">>>The item number: %d"%count)
