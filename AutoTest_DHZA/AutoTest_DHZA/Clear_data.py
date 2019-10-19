from Common import Read_config
from Common import DB

cf=Read_config.ReadConfig()
db_en=DB.DB_enterprise()
db_user=DB.DB_user()

"""
获取变量
"""
notphone=cf.get_userdatainfo('not_exist_phone')
projectid = cf.get_project("projectid")
corporation_master_id = cf.get_userdatainfo("corporation_master_id")
enterpriseid = cf.get_enterpriseinfo("enterpriseid")
buildenterpriseid = cf.get_enterpriseinfo("buildenterpriseid")
checkenterpriseid = cf.get_enterpriseinfo("checkenterpriseid")

"""
被执行的sql（管理员用户）
"""
del_Adminuser_sql=""" DELETE FROM tb_user WHERE phone = %s """
"""
被执行的sql（企业部门）
"""
del_company_sql = """ DELETE FROM `company` WHERE corporation_master_id = %s  """
#包含默认创建及测试添加
del_employee_sql = """ DELETE FROM `employee` WHERE company_id = %s """
del_department_sql = """ DELETE FROM `department` WHERE company_id = %s """

"""
被执行的sql（工程项目）
"""
del_project_sql=""" DELETE FROM project WHERE id = %s """
del_project_company_sql=""" DELETE FROM project_company WHERE project_id = %s """
del_invatation_sql=""" DELETE FROM invatation WHERE project_id = %s """
del_model_resource_sql=""" DELETE FROM model_resource WHERE project_id = %s """
del_work_surface_sql=""" DELETE FROM work_surface WHERE project_id = %s """
del_construction_sql=""" DELETE FROM construction WHERE project_id = %s """

def delete_Adminuser_correlation(phone):
    try:
        db_user.clear_data(del_Adminuser_sql,phone)
        print("Admin用户数据清除完成")
    except Exception as e:
        print("发生错误{}".format(e))

def delete_enterprise_correlation(master_id,enterpriseid,buildenterpriseid,checkenterpriseid):
    try:
        db_en.clear_data(del_company_sql,master_id)
        db_en.clear_data(del_employee_sql,enterpriseid)
        db_en.clear_data(del_employee_sql,buildenterpriseid)
        db_en.clear_data(del_employee_sql,checkenterpriseid)
        db_en.clear_data(del_department_sql,enterpriseid)
        db_en.clear_data(del_department_sql,buildenterpriseid)
        db_en.clear_data(del_department_sql,checkenterpriseid)
        print("企业数据清除完成")
    except Exception as e:
        print("发生错误{}".format(e))

def delete_projectid_correlation(id):
    try:
        db_en.clear_data(del_project_sql,id)
        db_en.clear_data(del_project_company_sql,id)
        db_en.clear_data(del_invatation_sql,id)
        db_en.clear_data(del_model_resource_sql,id)
        db_en.clear_data(del_work_surface_sql,id)
        db_en.clear_data(del_construction_sql,id)
        print("工程项目相关数据清除完成")
    except Exception as e:
        print("发生错误{}".format(e))

delete_projectid_correlation(projectid)
delete_enterprise_correlation(corporation_master_id,enterpriseid,buildenterpriseid,checkenterpriseid)
# delete_Adminuser_correlation(notphone)