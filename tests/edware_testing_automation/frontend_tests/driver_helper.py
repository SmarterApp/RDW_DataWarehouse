import time


def scroll_to_element(driver, element):
    count = 0
    while not element.is_displayed():
        driver.execute_script("window.scrollTo(0, " + str(element.location["y"]) + ");")
        time.sleep(0.5)
        count += 1
        if count > 20: break
    return element
