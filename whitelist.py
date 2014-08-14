#!/usr/bin/python
# -*- coding: utf-8 -*- 

whiteList=['杨舟','罗群芳','方金德','陈鸿钦','黎晓峰','杜靖','潘瑞','柳夫虎']

if __name__ == '__main__':
    execQuery("update Board set change_text='在' where id = 64001;")