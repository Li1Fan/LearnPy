from selenium import webdriver


def get_contact(name):
    # 创建浏览器对象
    driver = webdriver.Chrome()

    # 打开网页
    driver.get("file:///C:/Users/10262/Desktop/a.html")

    # 找到姓名为张三的行
    rows = driver.find_elements_by_xpath("//tbody/tr[td[text()='{}']]".format(name))
    rows = driver.find_elements_by_xpath("//tr[td[text()='李四']]")
    # rows = driver.find_element_by_css_selector("tbody tr td:contains('张三')")
    print(rows)
    # 如果找到了对应的行，则获取联系方式
    if len(rows) > 0:
        contact = rows[0].find_element_by_xpath("./td[2]")
        print(contact)
        contact = contact.text
    else:
        contact = None

    # 关闭浏览器
    driver.quit()

    # 返回联系方式
    return contact


if __name__ == '__main__':
    contact = get_contact("李四")
    if contact:
        print(contact)
    else:
        print("未找到对应的联系方式")
