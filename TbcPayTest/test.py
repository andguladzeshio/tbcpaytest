from allure_commons.types import AttachmentType
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

"""
    თითქმის ყველა ფუნქციას აქვს ერთნაირი ლოგიკა ამიტომ სათითაოდ კომენტარები აღარ დავუწერე
    
    ფუნქციებში get მეთოდს არგუმენტად ყოველთვის გადავცემ tbc ბანკის homepage-ს და შემდგომ გადავდივარ სასურველ გვერდზე
    ეს ანელებს ფუნქციების მოქმედებას , მაგრამ უფრო დეტალურს ხდის მათ
    
    ფუნქციებში შესამოწმებელი მნიშვნელობები წარმოდგენილი მაქვს სიმრავლეებად და ვცდილობ მათი სხვაობის შედეგით გავიგო
    არის თუ არა შესამოწმებელი მნიშვნელობები საიტზე(თუ ყველა ელემენტი ადგილზეა უნდა მივიღო
    ცარიელი სიმრავლე). კოდის ასეთი სახით წარმოდგენა უზრუნველყოფს მის გამართულ მუშაობას
    იმ შემთხვევაშიც , თუ საიტზე დაემატება სხვა ელემენტები , ხოლო შესამოწმებელი ელემენტების ჩამატებაც ძალიან ადვილად
    მოხერხდება უკვე შექმნილ სიმრავლეებში.
"""


def test_header_nav():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://tbcpay.ge/")
    cont = driver.find_element_by_xpath(
        '//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/header/section/div[2]/div/nav')
    itemsinnav = set(cont.text.split("\n"))
    itemstocheck = {"სერვისები", "გადარიცხვები", "ბიზნესისთვის", "გადაიხადე უცხოეთიდან"}
    if itemstocheck - itemsinnav == set():
        allure.attach(driver.get_screenshot_as_png(), name="HeaderNavSuccess", attachment_type=AttachmentType.PNG)
        driver.quit()
    else:
        allure.attach(driver.get_screenshot_as_png(), name="HeaderNavFailure", attachment_type=AttachmentType.PNG)
        driver.quit()
        assert False


def test_service_nav():     # მხოლოდ ეს ფუნქცია უნდა იყოს წარუმატებელი (კომუნალური გადახდები/კომუნალური გადასახადები)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://tbcpay.ge/")
    servicelink = driver.find_element_by_link_text("სერვისები")
    servicelink.click()
    try:
        mylist = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "sc-YY1t1ypb4-0")))
        listitems = mylist.find_elements_by_class_name("name")
        itemstocheck = {"პოპულარული სერვისები", "მობილური კავშირი", "ბანკები დაზღვევა მიკროსაფინანსო",
                        "ტოტალიზატორები კაზინო ლატარია", "ინტერნეტი ტელეფონი ტელევიზია", "კომუნალური გადახდები",
                        "ტრანსპორტი", "სახელმწიფო სერვისები", "სხვადასხვა"}
        existingitemsset = set()
        for item in listitems:
            existingitemsset.add(item.text)
        if itemstocheck - existingitemsset == set():
            allure.attach(driver.get_screenshot_as_png(), name="ServiceNavSuccess", attachment_type=AttachmentType.PNG)
            driver.quit()
        else:
            allure.attach(driver.get_screenshot_as_png(), name="ServiceNavFailure", attachment_type=AttachmentType.PNG)
            driver.quit()
            assert False
    except TimeoutException:
        allure.attach(driver.get_screenshot_as_png(), name="ServiceNavFailure", attachment_type=AttachmentType.PNG)
        driver.quit()
        assert False


def test_searchbarandbutton():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://tbcpay.ge/")
    form = driver.find_element_by_xpath(
        '//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/main/div/div/div[1]/div/div[2]/div/div/div/form')
    searchbar = form.find_element_by_tag_name("input")
    if not searchbar.is_displayed():
        allure.attach(driver.get_screenshot_as_png(), name="SearchBarFailure", attachment_type=AttachmentType.PNG)
        driver.quit()
        assert False
    searchbutton = form.find_element_by_tag_name("button")
    searchbuttontext = searchbutton.find_element_by_tag_name("span")
    if not (searchbutton.is_displayed() and searchbuttontext.text == "ძიება"):
        allure.attach(driver.get_screenshot_as_png(), name="SearchButtonFailure", attachment_type=AttachmentType.PNG)
        driver.quit()
        assert False
    allure.attach(driver.get_screenshot_as_png(), name="SearchFormSuccess", attachment_type=AttachmentType.PNG)
    driver.quit()


