#!/usr/bin/env python3
# coding: utf-8
# File: MedicalGraph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Revisor: JJ<rivertoday@163.com>
# Using multi threads to accelerate
# Date: 18-10-3

import os
import json
from py2neo import Graph,Node
import threading
from time import ctime

class MedicalGraph:
    Drugs = []
    Foods = []
    Checks = []
    Departments = []
    Producers = []
    Symptoms = []
    Diseases = []
    disease_infos = []
    rels_check = []
    rels_recommandeat = []
    rels_noteat = []
    rels_doeat = []
    rels_department = []
    rels_commonddrug = []
    rels_drug_producer = []
    rels_recommanddrug = []
    rels_symptom = []
    rels_acompany = []
    rels_category = []

    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/medical.json')
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="asdf1234")

    '''读取文件'''
    def read_nodes(self):
        # 共７类节点
        drugs = [] # 药品
        foods = [] #　食物
        checks = [] # 检查
        departments = [] #科室
        producers = [] #药品大类
        diseases = [] #疾病
        symptoms = []#症状

        disease_infos = []#疾病信息

        # 构建节点实体关系
        rels_department = [] #　科室－科室关系
        rels_noteat = [] # 疾病－忌吃食物关系
        rels_doeat = [] # 疾病－宜吃食物关系
        rels_recommandeat = [] # 疾病－推荐吃食物关系
        rels_commonddrug = [] # 疾病－通用药品关系
        rels_recommanddrug = [] # 疾病－热门药品关系
        rels_check = [] # 疾病－检查关系
        rels_drug_producer = [] # 厂商－药物关系

        rels_symptom = [] #疾病症状关系
        rels_acompany = [] # 疾病并发关系
        rels_category = [] #　疾病与科室之间的关系

        count = 0
        for data in open(self.data_path):
            disease_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)
            disease = data_json['name']
            disease_dict['name'] = disease
            diseases.append(disease)
            disease_dict['desc'] = ''
            disease_dict['prevent'] = ''
            disease_dict['cause'] = ''
            disease_dict['easy_get'] = ''
            disease_dict['cure_department'] = ''
            disease_dict['cure_way'] = ''
            disease_dict['cure_lasttime'] = ''
            disease_dict['symptom'] = ''
            disease_dict['cured_prob'] = ''

            if 'symptom' in data_json:
                symptoms += data_json['symptom']
                for symptom in data_json['symptom']:
                    rels_symptom.append([disease, symptom])

            if 'acompany' in data_json:
                for acompany in data_json['acompany']:
                    rels_acompany.append([disease, acompany])

            if 'desc' in data_json:
                disease_dict['desc'] = data_json['desc']

            if 'prevent' in data_json:
                disease_dict['prevent'] = data_json['prevent']

            if 'cause' in data_json:
                disease_dict['cause'] = data_json['cause']

            if 'get_prob' in data_json:
                disease_dict['get_prob'] = data_json['get_prob']

            if 'easy_get' in data_json:
                disease_dict['easy_get'] = data_json['easy_get']

            if 'cure_department' in data_json:
                cure_department = data_json['cure_department']
                if len(cure_department) == 1:
                     rels_category.append([disease, cure_department[0]])
                if len(cure_department) == 2:
                    big = cure_department[0]
                    small = cure_department[1]
                    rels_department.append([small, big])
                    rels_category.append([disease, small])

                disease_dict['cure_department'] = cure_department
                departments += cure_department

            if 'cure_way' in data_json:
                disease_dict['cure_way'] = data_json['cure_way']

            if 'cure_lasttime' in data_json:
                disease_dict['cure_lasttime'] = data_json['cure_lasttime']

            if 'cured_prob' in data_json:
                disease_dict['cured_prob'] = data_json['cured_prob']

            if 'common_drug' in data_json:
                common_drug = data_json['common_drug']
                for drug in common_drug:
                    rels_commonddrug.append([disease, drug])
                drugs += common_drug

            if 'recommand_drug' in data_json:
                recommand_drug = data_json['recommand_drug']
                drugs += recommand_drug
                for drug in recommand_drug:
                    rels_recommanddrug.append([disease, drug])

            if 'not_eat' in data_json:
                not_eat = data_json['not_eat']
                for _not in not_eat:
                    rels_noteat.append([disease, _not])
                foods += not_eat

            if 'do_eat' in data_json:
                do_eat = data_json['do_eat']
                for _do in do_eat:
                    rels_doeat.append([disease, _do])
                foods += do_eat

            if 'recommand_eat' in data_json:
                recommand_eat = data_json['recommand_eat']
                for _recommand in recommand_eat:
                    rels_recommandeat.append([disease, _recommand])
                foods += recommand_eat

            if 'check' in data_json:
                check = data_json['check']
                for _check in check:
                    rels_check.append([disease, _check])
                checks += check

            if 'drug_detail' in data_json:
                drug_detail = data_json['drug_detail']
                producer = [i.split('(')[0] for i in drug_detail]
                rels_drug_producer += [[i.split('(')[0], i.split('(')[-1].replace(')', '')] for i in drug_detail]
                producers += producer
            disease_infos.append(disease_dict)
        return set(drugs), set(foods), set(checks), set(departments), set(producers), set(symptoms), set(diseases), disease_infos,\
               rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,\
               rels_symptom, rels_acompany, rels_category

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱中心疾病的节点'''
    def create_diseases_nodes(self, disease_infos):
        count = 0
        for disease_dict in disease_infos:
            node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
                        prevent=disease_dict['prevent'] ,cause=disease_dict['cause'],
                        easy_get=disease_dict['easy_get'],cure_lasttime=disease_dict['cure_lasttime'],
                        cure_department=disease_dict['cure_department']
                        ,cure_way=disease_dict['cure_way'] , cured_prob=disease_dict['cured_prob'])
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos,rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,rels_symptom, rels_acompany, rels_category = self.read_nodes()
        self.create_diseases_nodes(disease_infos)
        self.create_node('Drug', Drugs)
        print(len(Drugs))
        self.create_node('Food', Foods)
        print(len(Foods))
        self.create_node('Check', Checks)
        print(len(Checks))
        self.create_node('Department', Departments)
        print(len(Departments))
        self.create_node('Producer', Producers)
        print(len(Producers))
        self.create_node('Symptom', Symptoms)
        return


    '''创建实体关系边'''
    def create_graphrels(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,rels_symptom, rels_acompany, rels_category = self.read_nodes()
        self.create_relationship('Disease', 'Food', rels_recommandeat, 'recommand_eat', '推荐食谱')
        self.create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
        self.create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
        self.create_relationship('Department', 'Department', rels_department, 'belongs_to', '属于')
        self.create_relationship('Disease', 'Drug', rels_commonddrug, 'common_drug', '常用药品')
        self.create_relationship('Producer', 'Drug', rels_drug_producer, 'drugs_of', '生产药品')
        self.create_relationship('Disease', 'Drug', rels_recommanddrug, 'recommand_drug', '好评药品')
        self.create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
        self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')
        self.create_relationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')
        self.create_relationship('Disease', 'Department', rels_category, 'belongs_to', '所属科室')

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''
    def export_data(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category = self.read_nodes()
        f_drug = open('drug.txt', 'w+')
        f_food = open('food.txt', 'w+')
        f_check = open('check.txt', 'w+')
        f_department = open('department.txt', 'w+')
        f_producer = open('producer.txt', 'w+')
        f_symptom = open('symptoms.txt', 'w+')
        f_disease = open('disease.txt', 'w+')

        f_drug.write('\n'.join(list(Drugs)))
        f_food.write('\n'.join(list(Foods)))
        f_check.write('\n'.join(list(Checks)))
        f_department.write('\n'.join(list(Departments)))
        f_producer.write('\n'.join(list(Producers)))
        f_symptom.write('\n'.join(list(Symptoms)))
        f_disease.write('\n'.join(list(Diseases)))

        f_drug.close()
        f_food.close()
        f_check.close()
        f_department.close()
        f_producer.close()
        f_symptom.close()
        f_disease.close()

        return

##################################
# Updated by JIANG Jeremy
# in order to use multi threads
##################################
    def create_basedata(self):
        self.Drugs, self.Foods, self.Checks, self.Departments, self.Producers, self.Symptoms, self.Diseases, self.disease_infos, self.rels_check, self.rels_recommandeat, self.rels_noteat, self.rels_doeat, self.rels_department, self.rels_commonddrug, self.rels_drug_producer, self.rels_recommanddrug, self.rels_symptom, self.rels_acompany, self.rels_category = self.read_nodes()
        self.create_diseases_nodes(self.disease_infos)
        return

    def generate_Drug_Food(self):
        self.create_node('Drug', self.Drugs)
        print(len(self.Drugs))
        self.create_node('Food', self.Foods)
        print(len(self.Foods))
        return

    def generate_Check_Departments(self):
        self.create_node('Check', self.Checks)
        print(len(self.Checks))
        self.create_node('Department', self.Departments)
        print(len(self.Departments))
        return

    def generate_Producers_Symptoms(self):
        self.create_node('Producer', self.Producers)
        print(len(self.Producers))
        self.create_node('Symptom', self.Symptoms)
        print(len(self.Symptoms))
        return

    def generate_rel_Disease_Food(self):
        self.create_relationship('Disease', 'Food', self.rels_recommandeat, 'recommand_eat', '推荐食谱')
        self.create_relationship('Disease', 'Food', self.rels_noteat, 'no_eat', '忌吃')
        self.create_relationship('Disease', 'Food', self.rels_doeat, 'do_eat', '宜吃')
        return

    def generate_rel_Disease_Drug(self):
        self.create_relationship('Department', 'Department', self.rels_department, 'belongs_to', '属于')
        self.create_relationship('Disease', 'Drug', self.rels_commonddrug, 'common_drug', '常用药品')
        self.create_relationship('Producer', 'Drug', self.rels_drug_producer, 'drugs_of', '生产药品')
        self.create_relationship('Disease', 'Drug', self.rels_recommanddrug, 'recommand_drug', '好评药品')
        return

    def generate_rel_Disease_Others(self):
        self.create_relationship('Disease', 'Check', self.rels_check, 'need_check', '诊断检查')
        self.create_relationship('Disease', 'Symptom', self.rels_symptom, 'has_symptom', '症状')
        self.create_relationship('Disease', 'Disease', self.rels_acompany, 'acompany_with', '并发症')
        self.create_relationship('Disease', 'Department', self.rels_category, 'belongs_to', '所属科室')
        return

if __name__ == '__main__':
    print(">>>The palace building start at %s" % ctime())
    handler = MedicalGraph()
    handler.create_basedata()
    print(">>>Generate base data at %s" % ctime())
    node_threads = []
    t11 = threading.Thread(target=handler.generate_Drug_Food, args=())
    node_threads.append(t11)
    t12 = threading.Thread(target=handler.generate_Check_Departments, args=())
    node_threads.append(t12)
    t13 = threading.Thread(target=handler.generate_Producers_Symptoms, args=())
    node_threads.append(t13)
    for t in node_threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print(">>>Generate nodes at %s" % ctime())

    rel_threads = []
    t21 = threading.Thread(target=handler.generate_rel_Disease_Food, args=())
    rel_threads.append(t21)
    t22 = threading.Thread(target=handler.generate_rel_Disease_Drug, args=())
    rel_threads.append(t22)
    t23 = threading.Thread(target=handler.generate_rel_Disease_Others, args=())
    rel_threads.append(t23)
    for t in rel_threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print(">>>Generate relations at %s" % ctime())

    # handler.export_data()
