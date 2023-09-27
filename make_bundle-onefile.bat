rem call .venv\Scripts\activate.bat

call echo y | pyinstaller "C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\src\boom_zip\boom.py" ^
    --distpath="C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\bundling-onefile\dist" ^
    --workpath "C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\bundling-onefile\build" ^
    --specpath "C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\bundling-onefile" ^
    --add-data "C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\src\boom_zip\eff.org_files_2016_07_18_eff_large_wordlist.txt:." ^
    --onefile
pause