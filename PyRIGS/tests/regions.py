from pypom import Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import datetime


def parse_bool_from_string(string):
    # Used to convert from attribute strings to boolean values, written after I found this:
    # >>> bool("false")
    # True
    if string == "true":
        return True
    else:
        return False


class BootstrapSelectElement(Region):
    _main_button_locator = (By.CSS_SELECTOR, 'button.dropdown-toggle')
    _option_box_locator = (By.CSS_SELECTOR, 'ul.dropdown-menu')
    _option_locator = (By.CSS_SELECTOR, 'ul.dropdown-menu.inner>li>a.dropdown-item')
    _select_all_locator = (By.CLASS_NAME, 'bs-select-all')
    _deselect_all_locator = (By.CLASS_NAME, 'bs-deselect-all')
    _search_locator = (By.CSS_SELECTOR, '.bs-searchbox>input')
    _status_locator = (By.CLASS_NAME, 'status')

    @property
    def is_open(self):
        return parse_bool_from_string(self.find_element(*self._main_button_locator).get_attribute("aria-expanded"))

    def toggle(self):
        original_state = self.is_open
        option_box = self.find_element(*self._option_box_locator)
        if not original_state:
            self.wait.until(expected_conditions.invisibility_of_element(option_box))
        else:
            self.wait.until(expected_conditions.visibility_of(option_box))
        return self.find_element(*self._main_button_locator).click()

    def open(self):
        if not self.is_open:
            self.toggle()

    def close(self):
        if self.is_open:
            self.toggle()

    def select_all(self):
        self.find_element(*self._select_all_locator).click()

    def deselect_all(self):
        self.find_element(*self._deselect_all_locator).click()

    def search(self, query):
        search_box = self.find_element(*self._search_locator)
        self.open()
        search_box.clear()
        search_box.send_keys(query)
        status_text = self.find_element(*self._status_locator)
        self.wait.until(expected_conditions.invisibility_of_element_located(self._status_locator))

    @property
    def options(self):
        options = list(self.find_elements(*self._option_locator))
        return [self.BootstrapSelectOption(self, i) for i in options]

    def set_option(self, name, selected):
        options = list((x for x in self.options if x.name == name))
        assert len(options) == 1
        options[0].set_selected(selected)

    class BootstrapSelectOption(Region):
        _text_locator = (By.CLASS_NAME, 'text')

        @property
        def selected(self):
            return parse_bool_from_string(self.root.get_attribute("aria-selected"))

        def toggle(self):
            self.root.click()

        def set_selected(self, selected):
            if self.selected != selected:
                self.toggle()

        @property
        def name(self):
            return self.find_element(*self._text_locator).text


class TextBox(Region):
    @property
    def value(self):
        return self.root.get_attribute("value")

    def set_value(self, value):
        self.root.clear()
        self.root.send_keys(value)


class CheckBox(Region):
    def toggle(self):
        self.root.click()

    @property
    def value(self):
        return parse_bool_from_string(self.root.get_attribute("checked"))

    def set_value(self, value):
        if value != self.value:
            self.toggle()


class DatePicker(Region):
    @property
    def value(self):
        return datetime.datetime.strptime(self.root.get_attribute("value"), "%Y-%m-%d")

    def set_value(self, value):
        self.root.clear()
        self.root.send_keys(value.strftime("%d%m%Y"))


class TimePicker(Region):
    @property
    def value(self):
        return datetime.datetime.strptime(self.root.get_attribute("value"), "%H:%M")

    def set_value(self, value):
        self.root.clear()
        self.root.send_keys(value.strftime("%H:%M"))


class DateTimePicker(Region):
    @property
    def value(self):
        return datetime.datetime.strptime(self.root.get_attribute("value"), "%Y-%m-%d %H:%M")

    def set_value(self, value):
        self.root.clear()

        date = value.date().strftime("%d%m%Y")
        time = value.time().strftime("%H%M")

        self.root.send_keys(date)
        self.root.send_keys(Keys.TAB)
        self.root.send_keys(time)

class SingleSelectPicker(Region):
    @property
    def value(self):
        picker = Select(self.root)
        return picker.first_selected_option.text

    def set_value(self, value):
        picker = Select(self.root)
        picker.select_by_visible_text(value)


class ErrorPage(Region):
    _error_item_selector = (By.CSS_SELECTOR, "dl>span")

    class ErrorItem(Region):
        _field_selector = (By.CSS_SELECTOR, "dt")
        _error_selector = (By.CSS_SELECTOR, "dd>ul>li")

        @property
        def field_name(self):
            return self.find_element(*self._field_selector).text

        @property
        def errors(self):
            return [x.text for x in self.find_elements(*self._error_selector)]

    @property
    def errors(self):
        error_items = [self.ErrorItem(self, x) for x in self.find_elements(*self._error_item_selector)]
        errors = {}
        for error in error_items:
            errors[error.field_name] = error.errors
        return errors


class Modal(Region):
    _submit_locator = (By.CSS_SELECTOR, '.btn-primary')
    _header_selector = (By.TAG_NAME, 'h3')

    form_items = {
        'name': (TextBox, (By.ID, 'id_name'))
    }

    @property
    def header(self):
        return self.find_element(*self._header_selector).text

    @property
    def is_open(self):
        return self.root.is_displayed()

    def submit(self):
        self.root.find_element(*self._submit_locator).click()

    def __getattr__(self, name):
        if name in self.form_items:
            element = self.form_items[name]
            form_element = element[0](self, self.find_element(*element[1]))
            return form_element.value
        else:
            return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name in self.form_items:
            element = self.form_items[name]
            form_element = element[0](self, self.find_element(*element[1]))
            form_element.set_value(value)
        else:
            self.__dict__[name] = value


# TODO Move to RIGS regions
class ItemModal(Modal):
    _header_selector = (By.TAG_NAME, 'h4')

    form_items = {
        'name': (TextBox, (By.ID, 'item_name')),
        'description': (TextBox, (By.ID, 'item_description')),
        'quantity': (TextBox, (By.ID, 'item_quantity')),
        'price': (TextBox, (By.ID, 'item_cost'))
    }
