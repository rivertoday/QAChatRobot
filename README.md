# QAChatRobot

作为一个医学知识问答机器人，本项目参考了开源项目https://github.com/liuhuanyong/QASystemOnMedicalKG

在实施部分做了改进，将数据导入部分改成多线程处理，双核2.3GHz处理器+4G内存的虚拟机，数据导入到neo4j数据库只需要74分钟，远高于原作的十几个小时。