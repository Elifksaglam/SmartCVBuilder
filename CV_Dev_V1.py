import sys
import base64
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit, QLabel, QFileDialog,
    QMessageBox, QSplitter, QInputDialog, QScrollArea, QGroupBox,
    QComboBox, QTableWidget, QTableWidgetItem, QDialog, QDialogButtonBox
)
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtGui import QTextDocument, QPageSize, QPageLayout
from PyQt6.QtCore import Qt, QMarginsF


class SmartCVBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart CV Builder - Multi Language")
        self.resize(1300, 900)

        # Data stores
        self.photo_path = ""
        self.languages = [("Turkish", 5), ("German", 5), ("English", 4), ("French", 2), ("Spanish", 1)]
        self.skills = [("Python", 3), ("Java", 3), ("C/C++", 2), ("Ruby", 1)]
        self.educations = [
            ("example Degree", "Example University", "08.2014 - 07.2015")]
        self.experiences = [
            ("example", "example", "08.2014 - 07.2015", "Description")
        ]
        self.projects = [
            ("...Builder", "Desktop application with PyQt6", "2026", 4)
        ]

        # Language selection
        self.current_lang = "English"
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "German", "Turkish", "French"])

        # Translation dictionary
        self.translations = {
            "English": {
                # UI text
                "cv_language": "CV Language:",
                "personal_info": "Personal Information:",
                "select_photo": "Select Profil Photo",
                "full_name": "Full Name:",
                "email": "Email:",
                "location_info": "Location & Info:",
                "add_sections": "Add Sections",
                "add_language": "+ Add Language",
                "edit_language": "✎ Edit Languages",
                "add_skill": "+ Add Skill",
                "edit_skill": "✎ Edit Skills",
                "add_education": "+ Add Education",
                "edit_education": "✎ Edit Education",
                "add_experience": "+ Add Professional Experience",
                "edit_experiece": "✎ Edit Experiences",
                "add_project": "+ Add Project",
                "edit_project": "✎ Edit Projects",
                "save_pdf": "Save as A4 PDF",
                # CV section headers
                "languages": "Languages",
                "skills": "Skills",
                "education": "Education",
                "experience": "Professional Experience",
                "projects": "Projects",
                "level": "Level",
                "contribution": "Contribution",
                # Proficiency levels
                "basic": "Basic",
                "elementary": "Elementary",
                "intermediate": "Intermediate",
                "advanced": "Advanced",
                "expert": "Expert",
                "language_name": "Language",
                "skill_name": "Skill",
                "title": "Title",
                "institution": "Institution",
                "dates": "Dates",
                "job_title": "Job Title",
                "company": "Company",
                "description": "Description",
                "project_name": "Project Name",
                "year": "Year"

            },
            "German": {
                # UI text
                "cv_language": "CV-Sprache",
                "personal_info": "Persönliche Informationen",
                "select_photo": "Profilfoto auswählen",
                "full_name": "Vollständiger Name:",
                "email": "E-Mail:",
                "location_info": "Standort & Info:",
                "add_sections": "Abschnitte hinzufügen",
                "add_language": "+ Sprache hinzufügen",
                "edit_language": "✎ Sprachen bearbeiten",
                "add_skill": "+ Fähigkeit hinzufügen",
                "edit_skill": "✎ Fähigkeiten bearbeiten",
                "add_education": "+ Ausbildung hinzufügen",
                "edit_education": "✎ Ausbildung bearbeiten",
                "add_experience": "+ Berufserfahrung hinzufügen",
                "edit_experience": "✎ Erfahrungen bearbeiten",
                "add_project": "+ Projekt hinzufügen",
                "edit_project": "✎ Projekte bearbeiten",
                "save_pdf": "Als PDF speichern",
                "languages": "Sprachen",
                "skills": "Fähigkeiten",
                "education": "Bildung",
                "experience": "Berufserfahrung",
                "projects": "Projekte",
                "level": "Niveau",
                "contribution": "Beitrag",
                "basic": "Grundkenntnisse",
                "elementary": "Elementare Kenntnisse",
                "intermediate": "Fortgeschritten",
                "advanced": "Erweitert",
                "expert": "Experte",
                "language_name": "Sprache",
                "skill_name": "Fähigkeit",
                "title": "Titel",
                "institution": "Einrichtung",
                "dates": "Daten",
                "job_title": "Jobtitel",
                "company": "Firma",
                "description": "Beschreibung",
                "project_name": "Projektname",
                "year": "Jahr"

            },
            "Turkish": {
                # UI text
                "cv_language": "CV Dili:",
                "personal_info": "Kişisel Bilgiler",
                "select_photo": "Profil Fotoğrafı Seç",
                "full_name": "Tam Ad:",
                "email": "E-posta:",
                "location_info": "Konum & Bilgi:",
                "add_sections": "Bölüm Ekle",
                "add_language": "+ Dil Ekle",
                "edit_language": "✎ Dilleri Düzenle",
                "add_skill": "+ Yetenek Ekle",
                "edit_skill": "✎ Yetenekleri Düzenle",
                "add_education": "+ Eğitim Ekle",
                "edit_education": "✎ Eğitimi Düzenle",
                "add_experience": "+ Profesyonel Deneyim Ekle",
                "edit_experience": "✎ Deneyimleri Düzenle",
                "add_project": "+ Proje Ekle",
                "edit_project": "✎ Projeleri Düzenle",
                "save_pdf": "A4 PDF Olarak Kaydet",
                "languages": "Diller",
                "skills": "Yetenekler",
                "education": "Eğitim",
                "experience": "Profesyonel Deneyim",
                "projects": "Projeler",
                "level": "Seviye",
                "contribution": "Katkı",
                "basic": "Temel",
                "elementary": "Başlangıç",
                "intermediate": "Orta",
                "advanced": "İleri",
                "expert": "Uzman",
                "language_name": "Dil",
                "skill_name": "Yetenek",
                "title": "Başlık",
                "institution": "Kurum",
                "dates": "Tarihler",
                "job_title": "İş Unvanı",
                "company": "Şirket",
                "description": "Açıklama",
                "project_name": "Proje Adı",
                "year": "Yıl"
            },
            "French": {
                # UI texts
                "cv_language": "Langue du CV :",
                "personal_info": "Informations personnelles",
                "select_photo": "Sélectionner une photo de profil",
                "full_name": "Nom complet :",
                "email": "E-mail :",
                "location_info": "Lieu et informations :",
                "add_sections": "Ajouter des sections",
                "add_language": "+ Ajouter une langue",
                "edit_language": "✎ Modifier les langues",
                "add_skill": "+ Ajouter une compétence",
                "edit_skill": "✎ Modifier les compétences",
                "add_education": "+ Ajouter une formation",
                "edit_education": "✎ Modifier la formation",
                "add_experience": "+ Ajouter une expérience professionnelle",
                "edit_experience": "✎ Modifier les expériences",
                "add_project": "+ Ajouter un projet",
                "edit_project": "✎ Modifier les projets",
                "save_pdf": "Enregistrer au format A4 PDF",
                "languages": "Langues",
                "skills": "Compétences",
                "education": "Formation",
                "experience": "Expérience professionnelle",
                "projects": "Projets",
                "level": "Niveau",
                "contribution": "Contribution",
                "basic": "Débutant",
                "elementary": "Élémentaire",
                "intermediate": "Intermédiaire",
                "advanced": "Avancé",
                "expert": "Expert",
                "language_name": "Langue",
                "skill_name": "Compétence",
                "title": "Titre",
                "institution": "Établissement",
                "dates": "Dates",
                "job_title": "Poste",
                "company": "Entreprise",
                "description": "Description",
                "project_name": "Nom du projet",
                "year": "Année"
            }
        }

        # Status Bar
        self.statusBar().showMessage(self.tr("Ready"), 2000)

        # Main splitter
        central_widget = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(central_widget)

        # Left panel - controls
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)

        # Language selector row
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel()
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_combo)
        control_layout.addLayout(lang_layout)

        # personal info group
        self.personal_group = QGroupBox()
        personal_layout = QVBoxLayout()

        self.btn_photo = QPushButton()
        self.btn_photo.clicked.connect(self.select_photo)

        self.name_label = QLabel()
        self.name_field = QLineEdit("Max Muster")

        self.email_label = QLabel()
        self.email_field = QLineEdit("max.muster@gmail.com")

        self.location_label = QLabel()
        self.location_field = QTextEdit("Bursa — TURKIYE")
        self.location_field.setMaximumHeight(60)

        personal_layout.addWidget(self.btn_photo)
        personal_layout.addWidget(self.name_label)
        personal_layout.addWidget(self.name_field)
        personal_layout.addWidget(self.email_label)
        personal_layout.addWidget(self.email_field)
        personal_layout.addWidget(self.location_label)
        personal_layout.addWidget(self.location_field)

        self.personal_group.setLayout(personal_layout)
        control_layout.addWidget(self.personal_group)

        # Dynamic Adders Group
        self.dynamic_group = QGroupBox()
        dynamic_layout = QVBoxLayout()

        self.btn_add_lang = QPushButton()
        self.btn_add_lang.clicked.connect(self.add_language)
        self.btn_edit_lang = QPushButton()
        self.btn_edit_lang.clicked.connect(self.edit_languages)

        self.btn_add_skill = QPushButton()
        self.btn_add_skill.clicked.connect(self.add_skill)
        self.btn_edit_skill = QPushButton()
        self.btn_edit_skill.clicked.connect(self.edit_skills)

        self.btn_add_edu = QPushButton()
        self.btn_add_edu.clicked.connect(self.add_education)
        self.btn_edit_edu = QPushButton()
        self.btn_edit_edu.clicked.connect(self.edit_education)

        self.btn_add_exp = QPushButton()
        self.btn_add_exp.clicked.connect(self.add_experience)
        self.btn_edit_exp = QPushButton()
        self.btn_edit_exp.clicked.connect(self.edit_experiences)

        self.btn_add_project = QPushButton()
        self.btn_add_project.clicked.connect(self.add_project)
        self.btn_edit_project = QPushButton()
        self.btn_edit_project.clicked.connect(self.edit_projects)

        dynamic_layout.addWidget(self.btn_add_lang)
        dynamic_layout.addWidget(self.btn_edit_lang)
        dynamic_layout.addWidget(self.btn_add_skill)
        dynamic_layout.addWidget(self.btn_edit_skill)
        dynamic_layout.addWidget(self.btn_add_edu)
        dynamic_layout.addWidget(self.btn_edit_edu)
        dynamic_layout.addWidget(self.btn_add_exp)
        dynamic_layout.addWidget(self.btn_edit_exp)
        dynamic_layout.addWidget(self.btn_add_project)
        dynamic_layout.addWidget(self.btn_edit_project)

        self.dynamic_group.setLayout(dynamic_layout)
        control_layout.addWidget(self.dynamic_group)

        # export button
        self.export_btn = QPushButton()
        self.export_btn.setStyleSheet(
            "background-color: #ef4444; color: white; font-weight: bold; padding: 15px; font-size: 14px;"
        )
        self.export_btn.clicked.connect(self.export_to_pdf)
        control_layout.addWidget(self.export_btn)

        control_layout.addStretch()
        scroll_area.setWidget(control_panel)

        # right panel preview
        self.preview_panel = QTextEdit()
        self.preview_panel.setReadOnly(True)
        self.preview_panel.setStyleSheet("background-color: #525659; padding: 20px;")

        central_widget.addWidget(scroll_area)
        central_widget.addWidget(self.preview_panel)
        central_widget.setSizes([350, 950])

        # connect live updates
        self.name_field.textChanged.connect(self.update_preview)
        self.email_field.textChanged.connect(self.update_preview)
        self.location_field.textChanged.connect(self.update_preview)

        # Connect language change
        self.lang_combo.currentTextChanged.connect(self.on_language_changed)

        # Initial UI translation
        self.update_ui_language()
        self.update_preview()

        # helper method

    def tr(self, key):
        return self.translations[self.current_lang].get(key, key)

    def update_ui_language(self):
        self.lang_label.setText(self.tr("cv_language"))
        self.personal_group.setTitle(self.tr("personal_info"))
        self.btn_photo.setText(self.tr("select_photo"))
        self.name_label.setText(self.tr("full_name"))
        self.email_label.setText(self.tr("email"))
        self.location_label.setText(self.tr("location_info"))
        self.dynamic_group.setTitle(self.tr("add_sections"))
        self.btn_add_lang.setText(self.tr("add_language"))
        self.btn_edit_lang.setText(self.tr("edit_language"))
        self.btn_add_skill.setText(self.tr("add_skill"))
        self.btn_edit_skill.setText(self.tr("edit_skill"))
        self.btn_add_edu.setText(self.tr("add_education"))
        self.btn_edit_edu.setText(self.tr("edit_education"))
        self.btn_add_exp.setText(self.tr("add_experience"))
        self.btn_edit_exp.setText(self.tr("edit_experience"))
        self.btn_add_project.setText(self.tr("add_project"))
        self.btn_edit_project.setText(self.tr("edit_project"))
        self.export_btn.setText(self.tr("save_pdf"))

    def on_language_changed(self, lang):
        self.current_lang = lang
        self.update_ui_language()
        self.update_preview()

        # helper 1-5 levels

    def level_to_text(self, level):
        level_map = {1: "basic", 2: "elementary", 3: "intermediate", 4: "advanced", 5: "expert"}
        return self.tr(level_map.get(level, "intermediate"))

        # image handling

    def image_to_base64(self):
        if not self.photo_path:
            return ""
        try:
            with open(self.photo_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode("utf-8")
                return f'<img src="data:image/jpeg;base64,{encoded}" width="160" style="margin-bottom: 20px; border-radius: 50%;">'

        except Exception:
            return ""

    def select_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.tr("select_photo"), "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.photo_path = file_path
            self.update_preview()
            self.statusBar().showMessage(self.tr("Photo updated"), 2000)

    # generic edit dialog helper
    def show_edit_dialog(self, title, headers, data, edit_callback=None, add_callback=None):
        """Generic dialog with a table for editing list data."""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.resize(500, 400)
        layout = QVBoxLayout(dialog)

        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        # allow direct editing inn cellls
        table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked |
                              QTableWidget.EditTrigger.EditKeyPressed)
        layout.addWidget(table)

        # Populate Table
        for row, item in enumerate(data):
            table.insertRow(row)
            for col, value in enumerate(item):
                table.setItem(row, col, QTableWidgetItem(str(value)))

        # buttons
        btn_layout = QHBoxLayout()
        btn_save = QPushButton(self.tr("Save"))
        btn_cancel = QPushButton(self.tr("Cancel"))
        btn_edit = QPushButton(self.tr("Edit Selected"))
        btn_delete = QPushButton(self.tr("Delete"))
        if add_callback:
            btn_add = QPushButton(self.tr("Add New"))

        def edit_selected():
            current = table.currentRow()
            if current >= 0:
                old_item = data[current]
                if edit_callback:
                    edit_callback(current, old_item, table, data, dialog)

        def delete_selected():
            current = table.currentRow()
            if current >= 0:
                reply = QMessageBox.question(dialog, self.tr("Confirm"),
                                             self.tr("Do you want to delete this item?"),
                                             QMessageBox.StandardButton.Yes |
                                             QMessageBox.StandardButton.No)

                if reply == QMessageBox.StandardButton.Yes:
                    table.removeRow(current)
                    self.update_preview()
                    self.statusBar().showMessage(self.tr("Item deleted"), 2000)

        def add_new():
            if add_callback:
                new_item = add_callback(dialog)
                if new_item:
                    row = table.rowCount()
                    table.insertRow(row)
                    for col, val in enumerate(new_item):
                        table.setItem(row, col, QTableWidgetItem(str(val)))
                    self.update_preview()
                    self.statusBar().showMessage(self.tr("Item Added"), 2000)

        def save_all():
            # read all data the table and update the original list
            new_data = []
            for row in range(table.rowCount()):
                row_data = []
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    if item is not None:
                        val = item.text()
                        # try to convert numeric columns to int
                        if col == len(headers) - 1 and headers[col].lower() in ('level', 'contribution'):
                            try:
                                val = int(val)
                            except ValueError:
                                pass
                        row_data.append(val)
                    else:
                        row_data.append("")
                new_data.append(tuple(row_data))
            # replace the original data
            data.clear()
            data.extend(new_data)
            self.update_preview()
            self.statusBar().showMessage(self.tr("Changes saved"), 2000)
            dialog.accept()

        btn_edit.clicked.connect(edit_selected)
        btn_delete.clicked.connect(delete_selected)
        if add_callback:
            btn_add.clicked.connect(add_new)
            btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        btn_save.clicked.connect(save_all)
        btn_cancel.clicked.connect(dialog.reject)

        dialog.exec()

        # dynamic item adders

    def add_language(self):
        name, ok1 = QInputDialog.getText(self, self.tr("add_language"), self.tr("Enter Language Name:"))

        if ok1 and name:
            level, ok2 = QInputDialog.getInt(self, self.tr("add_language"), self.tr("Level (1-5):"), 4, 1, 5)

            if ok2:
                self.languages.append((name, level))
                self.update_preview()
                self.statusBar().showMessage(self.tr("Language added: ") + name, 2000)

    def edit_languages(self):
        def edit_callback(index, old, table, data, dialog):
            name, level = old
            new_name, ok1 = QInputDialog.getText(dialog, self.tr("Edit Language"), self.tr("Language Name: "),
                                                 text=name)
            if ok1 and new_name:
                new_level, ok2 = QInputDialog.getInt(dialog, self.tr("Edit level"), self.tr("Level (1-5):"), level, 1,
                                                     5)
                if ok2:
                    data[index] = (new_name, new_level)
                    table.setItem(index, 0, QTableWidgetItem(new_name))
                    table.setItem(index, 1, QTableWidgetItem(str(new_level)))
                    self.update_preview()
                    self.statusBar().showMessage(self.tr("Language updated"), 2000)

        def add_callback(dialog):
            name, ok1 = QInputDialog.getText(dialog, self.tr("add_language"), self.tr("Enter Language Name:"))
            if ok1 and name:
                level, ok2 = QInputDialog.getInt(dialog, self.tr("add_language"), self.tr("Level (1-5):"), 4, 1, 5)
                if ok2:
                    return (name, level)
            return None

        self.show_edit_dialog(self.tr("Edit Languages"), [self.tr("language_name"), self.tr("level")],
                              self.languages, edit_callback, add_callback)

    def add_skill(self):
        name, ok1 = QInputDialog.getText(self, self.tr("add_skill"), self.tr("Enter Skill Name:"))
        if ok1 and name:
            level, ok2 = QInputDialog.getInt(self, self.tr("add_skill"), self.tr("Level (1-5):"), 4, 1, 5)
            if ok2:
                self.skills.append((name, level))
                self.update_preview()
                self.statusBar().showMessage(self.tr("Skill added:") + name, 2000)

    def edit_skills(self):
        def edit_callback(index, old, table, data, dialog):
            name, level = old
            new_name, ok1 = QInputDialog.getText(dialog, self.tr("Edit Skill"), self.tr("Skill name:"), text=name)
            if ok1 and new_name:
                new_level, ok2 = QInputDialog.getInt(dialog, self.tr("Edit Level"), self.tr("Level (1-5):"), level, 1,
                                                     5)
                if ok2:
                    data[index] = (new_name, new_level)
                    table.setItem(index, 0, QTableWidgetItem(new_name))
                    table.setItem(index, 1, QTableWidgetItem(str(new_level)))
                    self.update_preview()
                    self.statusBar().showMessage(self.tr("Skill updated"), 2000)

        def add_callback(dialog):
            name, ok1 = QInputDialog.getText(dialog, self.tr("add_skill"), self.tr("Enter Skill Name:"))
            if ok1 and name:
                level, ok2 = QInputDialog.getInt(dialog, self.tr("add_skill"), self.tr("Level (1-5):"), 4, 1, 5)
                if ok2:
                    return (name, level)
            return None

        self.show_edit_dialog(self.tr("Edit Skills"), [self.tr("skill_name"), self.tr("level")],
                              self.skills, edit_callback, add_callback)

    def add_education(self):
        title, ok1 = QInputDialog.getText(self, self.tr("add_education"), self.tr("Title (e.g., Bachelor in CS):"))
        if ok1 and title:
            school, ok2 = QInputDialog.getText(self, self.tr("add_education"), self.tr("Institution:"))
            if ok2:
                dates, ok3 = QInputDialog.getText(self, self.tr("add_education"),
                                                  self.tr("Dates (e.g., 2015-2019):"))
                if ok3:
                    self.educations.append((title, school, dates))
                    self.update_preview()
                    self.statusBar().showMessage(self.tr("Education added: ") + title, 2000)

    def edit_education(self):
        def edit_callback(index, old, table, data, dialog):
            title, school, dates = old
            new_title, ok1 = QInputDialog.getText(dialog, self.tr("Edit Education"), self.tr("Title:"), text=title)
            if ok1 and new_title:
                new_school, ok2 = QInputDialog.getText(dialog, self.tr("Edit Education"), self.tr("Institution:"),
                                                      text=school)
                if ok2:
                    new_dates, ok3 = QInputDialog.getText(dialog, self.tr("Edit Education"), self.tr("Dates:"),
                                                          text=dates)
                    if ok3:
                        data[index] = (new_title, new_school, new_dates)
                        table.setItem(index, 0, QTableWidgetItem(new_title))
                        table.setItem(index, 1, QTableWidgetItem(new_school))
                        table.setItem(index, 2, QTableWidgetItem(new_dates))
                        self.update_preview()
                        self.statusBar().showMessage(self.tr("Education updated"), 2000)

        def add_callback(dialog):
            title, ok1 = QInputDialog.getText(dialog, self.tr("add_education"), self.tr("Title:"))
            if ok1 and title:
                school, ok2 = QInputDialog.getText(dialog, self.tr("add_education"), self.tr("Institution:"))
                if ok2:
                    dates, ok3 = QInputDialog.getText(dialog, self.tr("add_education"), self.tr("Dates:"))
                    if ok3:
                        return (title, school, dates)
            return None

        self.show_edit_dialog(self.tr("Edit Education"), [self.tr("title"), self.tr("institution"), self.tr("dates")],
                              self.educations, edit_callback, add_callback)

    def add_experience(self):
        title, ok1 = QInputDialog.getText(self, self.tr("add_experience"), self.tr("Job Title/ Rolle:"))

        if ok1 and title:
            company, ok2 = QInputDialog.getText(self, self.tr("add_experience"), self.tr("Company Name:"))

            if ok2:
                dates, ok3 = QInputDialog.getText(self, self.tr("add_experience"), self.tr("Dates:"))

                if ok3:
                    description, ok4 = QInputDialog.getText(self, self.tr("add_experience"), self.tr("Description:"))

                    if ok4:
                        self.experiences.append((title, company, dates, description))
                        self.update_preview()
                        self.statusBar().showMessage(self.tr("Experience added: ") + title, 2000)

    def edit_experiences(self):
        def edit_callback(index, old, table, data, dialog):
            title, company, dates, desc = old
            new_title, ok1 = QInputDialog.getText(dialog, self.tr("Edit Experience"), self.tr("Job Title:"), text=title)
            if ok1 and new_title:
                new_company, ok2 = QInputDialog.getText(dialog, self.tr("Edit Experience"), self.tr("Company:"),
                                                      text=company)
                if ok2:
                    new_dates, ok3 = QInputDialog.getText(dialog, self.tr("Edit Experience"), self.tr("Dates:"),
                                                          text=dates)
                    if ok3:
                        new_desc, ok4 = QInputDialog.getText(dialog, self.tr("Edit Experience"),
                                                             self.tr("Description:"), text=desc)
                        if ok4:
                            data[index] = (new_title, new_company, new_dates, new_desc)
                            for col, val in enumerate(data[index]):
                                table.setItem(index, col, QTableWidgetItem(str(val)))
                            self.update_preview()
                            self.statusBar().showMessage(self.tr("Experience updated"), 2000)

        def add_callback(dialog):
            title, ok1 = QInputDialog.getText(dialog, self.tr("add_experience"), self.tr("Job Title / Role:"))
            if ok1 and title:
                company, ok2 = QInputDialog.getText(dialog, self.tr("add_experience"), self.tr("Company Name:"))
                if ok2:
                    dates, ok3 = QInputDialog.getText(dialog, self.tr("add_experience"), self.tr("Dates:"))
                    if ok3:
                        desc, ok4 = QInputDialog.getText(dialog, self.tr("add_experience"), self.tr("Description"))
                        if ok4:
                            return (title, company, dates, desc)
            return None

        self.show_edit_dialog(self.tr("Edit Experiences"),
                              [self.tr("job_title"), self.tr("company"), self.tr("dates"), self.tr("description")],
                              self.experiences, edit_callback, add_callback)

    def add_project(self):
        name, ok1 = QInputDialog.getText(self, self.tr("add_project"), self.tr("Project Name:"))
        if ok1 and name:
            desc, ok2 = QInputDialog.getText(self, self.tr("add_project"), self.tr("Short description:"))
            if ok2:
                year, ok3 = QInputDialog.getText(self, self.tr("add_project"), self.tr("Year (or period):"))
                if ok3:
                    level, ok4 = QInputDialog.getInt(self, self.tr("add_project"), self.tr("Contribution (1-5):"),
                                                     4, 1, 5)
                    if ok4:
                        self.projects.append((name, desc, year, level))
                        self.update_preview()
                        self.statusBar().showMessage(self.tr("Project added: ") + name, 2000)

    def edit_projects(self):
        def edit_callback(index, old, table, data, dialog):
            name, desc, year, level = old
            new_name, ok1 = QInputDialog.getText(dialog, self.tr("Edit Project"), self.tr("Project Name:"), text=name)
            if ok1 and new_name:
                new_desc, ok2 = QInputDialog.getText(dialog, self.tr("Edit Project"), self.tr("Description:"),
                                                     text=desc)
                if ok2:
                    new_year, ok3 = QInputDialog.getText(dialog, self.tr("Edit Project"), self.tr("Year:"), text=year)
                    if ok3:
                        new_level, ok4 = QInputDialog.getInt(dialog, self.tr("Edit Project"),
                                                             self.tr("Contribution (1-5):"), level, 1, 5)
                        if ok4:
                            data[index] = (new_name, new_desc, new_year, new_level)
                            for col, val in enumerate(data[index]):
                                table.setItem(index, col, QTableWidgetItem(str(val)))
                            self.update_preview()
                            self.statusBar().showMessage(self.tr("Project updated"), 2000)

        def add_callback(dialog):
            name, ok1 = QInputDialog.getText(dialog, self.tr("add_project"), self.tr("Project Name:"))
            if ok1 and name:
                desc, ok2 = QInputDialog.getText(dialog, self.tr("add_project"), self.tr("Short description:"))
                if ok2:
                    year, ok3 = QInputDialog.getText(dialog, self.tr("add_project"), self.tr("Year:"))
                    if ok3:
                        level, ok4 = QInputDialog.getInt(dialog, self.tr("add_project"), self.tr("Contribution (1-5):"),
                                                         4, 1, 5)
                        if ok4:
                            return (name, desc, year, level)
            return None

        self.show_edit_dialog(self.tr("Edit Projects"),
                              [self.tr("project_name"), self.tr("description"), self.tr("year"),
                               self.tr("contribution")],
                              self.projects, edit_callback, add_callback)