def test_search():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://tbcpay.ge/")
    form = driver.find_element_by_xpath(
        '//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/main/div/div/div[1]/div/div[2]/div/div/div/form')
    searchbar = form.find_element_by_tag_name("input")
    searchbar.send_keys("მობილური")
    mobilebalance = driver.find_element_by_link_text("მობილური ბალანსის შევსება")
    if mobilebalance.is_displayed():
        allure.attach(driver.get_screenshot_as_png(), name="BalanceSuccess", attachment_type=AttachmentType.PNG)
        driver.quit()
    else:
        allure.attach(driver.get_screenshot_as_png(), name="BalanceFailure", attachment_type=AttachmentType.PNG)
        driver.quit()
        assert False


def test_mobilenumber():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://tbcpay.ge/")
    form = driver.find_element_by_xpath(
        '//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/main/div/div/div[1]/div/div[2]/div/div/div/form')
    searchbar = form.find_element_by_tag_name("input")
    searchbar.send_keys("მობილური")
    mobilebalance = driver.find_element_by_link_text("მობილური ბალანსის შევსება")
    mobilebalance.click()
    mobilenumber = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.NAME, "1213-abonentCode")))
    checkbutton = driver.find_element_by_xpath('//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/main/'
                                               'div/div/main/section/div[1]/div[2]/div/div[2]/form/button')
    if not mobilenumber.is_displayed() or checkbutton.text != "შემოწმება":
        allure.attach(driver.get_screenshot_as_png(), name="MobileNumFailure", attachment_type=AttachmentType.PNG)
        driver.quit()
        assert False
    allure.attach(driver.get_screenshot_as_png(), name="MobileNumSuccess", attachment_type=AttachmentType.PNG)
    driver.quit()


def test_enter_mobile_number():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://tbcpay.ge/")
    form = driver.find_element_by_xpath(
        '//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/main/div/div/div[1]/div/div[2]/div/div/div/form')
    searchbar = form.find_element_by_tag_name("input")
    searchbar.send_keys("მობილური")
    mobilebalance = driver.find_element_by_link_text("მობილური ბალანსის შევსება")
    mobilebalance.click()
    mobilenumber = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.NAME, "1213-abonentCode")))
    mobilenumber.send_keys("555122334")
    allure.attach(driver.get_screenshot_as_png(), name="NumberInput", attachment_type=AttachmentType.PNG)


def test_choose_service():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://tbcpay.ge/")
    form = driver.find_element_by_xpath(
        '//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/main/div/div/div[1]/div/div[2]/div/div/div/form')
    searchbar = form.find_element_by_tag_name("input")
    searchbar.send_keys("მობილური")
    mobilebalance = driver.find_element_by_link_text("მობილური ბალანსის შევსება")
    mobilebalance.click()
    mobilenumber = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.NAME, "1213-abonentCode")))
    mobilenumber.send_keys("555122334")
    checkbutton = driver.find_element_by_xpath('//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/main/'
                                               'div/div/main/section/div[1]/div[2]/div/div[2]/form/button')
    checkbutton.click()
    service = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                              '//*[@id="mount"]/div/div[2]/div[2]'
                                                                              '/div/div/div/div/main'
                                                                              '/div/div/main/section/div[1]'
                                                                              '/div[2]/div[2]/div[2]/div/div')))
    service.click()
    servicesdiv = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "BONUS")))
    servicestocheck = {'ბალანსის შევსება', '"მეტი" - 8 ₾', '"მეტი" - 10 ₾'}
    servicesavailable = set(servicesdiv.text.split("\n"))
    if servicestocheck - servicesavailable == set():
        allure.attach(driver.get_screenshot_as_png(), name="ServicesSuccess", attachment_type=AttachmentType.PNG)
        driver.quit()
    else:
        allure.attach(driver.get_screenshot_as_png(), name="ServicesFailure", attachment_type=AttachmentType.PNG)
        driver.quit()
        assert False


def test_service():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://tbcpay.ge/")
    form = driver.find_element_by_xpath(
        '//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/main/div/div/div[1]/div/div[2]/div/div/div/form')
    searchbar = form.find_element_by_tag_name("input")
    searchbar.send_keys("მობილური")
    mobilebalance = driver.find_element_by_link_text("მობილური ბალანსის შევსება")
    mobilebalance.click()
    mobilenumber = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.NAME, "1213-abonentCode")))
    mobilenumber.send_keys("555122334")
    checkbutton = driver.find_element_by_xpath('//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/main/'
                                               'div/div/main/section/div[1]/div[2]/div/div[2]/form/button')
    checkbutton.click()
    service = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                              '//*[@id="mount"]/div/div[2]/div[2]'
                                                                              '/div/div/div/div/main'
                                                                              '/div/div/main/section/div[1]'
                                                                              '/div[2]/div[2]/div[2]/div/div')))
    service.click()
    servicetochoose = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.LINK_TEXT, '"მეტი" - 10 ₾')))
    servicetochoose.click()
    allure.attach(driver.get_screenshot_as_png(), name="ServiceChosen", attachment_type=AttachmentType.PNG)
    driver.quit()


