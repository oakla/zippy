rem call .venv\Scripts\activate.bat

call echo y | pyinstaller "C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\src\boom_zip\boom.py" ^
    --distpath="C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\bundling\dist" ^
    --workpath "C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\bundling\build" ^
    --specpath "C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\bundling" ^
    --add-data "C:\Users\Alexander.Oakley\my-stuff-noonedrive\Code\proj\py-boom-zip\src\boom_zip\eff.org_files_2016_07_18_eff_large_wordlist.txt:."
     
pause