# html generation with translation
    def generate_html_cv(self):
        name = self.name_field.text()
        email = self.email_field.text()
        location = self.location_field.toPlainText().replace('\n', '<br>')
        photo_html = self.image_to_base64()

        # Languages
        lang_html = ""
        for lang, level in self.languages:
            lang_html += f"""
                <div style="font-size: 11pt; font-weight: bold; margin-top: 5px;">{lang}</div>
                <div style="color: #163052; font-size: 10pt;">{self.tr('level')}: {self.level_to_text(level)}</div>
            """

        # Skills
        skill_html = ""
        for skill, level in self.skills:
            skill_html += f"""
                <div style="font-size: 11pt; font-weight: bold; margin-top: 5px;">{skill}</div>
                <div style="color: #163052; font-size: 10pt;">{self.tr('level')}: {self.level_to_text(level)}</div>
            """

        # Education
        edu_html = ""
        for title, school, dates in self.educations:
            edu_html += f"""
                <div style="margin-bottom: 15px;">
                    <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                            <td style="font-weight: bold; font-size: 12pt;">{title}</td>
                            <td align="right" style="color: #152e52; font-size: 10pt;">{dates}</td>
                        </tr>
                    </table>
                    <div style="color: #163052; font-size: 10pt; margin-top: 2px;">{school}</div>
                </div>
            """

        # Experience
        exp_html = ""
        for title, company, dates, desc in self.experiences:
            exp_html += f"""
                <div style="margin-bottom: 20px;">
                    <div style="font-weight: bold; font-size: 12pt;">{title}</div>
                    <div style="color: #163052; font-size: 10pt;">{company}</div>
                    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top: 4px;">
                        <tr>
                            <td width="20%" style="color: #424f61; font-size: 9pt;">{dates}</td>
                            <td width="80%" style="font-size: 10pt; color: #687382;">{desc}</td>
                        </tr>
                    </table>
                </div>
            """

        # Projects
        proj_html = ""
        for proj_name, desc, year, level in self.projects:
            proj_html += f"""
                <div style="margin-bottom: 15px;">
                    <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                            <td style="font-weight: bold; font-size: 12pt;">{proj_name}</td>
                            <td align="right" style="color: #424f61; font-size: 10pt;">{year}</td>
                        </tr>
                    </table>
                    <div style="color: #163052; font-size: 10pt; margin-top: 2px;">{desc}</div>
                    <div style="color: #687382; font-size: 9pt; margin-top: 4px;">{self.tr('contribution')}: {self.level_to_text(level)}</div>
                </div>
            """

        html = f"""
        <html>
        <head>
            <style>
                html, body {{
                    margin: 0;
                    padding: 0;
                }}
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    color: #163052;
                    background: white;
                }}
                .full-height-table {{
                    height: 100%;
                    width: 100%;
                    border-collapse: collapse;
                }}
                .left-column {{
                    background-color: #d3ecf5;
                    vertical-align: top;
                    padding: 30px;
                    color: #28507a;
                }}
                .right-column {{
                    background-color: white;
                    vertical-align: top;
                    padding: 30px 40px;
                }}
                h1 {{ font-size: 28pt; color: #334155; margin-top: 50px; margin-bottom: 40px; }}
                h2 {{ font-size: 14pt; color: #1e293b; border-bottom: 1px solid #cbd5e1; padding-bottom: 5px; margin-bottom: 15px; margin-top: 25px; }}
                h3 {{ font-size: 10pt; margin-bottom: 10px; margin-top: 20px; color: #21385e; }}
            </style>
        </head>
        <body>
            <table class="full-height-table" cellpadding="0" cellspacing="0">
                <tr>
                    <td class="left-column" width="30%">
                        {photo_html}
                        <div style="font-size: 10pt; margin-bottom: 30px;">
                            {email}<br><br>
                            {location}
                        </div>
                        <h3>{self.tr('languages')}</h3>
                        {lang_html}
                        <h3>{self.tr('skills')}</h3>
                        {skill_html}
                    </td>
                    <td class="right-column" width="70%">
                        <h1>{name}</h1>
                        <h2>{self.tr('education')}</h2>
                        {edu_html}
                        <h2>{self.tr('experience')}</h2>
                        {exp_html}
                        <h2>{self.tr('projects')}</h2>
                        {proj_html}
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        return html

    def update_preview(self):
        self.preview_panel.setHtml(self.generate_html_cv())

    # ========== PDF export ==========
    def export_to_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, self.tr("save_pdf"), "my_cv.pdf", "PDF Files (*.pdf)")
        if not file_path:
            return
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)

            page_layout = QPageLayout()
            page_layout.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            page_layout.setOrientation(QPageLayout.Orientation.Portrait)
            margins = QMarginsF(5, 5, 5, 5)
            page_layout.setMargins(margins)
            printer.setPageLayout(page_layout)

            doc = QTextDocument()
            doc.setHtml(self.generate_html_cv())
            doc.setPageSize(printer.pageRect(QPrinter.Unit.Point).size())
            doc.documentLayout().documentSize()  # force layout
            if doc.pageCount() > 1:
                print("Warning: Content exceeds Page 1!")
                # Optional: inform user
                self.statusBar().showMessage(self.tr("CV spans multiple pages"), 3000)

            doc.print(printer)
            QMessageBox.information(self, self.tr("save_pdf"), f"CV saved as PDF:\n{file_path}")
            self.statusBar().showMessage(self.tr("PDF saved: ") + file_path, 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate PDF: {str(e)}")
            self.statusBar().showMessage(self.tr("PDF export failed"), 3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartCVBuilder()
    window.show()
    sys.exit(app.exec())
