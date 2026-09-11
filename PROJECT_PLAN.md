# 1. Project Title

**AI Boom and the Semiconductor Value Chain: Who Captures the Growth?**

**ชื่อภาษาไทย:**  
การเติบโตของ AI และการเปลี่ยนแปลงทางการเงินในห่วงโซ่อุตสาหกรรมเซมิคอนดักเตอร์

## 2. Background

การเติบโตอย่างรวดเร็วของ Artificial Intelligence ตั้งแต่ช่วงปี 2022 ทำให้ความต้องการชิปประมวลผล ศูนย์ข้อมูล หน่วยความจำ และอุปกรณ์สำหรับผลิตเซมิคอนดักเตอร์เพิ่มขึ้น

อย่างไรก็ตาม บริษัทในอุตสาหกรรมเซมิคอนดักเตอร์มีบทบาทแตกต่างกัน เช่น บริษัทออกแบบชิป บริษัทรับจ้างผลิตชิป ผู้ผลิตหน่วยความจำ ผู้ผลิตเครื่องจักร และผู้พัฒนาซอฟต์แวร์ออกแบบวงจร

ดังนั้น การเติบโตของ AI อาจไม่ได้สร้างประโยชน์ให้ทุกบริษัทอย่างเท่าเทียมกัน Project นี้จะใช้ข้อมูลทางการเงินใน Dataset เพื่อสำรวจว่าการเติบโตของรายได้และกำไรหลังกระแส AI กระจุกตัวอยู่ในบริษัทหรือกลุ่มธุรกิจใด และสัมพันธ์กับการลงทุนด้าน R&D และ CapEx อย่างไร

## 3. Main Research Question

**หลังการเติบโตของ AI ตั้งแต่ปี 2022 บริษัทและกลุ่มธุรกิจใดในอุตสาหกรรมเซมิคอนดักเตอร์มีการเติบโตทางการเงินสูงที่สุด และการเติบโตนั้นสัมพันธ์กับ R&D และ CapEx อย่างไร?**

## 4. Supporting Questions

1. รายได้ของอุตสาหกรรมใน Dataset เปลี่ยนแปลงอย่างไรระหว่างปี 2010–2026?
2. บริษัทและ Segment ใดมีรายได้เติบโตเร็วที่สุดหลังปี 2022?
3. การเติบโตของรายได้กระจุกตัวอยู่ในบริษัทเพียงไม่กี่แห่งหรือไม่?
4. บริษัทที่รายได้เติบโตสูงมี Operating Margin สูงตามไปด้วยหรือไม่?
5. บริษัทที่ลงทุน R&D สูงเมื่อเทียบกับรายได้ มีการเติบโตสูงกว่าบริษัทอื่นหรือไม่?
6. บริษัทที่ลงทุน CapEx สูงเมื่อเทียบกับรายได้ มีผลประกอบการแตกต่างจากบริษัทที่ลงทุนต่ำอย่างไร?
7. ผลลัพธ์ระหว่าง Fabless, Foundry, IDM, Equipment และ EDA Software แตกต่างกันอย่างไร?

## 5. Project Scope

### Primary Dataset

`chip_companies_financials.csv`

### Period

ข้อมูลทั้งหมดครอบคลุมปี 2010–2026

สำหรับการวิเคราะห์เปรียบเทียบ จะแบ่งช่วงเวลาเบื้องต้นเป็น:

- **Smart automobile expansion:** 2010–2021
- **Transition Year:** 2022
- **AI expansion:** 2023–2026

การแบ่งช่วงเวลาดังกล่าวเป็นนิยามสำหรับการวิเคราะห์ใน Project นี้ ไม่ใช่นิยามมาตรฐานของอุตสาหกรรม

### Unit of Analysis

หนึ่งแถวแทนข้อมูลของบริษัทหรือหน่วยธุรกิจหนึ่งแห่งในหนึ่งปี

## 6. Main Variables

