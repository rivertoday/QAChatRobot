# QAChatRobot

作为一个医学知识问答机器人，本项目参考了开源项目https://github.com/liuhuanyong/QASystemOnMedicalKG

在实施部分做了改进，将数据导入部分改成多线程处理，双核2.3GHz处理器+4G内存的虚拟机，数据导入到neo4j数据库只需要74分钟，远好于原作的几个小时。

------

### 部署运行说明

**假定已经安装neo4j，python3.5以上版本，以及virtualenv**

neo4j的安装需要JDK1.8.0以上环境！

下载JDK1.8

<https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html>

```
vim ~/.bashrc
```

```
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_131

export JRE_HOME=${JAVA_HOME}/jre

export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib

export PATH=${JAVA_HOME}/bin:$PATH
```

```
source ~/.bashrc
```

[neo4j(3.5.2)]: https://go.neo4j.com/download-thanks.html?edition=community&amp;release=3.5.2&amp;flavour=unix&amp;_ga=2.216143190.1335352046.1548317037-342533476.1547192045

启动neo4j

```
neo4j-path/bin/neo4j start
```



项目代码需要相关包支持，进入虚拟环境安装

```
pip3 install py2neo
```

```
pip3 install pyahocorasick
```



以上准备工作都执行完毕，开始项目代码执行：

#### 执行数据导入

```
python ./build_medicalgraph.py
```

等待数据导入完毕，注意要修改代码里面neo4j的连接用户名和密码

#### 启动问答程序

数据导入完毕后，启动问答程序

```
python ./chatbot_graph.py
```

注意要修改answer_search.py里面的neo4j的连接用户民和密码