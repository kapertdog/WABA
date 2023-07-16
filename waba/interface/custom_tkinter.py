from dataclasses import dataclass
from PIL import Image, ImageTk
import customtkinter as ctk


@dataclass
class DefaultTheme:
    accent: tuple = ("#3b8ed0", "#1f6aa5")
    unpressed: tuple = ("#b5b5b5", "#424242")
    subText: tuple = ("#808080", "#707070")
    disabledText: tuple = ("#ffffff", "#ffffff")
    hover: tuple = ("#36719f", "#144870")
    background: tuple = ("#ebebec", "#212325")
    background2: tuple = ("#d1d5d8", "#2a2d2e")
    background3: tuple = ("#c0c2c5", "#343638")


class SettingsSect(ctk.CTkFrame):
    def __init__(self, *args, title_text: str, fg_color=DefaultTheme.background2,
                 centered=True, folded=True, title_font=("default", 20), title_color=DefaultTheme.subText,
                 frame_fg_color=DefaultTheme.background3, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        self.folded = folded
        self.title = ctk.CTkButton(self, text=title_text, font=title_font, fg_color=fg_color,
                                   command=self.show_or_hide,
                                   text_color=title_color, text_color_disabled=title_color)
        # self.title = ctk.CTkLabel(self, text=title_text, text_font=title_font,
        #                           text_color=title_color, anchor="center" if centered else "w")
        self.title.pack(anchor="center" if centered else "w", padx=10)
        self.frame = ctk.CTkFrame(self, fg_color=frame_fg_color)
        if not self.folded:
            self.frame.pack(expand=True, fill=ctk.BOTH)

    def show_or_hide(self):
        if self.folded:
            self.frame.pack(expand=True, fill=ctk.BOTH)
            self.folded = False
        else:
            # self.slow_hide()
            self.frame.pack_forget()
            self.folded = True

    def slow_hide(self):
        value = self.frame.winfo_height()
        for i in range(100):
            value = value - (value // 100 * i)
            self.frame.configure(width=value)
            self.update()
        self.frame.pack_forget()


class NamedOptionMenu(ctk.CTkFrame):
    def __init__(self, *args, name: str, values: dict, padding: int = 0,
                 bg_color=DefaultTheme.background3, dynamic_resizing=True, **kwargs):
        super().__init__(*args, fg_color=bg_color, **kwargs)
        self.name = ctk.CTkLabel(self, text=name, anchor="w")
        self.name.pack(anchor="w", padx=padding, pady=padding, side=ctk.LEFT)
        self.values = values
        self.mode = "dict" if type(values) == dict else "tuple"
        self.option_menu = ctk.CTkOptionMenu(self, values=[*values], dynamic_resizing=dynamic_resizing)
        self.option_menu.pack(anchor="w", padx=(5, padding), pady=padding, side=ctk.RIGHT, fill=ctk.X)

    def get_value(self):
        return self.values[self.option_menu.get()] if self.mode == "dict" else self.option_menu.get()

    def update_values(self, values):
        self.values = values
        self.mode = "dict" if type(values) == dict else "tuple"
        self.option_menu.configure(values=[*self.values])


class SubtitleLabel(ctk.CTkLabel):
    def __init__(self, *args, text_font=("default", 8), text_color=DefaultTheme.subText,
                 anchor="w", **kwargs):
        super().__init__(*args, font=text_font, text_color=text_color,
                         anchor=anchor, **kwargs)


class UpdateDisplay(ctk.CTkFrame):
    def __init__(self, *args, bg_color=DefaultTheme.background2, **kwargs):
        super().__init__(*args, fg_color=bg_color, **kwargs)
        self._state_frame = ctk.CTkFrame(self)
        self._state_frame.pack(fill=ctk.X, padx=5, pady=5)
        self._state_lbl = ctk.CTkLabel(
            self._state_frame, text="× " "Нет обновлений", anchor="w"
        )
        self._state_lbl.pack(padx=(10, 0), side=ctk.LEFT)
        self.download_btn = ctk.CTkButton(self._state_frame, text="Скачать")
        self.install_btn = ctk.CTkButton(self._state_frame, text="Установить")
        self.progress_bar = ctk.CTkProgressBar(self)
        self._last_update_lbl = ctk.CTkLabel(
            self, text="Последняя проверка: " "Только что" " ⧖"
        )
        self._last_update_lbl.pack(pady=(0, 5))
        # self.ready_to_download("v3.4.0.0")
        # self.ready_to_install("v3.4.0.0")
        # self.checking()

    def set_last_time_check(self, time: str):
        self._last_update_lbl.configure(text="Последняя проверка: " + time + " ⧖")
        ...

    def checking(self):
        self.hide_download_button()
        self.hide_install_button()
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.set(0)
        self.progress_bar.start()
        self.show_progress_bar()
        self._state_lbl.configure(text="Поиск обновлений...")
        ...

    def show_progress_bar(self):
        self.progress_bar.pack(fill=ctk.X, padx=5, pady=5)
        self._last_update_lbl.pack_forget()

    def hide_progress_bar(self):
        self.progress_bar.pack_forget()
        self._last_update_lbl.pack(pady=(0, 5))

    def show_download_button(self):
        self.download_btn.pack(fill=ctk.X)

    def hide_download_button(self):
        self.download_btn.pack_forget()

    def show_install_button(self):
        self.install_btn.pack(fill=ctk.X)

    def hide_install_button(self):
        self.install_btn.pack_forget()

    def downloading(self, filename):
        self.hide_download_button()
        self.progress_bar.set(0)
        self.show_progress_bar()
        self._state_lbl.configure(text=f"‣ Скачивание {filename}...")

    def preparing_for_install(self):
        self.hide_install_button()
        self.hide_download_button()
        self.show_progress_bar()
        self._state_lbl.configure(text=f"Подготовка к установке...")

    def nothing_to_update(self):
        self._state_lbl.configure(text="× " "Нет обновлений")

    def ready_to_download(self, version: str):
        self.hide_progress_bar()
        self.hide_install_button()
        self._state_lbl.configure(text="↥ Доступна " + version)
        self.show_download_button()

    def ready_to_install(self, version):
        self.hide_progress_bar()
        self.hide_download_button()
        self._state_lbl.configure(text="↥ Загружена " + version)
        self.show_install_button()


class Settings_page(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        boot_values = {"Никогда": "newer",
                       "При ручном запуске": "manually",
                       "При автозагрузке": "autostart",
                       "Всегда": "anyway"}
        notif_values = {"Не уведомлять": "muted",
                        "При ручном запуске": "manually",
                        "Каждый раз": "everytime"}
        tray_lmb_action_values = {
            "Развернуть окно": "deiconify",
            "Обновить яркость": "update_brightness",
            "Ничего": "nothing",
        }
        tray_hide_options = {
            "Вместо закрытия": "instead_exit",
            "Вместо сворачивания": "instead_iconify",
            "Не скрывать": "instead_iconify",
        }
        check_frequency_values = {
            "При запуске": "on_boot",
            "Каждый день": "per_day",
            "Раз в неделю": "per_week",
            "Никогда": "newer"
        }
        auto_install_values = {
            "Никогда": "newer",
            "После загрузки": "after_download",
            "Перед открытием": "before_opening"
        }
        installation_ways = {
            "ClickTeam установщик": "ClickTeam",
            "Встроенный распаковщик": "internal",
        }
        branches = [
            "release", "pre-release", "dev"
        ]
        themes = ["default", "material-3"]
        theme_mods = {
            "Как в системе": "system",
            "Тёмный": "dark",
            "Светлый": "light",
        }
        languages = {
            "Русский": "ru",
            "English": "en"
        }

        ...

        self.interface_sect = SettingsSect(self, title_text="Интерфейс")
        self.interface_sect.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="s")

        self.language_om = NamedOptionMenu(
            self.interface_sect.frame,
            name="Язык",
            values=languages
        )
        self.language_om.grid(row=0, column=0, sticky="wne", padx=10, pady=(10, 5))
        self.theme_chose_om = NamedOptionMenu(
            self.interface_sect.frame,
            name="Тема",
            values=themes
        )
        self.theme_chose_om.grid(row=1, column=0, sticky="wne", padx=10, pady=(0, 5))
        # image = ImageTk.PhotoImage(Image.open("resources/sync_dark.png"))
        # self.refresh_themes_btn = ctk.CTkButton(self.theme_chose_om, text="↺", height=20, width=10)
        # self.refresh_themes_btn.pack(side=ctk.RIGHT)
        self.theme_mode_om = NamedOptionMenu(
            self.interface_sect.frame,
            name="Режим темы",
            values=theme_mods
        )
        self.theme_mode_om.grid(row=2, column=0, sticky="wne", padx=10, pady=(0, 5))
        self.import_btn = ctk.CTkButton(
            self.interface_sect.frame,
            text="Импорт темы / языка"
        )
        self.import_btn.grid(row=3, column=0, sticky="wne", padx=10, pady=(5, 5))
        self.guide_btn = ctk.CTkButton(
            self.interface_sect.frame,
            text="Помощь в создании тем и переводов",
            fg_color=DefaultTheme.background3
        )
        self.guide_btn.grid(row=4, column=0, sticky="wne", padx=10, pady=(0, 10))
        ...

        self.boot_sect = SettingsSect(self, title_text="Запуск")
        self.boot_sect.grid(row=1, column=0, padx=10, pady=10, sticky="en")  # , sticky="nw")

        self.autostart_chbtn = ctk.CTkCheckBox(
            self.boot_sect.frame,
            text="Запускаться с системой"
        )
        self.autostart_chbtn.pack(padx=10, pady=(10, 5), anchor="w", fill=ctk.X)
        self.silent_boot_om = NamedOptionMenu(
            self.boot_sect.frame,
            name="Запускать бесшумно",
            values=boot_values
        )
        self.silent_boot_om.pack(padx=10, pady=(5, 5), anchor="w", fill=ctk.X)
        self.fast_boot_om = NamedOptionMenu(
            self.boot_sect.frame,
            name="Ускорить запуск",
            values=boot_values
        )
        self.fast_boot_om.pack(padx=10, pady=(0, 10), anchor="w", fill=ctk.X)
        self.fast_boot_tip = SubtitleLabel(
            self.boot_sect.frame,
            text="Используйте ускорение с осторожностью!\n"
                 "Возможны непредвиденные неполадки"
        )
        self.fast_boot_tip.pack(padx=10, pady=(0, 10))

        ...

        self.notification_sect = SettingsSect(self, title_text="Уведомления")
        self.notification_sect.grid(row=1, column=1, padx=10, pady=10, sticky="wn")  # , sticky="nw")

        self.brightness_changes_om = NamedOptionMenu(
            self.notification_sect.frame,
            name="Изменения яркости",
            values=notif_values
        )
        self.brightness_changes_om.pack(padx=10, pady=(10, 5), anchor="w", fill=ctk.X)
        self.tips_chbtn = ctk.CTkCheckBox(
            self.notification_sect.frame,
            text="Подсказки"
        )
        self.tips_chbtn.pack(padx=10, pady=(5, 5), anchor="w", fill=ctk.X)
        self.warnings_chbtn = ctk.CTkCheckBox(
            self.notification_sect.frame,
            text="Предупреждения"
        )
        self.warnings_chbtn.pack(padx=10, pady=(5, 5), anchor="w", fill=ctk.X)
        self.warnings_chbtn = ctk.CTkCheckBox(
            self.notification_sect.frame,
            text="Ошибки"
        )
        self.warnings_chbtn.pack(padx=10, pady=(5, 5), anchor="w", fill=ctk.X)
        self.warnings_chbtn = ctk.CTkCheckBox(
            self.notification_sect.frame,
            text="Обновления"
        )
        self.warnings_chbtn.pack(padx=10, pady=(5, 10), anchor="w", fill=ctk.X)

        ...

        self.tray_sect = SettingsSect(self, title_text="Иконка в трее")
        self.tray_sect.grid(row=2, column=0, padx=10, pady=10, sticky="ne")  # , sticky="nw")

        self.show_tray_chbtn = ctk.CTkCheckBox(
            self.tray_sect.frame,
            text="Отображать иконку в трее"
        )
        self.show_tray_chbtn.pack(padx=10, pady=(10, 5), anchor="w", fill=ctk.X)
        self.lmb_action_om = NamedOptionMenu(
            self.tray_sect.frame,
            name="Действие ЛКМ",
            values=tray_lmb_action_values
        )
        self.lmb_action_om.pack(padx=10, pady=(5, 5), anchor="w", fill=ctk.X)
        self.withdraw_to_tray_on = NamedOptionMenu(
            self.tray_sect.frame,
            name="Скрывать в трей",
            values=tray_hide_options
        )
        self.withdraw_to_tray_on.pack(padx=10, pady=(0, 5), anchor="w", fill=ctk.X)
        self.process_mirroring_chbtn = ctk.CTkCheckBox(
            self.tray_sect.frame,
            text="Отражать состояние программы"
        )
        self.process_mirroring_chbtn.pack(padx=10, pady=(5, 5), anchor="w", fill=ctk.X)
        self.show_github_button_chbtn = ctk.CTkCheckBox(
            self.tray_sect.frame,
            text="Показывать ссылку на GitHub"
        )
        self.show_github_button_chbtn.pack(padx=10, pady=(5, 10), anchor="w", fill=ctk.X)
        ...

        self.update_sect = SettingsSect(self, title_text="Обновление")
        self.update_sect.grid(row=2, column=1, padx=10, pady=10, sticky="wn")  # , sticky="nw")

        self.update_check_frequency_om = NamedOptionMenu(
            self.update_sect.frame,
            name="Проверять наличие обновлений",
            values=check_frequency_values
        )
        self.update_check_frequency_om.pack(padx=10, pady=(10, 5), anchor="w", fill=ctk.X)
        self.auto_downloading_chbtn = ctk.CTkCheckBox(
            self.update_sect.frame,
            text="Автоматически скачивать при наличии"
        )
        self.auto_downloading_chbtn.pack(padx=10, pady=(5, 5), anchor="w", fill=ctk.X)
        self.auto_install_om = NamedOptionMenu(
            self.update_sect.frame,
            name="Автоматически устанавливать",
            values=auto_install_values
        )
        self.auto_install_om.pack(padx=10, pady=(5, 5), anchor="w", fill=ctk.X)
        self.check_for_updates_btn = ctk.CTkButton(
            self.update_sect.frame,
            text="Проверить наличие обновлений"
        )
        self.check_for_updates_btn.pack(padx=10, pady=(5, 5), fill=ctk.X)
        self.update_display = UpdateDisplay(self.update_sect.frame)
        self.update_display.pack(padx=10, pady=(5, 5), fill=ctk.X)
        self.updating_branch_om = NamedOptionMenu(
            self.update_sect.frame,
            name="Ветка обновлений",
            values=branches
        )
        self.updating_branch_om.pack(padx=10, pady=(5, 5), anchor="w", fill=ctk.X)
        self.preferred_installation_way_om = NamedOptionMenu(
            self.update_sect.frame,
            name="Способ установки",
            values=installation_ways
        )
        self.preferred_installation_way_om.pack(padx=10, pady=(0, 10), anchor="w", fill=ctk.X)


class App(ctk.CTk):
    def __init__(self, textProvider, settingsProvider, versionProvider, updateProvider,
                 theme="system", show_pictures=True, previewProvider=None):
        ctk.set_appearance_mode(theme)
        super().__init__()

        self.geometry("950x580")
        self.title("Waba")
        self.lang = textProvider
        self.settings = settingsProvider
        self.version = versionProvider
        self.updater = updateProvider
        self.preview = previewProvider

        self.selected_page = ctk.StringVar(self, "main")

        ...

        self.button = ctk.CTkButton(self, text="Create Toplevel", command=self.create_toplevel)
        self.button.pack(side="top", padx=40, pady=40)

        self.button.pack_forget()

        ...

        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(side=ctk.TOP)

        self.title_lbl = ctk.CTkLabel(
            self.top_frame, text="Большой страшный амогус"
        )
        self.title_lbl.pack()

        self.top_frame.pack_forget()

        ...

        self.tab_manager = ctk.CTkFrame(self)
        self.tab_manager.pack(side=ctk.LEFT, padx=(10, 5), pady=10)

        if show_pictures:
            image = Image.open("../resources/waba_title.png")
            self.waba_logo = ImageTk.PhotoImage(image)
            # self.waba_logo = ctk.CTkImage(image)
            # self.waba_logo = ctk.CTkImage(
            #     Image.open("resources/waba_title.png"),
            #     size=(30, 10)
            # )
            self.logo_lbl = ctk.CTkLabel(self.tab_manager, image=self.waba_logo,
                                         text=None)
            self.logo_lbl.pack()

        self.main_btn = ctk.CTkButton(
            self.tab_manager,
            text="Главная страница", fg_color=DefaultTheme.unpressed,
            text_color_disabled=DefaultTheme.disabledText,
            command=self.open_main)
        self.main_btn.pack(padx=10, pady=(10, 5))

        self.calibration_btn = ctk.CTkButton(
            self.tab_manager,
            text="Калибровка",
            # text=textProvider.get("calibration"),
            fg_color=DefaultTheme.unpressed,
            text_color_disabled=DefaultTheme.disabledText,
            command=self.open_calibration)
        self.calibration_btn.pack(padx=10, pady=5)

        self.settings_btn = ctk.CTkButton(
            self.tab_manager,
            text="Настройки", fg_color=DefaultTheme.unpressed,
            text_color_disabled=DefaultTheme.disabledText,
            command=self.open_settings)
        self.settings_btn.pack(padx=10, pady=(5, 10))

        self.about_btn = ctk.CTkButton(
            self.tab_manager,
            text="О приложении", fg_color=DefaultTheme.unpressed,
            text_color_disabled=DefaultTheme.disabledText,
            command=self.open_about)
        self.about_btn.pack(padx=10, pady=10)

        ...

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.canvas = ctk.CTkCanvas(self)
        # self.canvas.pack(fill=ctk.BOTH, padx=10, pady=10)
        self.page_holder = ctk.CTkFrame(self)  # , fg_color=DefaultTheme.background)
        self.page_holder.pack(fill=ctk.BOTH, padx=10, pady=10)
        # self.scrollbar = ctk.CTkScrollbar(self.page_holder, command=self.canvas.yview)
        # self.scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y, padx=5, pady=5)
        # self.canvas.configure(yscrollcomman=self.scrollbar.set)

        ...

        self.main_page = ctk.CTkFrame(self.page_holder, fg_color=DefaultTheme.background2)

        ...

        self.calibration_page = ctk.CTkFrame(self.page_holder, fg_color=DefaultTheme.background2)
        ctk.CTkLabel(self.calibration_page, text="Копец на странице что-то есть").pack()

        ...  # -=- Страница настроек -=-
        self.settings_page = Settings_page(self.page_holder, fg_color=DefaultTheme.background2)
        # self.settings_page = ctk.CTkCanvas(self.page_holder, highlightthickness=0, bg=DefaultTheme.background2[1])
        # self.settings_page_scroll = ctk.CTkScrollbar(self.page_holder, command=self.settings_page.yview)
        # self.settings_page.configure(yscrollcommand=self.settings_page_scroll.set)
        # self.settings_page_holder = Settings_page(self.settings_page, fg_color=DefaultTheme.background2)
        # self.settings_page_holder.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

        # self.settings_page.create_window((0, 0), window=self.settings_page_holder, anchor="nw")
        # self.settings_page.update_idletasks()
        # self.settings_page.configure(scrollregion=self.settings_page.bbox("all"))

        # self.interface

        ...

        self.about_page = ctk.CTkFrame(self.page_holder, fg_color=DefaultTheme.background2)

        ...

        self.success_button = ctk.CTkButton(self, text="Применить", command=self.submit)
        self.success_button.pack(side=ctk.BOTTOM, anchor="e", padx=10, pady=10)

        ...

        self.open_main()
        # self.iconbitmap("../resources/logo2.ico")
        # self.protocol('WM_DELETE_WINDOW', self.iconify)

    def submit(self):
        print("silent_boot:", self.settings_page.silent_boot_om.get_value())
        print("fast_boot:", self.settings_page.fast_boot_om.get_value())
        print("brightness_update_notifications:", self.settings_page.brightness_changes_om.get_value())
        ctk.set_appearance_mode(self.settings_page.theme_mode_om.get_value())

    def unselect_all(self):
        # self.page_holder.pack_forget()
        # self.page_holder.pack(fill=ctk.BOTH, padx=10, pady=10)
        self.main_btn.configure(state="normal", fg_color=("#b5b5b5", "#424242"))
        self.main_page.pack_forget()
        self.calibration_btn.configure(state="normal", fg_color=("#b5b5b5", "#424242"))
        self.calibration_page.pack_forget()
        self.settings_btn.configure(state="normal", fg_color=("#b5b5b5", "#424242"))
        # self.settings_page_scroll.pack_forget()
        self.settings_page.pack_forget()
        self.about_btn.configure(state="normal", fg_color=("#b5b5b5", "#424242"))
        self.about_page.pack_forget()

    def open_main(self):
        self.unselect_all()
        self.main_page.pack(fill=ctk.BOTH, padx=5, pady=5)
        self.title("Waba - Главная")
        self.main_btn.configure(state="disabled", fg_color="#1f6aa5")

    def open_calibration(self):
        self.unselect_all()
        self.calibration_page.pack(fill=ctk.BOTH, padx=5, pady=5)
        self.title("Waba - Калибровка")
        self.calibration_btn.configure(state="disabled", fg_color="#1f6aa5")

    def open_settings(self):
        self.unselect_all()
        # self.page_holder.pack_forget()
        # self.page_holder.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        # self.settings_page_scroll.pack(fill=ctk.Y, side=ctk.RIGHT, padx=(0, 5), pady=5)
        self.settings_page.pack(fill=ctk.BOTH, padx=(5, 0), pady=5, expand=True)
        self.title("Waba - Настройки")
        self.settings_btn.configure(state="disabled", fg_color="#1f6aa5")

    def open_about(self):
        self.unselect_all()
        self.about_page.pack(fill=ctk.BOTH, padx=5, pady=5)
        self.title("Waba - О приложении")
        self.about_btn.configure(state="disabled", fg_color="#1f6aa5")

    def create_toplevel(self):
        window = ctk.CTkToplevel(self)
        window.geometry("400x200")

        # create label on CTkToplevel window
        label = ctk.CTkLabel(window, text="CTkToplevel window")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)


if __name__ == "__main__":
    import os

    app = App(None, None, None, None)
    app.mainloop()
