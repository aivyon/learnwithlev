# לומדים עם לב — Learn with Lev

אתר סטטי בעברית לשיעורים פרטיים במתמטיקה ובפיזיקה במודיעין והסביבה. האתר בנוי ב־HTML, CSS ו־JavaScript רגילים ומפורסם באמצעות GitHub Pages.

## תצוגה מקומית

מהתיקייה הראשית של הפרויקט:

```bash
python3 -m http.server 8000
```

לאחר מכן פותחים את `http://localhost:8000`. חשוב להשתמש בשרת מקומי ולא לפתוח את `index.html` ישירות, כי קישורי הנכסים הם מוחלטים משורש האתר.

בדיקת תקינות מהירה:

```bash
python3 scripts/validate_site.py
```

## פרסום

GitHub Pages מוגדר לפרסום מהענף `main`, מתיקיית השורש. כל push ל־`main` מפעיל בנייה ופריסה. הקובץ `CNAME` חייב להישאר בדיוק עם הערך `learnwithlev.com`.

## מבנה ונכסים

- `index.html` — תוכן, מטא־דאטה ונתונים מובנים.
- `styles.css` — מערכת העיצוב והפריסה הרספונסיבית.
- `site.js` — תפריט נייד, סימון ניווט ואנימציות חשיפה קלות.
- `favicon.svg` — סמל האתר.
- `assets/og/learnwithlev-social.png` — תמונת שיתוף לרשתות.
- `404.html`, `robots.txt`, `sitemap.xml` — קבצי תשתית ו־SEO.

## סרטונים עתידיים

כרטיסי הסרטונים הם כרגע איורי SVG קלים המקשרים לפרופילים הרשמיים. כדי להוסיף וידאו מקומי בהמשך, יש ליצור `assets/video/` ולהשתמש בשמות הבאים:

- `circuit-light.mp4` + `circuit-light-poster.webp`
- `ramp-motion.mp4` + `ramp-motion-poster.webp`
- `geometry-shapes.mp4` + `geometry-shapes-poster.webp`
- אופציונלי: `soldering-demo.mp4` + `soldering-demo-poster.webp`

מומלץ לייצא MP4 בקידוד H.264, ללא הפעלה אוטומטית ועם תמונת poster דחוסה. עד שהקבצים קיימים, אין בקשות רשת לוידאו ואין שגיאות 404.

## הנחות דומיין

האתר מיועד ל־`https://learnwithlev.com`. GitHub Pages וה־CNAME כבר מוגדרים. שינויי DNS נעשים בנפרד ורק לאחר בדיקה; אין לשנות רשומות DNS כחלק משינויי קוד רגילים.
