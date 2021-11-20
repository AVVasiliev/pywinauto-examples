from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto.timings import TimeoutError as PywinautoTimeoutError

if __name__ == '__main__':
    command = "control /name Microsoft.WindowsUpdate"
    app = Application(backend='uia').start(command)
    update_pane = Desktop(backend='uia').window(auto_id="PermanentNavigationView", top_level_only=False)

    list_updates = update_pane.child_window(auto_id="SystemSettings_MusUpdate_AvailableUpdatesList2_ListView")
    try:
        list_updates.wait('exists', timeout=3)
        data_about_updates = [el.children()[0].children_texts() for el in list_updates.children()]
        for update, state in data_about_updates:
            print(update, state)
    except PywinautoTimeoutError:
        print("List available updates not found")

    button_update = update_pane.child_window(auto_id='SystemSettings_MusUpdate_UpdateActionButton2_Button')
    button_update.click()
    print("Wait while button will be enabled - after updates")
    button_update.wait('enabled')
    print("Finish!")
    update_pane.parent().parent().close()
