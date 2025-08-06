#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interpretador de Laudos Laboratoriais - Interface Desktop
Aplicação PySide6 para análise de laudos laboratoriais
"""

import sys
import os
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QTextEdit, QComboBox,
    QSpinBox, QProgressBar, QScrollArea, QFrame, QGridLayout,
    QMessageBox, QSplitter, QGroupBox, QTabWidget
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QFont, QPixmap, QIcon, QPalette, QColor


class AnalysisWorker(QThread):
    """Worker thread para análise de PDF sem bloquear a UI"""
    
    finished = Signal(dict)
    error = Signal(str)
    progress = Signal(int)
    
    def __init__(self, pdf_path: str, gender: str, age: int):
        super().__init__()
        self.pdf_path = pdf_path
        self.gender = gender
        self.age = age
        self.api_url = "http://localhost:8000/interpret"
    
    def run(self):
        try:
            self.progress.emit(20)
            
            # Preparar arquivo para upload
            with open(self.pdf_path, 'rb') as file:
                files = {'file': file}
                data = {
                    'genero': self.gender.lower(),
                    'idade': self.age
                }
                
                self.progress.emit(50)
                
                # Fazer requisição para API
                response = requests.post(
                    self.api_url,
                    files=files,
                    data=data,
                    timeout=30
                )
                
                self.progress.emit(80)
                
                if response.status_code == 200:
                    result = response.json()
                    self.progress.emit(100)
                    self.finished.emit(result)
                else:
                    self.error.emit(f"Erro na API: {response.status_code} - {response.text}")
                    
        except requests.exceptions.ConnectionError:
            self.error.emit("Erro: Não foi possível conectar ao servidor. Verifique se o backend está rodando.")
        except requests.exceptions.Timeout:
            self.error.emit("Erro: Timeout na requisição. Tente novamente.")
        except Exception as e:
            self.error.emit(f"Erro inesperado: {str(e)}")


class ResultCard(QFrame):
    """Card para exibir resultado de um analito"""
    
    def __init__(self, finding: Dict[str, Any]):
        super().__init__()
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: white;
                margin: 5px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Nome do analito
        name_label = QLabel(finding.get('analito', 'N/A').title())
        name_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(name_label)
        
        # Valor e resultado
        valor = finding.get('valor', 'N/A')
        resultado = finding.get('resultado', 'N/A')
        value_label = QLabel(f"Valor: {valor} - {resultado.upper()}")
        
        # Cor baseada no resultado
        if resultado.lower() == 'baixo':
            value_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        elif resultado.lower() == 'alto':
            value_label.setStyleSheet("color: #e67e22; font-weight: bold;")
        else:
            value_label.setStyleSheet("color: #27ae60; font-weight: bold;")
            
        layout.addWidget(value_label)
        
        # Especialidade recomendada
        if finding.get('especialidade'):
            spec_label = QLabel(f"Especialidade: {finding['especialidade']}")
            spec_label.setStyleSheet("color: #3498db; font-style: italic;")
            layout.addWidget(spec_label)
        
        # Descrição do achado
        if finding.get('descricao_achado'):
            desc_label = QLabel(f"Achado: {finding['descricao_achado']}")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        self.setLayout(layout)


class MainWindow(QMainWindow):
    """Janela principal da aplicação"""
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.analysis_worker = None
        
        self.setWindowTitle("🩺 Interpretador de Laudos Laboratoriais")
        self.setGeometry(100, 100, 1200, 800)
        
        # Configurar estilo
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar interface do usuário"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter para dividir a tela
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Painel esquerdo - Upload e configurações
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Painel direito - Resultados
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Configurar proporções do splitter
        splitter.setSizes([400, 800])
        
    def create_left_panel(self) -> QWidget:
        """Criar painel esquerdo com controles"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Título
        title = QLabel("📋 Upload de Laudo")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Grupo de upload
        upload_group = QGroupBox("Arquivo PDF")
        upload_layout = QVBoxLayout(upload_group)
        
        self.file_label = QLabel("Nenhum arquivo selecionado")
        self.file_label.setWordWrap(True)
        self.file_label.setStyleSheet("padding: 10px; border: 2px dashed #ccc; border-radius: 5px;")
        upload_layout.addWidget(self.file_label)
        
        self.upload_btn = QPushButton("📁 Selecionar PDF")
        self.upload_btn.clicked.connect(self.select_file)
        upload_layout.addWidget(self.upload_btn)
        
        layout.addWidget(upload_group)
        
        # Grupo de dados do paciente
        patient_group = QGroupBox("Dados do Paciente")
        patient_layout = QGridLayout(patient_group)
        
        # Gênero
        patient_layout.addWidget(QLabel("Gênero:"), 0, 0)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["feminino", "masculino"])
        patient_layout.addWidget(self.gender_combo, 0, 1)
        
        # Idade
        patient_layout.addWidget(QLabel("Idade:"), 1, 0)
        self.age_spin = QSpinBox()
        self.age_spin.setRange(0, 120)
        self.age_spin.setValue(30)
        self.age_spin.setSuffix(" anos")
        patient_layout.addWidget(self.age_spin, 1, 1)
        
        layout.addWidget(patient_group)
        
        # Botão de análise
        self.analyze_btn = QPushButton("🔬 Analisar Laudo")
        self.analyze_btn.clicked.connect(self.analyze_pdf)
        self.analyze_btn.setEnabled(False)
        layout.addWidget(self.analyze_btn)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status
        self.status_label = QLabel("Pronto para análise")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #6c757d; font-style: italic;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        return panel
        
    def create_right_panel(self) -> QWidget:
        """Criar painel direito com resultados"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Título
        title = QLabel("📊 Resultados da Análise")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Tabs para organizar resultados
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Tab 1: Achados laboratoriais
        self.findings_scroll = QScrollArea()
        self.findings_scroll.setWidgetResizable(True)
        self.findings_widget = QWidget()
        self.findings_layout = QVBoxLayout(self.findings_widget)
        self.findings_scroll.setWidget(self.findings_widget)
        self.tabs.addTab(self.findings_scroll, "🧪 Achados")
        
        # Tab 2: Briefing para o paciente
        self.briefing_text = QTextEdit()
        self.briefing_text.setReadOnly(True)
        self.briefing_text.setPlaceholderText("O briefing personalizado aparecerá aqui após a análise...")
        self.tabs.addTab(self.briefing_text, "📝 Briefing")
        
        # Tab 3: Especialidades recomendadas
        self.specialties_text = QTextEdit()
        self.specialties_text.setReadOnly(True)
        self.specialties_text.setPlaceholderText("Especialidades recomendadas aparecerão aqui...")
        self.tabs.addTab(self.specialties_text, "👨‍⚕️ Especialidades")
        
        return panel
        
    def select_file(self):
        """Selecionar arquivo PDF"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Laudo PDF",
            "",
            "Arquivos PDF (*.pdf)"
        )
        
        if file_path:
            self.current_file = file_path
            filename = Path(file_path).name
            self.file_label.setText(f"📄 {filename}")
            self.file_label.setStyleSheet("padding: 10px; border: 2px solid #28a745; border-radius: 5px; background-color: #d4edda;")
            self.analyze_btn.setEnabled(True)
            self.status_label.setText("Arquivo carregado. Pronto para análise.")
            
    def analyze_pdf(self):
        """Iniciar análise do PDF"""
        if not self.current_file:
            QMessageBox.warning(self, "Aviso", "Selecione um arquivo PDF primeiro.")
            return
            
        # Preparar UI para análise
        self.analyze_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Analisando laudo...")
        
        # Obter dados do paciente
        gender = "feminino" if self.gender_combo.currentText() == "Feminino" else "masculino"
        age = self.age_spin.value()
        
        # Iniciar worker thread
        self.analysis_worker = AnalysisWorker(self.current_file, gender, age)
        self.analysis_worker.finished.connect(self.on_analysis_finished)
        self.analysis_worker.error.connect(self.on_analysis_error)
        self.analysis_worker.progress.connect(self.progress_bar.setValue)
        self.analysis_worker.start()
        
    def on_analysis_finished(self, result: Dict[str, Any]):
        """Callback quando análise termina com sucesso"""
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
        self.status_label.setText("Análise concluída com sucesso!")
        
        # Limpar resultados anteriores
        self.clear_results()
        
        # Exibir achados laboratoriais
        findings = result.get('lab_findings', [])
        if findings:
            for finding in findings:
                card = ResultCard(finding)
                self.findings_layout.addWidget(card)
        else:
            no_findings = QLabel("Nenhum achado laboratorial encontrado.")
            no_findings.setAlignment(Qt.AlignCenter)
            no_findings.setStyleSheet("color: #6c757d; font-style: italic; padding: 20px;")
            self.findings_layout.addWidget(no_findings)
            
        self.findings_layout.addStretch()
        
        # Exibir briefing
        briefing = result.get('patient_briefing', 'Briefing não disponível.')
        self.briefing_text.setHtml(f"<div style='font-family: Arial; line-height: 1.6;'>{briefing.replace(chr(10), '<br>')}</div>")
        
        # Exibir especialidades
        specialties = result.get('recommended_specialties', [])
        if specialties:
            specialties_html = "<h3>🏥 Especialidades Recomendadas:</h3><ul>"
            for specialty in specialties:
                specialties_html += f"<li><b>{specialty}</b></li>"
            specialties_html += "</ul>"
            self.specialties_text.setHtml(specialties_html)
        else:
            self.specialties_text.setPlainText("Nenhuma especialidade específica recomendada.")
            
        # Focar na primeira tab
        self.tabs.setCurrentIndex(0)
        
    def on_analysis_error(self, error_message: str):
        """Callback quando análise falha"""
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
        self.status_label.setText("Erro na análise.")
        
        QMessageBox.critical(self, "Erro na Análise", error_message)
        
    def clear_results(self):
        """Limpar resultados anteriores"""
        # Limpar achados
        while self.findings_layout.count():
            child = self.findings_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # Limpar textos
        self.briefing_text.clear()
        self.specialties_text.clear()


def main():
    """Função principal"""
    app = QApplication(sys.argv)
    
    # Configurar ícone da aplicação (se disponível)
    app.setApplicationName("Interpretador de Laudos Laboratoriais")
    app.setApplicationVersion("1.0.0")
    
    # Criar e mostrar janela principal
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()