| Variable | Meaning |
| --- | --- |
| `year` | ปีของข้อมูล |
| `company_name` | ชื่อบริษัทหรือหน่วยธุรกิจ |
| `ticker` | รหัสที่ Dataset ใช้แทนบริษัท |
| `country_iso3` | ประเทศที่ Dataset กำหนดให้บริษัท |
| `segment` | กลุ่มธุรกิจในอุตสาหกรรม |
| `revenue_usd_bn` | รายได้ หน่วยพันล้าน USD |
| `operating_margin_pct` | อัตรากำไรจากการดำเนินงาน |
| `operating_income_usd_bn` | กำไรจากการดำเนินงาน หน่วยพันล้าน USD |
| `rd_spend_usd_bn` | ค่าใช้จ่ายด้าน R&D หน่วยพันล้าน USD |
| `capex_usd_bn` | รายจ่ายลงทุน หน่วยพันล้าน USD |

## 7. Derived Metrics

Project จะสร้างตัวชี้วัดเพิ่มเติม ได้แก่:

### Revenue Growth

$$
Revenue\ Growth = \frac{Revenue_t - Revenue_{t-1}}{Revenue_{t-1}} \times 100
$$

### R&D Intensity

$$
R\&D\ Intensity = \frac{R\&D\ Spend}{Revenue} \times 100
$$

### CapEx Intensity

$$
CapEx\ Intensity = \frac{CapEx}{Revenue} \times 100
$$

### Operating Income Validation

$$
Calculated\ Operating\ Income = Revenue \times \frac{Operating\ Margin}{100}
$$

### Revenue Share within Dataset

$$
Revenue\ Share = \frac{Company\ Revenue}{Total\ Revenue\ in\ Dataset} \times 100
$$

## 8. Planned Analysis

1. ตรวจสอบโครงสร้างและคุณภาพข้อมูล
2. แปลงชนิดข้อมูลและตรวจ Primary Key
3. ตรวจความสอดคล้องของตัวเลขทางการเงิน
4. วิเคราะห์แนวโน้มรายได้และกำไรตามเวลา
5. เปรียบเทียบผลประกอบการตาม Segment
6. จัดอันดับบริษัทตามรายได้ การเติบโต และกำไร
7. วิเคราะห์ R&D Intensity และ CapEx Intensity
8. เปรียบเทียบช่วงก่อนและหลังปี 2022
9. วิเคราะห์การกระจุกตัวของรายได้ภายใน Dataset
10. สร้างกราฟด้วย Matplotlib และสรุป Insight

## 9. Tools

- Python
- Pandas
- Matplotlib
- Jupyter Notebook
- Visual Studio Code
- Codex
- Git
- GitHub

Project นี้จะไม่ใช้ Machine Learning ในขอบเขตหลัก

## 10. Expected Outputs

- Cleaned financial Dataset
- Data-quality report
- Derived financial metrics
- EDA Notebooks
- Matplotlib visualizations
- Key findings and limitations
- Public GitHub Repository
- README ที่ทำหน้าที่เป็นรายงานหลักของ Project

## 11. Known Limitations

1. Dataset ไม่มีแหล่งอ้างอิงระดับแถวหรือคำอธิบายวิธีรวบรวมตัวเลข
2. ตัวเลขบางคอลัมน์มีรูปแบบคล้ายค่าที่คำนวณจากอัตราส่วนคงที่
3. ข้อมูลปี 2025–2026 อาจประกอบด้วยค่าประมาณหรือ Forecast
4. `Samsung Foundry` และ `Samsung Memory` เป็นหน่วยธุรกิจ ไม่จำเป็นต้องเทียบเท่าบริษัททั้งบริษัท
5. `ticker` บางค่าอาจไม่ใช่รหัสหลักทรัพย์ที่สมบูรณ์
6. การแบ่งช่วง AI Boom ตั้งแต่ปี 2022 เป็นสมมติฐานในการวิเคราะห์ของ Project
7. ผลรวมและส่วนแบ่งตลาดจะหมายถึงส่วนแบ่งภายใน Dataset ไม่ใช่ส่วนแบ่งของตลาดโลก
8. ผลการวิเคราะห์จะแสดงความสัมพันธ์ ไม่ใช่ข้อพิสูจน์เชิงสาเหตุ

## 12. Disclaimer

Project นี้เป็นการวิเคราะห์เชิงสำรวจจาก Dataset ที่กำหนด ผลลัพธ์จึงควรเรียกว่า “ผลตามข้อมูลใน Dataset” และไม่ควรใช้แทนงบการเงิน รายงานประจำปี หรือข้อมูลทางการของบริษัทโดยไม่ตรวจสอบเพิ่มเติม
