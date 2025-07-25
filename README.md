# Graphical Cake Division — חלוקה הוגנת של גרף

זהו אתר Flask להדגמה של אלגוריתם לחלוקה הוגנת של גרף לפי המאמר "Fair Division of Graphs" (Cohen et al).  
המערכת מאפשרת להזין או ליצור גרף, להגדיר ערכים לפי קודקודים לשני סוכנים, ולקבל פלט של חלוקה הוגנת של הקשתות באמצעות תיוג רציף וסימולציית סכין.

 הדגמה חיה:  
🔗 http://10.112.4.121:5050/

---

## סקירה אלגוריתמית

1. תיוג רציף של הקשתות — Contiguous Oriented Labeling  
   מיושם בקובץ algorithm.py. תיוג הקשתות מתבצע לפי ear decomposition ומחזיר רשימת קשתות מכוונות עם מספרים סידוריים.

2. חלוקה הוגנת — Cake Division  
   מיושם בקובץ app.py לפי ערכים של קודקודים. סימולציית סכין מתבצעת לפי הערך המצטבר של הקשתות, כאשר כל קשת מקבלת את סכום הערכים של שני הקודקודים שלה.

---

##  תכונות עיקריות

-  הזנת גרף ידנית
-  יצירת גרף אקראי (עם שליטה על מספר הקודקודים)
-  הזנת ערכים לפי קודקוד לשני סוכנים
-  תצוגת גרף גרפית (vis.js)
-  תצוגת פלט ישירה ללא מעבר לעמוד אחר
-   ממשק מלא בעברית

---

##  התקנה

```bash
git clone https://github.com/your-username/graphical-cake-division.git
cd graphical-cake-division

python3 -m venv venv
source venv/bin/activate  # או venv\Scripts\activate ב־Windows

pip install -r requirements.txt
```

---

##  הרצה

```bash
python app.py
```

ואז לפתוח דפדפן בכתובת:  
http://localhost:5050  
או בכתובת האמיתית שלך:  
http://10.112.4.121:5050/

---

##  מבנה הפרויקט

```
project/
│
├── app.py                  # אפליקציית Flask הראשית
├── algorithm.py            # האלגוריתם לתיוג רציף (ללא שינויים)
├── templates/
│   ├── index.html          # דף ראשי עם טופס וקלט
│   └── about.html          # דף מידע נוסף (אופציונלי)
├── requirements.txt
└── README.md
```

---

##  הערות

- הערכים הם לפי קודקודים, ולא לפי קשתות.
- לא משנים את הקובץ algorithm.py (לפי דרישות המטלה).
- החלוקה מבוצעת על פי פלט התיוג הרציף.

---

##  מקורות

- Cohen, Segal-Halevi, Steinhardt & Yaniv (2023)  
  "Fair Division of Graphs"

---


