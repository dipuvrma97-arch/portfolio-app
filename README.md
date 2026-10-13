# Deepu Verma – Android App (Capacitor, live-website mode)

Yeh app aapki **live website** (https://dipuvrma97-arch.github.io/) ko app ke andar kholti hai.
Isliye website mein jo bhi badlo (text, image, certificate, project), woh app mein **apne aap** dikhta hai. App dobara banane ya install karne ki zaroorat nahi.

## APK banana (sirf ek baar)
1. GitHub par public repo `portfolio-app` banao, is folder ki saari files upload karo (`.github/workflows/build-apk.yml` zaroor check karo).
2. Actions > Build Android APK > Run workflow. 5 se 10 minute.
3. Releases mein `DeepuVerma.apk` milegi. Phone par install karo.
4. Website ke repo mein `website-patch` ki 3 files upload karo (index.html, app.js, app.css).

## App dobara kab banani padegi (kabhi kabhi)
Sirf tab jab app ka naam, icon, splash ya native settings badalni ho. Website ke content ke liye kabhi nahi.

## Zaroori batein
- App ko pehli baar khulne par internet chahiye. Uske baad website ka service worker kuch hissa offline cache kar leta hai.
- Website kharab ya band ho to app mein bhi wahi dikhega.
- Permissions: sirf INTERNET. Koi tracking nahi.
- Signing key (optional): neeche wale `Optional` section ya pichli guide dekho.

## Laptop par build (agar Android Studio + JDK 21 ho)
```
npm install
npx cap add android
python3 scripts/brand_android.py      # pip install pillow
npx cap sync android
cd android && ./gradlew assembleDebug
```
