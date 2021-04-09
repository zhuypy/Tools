import os
import xlrd
import xlwt
from xml.dom.minidom import parse
import xml.dom.minidom

def getXmlDict():
    dirPath = r'D:\test\xml'
    file_list = os.listdir(dirPath)
    xmlDict = {}
    for file_name in file_list:
        xmlDict[file_name.split('_')[0]+'_'+file_name.split('_')[1]] = os.path.join(dirPath,file_name)
    # print(xmlDixt)
    return xmlDict
def getTextMap():
    '''
    获取文本映射表
    :return:
    '''
    mapFilePath = r'D:\test\type\map.xls'
    text_map = {}
    text_map_sheet = xlrd.open_workbook(mapFilePath).sheet_by_name('map')
    for row in range(text_map_sheet.nrows):
        text_map[text_map_sheet.row_values(row)[0]]=text_map_sheet.row_values(row)[1]
    # print(text_map)
    return text_map

def getTaskTypeDict():
    '''
    从Excel表格中获取文件名对应的任务类型和协助类型的映射表
    :return:
    '''
    taskTypeFilePath = r'D:\test\type\task_type.xls'
    
    task_type_dict = {}
    task_type_sheet = xlrd.open_workbook(taskTypeFilePath).sheet_by_name('task_type')
    for row in range(task_type_sheet.nrows):
        # print(task_type_sheet.row_values(row))
        task_type_dict[task_type_sheet.row_values(row)[0]]=task_type_sheet.row_values(row)[1]
    # print(task_type_dict)

    assist_type_dict = {}
    assist_type_sheet = xlrd.open_workbook(taskTypeFilePath).sheet_by_name('assist_type')
    for row in range(assist_type_sheet.nrows):
        # print(assist_type_sheet.row_values(row))
        assist_type_dict[assist_type_sheet.row_values(row)[0]]=assist_type_sheet.row_values(row)[1]
    # print(assist_type_dict)
    
    return task_type_dict,assist_type_dict

def analysisXmlDict(xmlDict,task_type_dict,assist_type_dict):
    result_xmldict = {}
    for key in xmlDict.keys():
        # print(task_type_dict.get(key.split('_')[0]) + '_' + assist_type_dict.get(key.split('_')[1]))
        result_key = task_type_dict.get(key.split('_')[0])+'_'+assist_type_dict.get(key.split('_')[1])
        result_value = analysisXml(xmlDict.get(key))
        result_xmldict[result_key] = result_value
    # print(result_xmldict)
    return result_xmldict

def analysisXml(xmlFile):
    DOMTree = xml.dom.minidom.parse(xmlFile)
    collection = DOMTree.documentElement

    process = '申请人发起_'
    userTask_list = collection.getElementsByTagName("userTask")
    for userTask in userTask_list:
        if 'execute1' in userTask.getAttribute('activiti:candidateUsers'):
            # print('协助人'+ userTask.getAttribute('name'))
            process +='协助人'+ userTask.getAttribute('name')+'_'
        elif 'execute2' in userTask.getAttribute('activiti:candidateUsers'):
            # print('发起人'+userTask.getAttribute('name'))
            process += '发起人' + userTask.getAttribute('name')+'_'
        else:
            # print(userTask.getAttribute('name'))
            process +=userTask.getAttribute('name')+'_'
            
    # print(process[:-1])
    return process[:-1]

def writeDown(result_xmldict,text_map):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('湖北')
    
    row = 0
    for key in result_xmldict.keys():
        worksheet.write(row, 0, label=key if (text_map.get(key) == None) else text_map.get(key))
        point_list = result_xmldict.get(key).split('_')
        clo = 1
        for point in point_list:
            worksheet.write(row, clo, label=point if (text_map.get(point) == None) else text_map.get(point))
            clo += 1
        row += 1
    
    workbook.save(r'D:\test\test1.xls')

def editDict(result_xmldict):
    result_xmldict['电子数据调查_本地自办'] = '手动填入'
    result_xmldict['电子数据调查_本地协助'] = '手动填入'
    result_xmldict['电子数据调查_省内异地协助'] = '手动填入'
    result_xmldict['信息查询_省内异地协助'] = '手动填入'
    
    return result_xmldict
    

if __name__ == '__main__':
    
    task_type_dict,assist_type_dict = getTaskTypeDict()
    text_map= getTextMap()
    xmlDict = getXmlDict()
    result_xmldict = editDict(analysisXmlDict(xmlDict,task_type_dict,assist_type_dict))
    writeDown(result_xmldict,text_map)
    
    # analysisXml(r'D:\test\xml\93_3_1617174858382.bpmn20.xml')

    

    






