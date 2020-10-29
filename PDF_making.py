import shutil
import os
import time
old_file = r"C:\Users\Administrator\PycharmProjects\APItest\pic\501-07185242 主单.pdf"
old_file2 = r"C:\Users\Administrator\PycharmProjects\APItest\pic\大写的pdf.PDF"
file_png = r"C:\Users\Administrator\PycharmProjects\APItest\pic\模板.png"
file_png2 = r"C:\Users\Administrator\PycharmProjects\APItest\pic\1.png"
file_jpng = r"C:\Users\Administrator\PycharmProjects\APItest\pic\其他资料.jpeg"
file_jpng2 = r"C:\Users\Administrator\PycharmProjects\APItest\pic\123.jpeg"
file_jpg = r"C:\Users\Administrator\PycharmProjects\APItest\pic\案例.jpg"
file_jpg2 = r"C:\Users\Administrator\PycharmProjects\APItest\pic\timg.jpg"
new_file = r"C:\Users\Administrator\PycharmProjects\APItest\pdf_doc"
def output_pic(lading_number):
    try:
        if  "-" in lading_number:
            new = lading_number
            shutil.copy(old_file,new_file)
            os.rename(os.path.join(new_file,"501-07185242 主单.pdf"),os.path.join(new_file,new+"舱.pdf"))
            shutil.copy(old_file, new_file)
            os.rename(os.path.join(new_file, "501-07185242 主单.pdf"), os.path.join(new_file, new + "主.pdf"))
            shutil.copy(file_png, new_file)
            os.rename(os.path.join(new_file, "模板.png"), os.path.join(new_file, new + "分.png"))
            shutil.copy(file_jpng, new_file)
            os.rename(os.path.join(new_file, "其他资料.jpeg"), os.path.join(new_file, new+".jpeg"))
            shutil.copy(file_jpg, new_file)
            os.rename(os.path.join(new_file, "案例.jpg"), os.path.join(new_file, new+"其他.jpg"))
            shutil.copy(old_file, new_file)
            os.rename(os.path.join(new_file, "501-07185242 主单.pdf"), os.path.join(new_file, new + "+不知名.txt"))
        else:
            print("提单号输入不正确")
    except Exception as e:
        print(e)
def output_pic2(lading_number):
    try:
        if  "-" in lading_number:
            new = lading_number
            shutil.copy(old_file2,new_file)
            os.rename(os.path.join(new_file,"大写的pdf.PDF"),os.path.join(new_file,new+"舱.pdf"))
            shutil.copy(old_file2, new_file)
            os.rename(os.path.join(new_file,"大写的pdf.PDF"), os.path.join(new_file, new + "主.pdf"))
            shutil.copy(file_png2, new_file)
            os.rename(os.path.join(new_file,"1.png"), os.path.join(new_file, new + "分.png"))
            shutil.copy(file_jpng2, new_file)
            os.rename(os.path.join(new_file,"123.jpeg"), os.path.join(new_file, new+".jpeg"))
            shutil.copy(file_jpg2, new_file)
            os.rename(os.path.join(new_file,"timg.jpg"), os.path.join(new_file, new+"其他.jpg"))
            shutil.copy(old_file2, new_file)
            os.rename(os.path.join(new_file,"大写的pdf.PDF"), os.path.join(new_file, new + "+不知名.txt"))
        else:
            print("提单号输入不正确")
    except Exception as e:
        print(e)
if  __name__=="__main__":
    lading_numeber = "172-12344321"
    output_pic(lading_numeber)