from fpdf import FPDF
import pandas as pd

# Verileri DataFrame olarak oluştur
data = [
    [1, 1, 1, 15, 5, 14, 6, 13, 7, 12, 8, "2025-05-01", 8],
    [1, 2, 1, 12, 8, 11, 9, 10, 10, 9, 11, "2025-05-01", 8],
 
]

columns = [
    "Id",
    "UserId",
    "ExamId",
    "TurkishTN",
    "TurkishFN",
    "MathTN",
    "MathFN",
    "ScienceTN",
    "ScienceFN",
    "SocialTN",
    "SocialFN",
    "Date",
    "Grade",
]

df = pd.DataFrame(data, columns=columns)

# PDF oluştur
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=10)

# Başlık
pdf.set_font("Arial", style="B", size=10)
pdf.cell(220, 10, ln=1, align="C")
pdf.set_font("Arial", size=5)

# Tablo başlığı
col_width = 220 / len(columns)
for col in columns:
    pdf.cell(col_width-2, 5, col+" ", border=1)
pdf.ln()

# Satır verileri
for _, row in df.iterrows():
    for item in row:
        pdf.cell(col_width-2, 5, str(item)+" ", border=1)
    pdf.ln()

# PDF'i kaydet
output_path = "student_results.pdf"
pdf.output(output_path)

output_path
