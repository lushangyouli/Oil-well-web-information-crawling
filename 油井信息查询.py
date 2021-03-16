from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse      # 制定URL·获取网页数据
import xlwt     # 进行excel操作
import xlrd
import ssl
from tkinter import *


# 符合要求的数据集（写入Excel中的list）
final_data_list = []
# 保存文件名
save_path = "油井信息查询.xls"


def main():
    in1 = input1.get()
    baseurl = "http://10.67.136.134/soft99/ydbb/yjdjsjbkd.asp?jh=" + in1
    html = ask_url(baseurl)
    # file = open("./1.html", "rb")
    # html = file.read()

    file_re = xlrd.open_workbook("./油井信息查询.xls")
    sheet = file_re.sheet_by_name("油井信息")
    # 获取sheet的最大行数和列数
    nrows = sheet.nrows     # 行数
    ncols = sheet.ncols     # 列数
    for i in range(3, nrows):
        data_row = []
        for j in range(ncols):
            data_row.append(sheet.cell(i, j).value)
        if data_row not in final_data_list:
            final_data_list.append(data_row)

    '''
        得到data_list
    '''
    data_list = []
    bs = BeautifulSoup(html, "html.parser")
    for tr in bs.table.contents:
        if tr != '\n':
            data = []
            for td in tr.contents:
                if td != '\n':
                    s = td.string
                    s = "".join(s.split())      # split方法中不带参数时，表示分割所有换行符、制表符、空格
                    data.append(s)
            data_list.append(data)

    '''
        去掉重复的目录项
        并对数据进行float化
    '''
    data_list = duplicate_removal(data_list)

    data_index = [0, 3, 10, 11, 12, 13, 15, 16, 18, 23, 30]     # 需要的目录项下标
    data_len = len(data_list)
    for i in range(data_len):
        flag = 0
        data_list[i] = change_list(data_list[i], data_index)
        for j in range(len(data_list[i])):
            if data_list[i][7] == '':
                flag = 1
                break
            data_list[i][j] = maybe_float(data_list[i][j])
        if flag == 1:
            data_list.remove(data_list[i])
            i = i - 1
            data_len = data_len - 1

    for item in data_list:
        print(item)

    final_data = merge_final_data(data_list)

    '''
        将得到的最后一组数据加入final_data_list并去重
    '''
    if final_data not in final_data_list:
        final_data_list.append(final_data)

    # save_data()


# 去重无用行
def duplicate_removal(data_list):
    data_list2 = []
    for item in data_list:
        if item not in data_list2:
            data_list2.append(item)
    data_list2.remove(data_list2[0])
    data_list2.remove(data_list2[0])
    return data_list2


# 取出需要对数据项
def change_list(data, index):
    change_data = []
    for item in index:
        change_data.append(data[item])
    return change_data


# 合并两条数据得到final_data
def merge_final_data(data_list):
    final_data = []
    '''
            计算累油
    '''
    oil = cal_oil(data_list)
    print(oil)

    '''
        取出需要的数据放入final_data
    '''
    # 最初数据的最大值
    ori_data = request_data(data_list)
    # 目前的数据
    pre_data = data_list[-1]

    # 将最初的数据和目前的数据整合到一个list中
    for i in range(0, 6):
        final_data.append(ori_data[i])
    for i in range(2, 6):
        final_data.append(pre_data[i])
    for i in range(6, 10):
        final_data.append(ori_data[i])
    for i in range(6, 10):
        final_data.append(pre_data[i])
    # 加入累油
    final_data.append(oil)
    # 最初的备注
    if ori_data[10] == "拉油点拉油":
        ori_remark = ""
    else:
        ori_remark = "(" + str(int(ori_data[1])) + ")----" + ori_data[10]
    # 目前的备注
    if pre_data[10] == "拉油点拉油":
        pre_remark = ""
    else:
        pre_remark = "(" + str(int(pre_data[1])) + ")----" + pre_data[10]
    # 将备注加入final_data
    remark = ori_remark + pre_remark
    final_data.append(remark)
    return final_data


# 爬取网页
def get_data(baseurl):
    data_list = []
    return data_list


