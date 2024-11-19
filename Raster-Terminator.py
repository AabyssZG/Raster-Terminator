from PIL import Image
import numpy as np
import argparse, io, sys, os

def title():
    logo0='''
 +------------------------------+--------------------------------------------------+
 + Title: Raster Terminator     +..%%%%%....%%%%....%%%%...%%%%%%..%%%%%%..%%%%%...+
 + Introduction: 光栅图秒杀器   +..%%..%%..%%..%%..%%........%%....%%......%%..%%..+
 + Author: 曾哥(@AabyssZG)      +..%%%%%...%%%%%%...%%%%.....%%....%%%%....%%%%%...+
 + Version: V1.1                +..%%..%%..%%..%%......%%....%%....%%......%%..%%..+
 + Whoami:                      +..%%..%%..%%..%%...%%%%.....%%....%%%%%%..%%..%%..+
 + https://github.com/AabyssZG  +..................................................+
 +------------------------------+..................................................+
 +.................................................................................+
 +.%%%%%%..%%%%%%..%%%%%...%%...%%..%%%%%%..%%..%%...%%%%...%%%%%%...%%%%...%%%%%..+
 +...%%....%%......%%..%%..%%%.%%%....%%....%%%.%%..%%..%%....%%....%%..%%..%%..%%.+
 +...%%....%%%%....%%%%%...%%.%.%%....%%....%%.%%%..%%%%%%....%%....%%..%%..%%%%%..+
 +...%%....%%......%%..%%..%%...%%....%%....%%..%%..%%..%%....%%....%%..%%..%%..%%.+
 +...%%....%%%%%%..%%..%%..%%...%%..%%%%%%..%%..%%..%%..%%....%%.....%%%%...%%..%%.+
 +------------------------------+--------------------------------------------------+
'''
    print(logo0)

def ImageRead(imagename):
    print('[.] 读取图片当中.....')
    img = Image.open(imagename)
    width, height = img.size
    print('[+] 图片长为：{} \n[+] 图片宽为：{}'.format(width, height))
    return width, height

def del_file(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)

def Folder():
    if os.path.exists("./output"):
        print(f"[.] 输出文件夹已经存在，无需创建")
        datanames = os.listdir("./output")
        for i in datanames:
            c_path = os.path.join("./output", i)
            if os.path.isdir(c_path):#如果是文件夹那么递归调用一下
                del_file(c_path)
            else:                    #如果是一个文件那么直接删除
                os.remove(c_path)
        print(f"[+] 已经清空输出文件夹./output\n")
    else:
        os.mkdir("./output")
        print(f"[+] 切割文件夹不存在，已经创建\n")

def Operations(width,height,x,y):
    width,height = int(width),int(height)
    x,y = int(x),int(y)
    output = []
    if x == 2:
        while x <= 10:
            if (width % x == 0):
                output.insert(1,x)
            x = x+1
        print('[+] 计算成功，获得以下横向数值' + str(output))
    elif y == 2:
        while y <= 10:
            if (height % y == 0):
                output.insert(1,y)
            y = y+1
        print('[+] 计算成功，获得以下纵向数值' + str(output))
    else:
        print('[-] 出现错误，请排查')
    return output

def ImageWrite(x,y,imagename):
    x,y = int(x),int(y)
    img = np.array(Image.open(imagename))
    img_array = np.array(img)

    # 检查图片为彩色还是灰度
    if len(img_array.shape) ==2 :
        # 灰度图像
        for i in range(x):
            print('[+] 正在输出第 {} 张图片'.format(i+1))
            z = np.zeros_like(img)
            z[:, i::x] = img[:, i::x]
            imgnew = Image.fromarray(z)
            imgnew.save('./output/{}-{}.png'.format(x,i+1))
    elif len(img_array.shape) == 3:
        # 彩色图像
        for i in range(x):
            print('[+] 正在输出第 {} 张图片'.format(i+1))
            z = np.zeros_like(img)
            z[:, i::x, :] = img[:, i::x, :]
            imgnew = Image.fromarray(z)
            imgnew.save('./output/{}-{}.png'.format(x,i+1))
    else:
        print('[-] 出现色彩通道错误，请排查')

    print('[+] 文件写入完毕，请查收！')

def ImageOut(x,y,imagename):
    x,y = int(x),int(y)
    img = np.array(Image.open(imagename))
    img_array = np.array(img)

    # 检查图片为彩色还是灰度
    if len(img_array.shape) ==2 :
        # 灰度图像
        for i in range(y):
            print('[+] 正在输出第 {} 张图片'.format(i+1))
            z = np.zeros_like(img)
            z[i::y, :] = img[i::y, :]
            imgnew = Image.fromarray(z)
            imgnew.save('./output/{}-{}.png'.format(y,i+1))
    elif len(img_array.shape) == 3:
        # 彩色图像
        for i in range(y):
            print('[+] 正在输出第 {} 张图片'.format(i+1))
            z = np.zeros_like(img)
            z[i::y, :, :] = img[i::y, :, :]
            imgnew = Image.fromarray(z)
            imgnew.save('./output/{}-{}.png'.format(y,i+1))
    else:
        print('[-] 出现色彩通道错误，请排查')

    print('[+] 文件写入完毕，请查收！')

if __name__ == '__main__':
    title()
    parser = argparse.ArgumentParser(description="Raster Terminator V1.1", epilog='自动读取图片并尝试爆破光栅，诸如：python3 Raster-Terminator.py -x demo.png')
    parser.add_argument('-x', action='store', dest='xcoordinate', help='自动读取图片并尝试爆破横向光栅图')
    parser.add_argument('-y', action='store', dest='ycoordinate', help='自动读取图片并尝试爆破纵向光栅图')
    parser.add_argument('-i', action='store', dest='imageout', help='自定义爆破光栅图')
    args = parser.parse_args()
    try:
        if args.xcoordinate:
            width, height = ImageRead(args.xcoordinate)
            x,y,index = 2,0,0
            outputend = []
            outputend = Operations(width,height,x,y)
            Folder()
            while index < len(outputend):
                x = outputend[index]
                ImageWrite(x,y,args.xcoordinate)
                index += 1
        if args.ycoordinate:
            width, height = ImageRead(args.ycoordinate)
            x,y,index = 0,2,0
            outputend = []
            outputend = Operations(width,height,x,y)
            Folder()
            while index < len(outputend):
                y = outputend[index]
                ImageWrite(x,y,args.ycoordinate)
                index += 1
        if args.imageout:
            ImageRead(args.imageout)
            state = input("横向光栅还是纵向光栅（x/y） >>> ")
            x,y = 0,0
            if state == "x":
                x = input("横向光栅多少量 >>> ")
                ImageOut(x,y,args.imageout)
            elif state == "y":
                y = input("纵向光栅多少量 >>> ")
                ImageOut(x,y,args.imageout)
            else:
                print("请输入x或者y")
                sys.exit()
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except BaseException as e:
        err = str(e)
        print('脚本详细报错：' + err)
        sys.exit(0)