from utills import *

driver = get_driver()

navigate_to_login(driver)

# 1) 로그인
login(driver, "qa3team03@elicer.com", "@qa12345")
print_current_url(driver)

# 2) 로그아웃
logout(driver)
print_current_url(driver)

# 3) 재로그인
relogin(driver, "@qa12345")
print_current_url(driver)