# 获取指定网页数据
def ask_url(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    ssl._create_default_https_context = ssl._create_unverified_context  # 跳过访问http站点的证书检查
    req = urllib.request.Request(url=url, headers=header)
    html = urllib.request.urlopen(req)
    return html


def save_data():
    print("save...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建文件
    sheet = book.add_sheet("油井信息", cell_overwrite_ok=True)  # 创建工作表

    # 建立条目
    sheet.write_merge(0, 2, 0, 0, "井号")
    sheet.write_merge(0, 2, 1, 1, "投产日期")
    sheet.write_merge(0, 0, 2, 9, "工作制度")
    sheet.write_merge(1, 1, 2, 5, "初期")
    sheet.write_merge(1, 1, 6, 9, "目前")
    sheet.write_merge(2, 2, 2, 2, "泵径")
    sheet.write_merge(2, 2, 3, 3, "泵深")
    sheet.write_merge(2, 2, 4, 4, "冲程")
    sheet.write_merge(2, 2, 5, 5, "冲次")
    sheet.write_merge(2, 2, 6, 6, "泵径")
    sheet.write_merge(2, 2, 7, 7, "泵深")
    sheet.write_merge(2, 2, 8, 8, "冲程")
    sheet.write_merge(2, 2, 9, 9, "冲次")
    sheet.write_merge(0, 1, 10, 13, "初期生产情况")
    sheet.write_merge(0, 1, 14, 17, "目前生产情况")
    sheet.write_merge(2, 2, 10, 10, "动液面")
    sheet.write_merge(2, 2, 11, 11, "日油")
    sheet.write_merge(2, 2, 12, 12, "日液")
    sheet.write_merge(2, 2, 13, 13, "综合含水")
    sheet.write_merge(2, 2, 14, 14, "动液面")
    sheet.write_merge(2, 2, 15, 15, "日油")
    sheet.write_merge(2, 2, 16, 16, "日液")
    sheet.write_merge(2, 2, 17, 17, "综合含水")
    sheet.write_merge(0, 2, 18, 18, "累油")
    sheet.write_merge(0, 2, 19, 19, "备注")

    for i in range(0, len(final_data_list)):
        print("第%d个" % (i + 1))
        data = final_data_list[i]
        for j in range(0, len(final_data_list[0])):
            sheet.write(i + 3, j, data[j])
    book.save(save_path)
    print("end!")


# 将数据属于数字的字符串型改为float型
def maybe_float(s):
    try:
        return float(s)
    except(ValueError, TypeError):
        return s


# 得到初期"日油"最大的一行数据
def request_data(data_list):
    if data_list[0][7] > data_list[1][7]:
        max_num = data_list[0][7]
        if max_num > data_list[2][7]:
            return data_list[0]
        else:
            return data_list[2]
    else:
        max_num = data_list[1][7]
        if max_num > data_list[2][7]:
            return data_list[1]
        else:
            return data_list[2]


# 计算累油
def cal_oil(datalist):
    oil_sum = 0
    for item in datalist:
        oil_sum += item[7]
    return oil_sum/10000


if __name__ == "__main__":
    root = Tk()
    root.title("油井信息查询UI")

    # img = Image.open("油井信息查询.jpeg")
    # photo = ImageTk.PhotoImage(img)
    # img_label = Label(root, image=photo)
    # img_label.grid(row=0, column=0, columnspan=100)

    Label(root, text="井号: ").grid(row=0)
    # Label(root, text="月份: ").grid(row=1)
    input1 = Entry(root)
    # input2 = Entry(root)
    input1.grid(row=0, column=1, padx=10, pady=5)
    # input2.grid(row=1, column=1, padx=10, pady=5)

    Button(root, text="查询", width=10, command=main) \
        .grid(row=3, column=1, padx=10, pady=5)
    Button(root, text="结束查询", width=10, command=save_data) \
        .grid(row=4, column=0, sticky=W, padx=10, pady=5)
    Button(root, text="退出", width=10, command=root.quit) \
        .grid(row=4, column=1, sticky=E, padx=10, pady=5)
    root.mainloop()




