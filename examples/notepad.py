import time
from pywinauto.application import Application

if __name__ == "__main__":
    app_name = "notepad"
    app = Application(backend='uia').start(app_name)
    main_form = app.top_window()
    main_form.wait('visible')
    wrap_object = main_form.wrapper_object()
    main_form.print_control_identifiers()
    edit_form = main_form.child_window(auto_id="15").wrapper_object()
    edit_form.set_edit_text("It just works")
    time.sleep(5)
    wrap_object.close()
    main_form.print_control_identifiers()
    not_save = main_form.child_window(title="Не сохранять", auto_id="CommandButton_7", control_type="Button")\
        .wrapper_object()
    time.sleep(3)
    print(app.is_process_running())
    not_save.click()
    time.sleep(1)
    print(app.is_process_running())