def test_check_elements_in_service():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://tbcpay.ge/")
    form = driver.find_element_by_xpath(
        '//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/main/div/div/div[1]/div/div[2]/div/div/div/form')
    searchbar = form.find_element_by_tag_name("input")
    searchbar.send_keys("მობილური")
    mobilebalance = driver.find_element_by_link_text("მობილური ბალანსის შევსება")
    mobilebalance.click()
    mobilenumber = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.NAME, "1213-abonentCode")))
    mobilenumber.send_keys("555122334")
    checkbutton = driver.find_element_by_xpath('//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/main/'
                                               'div/div/main/section/div[1]/div[2]/div/div[2]/form/button')
    checkbutton.click()
    service = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                              '//*[@id="mount"]/div/div[2]/div[2]'
                                                                              '/div/div/div/div/main'
                                                                              '/div/div/main/section/div[1]'
                                                                              '/div[2]/div[2]/div[2]/div/div')))
    service.click()
    servicetochoose = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.LINK_TEXT, '"მეტი" - 10 ₾')))
    servicetochoose.click()
    maincontainer = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                                    '//*[@id="mount"]/div/div[2]/div[2]'
                                                                                    '/div/div/div/div/main/div/div/main'
                                                                                    '/section/div[1]/div[2]/div[3]'
                                                                                    '/div')))
    setforallelements = set()
    smalltext = maincontainer.find_elements_by_tag_name("small")
    for text in smalltext:
        setforallelements.add(text.text.replace(":", ""))
    setforallelements.remove("საკომისიო")
    totalcomision = maincontainer.find_element_by_class_name("total-commission").text.replace("\n", " ")
    setforallelements.add(totalcomision)
    debt = maincontainer.find_element_by_class_name("debt")
    setforallelements.add(debt.text)
    inputwithtext = maincontainer.find_element_by_name("1327")
    setforallelements.add(inputwithtext.get_attribute("value"))
    innerdiv = maincontainer.find_element_by_class_name("payment")
    totalamount = innerdiv.find_element_by_tag_name("b")
    paybutton = innerdiv.find_element_by_class_name("pay-btn")
    setforallelements.add(totalamount.text)
    setforallelements.add(paybutton.text)
    setforelementstocheck = {"დავალიანება", "10.00 c", "თანხის ოდენობა c", "10", "საკომისიო 0.12c",
                             "ჯამში გადასახდელი", "10.12 c", "გადახდა"}
    if setforelementstocheck - setforallelements == set():
        allure.attach(driver.get_screenshot_as_png(), name="ServiceElementsSuccess", attachment_type=AttachmentType.PNG)
        driver.quit()
    else:
        allure.attach(driver.get_screenshot_as_png(), name="ServiceElementsFailure", attachment_type=AttachmentType.PNG)
        driver.quit()
        assert False


def test_click_paybutton():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://tbcpay.ge/")
    form = driver.find_element_by_xpath(
        '//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/main/div/div/div[1]/div/div[2]/div/div/div/form')
    searchbar = form.find_element_by_tag_name("input")
    searchbar.send_keys("მობილური")
    mobilebalance = driver.find_element_by_link_text("მობილური ბალანსის შევსება")
    mobilebalance.click()
    mobilenumber = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.NAME, "1213-abonentCode")))
    mobilenumber.send_keys("555122334")
    checkbutton = driver.find_element_by_xpath('//*[@id="mount"]/div/div[2]/div[2]/div/div/div/div/main/'
                                               'div/div/main/section/div[1]/div[2]/div/div[2]/form/button')
    checkbutton.click()
    service = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                              '//*[@id="mount"]/div/div[2]/div[2]'
                                                                              '/div/div/div/div/main'
                                                                              '/div/div/main/section/div[1]'
                                                                              '/div[2]/div[2]/div[2]/div/div')))
    service.click()
    servicetochoose = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.LINK_TEXT, '"მეტი" - 10 ₾')))
    servicetochoose.click()
    paybutton = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "pay-btn")))
    paybutton.click()
    try:
        WebDriverWait(driver, 10).until(ec.url_contains("ecommerce.ufc.ge"))
        allure.attach(driver.get_screenshot_as_png(), name="UrlMatch", attachment_type=AttachmentType.PNG)
        driver.quit()
    except TimeoutException:
        allure.attach(driver.get_screenshot_as_png(), name="UrlMisMatch", attachment_type=AttachmentType.PNG)
        driver.quit()
        assert False
