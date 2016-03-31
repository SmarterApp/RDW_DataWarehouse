# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

import time


def scroll_to_element(driver, element):
    count = 0
    while not element.is_displayed():
        driver.execute_script("window.scrollTo(0, " + str(element.location["y"]) + ");")
        time.sleep(0.5)
        count += 1
        if count > 20: break
    return element
