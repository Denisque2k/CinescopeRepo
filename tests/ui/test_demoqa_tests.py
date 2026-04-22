import re
import time
from datetime import datetime
import os

from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://demoqa.com/text-box")
    page.get_by_role("textbox", name="Full Name").click()
    page.get_by_role("textbox", name="Full Name").fill("Gogushtance Koltsutabskiy")
    page.get_by_role("textbox", name="Full Name").press("Enter")
    page.get_by_role("textbox", name="name@example.com").click()
    page.get_by_role("textbox", name="name@example.com").fill("gogushtancer@koltsmail.com")
    page.get_by_role("textbox", name="Current Address").click()
    page.get_by_role("textbox", name="Current Address").fill("Kurrent addruss tipa")
    page.locator("#permanentAddress").click()
    page.locator("#permanentAddress").fill("Tut permanent address tipa")
    page.get_by_role("button", name="Submit").click()
    expect(page.locator("#name")).to_contain_text("Name:Gogushtance Koltsutabskiy")
    expect(page.locator("#email")).to_contain_text("Email:gogushtancer@koltsmail.com")
    expect(page.locator("#output")).to_contain_text("Current Address :Kurrent addruss tipa")
    expect(page.locator("#output")).to_contain_text("Permananet Address :Tut permanent address tipa")
    time.sleep(10)

def test_page_web_tables(page: Page):
    page.goto('https://demoqa.com/webtables')
    page.get_by_role("button", name="Add").click()
    expect(page.locator(".modal-content")).to_be_visible()
    modal_title = page.locator(".modal-content .modal-header .modal-title.h4")
    expect(modal_title).to_have_text("Registration Form")
    expect(modal_title).to_be_visible()
    page.get_by_placeholder("First Name").fill("Tarbantine")
    page.locator("#lastName").fill("Gulbaroskin")
    page.locator("#userEmail").fill("Laptusir@gazyet.com")
    page.get_by_placeholder("Age").fill("26")
    page.locator("#salary").fill("100000")
    page.get_by_placeholder("Department").fill("Developers")
    page.get_by_role("button", name="Submit").click()
    time.sleep(5)

def test_page_practice_form(page: Page):
    page.goto("https://demoqa.com/automation-practice-form")
    page.type("#firstName", "Raskoryak", delay=250)
    page.fill("#lastName", "Barkuselkin")
    page.fill("#userEmail", "gorshochekbatvyi@otlichnyu.com")
    page.check('#gender-radio-1')
    page.fill("#userNumber", "88005553535")
    expected_date = datetime.now().strftime("%d %b %Y")
    actual_value = page.get_attribute("#dateOfBirthInput", "value")
    assert expected_date == actual_value
    page.locator("#subjectsInput").fill("M")
    page.get_by_role("option", name="Maths").click()
    page.check("#hobbies-checkbox-1")
    page.get_by_role("button", name="Choose File").click()
    file_path = os.path.abspath("/Users/ekaterinasvecnikova/Desktop/test_logs.pdf")
    page.get_by_role("button", name="Choose File").set_input_files(file_path)
    page.fill("#currentAddress", "Current state, current city, current street, etc")
    page.locator("#state > .css-13cymwt-control > .css-hlgwow > .css-19bb58m").click()
    page.get_by_role("option", name="NCR").click()
    page.locator("#city > .css-13cymwt-control > .css-hlgwow > .css-19bb58m").click()
    page.get_by_role("option", name="Delhi").click()
    page.get_by_role("button", name="Submit").click()
    footer = page.locator("footer")
    #footer_text = footer.text_content().strip()
    expect(footer).to_contain_text("TOOLSQA.COM")
    expect(footer).to_contain_text("ALL RIGHTS RESERVED")
    time.sleep(10)

def test_page_radiobutton(page: Page):
    page.goto("https://demoqa.com/radio-button")
    page.is_enabled("#yesRadio")
    page.is_enabled("#impressiveRadio")
    page.is_disabled("#noRadio")
    time.sleep(5)

def test_page_check_box(page: Page):
    page.goto("https://demoqa.com/checkbox")
    expect(page.get_by_text("Home")).to_be_visible()
    expect(page.get_by_text("Desktop")).to_be_hidden()
    page.locator(".rc-tree-switcher").click()
    expect(page.get_by_text("Desktop")).to_be_visible()

def test_page_dynamic_properties(page: Page):
    page.goto("https://demoqa.com/dynamic-properties")
    expect(page.locator("#visibleAfter")).to_be_hidden()
    page.wait_for_selector("#visibleAfter", timeout=6000)

def test_expect(page: Page):
    page.goto("https://demoqa.com/radio-button")
    yes_radio = page.get_by_role("radio", name="Yes")
    impressive_radio = page.get_by_role("radio", name="Impressive")
    no_radio = page.get_by_role("radio", name="No")
    expect(no_radio).to_be_disabled()  # проверяем, что не доступен
    expect(yes_radio).to_be_enabled()  # проверяем, что доступен
    expect(impressive_radio).to_be_enabled()  # проверяем, что доступен
    page.locator('[for="yesRadio"]').click()  # тут хитрый лейбл не позволяет кликнуть прямо на инпут, обращаемся по лейблу
    expect(yes_radio).to_be_checked()  # проверяем, что отмечен
    expect(impressive_radio).not_to_be_checked()  # проверяем, что не отмечен

