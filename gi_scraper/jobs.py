from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib import parse
import time

url_frame = "https://www.google.com/search?{}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjR5qK3rcbxAhXYF3IKHYiBDf8Q_AUoAXoECAEQAw&biw=1291&bih=590"


def worker_args() -> tuple:
    options = webdriver.ChromeOptions()
    options.add_argument("ignore-certificate-errors")
    options.add_argument("incognito")
    options.add_argument("headless")
    options.add_argument("log-level=3")
    options.add_argument("disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(chrome_options=options)
    return (driver, )


def low_res(pid, total_workers, output_queue, driver, query, task):
    global url_frame
    url = url_frame.format(parse.urlencode({'q': query.value}))
    driver.get(url)

    action = ActionChains(driver)

    scroll_to_y(action, 20000, task)

    imgs = driver.find_elements(By.CLASS_NAME, "rg_i")

    for img in imgs:
        if not task.value: break
        img_url = img.get_attribute("src")
        if isinstance(img_url, str):
            output_queue.put(img_url)


def high_res(pid, total_workers, output_queue, driver, query, task):
    global url_frame
    url = url_frame.format(parse.urlencode({'q': query.value}))
    driver.get(url)

    action = ActionChains(driver)

    index = pid

    delay = 3  #seconds

    wait = WebDriverWait(driver, delay)

    imgs = list(set(driver.find_elements(By.CLASS_NAME, "rg_i")))

    while task.value:
        try:
            img = imgs[index]
            action.click(img).perform()
            elements = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "KAlRDb")))

            img_element = elements[-1]
            img_url = img_element.get_attribute("src")

            if isinstance(img_url, str):
                output_queue.put(img_url)
            index += total_workers
            if index >= len(imgs):
                old_set = set(imgs)
                new_set = set(driver.find_elements(By.CLASS_NAME, "rg_i"))
                imgs = list(old_set.union(new_set))
        except Exception as e:
            index += total_workers
            # print(e)


def scroll_to_y(action, y, task):
    delta_y = y // 1000
    for _ in range(delta_y):
        if not task.value: break
        action.scroll_by_amount(delta_x=0, delta_y=1000).perform()
        time.sleep(0.5)
